#-------------------------------------
# BCE Node - Launch Hook
# 
# BCE VERSION 1.0.0
#
#-------------------------------------

import flame  # type: ignore

import bce_lib as bce


bce.msg("LOADED bce_launch.py", "info", 5)

# Launch prepared job: render source, write result OpenClip, start backend
# Consumes selected Write node/job files; mutates Batch compass state
def bce_launch(selection):
    try:
        job_id, job_dir, node = bce.get_job_id(selection)
        if not job_dir:
            return

        bce.dbg(f"launch node type={getattr(node, 'type', None)}")
        bce.dbg(f"launch node name={str(getattr(node, 'name', ''))}")
        bce.dbg(f"launch media_path={str(getattr(node, 'media_path', ''))}")
        bce.dbg(f"launch job_dir={job_dir}")
        manifest_path, api_json = bce.check_files(job_dir)

        if not manifest_path:
            return

        cfg = bce.load_config()
        render_mode = cfg.get("backend_mode", "local")

        if not bce.preflight_backend(render_mode):
            return

        # 1) render source write node (writes source_frame plate + .clip)
        bce.render_write_node(node)

        # 2) compute shared result_size and patch result OpenClip
        manifest = bce.load_manifest(manifest_path)
        job_id_short = manifest.get("job_id_short")
        iters = int(((manifest.get("settings") or {}).get("iterations")) or 1)
        files = manifest.get("files") or {}
        source_name_base = files.get("source")
        result_name_base = files.get("result")

        result_size = bce.compute_result_size(job_dir, manifest, api_json)

        result_clip = bce.write_result_openclip(
            job_dir,
            job_id_short,
            iters,
            api_json,
            ext="exr",
            node_name="BCE",
            result_size=result_size,
            source_name_base=source_name_base,
            result_name_base=result_name_base,
        )
        if not result_clip:
            bce.msg("launch stopped: result OpenClip was not created", "error", 8)
            return

        # 3) launch backend runner
        if not bce.run_backend(
            api_json,
            cfg,
            result_size=result_size,
            node_name="BCE",
        ):
            return

        bce.set_compass_color_for_job(job_id, bce.BCE_COLOR_LAUNCHED)

        bce.dbg(f"job_id={job_id}")
        bce.dbg(f"job_dir={job_dir}")
        bce.dbg(f"api_json={api_json}")

    except Exception as e:
        bce.msg(f"launch failed: {e}", "error", 10)


# Import finished BCE render result back into Batch
# Consumes selected job node and done flag; imports clip and marks compass done
# Import finished SAM result movie back into Batch
# Consumes selection, manifest, job_dir; imports clip and marks compass done
def import_sam_result(selection, manifest, job_dir):
    job_id, _job_dir, _node = bce.get_job_id(selection)
    done_flag = bce.os.path.join(job_dir, "comfy", "done.flag")
    if not bce.os.path.exists(done_flag):
        bce.msg("not ready (no done.flag)", "info", 5)
        return

    movie = (manifest.get("sam") or {}).get("last_result_movie")
    if not movie:
        bce.msg("SAM has no last_result_movie", "error", 8)
        return

    if not bce.os.path.exists(movie):
        bce.msg(f"missing SAM result movie: {movie}", "error", 8)
        return

    reel_name = "BCE Renders"
    try:
        if reel_name not in [r.name for r in flame.batch.reels]:
            flame.batch.create_reel(reel_name)
    except Exception:
        pass

    prev_cache_mode = None
    try:
        prev_cache_mode = flame.mediahub.files.options.cache_mode
    except Exception:
        pass

    try:
        flame.mediahub.files.options.cache_mode = True
    except Exception:
        pass

    try:
        names_before = {str(n.name) for n in flame.batch.nodes}
        try:
            flame.batch.import_clip(movie, reel_name)
        finally:
            if prev_cache_mode is not None:
                try:
                    flame.mediahub.files.options.cache_mode = prev_cache_mode
                except Exception:
                    pass

        for n in flame.batch.nodes:
            if str(n.name) not in names_before:
                try:
                    n.pos_y.set_value(n.pos_y.get_value() - 40)
                except Exception:
                    pass

        bce.set_compass_color_for_job(job_id, bce.BCE_COLOR_IMPORTED)

        kind = (manifest.get("sam") or {}).get("last_result_kind") or "movie"
        bce.msg(f"SAM import done: {kind}", "info", 8)

    except Exception as e:
        bce.msg(f"SAM import failed: {e}", "error", 10)


