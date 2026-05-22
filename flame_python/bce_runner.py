#!/usr/bin/env python3

import json
import os
import subprocess
import socket
import sys
import time
import urllib.error
import urllib.request
import urllib.parse
import uuid


SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 8188
SERVER_URL = "http://127.0.0.1:8188"

FRAME_TIMEOUT_MIN = 5  # per-frame timeout in minutes
FRAME_TIMEOUT_S = FRAME_TIMEOUT_MIN * 60


def log(text):
    text = str(text).strip()

    noisy_prefixes = (
        "API_JSON=",
        "JOB_DIR=",
        "SRC_DIR=",
        "OUT_DIR=",
        "MANIFEST=",
        "SERVER_URL=",
        "MODE=",
        "COMFY_PY=",
        "COMFY_ROOT=",
        "MAIN=",
        "CLOUD_URL=",
        "source_image=",
        "input_blob=",
        "expected_output=",
        "comfy_pid=",
    )

    if text.startswith(noisy_prefixes):
        return

    if text == "server up":
        text = "SERVER UP"
    elif text.startswith("uploading cloud source image"):
        text = "UPLOAD OK"
    elif text.startswith("queued prompt_id="):
        text = "JOB SUBMITTED"
    elif text.startswith("history ready prompt_id="):
        return
    elif text.startswith("fetching history"):
        return
    elif text.startswith("downloading "):
        text = "WRITING OUTPUT"
    elif text.startswith("waiting for completion"):
        return
    elif text.startswith("waiting for cloud completion"):
        return
    elif text.startswith("waiting for local saved file"):
        return
    elif text.startswith("waiting for output file"):
        return
    elif text.startswith("iterations="):
        return
    elif text.startswith("iter=") and " seed=" in text:
        return
    elif text.startswith("iter=") and " complete -> " in text:
        parts = text.split()
        if parts:
            iter_part = parts[0]
            iter_num = iter_part.split("=")[1]
            text = f"FRAME {int(iter_num):d} COMPLETE"
    elif text == "ALL PASSES COMPLETE":
        return
    elif text == "DONE":
        text = "DONE"

    print(f"[BCE] {text}", flush=True)


def fail(text, code=1):
    log(f"ERROR: {text}")
    raise SystemExit(code)


def port_listening(host, port, timeout_s=0.5):
    try:
        with socket.create_connection((host, int(port)), timeout=timeout_s):
            return True
    except Exception:
        return False


def workflow_failure_messages(mode):
    log("Comfy did not complete this workflow.")
    log("Open the workflow directly in ComfyUI, confirm it runs, then try BCE again.")
    log("See comfy_server.log for the ComfyUI error details.")

    if mode == "local" and port_listening("127.0.0.1", 8188, timeout_s=0.5):
        log("Local ComfyUI may still be running after this failed render.")
        log("Close or restart ComfyUI before trying again.")


def find_by_tag(wf, tag, class_type=None):
    for nid, node in (wf or {}).items():
        title = ((node.get("_meta") or {}).get("title") or "")
        if tag in title and (class_type is None or node.get("class_type") == class_type):
            return nid, node
    return None, None


def _next_api_node_id(api):
    max_id = 0

    for node_id in (api or {}).keys():
        node_id = str(node_id)
        if node_id.isdigit():
            max_id = max(max_id, int(node_id))

    return str(max_id + 1)


def _is_api_link(value, node_id, output_idx):
    return (
        isinstance(value, list)
        and len(value) == 2
        and str(value[0]) == str(node_id)
        and value[1] == output_idx
    )


def _is_bce_cloud_mask_invert(node):
    if not isinstance(node, dict):
        return False

    title = ((node.get("_meta") or {}).get("title") or "")
    return node.get("class_type") == "InvertMask" and "[BCE:CLOUD_MASK_INVERT]" in title


# Splice an InvertMask node between the [BCE:LOAD] mask output and its consumers
# Consumes API graph and load node id; mutates graph in place
def insert_invert_mask_after_loadimage_mask(api, load_id):
    if not isinstance(api, dict):
        return 0

    load_id = str(load_id)
    invert_id = None

    for node_id, node in api.items():
        if not _is_bce_cloud_mask_invert(node):
            continue

        inputs = node.get("inputs") or {}
        if _is_api_link(inputs.get("mask"), load_id, 1):
            invert_id = str(node_id)
            break

    consumers = []
    for node_id, node in list(api.items()):
        node_id = str(node_id)
        if node_id == load_id or node_id == invert_id:
            continue
        if not isinstance(node, dict):
            continue

        inputs = node.get("inputs") or {}
        if not isinstance(inputs, dict):
            continue

        for input_name, input_value in inputs.items():
            if _is_api_link(input_value, load_id, 1):
                consumers.append((inputs, input_name))

    if not consumers:
        return 0

    if invert_id is None:
        invert_id = _next_api_node_id(api)
        api[invert_id] = {
            "class_type": "InvertMask",
            "inputs": {
                "mask": [load_id, 1],
            },
            "_meta": {
                "title": "InvertMask [BCE:CLOUD_MASK_INVERT]",
            },
        }

    rewired = 0
    for inputs, input_name in consumers:
        inputs[input_name] = [invert_id, 0]
        rewired += 1

    return rewired


