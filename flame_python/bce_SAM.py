# BCE SAM Node - Prepare Hook


import os
import re
import json
import flame  # type: ignore
import bce_lib as bce


# Workflow popup order in BCE_SAM.xml:
#   0 = SAM3 Text Prompt
#
# Flame saves the popup as a positional integer.

TEMPLATE_0 = "bce_SAM3_API.json"
TEMPLATE_1 = ""


SHADER_NAME = "BCE SAM"
WORK_SUBDIR = "sam"
NODE_LABEL = "SAM"
ARTIFACT_PREFIX = "sam"


bce.msg(f"LOADED {os.path.basename(__file__)}", "info", 5)


#-------------------------------------
# Entry
#-------------------------------------


# Fill Flame-default control values that may be absent from the saved Matchbox setup XML
# Consumes parsed parameter dict; mutates and returns the same dict
def normalize_probe_defaults(probe):
    if probe["workflow_index"] is None:
        probe["workflow_index"] = 0

    if probe["threshold"] is None:
        probe["threshold"] = 0.5

    if probe["max_objects"] is None:
        probe["max_objects"] = 6

    if probe["preview_mode"] is None:
        probe["preview_mode"] = False

    for idx in range(6):
        key = f"mask_{idx}"
        if probe[key] is None:
            probe[key] = 0

    probe["workflow_index"] = int(probe["workflow_index"])
    probe["threshold"] = float(probe["threshold"])
    probe["max_objects"] = int(probe["max_objects"])
    probe["preview_mode"] = bool(probe["preview_mode"])

    for idx in range(6):
        key = f"mask_{idx}"
        probe[key] = int(probe[key])

    return probe


# Prepare a selected BCE node for launch
# Creates job files, source Write branch, API JSON, and manifest state
def prepare_job(selection):
    node = _find_node(selection)
    if node is None:
        return

    cfg = bce.load_config()
    cfg = dict(cfg)
    cfg["work_root"] = os.path.join(cfg["work_root"], WORK_SUBDIR)

    job = bce.new_job(cfg, node, selection)
    render_mode = job["cfg"].get("backend_mode", "local")

    bce.msg(f"job_id={job['job_id']}  short={job['job_id_short']}")
    manifest = bce.new_manifest(job)

    try:
        source_name_base = f"{ARTIFACT_PREFIX}_{job['job_id_short']}_src"
        result_name_base = f"{ARTIFACT_PREFIX}_{job['job_id_short']}"
        manifest["files"] = {
            "source": source_name_base,
            "result": result_name_base,
        }

        bce.save_mbox_setup(job, manifest)

        probe = _read_normalized_mbox_setup(job["mbox_setup_path"])
        job["probe"] = probe
        manifest["settings"] = probe
        manifest["status"] = "probe_read"

        manifest["geometry"] = {
            "mode": "same_as_source",
            "show_axis_offset": False,
        }
        validate_api_template(job)

        prep = bce.prepare_write_export(
            job["selection"],
            job["cfg"],
            job["job_dir"],
            job["job_id_short"],
            job["mbox_setup_path"],
            render_mode,
            _read_normalized_mbox_setup,
            _find_node,
            source_name_base=source_name_base,
            export_template_name="bce_wf_jpeg",
        )

        if prep:
            # TODO SAM Phase 2: replace this temporary full-range branch with a dedicated sequence/transport export branch.
            nodes = bce.add_write_branch(
                prep,
                job["job_id"],
                job["job_id_short"],
                mux_name_base=f"{NODE_LABEL}_on_Sequence",
                write_name_base=source_name_base,
                source_has_matte=False,
                freeze_current_frame=False,
                include_frame_in_mux_name=False,
            )
            if nodes:
                bce.record_write_branch(job, manifest, prep, nodes)

        patch_api_json(job, manifest)
        manifest["status"] = "prepare_done"
    except Exception as e:
        manifest["status"] = "prepare_failed"
        manifest["error"] = str(e)
        bce.msg(f"ERROR: {e}", "error", 10)

    bce.save_manifest(job["manifest_path"], manifest)

    if manifest.get("status") == "prepare_done":
        bce.msg("prepare done", "info", 5)
    else:
        bce.msg("prepare failed", "error", 5)


#-------------------------------------
# Node and Matchbox helpers
#-------------------------------------


# Find the editable BCE Matchbox node in the current selection
# Consumes Flame selection; returns the node or None
def _find_node(selection):
    return bce.find_matchbox_node(selection, SHADER_NAME)