# Import completed BCE result back into Batch, routing SAM separately
# Consumes selection; delegates to SAM or standard import path
def import_result(selection):
    try:
        _job_id, job_dir, _node = bce.get_job_id(selection)
        if not job_dir:
            return

        manifest_path = f"{job_dir}/manifest.json"
        if not bce.os.path.exists(manifest_path):
            bce.msg(f"missing manifest: {manifest_path}", "error", 8)
            return

        _manifest_path, api_json = bce.check_files(job_dir)
        if not api_json:
            return

        manifest = bce.load_manifest(manifest_path)
        sam = manifest.get("sam") or {}
        if sam:
            return import_sam_result(selection, manifest, job_dir)

        result_size = bce.compute_result_size(job_dir, manifest, api_json)

        bce.import_result(
            selection,
            node_name="BCE",
            result_size=result_size,
        )

    except Exception as e:
        bce.msg(f"import failed: {e}", "error", 10)


#-------------------------------------
# Batch Menu
#-------------------------------------

# Classify BCE job category from the selected Write File node name
# Consumes selection; returns "sam", "ip", "op", or None
def get_bce_job_type(selection):
    for item in (selection or []):
        if isinstance(item, flame.PyNode):
            name = str(getattr(item, "name", "")).strip("'\"")
            break
    else:
        return None

    if not name.endswith("_src"):
        return None

    prefix = name.split("_", 1)[0].lower()

    if prefix.startswith("sam"):
        return "sam"
    if prefix == "ip":
        return "ip"
    if prefix == "op":
        return "op"

    return None


# Load the manifest for the job identified by selection
# Consumes selection; returns (manifest, job_dir) or (None, job_dir)
def get_job_manifest(selection):
    _job_id, job_dir, _node = bce.get_job_id(selection, quiet=True)
    if not job_dir:
        return None, None

    manifest_path = bce.os.path.join(job_dir, "manifest.json")
    if not bce.os.path.exists(manifest_path):
        return None, job_dir

    try:
        return bce.load_manifest(manifest_path), job_dir
    except Exception:
        return None, job_dir


# Check whether a SAM preview movie is already on disk for this job
# Consumes manifest and optional job_dir; returns bool
def sam_preview_exists(manifest, job_dir=None):
    sam = manifest.get("sam") or {}
    movie = sam.get("last_result_movie")
    if sam.get("last_result_kind") == "preview" and movie and bce.os.path.exists(movie):
        return True

    if job_dir:
        files = manifest.get("files") or {}
        result_name_base = files.get("result")
        if result_name_base:
            preview = bce.os.path.join(job_dir, "comfy_out", f"{result_name_base}_preview.mp4")
            return bce.os.path.exists(preview)

    return False


# Determine whether the next SAM menu action is preview or render
# Consumes selection; returns "preview", "render", or None
def get_sam_next_action(selection):
    if get_bce_job_type(selection) != "sam":
        return None

    manifest, job_dir = get_job_manifest(selection)
    if not manifest:
        return None

    sam = manifest.get("sam") or {}
    if sam_preview_exists(manifest, job_dir):
        return "render"

    return sam.get("next_action") or "render"


# Register Batch context menu actions for prepared BCE jobs
# Consumed by Flame; returns menu action descriptors
def get_batch_custom_ui_actions():
    return [
        {
            "name": "BCE",
            "actions": [
                {
                    "name": "Render Preview",
                    "isVisible": lambda sel: get_sam_next_action(sel) == "preview",
                    "execute": lambda sel: bce.launch_video_transport_job(sel, meta_key="sam", label="SAM"),
                    "minimumVersion": "2023.1.0"
                },
                {
                    "name": "Render Mattes",
                    "isVisible": lambda sel: get_sam_next_action(sel) == "render",
                    "execute": lambda sel: bce.launch_video_transport_job(sel, meta_key="sam", label="SAM"),
                    "minimumVersion": "2023.1.0"
                },
                {
                    "name": "Launch Comfy",
                    "isVisible": lambda sel: get_bce_job_type(sel) in ("ip", "op"),
                    "execute": lambda sel: bce_launch(sel),
                    "minimumVersion": "2023.1.0"
                },
                {
                    "name": "Results Import...",
                    "isVisible": lambda sel: get_bce_job_type(sel) in ("sam", "ip", "op"),
                    "execute": import_result,
                    "minimumVersion": "2023.1.0"
                },
            ],
        }
    ]