def configure_server(mode):
    global SERVER_ADDR, SERVER_PORT, SERVER_URL

    if mode == "lan":
        SERVER_ADDR = os.environ.get("BCE_LAN_HOST", "").strip() or "127.0.0.1"
        SERVER_PORT = int((os.environ.get("BCE_LAN_PORT", "").strip() or "8188"))
    else:
        SERVER_ADDR = "127.0.0.1"
        SERVER_PORT = 8188

    SERVER_URL = f"http://{SERVER_ADDR}:{SERVER_PORT}"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_done_flag(done_flag_path):
    os.makedirs(os.path.dirname(done_flag_path), exist_ok=True)
    with open(done_flag_path, "w", encoding="utf-8") as f:
        f.write("[BCE] done\n")


# Poll until ComfyUI HTTP server is accepting requests
# Consumes host/port/timeout; returns True when ready
def wait_for_comfy(host, port, timeout_seconds):
    t0 = time.time()
    url = f"http://{host}:{int(port)}/system_stats"

    while (time.time() - t0) < timeout_seconds:
        try:
            urllib.request.urlopen(url, timeout=1).read()
            log("server up")
            return True
        except Exception:
            time.sleep(0.25)

    log("ComfyUI did not become ready.")
    log("See comfy_server.log for the ComfyUI error details.")
    return False


def wait_for_server(timeout_s=30.0):
    if not wait_for_comfy(SERVER_ADDR, SERVER_PORT, timeout_s):
        fail("server did not come up", 10)


# Submit a Comfy API prompt and return the prompt_id
# Consumes graph dict; returns prompt_id string
def post_prompt(graph):
    payload = {
        "prompt": graph,
        "client_id": str(uuid.uuid4()),
    }

    req = urllib.request.Request(
        SERVER_URL + "/prompt",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    raw = urllib.request.urlopen(req, timeout=30).read()
    resp = json.loads(raw)

    prompt_id = resp.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"no prompt_id: {resp}")

    return prompt_id


def wait_history(prompt_id, save_nid, timeout_s=FRAME_TIMEOUT_S):
    url = SERVER_URL + f"/history/{prompt_id}"
    t0 = time.time()
    last_log = 0

    while (time.time() - t0) < timeout_s:
        try:
            raw = urllib.request.urlopen(url, timeout=10).read()
            hist = json.loads(raw)

            if prompt_id in hist:
                out = hist[prompt_id]
                outputs = out.get("outputs", {})
                node_out = (outputs or {}).get(str(save_nid)) or (outputs or {}).get(save_nid)

                if node_out is not None:
                    log(f"history ready prompt_id={prompt_id} save_nid={save_nid}")
                    return outputs
        except Exception:
            pass

        now = time.time()
        if (now - last_log) >= 10:
            elapsed = int(now - t0)
            log(f"waiting for completion... {elapsed}s")
            last_log = now

        time.sleep(0.25)

    raise TimeoutError(f"timeout waiting for history on [BCE:SAVE] node {save_nid}")


def wait_prompt_done(prompt_id, timeout_s=FRAME_TIMEOUT_S):
    url = SERVER_URL + f"/history/{prompt_id}"
    t0 = time.time()
    last_log = 0

    while (time.time() - t0) < timeout_s:
        try:
            raw = urllib.request.urlopen(url, timeout=10).read()
            hist = json.loads(raw)

            if prompt_id in hist:
                log(f"history ready prompt_id={prompt_id}")
                return hist[prompt_id]
        except Exception:
            pass

        now = time.time()
        if (now - last_log) >= 10:
            elapsed = int(now - t0)
            log(f"waiting for completion... {elapsed}s")
            last_log = now

        time.sleep(0.25)

    raise TimeoutError(f"timeout waiting for history prompt: {prompt_id}")


def get_save_info(wf):
    save_nid, n_save = find_by_tag(wf, "[BCE:SAVE]")

    if not n_save:
        raise RuntimeError("Could not find [BCE:SAVE] node")

    save_type = str(n_save.get("class_type") or "")

    if save_type == "SaveImage":
        out_ext = "png"
    elif save_type == "SaveEXR":
        out_ext = "exr"
    elif "RadianceDigitalCinemaWrite" in save_type:
        out_ext = "exr"
    else:
        raise RuntimeError(f"Unsupported [BCE:SAVE] node type: {save_type}")

    inputs = n_save.get("inputs") or {}
    raw_prefix = (inputs.get("filename_prefix") or "").strip()
    base_prefix = os.path.basename(raw_prefix)
    if base_prefix.endswith("."):
        base_prefix = base_prefix[:-1]
    if not base_prefix:
        base_prefix = "bce_out"

    return save_nid, save_type, base_prefix, out_ext


def patch_iter_graph(graph, save_nid, save_type, iter_idx):
    node = (graph or {}).get(str(save_nid)) or (graph or {}).get(save_nid)
    if not node:
        raise RuntimeError(f"Could not find save node in graph: {save_nid}")

    ins = node.get("inputs") or {}

    if save_type == "SaveEXR":
        ins["start_frame"] = int(iter_idx)
    elif "RadianceDigitalCinemaWrite" in save_type:
        ins["start_frame"] = int(iter_idx)
        ins["write_mode"] = "Sequence"
    elif save_type == "SaveImage":
        pass
    else:
        raise RuntimeError(f"Unsupported save_type: {save_type}")