# Read the saved Matchbox setup XML into BCE's parameter dictionary
# Consumes setup XML path; returns parsed prompt, frame, size, and controls
def read_mbox_setup(mbox_setup_path):
    with open(mbox_setup_path, "r", encoding="utf-8") as f:
        xml = f.read()

    out = {}

    out["prompt"] = (m.group(1).strip() if (m := re.search(r"<Note>(.*?)</Note>", xml, re.DOTALL)) else "")
    out["current_time"] = int(re.search(r"<Current_Time>(\d+)</Current_Time>", xml).group(1))

    m_fb = re.search(r'<FrameBounds[^>]*\bW="(\d+)"\s+H="(\d+)"', xml, re.DOTALL)
    if m_fb:
        out["width"] = int(m_fb.group(1))
        out["height"] = int(m_fb.group(2))
    else:
        out["width"] = int(re.search(r"<OutputResolution>.*?<Width>(\d+)</Width>", xml, re.DOTALL).group(1))
        out["height"] = int(re.search(r"<OutputResolution>.*?<Height>(\d+)</Height>", xml, re.DOTALL).group(1))

    def read_chan(name):
        m = re.search(rf'<Channel Name="{re.escape(name)}">(.*?)</Channel>', xml, re.DOTALL)
        if not m:
            return None
        block = m.group(1)
        vm = re.search(r"<Value>(-?\d+(?:\.\d+)?)</Value>", block)
        return float(vm.group(1)) if vm else None

    def read_shader_param(index):
        m = re.search(r"<ShaderParameters>(.*?)</ShaderParameters>", xml, re.DOTALL)
        if not m:
            return None
        block = m.group(1)
        params = re.findall(r"<Parameter>(.*?)</Parameter>", block, re.DOTALL)
        if index >= len(params):
            return None
        pm = re.search(r"<value>(-?\d+(?:\.\d+)?)</value>", params[index], re.DOTALL)
        return float(pm.group(1)) if pm else None

    out["workflow_index"] = read_shader_param(0)
    out["preview_mode"] = read_shader_param(7)
    out["threshold"] = read_chan("Threshold")
    out["max_objects"] = read_chan("Max Objects")
    if out["max_objects"] is None:
        out["max_objects"] = read_chan("max_objects")

    for idx in range(6):
        out[f"mask_{idx}"] = read_chan(f"Mask_{idx}")

    if out["preview_mode"] is not None:
        out["preview_mode"] = bool(int(out["preview_mode"]))

    return out


#-------------------------------------
# Prepare helpers
#-------------------------------------


# Read and normalize Matchbox setup values for shared export preparation
# Consumes setup XML path; returns normalized parameter dict
def _read_normalized_mbox_setup(mbox_setup_path):
    return normalize_probe_defaults(read_mbox_setup(mbox_setup_path))


# Fail early when the selected template is not a BCE-compatible Comfy API JSON graph
# Consumes job; stores validated template data on job for later patching
def validate_api_template(job):
    cfg = job.get("cfg") or {}
    probe = job.get("probe") or {}
    workflow_index = int(probe.get("workflow_index") or 0)

    if workflow_index == 0:
        template_name = TEMPLATE_0
    elif workflow_index == 1:
        template_name = TEMPLATE_1
    else:
        raise RuntimeError(f"Unknown workflow template index: {workflow_index}")

    if not template_name:
        raise RuntimeError(f"No API template mapped for workflow index: {workflow_index}")

    job["_workflow_index"] = workflow_index
    job["_api_template_name"] = template_name

    template_path = os.path.join(
        cfg.get("templates_dir", bce.TEMPLATES_DIR),
        template_name,
    )

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load API template: {e}")

    graph = bce.api_graph_from_template(data)
    nodes = list(bce.iter_api_nodes(graph))
    if not nodes:
        raise RuntimeError("Selected template does not contain Comfy API node entries.")

    tags = set()
    for node in nodes:
        title = (node.get("_meta", {}).get("title") or "").upper()
        if "[BCE:LOAD]" in title:
            tags.add("[BCE:LOAD]")
        if "[BCE:PROMPT]" in title:
            tags.add("[BCE:PROMPT]")
        if "[BCE:VIDTRACK]" in title:
            tags.add("[BCE:VIDTRACK]")
        if "[BCE:PREVIEW]" in title:
            tags.add("[BCE:PREVIEW]")
        if "[BCE:INDEX]" in title:
            tags.add("[BCE:INDEX]")
        if "[BCE:SAVE]" in title:
            tags.add("[BCE:SAVE]")

    required = (
        "[BCE:LOAD]",
        "[BCE:PROMPT]",
        "[BCE:VIDTRACK]",
        "[BCE:PREVIEW]",
        "[BCE:INDEX]",
        "[BCE:SAVE]",
    )
    missing = [tag for tag in required if tag not in tags]
    found_tags = ", ".join(sorted(tags)) or "(none)"
    tag_context = f"\nTemplate: {template_path}\nFound BCE tags: {found_tags}"

    if missing:
        raise RuntimeError(
            f"Selected API template is missing required BCE tag(s): {', '.join(missing)}"
            f"{tag_context}"
        )

    job["_api_template_data"] = data
    job["_api_template_graph"] = graph
    job["_api_template_path"] = template_path

    return data, template_path


