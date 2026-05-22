
# BCE Node - Prepare Hook


import os
import re
import json
import random
import flame  # type: ignore
import bce_lib as bce


# Workflow popup order in BCE_Outpaint.xml:
#   0 = Flux.1 Fill
#   1 = Flux.1 Fill GGUF
#
# Flame saves the popup as a positional integer.
# Keep these template numbers matched to the XML PopupEntry order.

TEMPLATE_0 = "bce_OP_flux1_API.json"
TEMPLATE_1 = "bce_OP_flux2_klein9b_API.json"

# Cloud note:
# BCE may use the same canonical template for local/LAN/cloud.
# In cloud mode, [BCE:LOAD] is mutated to LoadImage.
# [BCE:SAVE] keeps its template class and only its output path is patched.
# This is only for generated per-job API JSON.
# It does not solve missing custom nodes or unsupported model loaders.

SHADER_NAME = "BCE Outpaint"
WORK_SUBDIR = "outpaint"
NODE_LABEL = "Outpaint"
ARTIFACT_PREFIX = "op"


bce.msg(f"LOADED {os.path.basename(__file__)}", "info", 5)


#-------------------------------------
# BCE OUTPAINT CATEGORY NODE
#
# This node can run multiple compatible Outpaint Comfy API templates.
#
# To add an Outpaint template:
#     1. Make/save Comfy API JSON.
#     2. Add required [BCE:*] tags.
#     3. Add a PopupEntry to BCE_Outpaint.xml.
#     4. Add matching TEMPLATE_N / TEMPLATE_N_CLOUD constants below.
#     5. Extend _selected_template_name() for the new index.
#
# Important:
#     Popup order in XML must match TEMPLATE_N order.
#     Flame saves the popup as a positional integer, not as the label.
#     PopupEntry Value is not used as source of truth.
#
# Preferred modern template tags:
#     [BCE:SEED], [BCE:STEPS], [BCE:PROMPT], [BCE:LOAD], [BCE:PAD], [BCE:SAVE]
# Optional:
#     [BCE:GUIDE]
# Legacy:
#     [BCE:KSAMPLER] is still supported as fallback.
#
# To make a different category node, such as Inpaint or Upscale:
#     Start from bce_node_template.py and see docs.
#-------------------------------------


#-------------------------------------
# Entry
#-------------------------------------


# Fill Flame-default control values that may be absent from the saved Matchbox setup XML
# Consumes parsed parameter dict; mutates and returns the same dict
def normalize_probe_defaults(probe):
    if probe["workflow_index"] is None:
        probe["workflow_index"] = 0

    if probe["left"] is None:
        probe["left"] = 0

    if probe["right"] is None:
        probe["right"] = 0

    if probe["top"] is None:
        probe["top"] = 0

    if probe["bottom"] is None:
        probe["bottom"] = 0

    if probe["iterations"] is None:
        probe["iterations"] = 4

    if probe["steps"] is None:
        probe["steps"] = 12

    if probe["guidance"] is None:
        probe["guidance"] = 29.0

    if probe["seed"] is None:
        probe["seed"] = 0

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
        _resolve_probe_seed(job, manifest)
        probe = manifest.get("settings") or {}
        manifest["geometry"] = {
            "mode": "source_plus_padding",
            "left": int(probe.get("left") or 0),
            "right": int(probe.get("right") or 0),
            "top": int(probe.get("top") or 0),
            "bottom": int(probe.get("bottom") or 0),
            "show_axis_offset": True,
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
        )

        if prep:
            nodes = bce.add_write_branch(
                prep,
                job["job_id"],
                job["job_id_short"],
                mux_name_base=f"{NODE_LABEL}_on_frame",
                write_name_base=source_name_base,
            )
            if nodes:
                bce.record_write_branch(job, manifest, prep, nodes)

        patch_api_json(render_mode, job, manifest)
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
# Consumes setup XML path; returns parsed prompt, frame, bounds, controls
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
        out["width"]  = int(re.search(r"<OutputResolution>.*?<Width>(\d+)</Width>",  xml, re.DOTALL).group(1))
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
        vals = re.findall(r"<Parameter>\s*<value>(-?\d+(?:\.\d+)?)</value>\s*</Parameter>", block)
        if index >= len(vals):
            return None
        return float(vals[index])

    out["workflow_index"] = read_shader_param(0)

    out["left"]   = read_chan("Left")
    out["right"]  = read_chan("Right")
    out["top"]    = read_chan("Top")
    out["bottom"] = read_chan("Bottom")

    out["iterations"] = read_chan("Iterations")
    out["steps"]      = read_chan("Steps")
    out["guidance"]   = read_chan("Guidance")
    out["seed"]       = read_chan("Seed")

    for k in ("workflow_index", "left", "right", "top", "bottom", "iterations", "steps", "seed"):
        if out[k] is not None:
            out[k] = int(out[k])

    return out