def patch_seed_for_iteration(graph, seed_patch, seed):
    if not seed_patch:
        # Compatibility fallback only for old prepared jobs that do not have seed_patch.
        _nid, n_seed = find_by_tag(graph, "[BCE:SEED]")
        if n_seed:
            inputs = n_seed.get("inputs") or {}
            if "noise_seed" in inputs:
                inputs["noise_seed"] = int(seed)
                return
            if "seed" in inputs:
                inputs["seed"] = int(seed)
                return

        _nid, n_ksam = find_by_tag(graph, "[BCE:KSAMPLER]")
        if n_ksam:
            inputs = n_ksam.get("inputs") or {}
            if "noise_seed" in inputs:
                inputs["noise_seed"] = int(seed)
                return
            if "seed" in inputs:
                inputs["seed"] = int(seed)
                return

        raise RuntimeError("No seed patch target found")

    node_id = str(seed_patch.get("node_id"))
    input_name = str(seed_patch.get("input"))

    node = (graph or {}).get(node_id) or (graph or {}).get(int(node_id) if node_id.isdigit() else node_id)
    if not node:
        raise RuntimeError(f"Seed patch node not found: {node_id}")

    inputs = node.get("inputs") or {}
    if input_name not in inputs:
        raise RuntimeError(f"Seed patch input not found: node {node_id} input {input_name}")

    inputs[input_name] = int(seed)


def read_iterations(manifest_path):
    try:
        m = load_json(manifest_path)
        return int(((m.get("settings") or {}).get("iterations")) or 1)
    except Exception:
        return 1


def read_base_seed(manifest_path):
    m = load_json(manifest_path)
    seed = int(((m.get("seed") or {}).get("value")) or 0)

    if seed <= 0:
        raise RuntimeError("manifest seed.value is missing or zero")

    return seed


def read_seed_patch(manifest_path):
    m = load_json(manifest_path)
    seed = m.get("seed") or {}

    node_id = str(seed.get("node_id") or "").strip()
    input_name = str(seed.get("input") or "").strip()
    tag = str(seed.get("tag") or "").strip()

    if not node_id or not input_name:
        return None

    return {
        "tag": tag,
        "node_id": node_id,
        "input": input_name,
    }


def resolve_local_output(iter_idx, out_dir, base_prefix, out_ext):
    dst_path = os.path.join(out_dir, f"{base_prefix}.{iter_idx:04d}.{out_ext}")

    t0 = time.time()
    last_log = 0

    while (time.time() - t0) < 120.0:
        matches = []

        for name in os.listdir(out_dir):
            if not name.lower().endswith(f".{out_ext}"):
                continue
            if not name.startswith(base_prefix):
                continue

            full = os.path.join(out_dir, name)
            if not os.path.isfile(full):
                continue

            matches.append(full)

        if matches:
            matches.sort(key=os.path.getmtime, reverse=True)
            src_path = matches[0]

            if src_path != dst_path:
                if os.path.exists(dst_path):
                    os.remove(dst_path)
                os.rename(src_path, dst_path)

            return dst_path

        now = time.time()
        if (now - last_log) >= 5:
            elapsed = int(now - t0)
            log(f"waiting for local saved file... {elapsed}s")
            last_log = now

        time.sleep(0.25)

    raise TimeoutError(f"timeout waiting for local saved file for prefix: {base_prefix}")


def start_comfy_server(comfy_py, comfy_root, src_dir, out_dir, comfy_server_log):
    main_py = os.path.join(comfy_root, "main.py")

    cmd = [
        comfy_py,
        main_py,
        "--listen", SERVER_ADDR,
        "--port", str(SERVER_PORT),
        "--output-directory", out_dir,
        "--input-directory", src_dir,
        "--dont-print-server",
        "--disable-auto-launch",
        #"--force-fp16",
    ]

    log(f"COMFY_PY={comfy_py}")
    log(f"COMFY_ROOT={comfy_root}")
    log(f"MAIN={main_py}")
    log(f"SRC_DIR={src_dir}")
    log(f"OUT_DIR={out_dir}")

    os.makedirs(os.path.dirname(comfy_server_log), exist_ok=True)

    f = open(comfy_server_log, "w", encoding="utf-8")
    proc = subprocess.Popen(
        cmd,
        stdout=f,
        stderr=f,
        cwd=comfy_root,
    )

    return proc, f


def _shutdown_comfy(proc, proc_log):
    if proc is not None:
        try:
            proc.terminate()
        except Exception:
            pass

        try:
            proc.wait(timeout=10)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass

            try:
                proc.wait(timeout=3)
            except Exception:
                pass

    if proc_log is not None:
        try:
            proc_log.close()
        except Exception:
            pass


def download_view_file(view_url, rec, dst_path, default_type, headers=None):
    blob_name = rec.get("filename")
    if not blob_name:
        fail("output record missing filename", 57)

    blob_type = rec.get("type") or default_type
    blob_subfolder = rec.get("subfolder") or ""

    view_url = (
        f"{view_url}?filename={urllib.parse.quote(blob_name)}"
        f"&type={urllib.parse.quote(blob_type)}"
        f"&subfolder={urllib.parse.quote(blob_subfolder)}"
    )

    req = urllib.request.Request(
        view_url,
        headers=headers or {},
        method="GET",
    )

    with urllib.request.urlopen(req, timeout=180) as resp, open(dst_path, "wb") as f:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)


def _http_json(method, url, headers=None, data=None, timeout=120):
    req = urllib.request.Request(
        url,
        data=data,
        headers=headers or {},
        method=method,
    )

    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()

    if not raw:
        return {}

    return json.loads(raw.decode("utf-8"))