# Patch the Comfy API template with parsed Mbox values and job paths
# Consumes job and manifest; writes API JSON and mutates manifest
def patch_api_json(job, manifest):
    probe = job.get("probe") or {}
    job_id_short = job["job_id_short"]
    comfy_dir = job["comfy_dir"]
    source_name_base = f"{ARTIFACT_PREFIX}_{job_id_short}_src"
    result_name_base = f"{ARTIFACT_PREFIX}_{job_id_short}"
    source_ext = "jpg"
    object_indices = ""

    api_json_path = os.path.join(
        comfy_dir,
        f"{result_name_base}_API.json"
    )

    try:
        data = job.get("_api_template_data")
        graph = job.get("_api_template_graph")
        if data is None or graph is None:
            data, _template_path = validate_api_template(job)
            graph = job["_api_template_graph"]
    except Exception as e:
        bce.msg(f"ERROR: Failed to load template: {e}", "error", 8)
        manifest["status"] = "api_json_patch_failed"
        return

    workflow_index = job.get("_workflow_index", int(probe.get("workflow_index") or 0))
    template_name = job.get("_api_template_name", "")

    bce.dbg(f"workflow_index={workflow_index} template={template_name}")

    manifest["template"] = template_name

    ids = []
    for idx in range(6):
        if int(probe.get(f"mask_{idx}") or 0) == 1:
            ids.append(str(idx))
    object_indices = ",".join(ids)

    for _node_id, node in bce.iter_api_items(graph):
        title = (node.get("_meta", {}).get("title") or "").upper()
        inputs = node.get("inputs", {})

        if "[BCE:LOAD]" in title:
            if "video" in inputs:
                inputs["video"] = f"{source_name_base}.mp4"

        if "[BCE:PROMPT]" in title:
            if "text" in inputs:
                inputs["text"] = probe.get("prompt", "")
            elif "prompt" in inputs:
                inputs["prompt"] = probe.get("prompt", "")

        if "[BCE:VIDTRACK]" in title:
            if "detection_threshold" in inputs:
                inputs["detection_threshold"] = float(probe.get("threshold", 0.5))
            if "max_objects" in inputs:
                inputs["max_objects"] = int(probe.get("max_objects", 6))
            if "detect_interval" in inputs:
                inputs["detect_interval"] = 1

        if "[BCE:INDEX]" in title:
            if "object_indices" in inputs:
                inputs["object_indices"] = object_indices

        if "[BCE:SAVE]" in title:
            if "filename_prefix" in inputs:
                inputs["filename_prefix"] = result_name_base

    manifest["files"] = {
        "source": source_name_base,
        "result": result_name_base,
        "source_ext": source_ext,
        "transport_movie": f"{result_name_base}_transport.mp4",
        "preview_movie": f"{result_name_base}_preview.mp4",
    }
    manifest["comfy_api"] = {
        "comfy_source_media": f"{result_name_base}_transport.mp4",
    }
    preview_mode = bool(probe.get("preview_mode"))
    manifest["sam"] = {
        "threshold": float(probe.get("threshold", 0.5)),
        "max_objects": int(probe.get("max_objects", 6)),
        "object_indices": object_indices,
        "preview_mode": preview_mode,
        "next_action": "preview" if preview_mode else "render",
    }

    try:
        with open(api_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        bce.msg(f"ERROR: Failed to write API JSON: {e}", "error", 8)
        manifest["status"] = "api_json_patch_failed"
        return

    job["api_json_path"] = api_json_path
    manifest["status"] = "api_json_patched"


#-------------------------------------
# Batch Menu
#-------------------------------------


# Show Prepare only when a BCE Matchbox node is selected
# Consumes Flame selection; returns menu visibility
def scope_node(selection):
    return _find_node(selection) is not None


# Flame menu wrapper for prepare action
# Consumes selection; delegates to prepare entrypoint
def run(selection):
    prepare_job(selection)


# Register Batch context menu action for BCE nodes
# Consumed by Flame; returns menu action descriptors
def get_batch_custom_ui_actions():
    return [
        {
            "name": SHADER_NAME,
            "actions": [
                {
                    "name": "Prepare Job",
                    "isVisible": scope_node,
                    "execute": run,
                    "minimumVersion": "2024.1.0"
                }
            ],
        }
    ]