#-------------------------------------
# Prepare helpers
#-------------------------------------

# Read and normalize Matchbox setup values for shared export preparation
# Consumes setup XML path; returns normalized parameter dict
def _read_normalized_mbox_setup(mbox_setup_path):
    return normalize_probe_defaults(read_mbox_setup(mbox_setup_path))


# Preserve a user seed or generate one and reload the node setup
# Consumes saved Matchbox setup; mutates setup XML, node, job, and manifest
def _resolve_probe_seed(job, manifest):
    mbox_setup_path = job["mbox_setup_path"]
    node = job["node"]

    probe = read_mbox_setup(mbox_setup_path)
    probe = normalize_probe_defaults(probe)

    seed = int(probe.get("seed") or 0)

    if seed == 0:
        seed = random.randint(1, 9_999_999)
        bce.patch_mbox_seed_value(mbox_setup_path, seed)
        node.load_node_setup(mbox_setup_path)
        bce.dbg(f"seed generated: {seed}")
    else:
        bce.dbg(f"seed preserved: {seed}")

    probe["seed"] = int(seed)
    job["probe"] = probe
    manifest["settings"] = probe
    manifest["status"] = "seed_resolved"


def _seed_input_name(inputs):
    if "noise_seed" in inputs:
        return "noise_seed"
    if "seed" in inputs:
        return "seed"
    return None


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
        if "[BCE:SAVE]" in title:
            tags.add("[BCE:SAVE]")
        if "[BCE:SEED]" in title:
            tags.add("[BCE:SEED]")
        if "[BCE:STEPS]" in title:
            tags.add("[BCE:STEPS]")
        if "[BCE:KSAMPLER]" in title:
            tags.add("[BCE:KSAMPLER]")

    missing = [tag for tag in ("[BCE:LOAD]", "[BCE:SAVE]") if tag not in tags]
    if missing:
        raise RuntimeError(f"Selected API template is missing required BCE tag(s): {', '.join(missing)}")

    has_modern_tags = "[BCE:SEED]" in tags and "[BCE:STEPS]" in tags
    has_legacy_tag = "[BCE:KSAMPLER]" in tags
    if not has_modern_tags and not has_legacy_tag:
        raise RuntimeError(
            "Selected API template needs [BCE:SEED] + [BCE:STEPS], or legacy [BCE:KSAMPLER]."
        )

    job["_api_template_data"] = data
    job["_api_template_graph"] = graph
    job["_api_template_path"] = template_path

    return data, template_path