def _multipart_form_data(fields, files):
    boundary = f"----BCEBoundary{uuid.uuid4().hex}"
    body = bytearray()

    for name, value in (fields or {}).items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(str(value).encode("utf-8"))
        body.extend(b"\r\n")

    for name, file_info in (files or {}).items():
        filename, content, content_type = file_info
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode("utf-8")
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        body.extend(content)
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    return (
        bytes(body),
        f"multipart/form-data; boundary={boundary}",
    )


def _content_type_for_source(path):
    ext = os.path.splitext(path)[1].lower()

    if ext in (".tif", ".tiff"):
        return "image/tiff"
    if ext == ".png":
        return "image/png"

    return "application/octet-stream"


def log_history_filenames(value):
    if isinstance(value, dict):
        if "filename" in value:
            log(
                "history file: "
                f"filename={value.get('filename')} "
                f"type={value.get('type')} "
                f"subfolder={value.get('subfolder')}"
            )

        for child in value.values():
            log_history_filenames(child)
    elif isinstance(value, list):
        for child in value:
            log_history_filenames(child)


# Recursively locate the output file entry in a Comfy Cloud history response
# Consumes history value and expected prefix/ext; returns (filename, type, subfolder) or None
def find_cloud_output_file(history, result_name_base, ext="exr"):
    ext = str(ext or "").lower().lstrip(".")
    suffix = f".{ext}"
    files = []

    def walk(value):
        if isinstance(value, dict):
            if "filename" in value:
                files.append(value)

            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(history)

    exr_files = [
        item
        for item in files
        if str(item.get("filename") or "").lower().endswith(suffix)
    ]

    if not exr_files:
        names = [str(item.get("filename") or "") for item in files]
        compact = ", ".join(name for name in names if name)
        if not compact:
            compact = "(none)"
        raise RuntimeError(f"history has no .{ext} output files; filenames: {compact}")

    chosen = None
    for item in exr_files:
        if result_name_base in str(item.get("filename") or ""):
            chosen = item
            break

    if chosen is None:
        chosen = exr_files[0]

    return {
        "filename": chosen.get("filename"),
        "type": chosen.get("type") or "output",
        "subfolder": chosen.get("subfolder") or "",
    }


# Upload a still image or TIFF to Comfy Cloud input storage
# Consumes cloud URL, auth headers, file path; returns blob name
def upload_asset(cloud_url, auth_headers, input_path):
    with open(input_path, "rb") as f:
        source_bytes = f.read()

    upload_body, upload_ct = _multipart_form_data(
        fields={
            "type": "input",
            "overwrite": "true",
        },
        files={
            "image": (
                os.path.basename(input_path),
                source_bytes,
                _content_type_for_source(input_path),
            )
        },
    )

    upload_data = _http_json(
        "POST",
        f"{cloud_url}/api/upload/image",
        headers={
            **auth_headers,
            "Content-Type": upload_ct,
        },
        data=upload_body,
        timeout=120,
    )

    return upload_data.get("name")


# Upload an MP4 video to Comfy Cloud asset storage
# Consumes cloud URL, auth headers, file path; returns blob name
def upload_video(cloud_url, auth_headers, input_path):
    with open(input_path, "rb") as f:
        input_bytes = f.read()

    basename = os.path.basename(input_path)
    ext = os.path.splitext(input_path)[1]

    upload_body, upload_ct = _multipart_form_data(
        fields={
            "tags": "input,video",
            "name": basename,
            "mime_type": "video/mp4",
        },
        files={
            "file": (
                basename,
                input_bytes,
                "video/mp4",
            )
        },
    )

    upload_data = _http_json(
        "POST",
        f"{cloud_url}/api/assets",
        headers={
            **auth_headers,
            "Content-Type": upload_ct,
        },
        data=upload_body,
        timeout=120,
    )

    blob = upload_data.get("asset_hash") or upload_data.get("name")
    if not blob:
        return None

    if blob.startswith("blake3:"):
        blob = blob.split(":", 1)[1]
    if not os.path.splitext(blob)[1]:
        blob += ext

    return blob


