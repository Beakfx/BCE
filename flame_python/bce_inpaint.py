
# BCE Inpaint Node - Prepare Hook


import os
import re
import json
import random
import flame  # type: ignore
import bce_lib as bce


# Workflow popup order in BCE_Inpaint.xml:
#   0 = Flux.2 Klein9B Inpaint
#   1 = Qwen Inpaint
#
# Flame saves the popup as a positional integer.
# Keep these template numbers matched to the XML PopupEntry order.

TEMPLATE_0 = "bce_IP_flux2_klein9b_API.json"
TEMPLATE_1 = "bce_IP_qwen_2509_API.json"


SHADER_NAME = "BCE Inpaint"
WORK_SUBDIR = "inpaint"
NODE_LABEL = "Inpaint"
ARTIFACT_PREFIX = "ip"


bce.msg(f"LOADED {os.path.basename(__file__)}", "info", 5)


#-------------------------------------
# Entry
#-------------------------------------


# Fill Flame-default control values that may be absent from the saved Matchbox setup XML
# Consumes parsed parameter dict; mutates and returns the same dict
def normalize_probe_defaults(probe):
    if probe["workflow_index"] is None:
        probe["workflow_index"] = 0

    if probe["iterations"] is None:
        probe["iterations"] = 4

    if probe["steps"] is None:
        probe["steps"] = 5

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
        manifest["cloud_invert_loadimage_mask"] = True
        manifest["files"] = {
            "source": source_name_base,
            "result": result_name_base,
        }

        bce.save_mbox_setup(job, manifest)
        _resolve_probe_seed(job, manifest)
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
        )

        if prep:
            nodes = bce.add_write_branch(
                prep,
                job["job_id"],
                job["job_id_short"],
                mux_name_base=f"{NODE_LABEL}_on_frame",
                write_name_base=source_name_base,
                source_has_matte=True,
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
        vals = re.findall(r"<Parameter>\s*<value>(-?\d+(?:\.\d+)?)</value>\s*</Parameter>", block)
        if index >= len(vals):
            return None
        return float(vals[index])

    out["workflow_index"] = read_shader_param(0)
    out["iterations"] = read_chan("Iterations")
    out["steps"] = read_chan("Steps")
    out["lanpaint_steps"] = read_chan("LanPaint Steps")
    out["seed"] = read_chan("Seed")

    for k in ("workflow_index", "iterations", "steps", "lanpaint_steps", "seed"):
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
        if "[BCE:PROMPT]" in title:
            tags.add("[BCE:PROMPT]")
        if "[BCE:SEED]" in title:
            tags.add("[BCE:SEED]")
        if "[BCE:STEPS]" in title:
            tags.add("[BCE:STEPS]")
        if "[BCE:SAMPLER]" in title:
            tags.add("[BCE:SAMPLER]")
        if "[BCE:KSAMPLER]" in title:
            tags.add("[BCE:KSAMPLER]")

    required = ("[BCE:LOAD]", "[BCE:SAVE]", "[BCE:PROMPT]")
    missing = [tag for tag in required if tag not in tags]
    found_tags = ", ".join(sorted(tags)) or "(none)"
    tag_context = f"\nTemplate: {template_path}\nFound BCE tags: {found_tags}"

    if missing:
        raise RuntimeError(
            f"Selected API template is missing required BCE tag(s): {', '.join(missing)}"
            f"{tag_context}"
        )

    seed_tags = ("[BCE:SEED]", "[BCE:SAMPLER]", "[BCE:KSAMPLER]")
    if not any(tag in tags for tag in seed_tags):
        raise RuntimeError(
            "Selected API template is missing BCE seed control tag: [BCE:SEED] or [BCE:SAMPLER]/[BCE:KSAMPLER]"
            f"{tag_context}"
        )

    steps_tags = ("[BCE:STEPS]", "[BCE:SAMPLER]", "[BCE:KSAMPLER]")
    if not any(tag in tags for tag in steps_tags):
        raise RuntimeError(
            "Selected API template is missing BCE steps control tag: [BCE:STEPS] or [BCE:SAMPLER]/[BCE:KSAMPLER]"
            f"{tag_context}"
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

    seed = int(probe.get("seed", 0))
    steps = int(probe.get("steps", 5))
    lanpaint_steps = probe.get("lanpaint_steps")
    seed_patch = None

    for node_id, node in bce.iter_api_items(graph):
        title = (node.get("_meta", {}).get("title") or "").upper()
        inputs = node.get("inputs", {})

        # load
        if "[BCE:LOAD]" in title:
            if render_mode == "cloud":
                bce.mutate_load_node_for_cloud(
                    node,
                    f"{source_name_base}.0001.{source_ext}",
                )
            elif "source_path" in inputs:
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

        # prompt
        if "[BCE:PROMPT]" in title:
            if "text" in inputs:
                inputs["text"] = probe.get("prompt", "")
            elif "prompt" in inputs:
                inputs["prompt"] = probe.get("prompt", "")

        # guide
        if "[BCE:GUIDE]" in title:
            pass

        # modern seed
        if "[BCE:SEED]" in title:
            if "noise_seed" in inputs:
                seed_input = "noise_seed"
            elif "seed" in inputs:
                seed_input = "seed"
            else:
                raise RuntimeError(
                    "Selected API template has [BCE:SEED] but no noise_seed or seed input."
                )

            inputs[seed_input] = seed
            seed_patch = {
                "tag": "[BCE:SEED]",
                "node_id": str(node_id),
                "input": seed_input,
            }

        # modern steps
        if "[BCE:STEPS]" in title:
            if "steps" not in inputs:
                raise RuntimeError("Selected API template has [BCE:STEPS] but no steps input.")
            inputs["steps"] = steps

        # legacy monolithic sampler
        if "[BCE:SAMPLER]" in title or "[BCE:KSAMPLER]" in title:
            legacy_tag = "[BCE:SAMPLER]" if "[BCE:SAMPLER]" in title else "[BCE:KSAMPLER]"

            if seed_patch is None:
                if "seed" in inputs:
                    inputs["seed"] = seed
                    seed_patch = {
                        "tag": legacy_tag,
                        "node_id": str(node_id),
                        "input": "seed",
                    }
                elif "noise_seed" in inputs:
                    inputs["noise_seed"] = seed
                    seed_patch = {
                        "tag": legacy_tag,
                        "node_id": str(node_id),
                        "input": "noise_seed",
                    }

            if "steps" in inputs:
                inputs["steps"] = steps

            if "LanPaint_NumSteps" in inputs and lanpaint_steps is not None:
                inputs["LanPaint_NumSteps"] = int(lanpaint_steps)

        # save
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

    if seed_patch is None:
        raise RuntimeError(
            "Selected API template has no BCE seed target. Tag RandomNoise [BCE:SEED] or a monolithic sampler [BCE:SAMPLER]/[BCE:KSAMPLER]."
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
                    "minimumVersion": "2023.1.0"
                }
            ],
        }
    ]