# Patch the Comfy API template with parsed Mbox values and job paths
# Consumes job, parsed values, and template mode; writes API JSON and mutates job/manifest
def patch_api_json(render_mode, job, manifest):

    probe = job.get("probe") or {}
    frame = probe.get("current_time")

    if frame is None:
        bce.msg("ERROR: No current_time in probe", "error", 8)
        manifest["status"] = "api_json_patch_failed"
        return

    job_dir = job["job_dir"]
    job_id_short = job["job_id_short"]
    comfy_dir = job["comfy_dir"]
    source_name_base = f"{ARTIFACT_PREFIX}_{job_id_short}_src"
    result_name_base = f"{ARTIFACT_PREFIX}_{job_id_short}"
    source_ext = bce.get_source_ext_for_backend(render_mode)

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

    items = list(bce.iter_api_items(graph))
    has_seed_tag = any("[BCE:SEED]" in ((node.get("_meta", {}).get("title") or "").upper()) for _node_id, node in items)
    has_steps_tag = any("[BCE:STEPS]" in ((node.get("_meta", {}).get("title") or "").upper()) for _node_id, node in items)

    seed = int(probe.get("seed", 0))
    steps = int(probe.get("steps", 12))
    guidance = probe.get("guidance", 30.0)
    seed_patch = None

    for node_id, node in items:
        title = (node.get("_meta", {}).get("title") or "").upper()
        inputs = node.get("inputs", {})

        if "[BCE:LOAD]" in title:
            if render_mode == "cloud":
                bce.mutate_load_node_for_cloud(
                    node,
                    f"{source_name_base}.0001.{source_ext}",
                )
            else:
                if "source_path" in inputs:
                    inputs["source_path"] = os.path.join(
                        job_dir,
                        "source_frame",
                        f"{source_name_base}.0001.{source_ext}",
                    )
                elif "filepath" in inputs:
                    inputs["filepath"] = os.path.join(
                        job_dir,
                        "source_frame",
                        f"{source_name_base}.0001.{source_ext}",
                    )
                else:
                    bce.msg(f"WARNING: LOAD node missing 'filepath' input: {node.get('class_type')}", "warning", 6)

        elif "[BCE:PAD]" in title:
            inputs["left"] = probe.get("left", 0)
            inputs["top"] = probe.get("top", 0)
            inputs["right"] = probe.get("right", 0)
            inputs["bottom"] = probe.get("bottom", 0)

        if "[BCE:SEED]" in title:
            input_name = _seed_input_name(inputs)
            if input_name:
                inputs[input_name] = seed
                seed_patch = {
                    "tag": "[BCE:SEED]",
                    "node_id": str(node_id),
                    "input": input_name,
                }
            else:
                bce.msg(f"WARNING: [BCE:SEED] node has no seed/noise_seed input: {node.get('class_type')}", "warning", 6)

        if "[BCE:STEPS]" in title:
            if "steps" in inputs:
                inputs["steps"] = steps
            else:
                bce.msg(f"WARNING: [BCE:STEPS] node has no steps input: {node.get('class_type')}", "warning", 6)

        if "[BCE:KSAMPLER]" in title:
            input_name = _seed_input_name(inputs)
            if input_name and not has_seed_tag:
                inputs[input_name] = seed
                seed_patch = {
                    "tag": "[BCE:KSAMPLER]",
                    "node_id": str(node_id),
                    "input": input_name,
                }
            if "steps" in inputs and not has_steps_tag:
                inputs["steps"] = steps

        if "[BCE:GUIDE]" in title:
            if "guidance" in inputs:
                inputs["guidance"] = guidance
            elif "cfg" in inputs:
                inputs["cfg"] = guidance
            else:
                bce.msg(f"WARNING: [BCE:GUIDE] node has no guidance/cfg input: {node.get('class_type')}", "warning", 6)

        if "[BCE:PROMPT]" in title:
            inputs["text"] = probe.get("prompt", "")

        if "[BCE:SAVE]" in title:
            class_type = str(node.get("class_type") or "")
            if "RadianceDigitalCinemaWrite" in class_type:
                inputs["filename_prefix"] = os.path.join(
                    job_dir,
                    "comfy_out",
                    result_name_base,
                )
                inputs["write_mode"] = "Sequence"
                inputs["output_path"] = ""
            elif "filename_prefix" in inputs:
                inputs["filename_prefix"] = result_name_base
            else:
                bce.msg(f"WARNING: SAVE node missing filename_prefix: {node.get('class_type')}", "warning", 6)

    if seed_patch is None:
        raise RuntimeError(
            "Selected API template has no patchable seed target. Add [BCE:SEED] to a node with noise_seed/seed, or use legacy [BCE:KSAMPLER]."
        )

    manifest["seed"] = {
        "value": seed,
        "node_id": seed_patch["node_id"],
        "input": seed_patch["input"],
        "tag": seed_patch["tag"],
    }

    try:
        with open(api_json_path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        bce.msg(f"ERROR: Failed to write API JSON: {e}", "error", 8)
        manifest["status"] = "api_json_patch_failed"
        return

    job["api_json_path"] = api_json_path

    manifest["files"] = {
        "source": source_name_base,
        "result": result_name_base,
        "source_ext": source_ext,
    }
    manifest["comfy_api"] = {
        "comfy_source_media": f"{source_name_base}.0001.{source_ext}",
    }

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