# Execute a BCE job against the local or LAN ComfyUI server
# Consumes API JSON path and Comfy config; starts server if needed, runs prompt, saves result
def run_local(api_json, comfy_py, comfy_root):
    mode = os.environ.get("BCE_BACKEND_MODE", "local").strip().lower()

    job_dir = os.path.dirname(os.path.dirname(api_json))
    src_dir = os.path.join(job_dir, "source_frame")
    out_dir = os.path.join(job_dir, "comfy_out")
    manifest_path = os.path.join(job_dir, "manifest.json")
    comfy_dir = os.path.join(job_dir, "comfy")
    comfy_server_log = os.path.join(comfy_dir, "comfy_server.log")
    done_flag = os.path.join(comfy_dir, "done.flag")

    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(comfy_dir, exist_ok=True)

    log(f"API_JSON={api_json}")
    log(f"JOB_DIR={job_dir}")
    log(f"OUT_DIR={out_dir}")
    log(f"MANIFEST={manifest_path}")
    log(f"SERVER_URL={SERVER_URL}")
    log(f"MODE={mode}")

    manifest = load_json(manifest_path)

    # --- SAM (local only) ---
    if mode == "local" and manifest.get("sam"):
        sam = manifest["sam"]
        transport_path = sam["transport_path"]
        fps = float(sam.get("fps") or 0.0)
        next_action = sam.get("next_action", "render")
        files = manifest.get("files") or {}
        result_name_base = files.get("result") or ""

        if not os.path.isfile(transport_path):
            fail(f"SAM transport not found: {transport_path}", 41)

        input_dir = os.path.dirname(transport_path)
        transport_name = os.path.basename(transport_path)

        proc = None
        proc_log = None
        try:
            proc, proc_log = start_comfy_server(comfy_py, comfy_root, input_dir, out_dir, comfy_server_log)
            log(f"comfy_pid={proc.pid}")
            if not wait_for_comfy("127.0.0.1", 8188, 30.0):
                raise SystemExit(10)

            graph = load_json(api_json)

            _nid, n_load = find_by_tag(graph, "[BCE:LOAD]")
            if not n_load:
                fail("Could not find [BCE:LOAD] node", 44)
            n_load["inputs"]["video"] = transport_name
            n_load["inputs"]["frame_load_cap"] = 1 if next_action == "preview" else 0

            _nid, n_preview = find_by_tag(graph, "[BCE:PREVIEW]")
            if n_preview:
                n_preview["inputs"]["fps"] = fps

            _nid, n_save_node = find_by_tag(graph, "[BCE:SAVE]")
            if n_save_node:
                n_save_node["inputs"]["frame_rate"] = fps
                if next_action == "render":
                    n_save_node["inputs"]["filename_prefix"] = result_name_base

            try:
                prompt_id = post_prompt(graph)
            except urllib.error.HTTPError as e:
                err = e.read().decode("utf-8", errors="replace")
                log(f"/prompt returned {e.code}")
                log(err)
                workflow_failure_messages("local")
                raise SystemExit(30)
            except Exception as e:
                log(f"ERROR: {e}")
                workflow_failure_messages("local")
                raise SystemExit(30)

            log(f"queued prompt_id={prompt_id}")

            if next_action == "preview":
                output_tag = "[BCE:PREVIEW]"
                output_array = "images"
                output_default_type = "temp"
                local_name = f"{result_name_base}_preview.mp4"
                result_kind = "preview"
            else:
                output_tag = "[BCE:SAVE]"
                output_array = "gifs"
                output_default_type = "output"
                local_name = f"{result_name_base}_matte.mp4"
                result_kind = "matte"

            output_nid, output_node = find_by_tag(graph, output_tag)
            if not output_node:
                fail(f"Could not find {output_tag} node", 45)

            try:
                outputs = wait_history(prompt_id, output_nid, timeout_s=FRAME_TIMEOUT_S)
            except Exception as e:
                log(f"ERROR: {e}")
                workflow_failure_messages("local")
                raise SystemExit(31)

            node_out = (outputs or {}).get(str(output_nid)) or (outputs or {}).get(output_nid)
            if not node_out:
                fail(f"history missing output for {output_tag}", 55)
            records = node_out.get(output_array) or []
            if not records:
                fail(f"{output_tag} has no {output_array}", 56)
            rec = records[0]

            dst = os.path.join(out_dir, local_name)
            log("WRITING PREVIEW" if result_kind == "preview" else "WRITING MATTE")

            try:
                download_view_file(f"{SERVER_URL}/view", rec, dst, output_default_type)
            except urllib.error.HTTPError as e:
                err = e.read().decode("utf-8", errors="replace")
                fail(f"download failed: HTTP {e.code} {err}", 58)
            except Exception as e:
                fail(f"download failed: {e}", 58)

            if not os.path.isfile(dst):
                fail(f"downloaded file missing: {dst}", 59)

            sam["last_prompt_id"] = prompt_id
            sam["last_result_kind"] = result_kind
            sam["last_result_movie"] = dst
            sam["last_result_display_name"] = rec.get("display_name", "")
            sam["last_result_blob"] = rec.get("filename", "")
            sam["next_action"] = "render"
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2)

            save_done_flag(done_flag)
            log("DONE")

        finally:
            _shutdown_comfy(proc, proc_log)
        return

    # --- Image (Outpaint / Inpaint) local and LAN ---
    proc = None
    proc_log = None

    try:
        if mode == "local":
            proc, proc_log = start_comfy_server(
                comfy_py=comfy_py,
                comfy_root=comfy_root,
                src_dir=src_dir,
                out_dir=out_dir,
                comfy_server_log=comfy_server_log,
            )
            log(f"comfy_pid={proc.pid}")
            if not wait_for_comfy("127.0.0.1", 8188, 30.0):
                raise SystemExit(10)
        elif mode == "lan":
            wait_for_server(timeout_s=30.0)
        else:
            fail(f"unsupported runner mode: {mode}", 22)

        iters = read_iterations(manifest_path)
        base_seed = read_base_seed(manifest_path)
        seed_patch = read_seed_patch(manifest_path)
        log(f"iterations={iters}")

        base = load_json(api_json)
        save_nid, save_type, base_prefix, out_ext = get_save_info(base)

        for i in range(1, iters + 1):
            graph = json.loads(json.dumps(base))
            seed = int(base_seed) + (i - 1)

            patch_seed_for_iteration(graph, seed_patch, seed)
            patch_iter_graph(graph, save_nid, save_type, i)

            expected_path = os.path.join(out_dir, f"{base_prefix}.{i:04d}.{out_ext}")

            log(f"iter={i:02d} seed={seed}")
            log(f"expected_output={expected_path}")

            try:
                prompt_id = post_prompt(graph)
            except urllib.error.HTTPError as e:
                err = e.read().decode("utf-8", errors="replace")
                log(f"/prompt returned {e.code}")
                log(err)
                workflow_failure_messages(mode)
                raise SystemExit(30)
            except Exception as e:
                log(f"ERROR: {e}")
                workflow_failure_messages(mode)
                raise SystemExit(30)

            log(f"queued prompt_id={prompt_id}")

            try:
                if "RadianceDigitalCinemaWrite" in save_type:
                    wait_prompt_done(prompt_id, timeout_s=FRAME_TIMEOUT_S)
                    if not os.path.isfile(expected_path):
                        raise RuntimeError(f"expected Radiance output missing: {expected_path}")
                else:
                    wait_history(prompt_id, save_nid, timeout_s=FRAME_TIMEOUT_S)
                    expected_path = resolve_local_output(i, out_dir, base_prefix, out_ext)
            except Exception as e:
                log(f"ERROR: {e}")
                workflow_failure_messages(mode)
                raise SystemExit(31)

            log(f"iter={i:02d} complete -> {os.path.basename(expected_path)}")

        save_done_flag(done_flag)
        log("ALL PASSES COMPLETE")
        log("DONE")

    finally:
        _shutdown_comfy(proc, proc_log)


# Execute a BCE job against Comfy Cloud
# Consumes API JSON path; uploads source, submits prompt, downloads result
def run_cloud(api_json):
    cloud_url = os.environ.get("BCE_CLOUD_URL", "").strip().rstrip("/")
    cloud_api_key = os.environ.get("BCE_CLOUD_API_KEY", "").strip()

    if not cloud_url:
        fail("BCE_CLOUD_URL not set", 2)
    if not cloud_api_key:
        fail("BCE_CLOUD_API_KEY not set", 2)

    job_dir = os.path.dirname(os.path.dirname(api_json))
    src_dir = os.path.join(job_dir, "source_frame")
    out_dir = os.path.join(job_dir, "comfy_out")
    manifest_path = os.path.join(job_dir, "manifest.json")
    comfy_dir = os.path.join(job_dir, "comfy")
    done_flag = os.path.join(comfy_dir, "done.flag")

    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(comfy_dir, exist_ok=True)

    log(f"API_JSON={api_json}")
    log(f"JOB_DIR={job_dir}")
    log(f"SRC_DIR={src_dir}")
    log(f"OUT_DIR={out_dir}")
    log(f"MANIFEST={manifest_path}")
    log(f"CLOUD_URL={cloud_url}")

    auth_headers = {"X-API-Key": cloud_api_key}
    manifest = load_json(manifest_path)

    # --- SAM cloud ---
    if manifest.get("sam"):
        sam = manifest["sam"]
        transport_path = sam["transport_path"]
        fps = float(sam.get("fps") or 0.0)
        next_action = sam.get("next_action", "render")
        files = manifest.get("files") or {}
        result_name_base = files.get("result") or ""

        if not os.path.isfile(transport_path):
            fail(f"SAM transport not found: {transport_path}", 41)

        log("UPLOAD TRANSPORT")
        try:
            uploaded_blob = upload_video(cloud_url, auth_headers, transport_path)
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")
            fail(f"upload failed: HTTP {e.code} {err}", 42)
        except Exception as e:
            fail(f"upload failed: {e}", 42)

        if not uploaded_blob:
            fail("upload response missing blob name", 43)

        graph = load_json(api_json)

        _nid, n_load = find_by_tag(graph, "[BCE:LOAD]")
        if not n_load:
            fail("Could not find [BCE:LOAD] node", 44)
        n_load["inputs"]["video"] = uploaded_blob
        n_load["inputs"]["frame_load_cap"] = 1 if next_action == "preview" else 0

        _nid, n_preview = find_by_tag(graph, "[BCE:PREVIEW]")
        if n_preview:
            n_preview["inputs"]["fps"] = fps

        _nid, n_save_node = find_by_tag(graph, "[BCE:SAVE]")
        if n_save_node:
            n_save_node["inputs"]["frame_rate"] = fps
            if next_action == "render":
                n_save_node["inputs"]["filename_prefix"] = result_name_base

        try:
            submit_data = _http_json(
                "POST",
                f"{cloud_url}/api/prompt",
                headers={**auth_headers, "Content-Type": "application/json"},
                data=json.dumps({"prompt": graph}).encode("utf-8"),
                timeout=120,
            )
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")
            workflow_failure_messages("cloud")
            fail(f"submit failed: HTTP {e.code} {err}", 48)
        except Exception as e:
            workflow_failure_messages("cloud")
            fail(f"submit failed: {e}", 48)

        prompt_id = submit_data.get("prompt_id")
        if not prompt_id:
            fail(f"submit response missing prompt_id: {submit_data}", 49)
        log("JOB SUBMITTED")

        t0 = time.time()
        status_data = None
        while (time.time() - t0) < FRAME_TIMEOUT_S:
            try:
                status_data = _http_json(
                    "GET",
                    f"{cloud_url}/api/job/{prompt_id}/status",
                    headers=auth_headers,
                    timeout=60,
                )
                status = status_data.get("status", "")
                if status in ("success", "completed", "failed", "cancelled", "non_retryable_error"):
                    break
            except Exception:
                pass
            time.sleep(0.5)
        else:
            workflow_failure_messages("cloud")
            fail(f"timeout waiting for cloud status: {prompt_id}", 50)

        if not status_data:
            workflow_failure_messages("cloud")
            fail(f"no status data for prompt_id={prompt_id}", 51)
        if status_data.get("status") not in ("success", "completed"):
            err = status_data.get("error_message") or status_data
            workflow_failure_messages("cloud")
            fail(f"cloud run failed: {err}", 52)

        try:
            job_data = _http_json(
                "GET",
                f"{cloud_url}/api/jobs/{prompt_id}",
                headers=auth_headers,
                timeout=120,
            )
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")
            fail(f"job fetch failed: HTTP {e.code} {err}", 53)
        except Exception as e:
            fail(f"job fetch failed: {e}", 53)

        outputs = job_data.get("outputs") or {}

        if next_action == "preview":
            output_tag = "[BCE:PREVIEW]"
            output_array = "images"
            output_default_type = "temp"
            local_name = f"{result_name_base}_preview.mp4"
            result_kind = "preview"
        else:
            output_tag = "[BCE:SAVE]"
            output_array = "gifs"
            output_default_type = "output"
            local_name = f"{result_name_base}_matte.mp4"
            result_kind = "matte"

        output_nid, output_node = find_by_tag(graph, output_tag)
        if not output_node:
            fail(f"Could not find {output_tag} node", 45)
        node_out = (outputs or {}).get(str(output_nid)) or (outputs or {}).get(output_nid)
        if not node_out:
            fail(f"outputs missing node for {output_tag}: {output_nid}", 55)
        records = node_out.get(output_array) or []
        if not records:
            fail(f"{output_tag} has no {output_array}", 56)
        rec = records[0]

        dst = os.path.join(out_dir, local_name)
        log("WRITING PREVIEW" if result_kind == "preview" else "WRITING MATTE")

        try:
            download_view_file(f"{cloud_url}/api/view", rec, dst, output_default_type, headers=auth_headers)
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")
            fail(f"download failed: HTTP {e.code} {err}", 58)
        except Exception as e:
            fail(f"download failed: {e}", 58)

        if not os.path.isfile(dst):
            fail(f"downloaded file missing: {dst}", 59)

        sam["last_prompt_id"] = prompt_id
        sam["last_result_kind"] = result_kind
        sam["last_result_movie"] = dst
        sam["last_result_display_name"] = rec.get("display_name", "")
        sam["last_result_blob"] = rec.get("filename", "")
        sam["next_action"] = "render"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        save_done_flag(done_flag)
        log("DONE")
        return

    # --- Image cloud (Outpaint / Inpaint) ---
    job_id_short = manifest.get("job_id_short")
    if not job_id_short:
        fail("manifest missing job_id_short", 40)

    files = manifest.get("files") or {}
    source_name_base = files.get("source")
    result_name_base = files.get("result")

    if not source_name_base:
        fail("manifest missing files.source", 40)

    if not result_name_base:
        fail("manifest missing files.result", 40)

    source_ext = files.get("source_ext")
    if not source_ext:
        comfy_api = manifest.get("comfy_api") or {}
        comfy_source_media = str(comfy_api.get("comfy_source_media") or "")
        _root, ext = os.path.splitext(comfy_source_media)
        source_ext = ext.lstrip(".")
    if not source_ext:
        fail("manifest missing files.source_ext", 40)

    src_image = os.path.join(src_dir, f"{source_name_base}.0001.{source_ext}")
    if not os.path.isfile(src_image):
        fail(f"cloud source image not found: {src_image}", 41)

    iters = read_iterations(manifest_path)
    base_seed = read_base_seed(manifest_path)
    seed_patch = read_seed_patch(manifest_path)
    log(f"iterations={iters}")
    log(f"source_image={src_image}")

    log("uploading cloud source image...")
    try:
        input_blob = upload_asset(cloud_url, auth_headers, src_image)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        fail(f"upload failed: HTTP {e.code} {err}", 42)
    except Exception as e:
        fail(f"upload failed: {e}", 42)

    if not input_blob:
        fail("upload response missing blob name", 43)

    log(f"input_blob={input_blob}")

    base = load_json(api_json)

    load_nid, n_load = find_by_tag(base, "[BCE:LOAD]")
    if not n_load:
        fail("Could not find [BCE:LOAD] node", 44)

    if manifest.get("cloud_invert_loadimage_mask"):
        rewired = insert_invert_mask_after_loadimage_mask(base, load_nid)
        log(f"[BCE] cloud mask invert inserted: {rewired} connection(s)")

    save_nid, n_save = find_by_tag(base, "[BCE:SAVE]")
    if not n_save:
        fail("Could not find [BCE:SAVE] node", 45)

    save_inputs = n_save.get("inputs") or {}
    if "filename_prefix" not in save_inputs:
        fail("[BCE:SAVE] missing filename_prefix", 46)
    save_type = str(n_save.get("class_type") or "")

    for i in range(1, iters + 1):
        graph = json.loads(json.dumps(base))
        seed = int(base_seed) + (i - 1)

        patch_seed_for_iteration(graph, seed_patch, seed)
        patch_iter_graph(graph, save_nid, save_type, i)

        node_load = graph[str(load_nid)]
        load_inputs = node_load.get("inputs") or {}
        if "image" not in load_inputs:
            fail("[BCE:LOAD] missing image input", 47)
        load_inputs["image"] = input_blob

        node_save = graph[str(save_nid)]
        save_inputs = node_save.get("inputs") or {}
        if "RadianceDigitalCinemaWrite" in save_type:
            save_inputs["filename_prefix"] = result_name_base
            save_inputs["write_mode"] = "Sequence"
            save_inputs["output_path"] = ""
            save_inputs["start_frame"] = int(i)
        else:
            save_inputs["filename_prefix"] = result_name_base

        log(f"iter={i:02d} seed={seed}")
        log("submitting prompt...")

        try:
            submit_data = _http_json(
                "POST",
                f"{cloud_url}/api/prompt",
                headers={**auth_headers, "Content-Type": "application/json"},
                data=json.dumps({"prompt": graph}).encode("utf-8"),
                timeout=120,
            )
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")
            workflow_failure_messages("cloud")
            fail(f"submit failed: HTTP {e.code} {err}", 48)
        except Exception as e:
            workflow_failure_messages("cloud")
            fail(f"submit failed: {e}", 48)

        prompt_id = submit_data.get("prompt_id")
        if not prompt_id:
            fail(f"submit response missing prompt_id: {submit_data}", 49)

        log(f"queued prompt_id={prompt_id}")

        t0 = time.time()
        last_log = 0
        status_data = None

        while (time.time() - t0) < FRAME_TIMEOUT_S:
            try:
                status_data = _http_json(
                    "GET",
                    f"{cloud_url}/api/job/{prompt_id}/status",
                    headers=auth_headers,
                    timeout=60,
                )
                status = status_data.get("status", "")

                if status in ("success", "failed", "cancelled", "non_retryable_error"):
                    log(f"status={status}")
                    break
            except Exception:
                pass

            now = time.time()
            if (now - last_log) >= 10:
                elapsed = int(now - t0)
                log(f"waiting for cloud completion... {elapsed}s")
                last_log = now

            time.sleep(0.5)
        else:
            workflow_failure_messages("cloud")
            fail(f"timeout waiting for cloud status: {prompt_id}", 50)

        if not status_data:
            workflow_failure_messages("cloud")
            fail(f"no status data for prompt_id={prompt_id}", 51)

        if status_data.get("status") != "success":
            err = status_data.get("error_message") or status_data
            workflow_failure_messages("cloud")
            fail(f"cloud run failed: {err}", 52)

        log("fetching history...")

        try:
            hist = _http_json(
                "GET",
                f"{cloud_url}/api/history_v2/{prompt_id}",
                headers=auth_headers,
                timeout=120,
            )
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")
            fail(f"history fetch failed: HTTP {e.code} {err}", 53)
        except Exception as e:
            fail(f"history fetch failed: {e}", 53)

        if not hist:
            fail("history response is empty", 54)

        log_history_filenames(hist)

        top_key = next(iter(hist.keys()))
        run_block = hist[top_key]

        outputs = run_block.get("outputs") or {}
        if "RadianceDigitalCinemaWrite" in save_type:
            out_file = find_cloud_output_file(hist, result_name_base, "exr")
            blob_name = out_file["filename"]
            blob_type = out_file["type"]
            blob_subfolder = out_file["subfolder"]
        else:
            node_out = outputs.get(str(save_nid)) or outputs.get(save_nid)
            if not node_out:
                fail(f"history missing save node outputs: {save_nid}", 55)

            images = node_out.get("images") or []
            if not images:
                fail("history save node has no images", 56)

            blob_name = images[0].get("filename")
            if not blob_name:
                fail("history image missing filename", 57)
            blob_type = images[0].get("type") or "output"
            blob_subfolder = images[0].get("subfolder") or ""

        dst_exr = os.path.join(out_dir, f"{result_name_base}.{i:04d}.exr")
        log(f"downloading {blob_name} -> {dst_exr}")

        view_url = (
            f"{cloud_url}/api/view"
            f"?filename={urllib.parse.quote(blob_name)}"
            f"&type={urllib.parse.quote(blob_type)}"
            f"&subfolder={urllib.parse.quote(blob_subfolder)}"
        )

        req = urllib.request.Request(
            view_url,
            headers=auth_headers,
            method="GET",
        )

        try:
            with urllib.request.urlopen(req, timeout=180) as resp, open(dst_exr, "wb") as f:
                while True:
                    chunk = resp.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")
            fail(f"download failed: HTTP {e.code} {err}", 58)
        except Exception as e:
            fail(f"download failed: {e}", 58)

        if not os.path.isfile(dst_exr):
            fail(f"downloaded file missing: {dst_exr}", 59)

        log(f"iter={i:02d} complete -> {os.path.basename(dst_exr)}")

    save_done_flag(done_flag)
    log("ALL PASSES COMPLETE")
    log("DONE")


# Runner entry point: dispatch to local or cloud backend from API JSON
# Reads manifest/config from env; calls run_local or run_cloud
def main():
    if len(sys.argv) < 2:
        fail("usage: bce_runner.py /path/to/_API.json", 2)

    api_json = sys.argv[1]
    mode = os.environ.get("BCE_BACKEND_MODE", "local").strip().lower()
    configure_server(mode)

    comfy_root = os.environ.get("BCE_COMFY_ROOT", "").strip()
    comfy_py = os.environ.get("BCE_COMFY_PY", "").strip()

    if not api_json:
        fail("missing api_json", 2)
    if not os.path.isfile(api_json):
        fail(f"api_json not found: {api_json}", 2)

    if mode == "local":
        if not comfy_root:
            fail("BCE_COMFY_ROOT not set", 2)
        if not comfy_py:
            fail("BCE_COMFY_PY not set", 2)
        run_local(api_json, comfy_py, comfy_root)
    elif mode == "lan":
        run_local(api_json, comfy_py, comfy_root)
    elif mode == "cloud":
        run_cloud(api_json)
    else:
        fail(f"unknown backend mode: {mode}", 22)


if __name__ == "__main__":
    main()
