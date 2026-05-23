#-------------------------------------
# BCE - Shared Library
#
# BCE VERSION 1.0.0
#
#-------------------------------------

import flame  # type: ignore

import math
import os
import re
import json
import time
import struct
import datetime
import subprocess
import sys
import socket
from pathlib import PurePosixPath

import pyflame_lib_bce as ui


#-------------------------------------
# Constants / Defaults
#-------------------------------------


# ------------------------------------------------
# BCE library identity
# ------------------------------------------------

SCRIPT_NAME = "BCE"
SCRIPT_VERSION = "1.0.0"

# ------------------------------------------------
# BCE install paths
# ------------------------------------------------

BCE_HOME = os.path.join(os.path.expanduser("~"), "bce")
CONFIG_DIR = os.path.join(BCE_HOME, "config")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

SCRIPT_PATH = "/opt/Autodesk/shared/python/BCE"
RUNNER_PY = SCRIPT_PATH + "/bce_runner.py"

# ------------------------------------------------
# BCE default config values
# ------------------------------------------------

DEFAULT_WORK_ROOT = os.path.join(BCE_HOME, "bce_jobs")
DEFAULT_TEMPLATES_DIR = os.path.join(BCE_HOME, "templates")
TEMPLATES_DIR = DEFAULT_TEMPLATES_DIR
DEFAULT_BACKEND_MODE = "local"
DEFAULT_LAN_PORT = "8188"
DEFAULT_CLOUD_URL = "https://cloud.comfy.org"

_CONFIG_MISSING_WARNED = False

# ------------------------------------------------
# Flame UI colors for compass nodes
# ------------------------------------------------

BCE_COLOR_PREP = (0.192, 0.326, 0.377)      # blue like serenity
BCE_COLOR_LAUNCHED = (0.507, 0.467, 0.232)      #yellow like a post-it
BCE_COLOR_IMPORTED = (0.230, 0.230, 0.230)      #grey like tired of working, done



#-------------------------------------
# Console helper
#-------------------------------------

# Show a BCE message in Flame, with print fallback outside Flame UI
# Consumes text/severity; affects console output only
def msg(text, level="info", timeout=5):
    try:
        flame.messages.show_in_console(f"[BCE] {text}", level, timeout)
    except Exception:
        print(f"[BCE] {text}")


BCE_DEBUG = 0  # set to 1 to enable verbose output

def dbg(text):
    if BCE_DEBUG:
        print(f"[BCE] {text}")


#-------------------------------------
# Setup UI (Main menu)
#-------------------------------------

# Open BCE configuration UI from the main menu
# Consumes optional Flame selection; shows setup window
def setup(selection=None, *args, **kwargs):
    BCESetupUI().show()


# Build and manage the BCE configuration dialog
# Consumes stored config; writes config when Save is pressed
class BCESetupUI:
    def __init__(self):
        self.cfg = load_config()
        self.window = None

        self.work_root_entry = None
        self.templates_entry = None

        self.comfy_root_entry = None
        self.comfy_py_entry = None

        self.lan_host_entry = None
        self.lan_port_entry = None

        self.cloud_url_entry = None
        # self.cloud_deployment_entry = None    #reserved for future
        self.cloud_api_key_entry = None

        self.local_btn = None
        self.lan_btn = None
        self.cloud_btn = None

    def show(self):
        self._build()
        self.window.show()

    def _build(self):
        def set_mode(mode):
            self.local_btn.setChecked(mode == "local")
            self.lan_btn.setChecked(mode == "lan")
            self.cloud_btn.setChecked(mode == "cloud")

        def on_save():
            self.cfg["work_root"] = self.work_root_entry.text().strip()
            self.cfg["templates_dir"] = self.templates_entry.text().strip()

            # local comfy
            self.cfg["comfy_root"] = self.comfy_root_entry.text().strip()
            self.cfg["comfy_dir"] = self.cfg["comfy_root"]
            self.cfg["comfy_py"] = self.comfy_py_entry.text().strip()

            # lan
            self.cfg["lan_host"] = self.lan_host_entry.text().strip()
            self.cfg["lan_port"] = self.lan_port_entry.text().strip()

            # cloud
            self.cfg["cloud_url"] = self.cloud_url_entry.text().strip()
            # self.cfg["cloud_deployment_id"] = self.cloud_deployment_entry.text().strip()  #reserved
            self.cfg["cloud_api_key"] = self.cloud_api_key_entry.text().strip()

            if self.local_btn.isChecked():
                self.cfg["backend_mode"] = "local"
            elif self.lan_btn.isChecked():
                self.cfg["backend_mode"] = "lan"
            else:
                self.cfg["backend_mode"] = "cloud"

            normalize_config_paths(self.cfg)
            save_config(self.cfg)
            ensure_work_root(self.cfg["work_root"])

            msg(f"saved config: {CONFIG_PATH}", "info", 6)
            dbg(f"work root ready: {self.cfg['work_root']}")
            self.window.close()

        self.window = ui.PyFlameWindow(
            title=f"{SCRIPT_NAME} Setup <small>{SCRIPT_VERSION}",
            return_pressed=on_save,
            line_color=ui.LineColor.BLUE,
            grid_layout_columns=6,
            grid_layout_rows=16,
        )

        self.work_root_entry = ui.PyFlameEntry(
            text=self.cfg.get("work_root", DEFAULT_WORK_ROOT)
        )
        self.templates_entry = ui.PyFlameEntry(
            text=self.cfg.get("templates_dir", DEFAULT_TEMPLATES_DIR)
        )

        comfy_root = self.cfg.get("comfy_root") or self.cfg.get("comfy_dir") or ""
        comfy_py = self.cfg.get("comfy_py") or ""

        self.comfy_root_entry = ui.PyFlameEntry(text=comfy_root)
        self.comfy_py_entry = ui.PyFlameEntry(text=comfy_py)

        self.lan_host_entry = ui.PyFlameEntry(text=self.cfg.get("lan_host", ""))
        self.lan_port_entry = ui.PyFlameEntry(text=self.cfg.get("lan_port", "8188"))

        self.cloud_url_entry = ui.PyFlameEntry(
            text=self.cfg.get("cloud_url", DEFAULT_CLOUD_URL)
        )
        ### reserved for future, as in other places. Not needed for 'comfy cloud'
        # self.cloud_deployment_entry = ui.PyFlameEntry(
        #     text=self.cfg.get("cloud_deployment_id", "")
        # )
        self.cloud_api_key_entry = ui.PyFlameEntry(
            text=self.cfg.get("cloud_api_key", "")
        )

        mode = self.cfg.get("backend_mode", "local")

        save_btn = ui.PyFlameButton(text="Save", connect=on_save, color=ui.Color.BLUE)
        cancel_btn = ui.PyFlameButton(text="Cancel", connect=self.window.close)

        gl = self.window.grid_layout

        # ------------------------------------------------
        # BCE  Config
        # ------------------------------------------------

        gl.addWidget(ui.PyFlameLabel(text="BCE Config", style=ui.Style.UNDERLINE), 0, 0, 1, 6)
        gl.addWidget(ui.PyFlameLabel(text="Work Root"), 1, 0)
        gl.addWidget(self.work_root_entry, 1, 1, 1, 5)
        gl.addWidget(ui.PyFlameLabel(text="Templates Dir"), 2, 0)
        gl.addWidget(self.templates_entry, 2, 1, 1, 5)



        # ------------------------------------------------
        # Rendering Method
        # ------------------------------------------------

        gl.addWidget(ui.PyFlameLabel(text="Rendering Method", style=ui.Style.UNDERLINE), 3, 0, 1, 6)

        self.local_btn = ui.PyFlamePushButton(
            text="Local",
            button_checked=(mode == "local"),
            connect=lambda: set_mode("local"),
        )

        self.lan_btn = ui.PyFlamePushButton(
            text="LAN",
            button_checked=(mode == "lan"),
            connect=lambda: set_mode("lan"),
        )

        self.cloud_btn = ui.PyFlamePushButton(
            text="Cloud",
            button_checked=(mode == "cloud"),
            connect=lambda: set_mode("cloud"),
        )

        gl.addWidget(self.local_btn, 4, 0)
        gl.addWidget(ui.PyFlameLabel(text="<i> This Machine</i>"), 4, 1, 1, 5)

        gl.addWidget(self.lan_btn, 5, 0)
        gl.addWidget(ui.PyFlameLabel(text="<i> Network Render Node</i>"), 5, 1, 1, 5)

        gl.addWidget(self.cloud_btn, 6, 0)
        gl.addWidget(ui.PyFlameLabel(text="<i>  Cloud Comfy (cloud.comfy.org for now)</i>"), 6, 1, 1, 5)

        # ------------------------------------------------
        # Local Comfy
        # ------------------------------------------------

        gl.addWidget(ui.PyFlameLabel(text="Local Comfy", style=ui.Style.UNDERLINE), 7, 0, 1, 6)
        gl.addWidget(ui.PyFlameLabel(text="Comfy Root"), 8, 0)
        gl.addWidget(self.comfy_root_entry, 8, 1, 1, 5)
        gl.addWidget(ui.PyFlameLabel(text="Comfy Python"), 9, 0)
        gl.addWidget(self.comfy_py_entry, 9, 1, 1, 5)

        # ------------------------------------------------
        # LAN Setup
        # ------------------------------------------------

        gl.addWidget(ui.PyFlameLabel(text="LAN Setup", style=ui.Style.UNDERLINE), 10, 0, 1, 6)
        gl.addWidget(ui.PyFlameLabel(text="Server Address"), 11, 0)
        gl.addWidget(self.lan_host_entry, 11, 1, 1, 5)
        gl.addWidget(ui.PyFlameLabel(text="Server Port"), 12, 0)
        gl.addWidget(self.lan_port_entry, 12, 1, 1, 5)

        # ------------------------------------------------
        # Cloud Setup
        # ------------------------------------------------

        gl.addWidget(ui.PyFlameLabel(text="Cloud Setup", style=ui.Style.UNDERLINE), 13, 0, 1, 6)
        gl.addWidget(ui.PyFlameLabel(text="Cloud Server"), 14, 0)
        gl.addWidget(self.cloud_url_entry, 14, 1, 1, 5)
        gl.addWidget(ui.PyFlameLabel(text="API Key"), 15, 0)
        gl.addWidget(self.cloud_api_key_entry, 15, 1, 1, 5)
        # reserved for future
        # gl.addWidget(ui.PyFlameLabel(text="API Key"), 16, 0)
        # gl.addWidget(self.cloud_deployment_entry, 16, 1, 1, 5)
        
        # ------------------------------------------------
        # Spacer
        # ------------------------------------------------

        gl.addWidget(ui.PyFlameLabel(text=""), 16, 0, 1, 6)

        # ------------------------------------------------
        # Buttons
        # ------------------------------------------------

        gl.addWidget(save_btn, 18, 4)
        gl.addWidget(cancel_btn, 18, 5)


#-------------------------------------
# Config
#-------------------------------------

# Build safe config values used before the user saves setup
# Returns expanded user paths and blank machine-specific values
def default_config():
    return {
        "work_root": DEFAULT_WORK_ROOT,
        "templates_dir": DEFAULT_TEMPLATES_DIR,
        "backend_mode": DEFAULT_BACKEND_MODE,
        "comfy_dir": "",
        "comfy_root": "",
        "comfy_py": "",
        "lan_host": "",
        "lan_port": DEFAULT_LAN_PORT,
        "cloud_url": DEFAULT_CLOUD_URL,
        "cloud_deployment_id": "",
        "cloud_api_key": "",
    }


# Normalize path-like config keys in place
# Consumes config dict; returns same dict for convenience
def normalize_config_paths(cfg):
    for key in ("work_root", "templates_dir", "comfy_root", "comfy_dir", "comfy_py"):
        if cfg.get(key):
            cfg[key] = os.path.abspath(os.path.expanduser(str(cfg[key])))
    return cfg


# Load BCE config, returning defaults when missing
# Consumes config path; returns normalized config dict
def load_config():
    global _CONFIG_MISSING_WARNED

    os.makedirs(CONFIG_DIR, exist_ok=True)

    if not os.path.exists(CONFIG_PATH):
        if not _CONFIG_MISSING_WARNED:
            msg("No BCE config found. Run BCE > Setup and Config.", "warning", 8)
            _CONFIG_MISSING_WARNED = True
        return default_config()

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    defaults = default_config()
    for key, value in defaults.items():
        if not cfg.get(key):
            cfg[key] = value

    if not cfg.get("comfy_root") and cfg.get("comfy_dir"):
        cfg["comfy_root"] = cfg["comfy_dir"]
    if not cfg.get("comfy_dir") and cfg.get("comfy_root"):
        cfg["comfy_dir"] = cfg["comfy_root"]

    return normalize_config_paths(cfg)


# Persist BCE config in a stable order for easier reading
# Consumes config dict; writes config JSON
def save_config(cfg):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    cfg = dict(cfg)
    normalize_config_paths(cfg)

    ordered = {
        "work_root": cfg.get("work_root") or DEFAULT_WORK_ROOT,
        "templates_dir": cfg.get("templates_dir") or DEFAULT_TEMPLATES_DIR,
        "backend_mode": cfg.get("backend_mode") or DEFAULT_BACKEND_MODE,
        "comfy_dir": cfg.get("comfy_dir") or "",
        "comfy_root": cfg.get("comfy_root") or "",
        "comfy_py": cfg.get("comfy_py") or "",
        "lan_host": cfg.get("lan_host") or "",
        "lan_port": cfg.get("lan_port") or DEFAULT_LAN_PORT,
        "cloud_url": cfg.get("cloud_url") or DEFAULT_CLOUD_URL,
        "cloud_deployment_id": cfg.get("cloud_deployment_id") or "",
        "cloud_api_key": cfg.get("cloud_api_key") or "",
    }

    text = json.dumps(ordered, indent=2)
    text = text.replace('  "backend_mode"', '\n  "backend_mode"')
    text = text.replace('  "comfy_dir"', '\n  "comfy_dir"')
    text = text.replace('  "lan_host"', '\n  "lan_host"')
    text = text.replace('  "cloud_url"', '\n  "cloud_url"')

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(text)
        f.write("\n")


# Ensure the BCE work root exists
# Consumes work root path; creates directory
def ensure_work_root(work_root):
    os.makedirs(work_root, exist_ok=True)


# Remove existing job folders below a jobs root
# Consumes jobs root path; deletes direct child directories and returns count
def purge_jobs(jobs_root):
    removed = 0

    if os.path.isdir(jobs_root):
        for name in os.listdir(jobs_root):
            path = os.path.join(jobs_root, name)
            if os.path.isdir(path):
                subprocess.run(["/bin/rm", "-rf", path], check=False)
                removed += 1

    os.makedirs(jobs_root, exist_ok=True)
    return removed


#-------------------------------------
# Job / Manifest
#-------------------------------------

# Create timestamp-based job identifiers
# Returns full and short IDs used in paths/node names
def now_job_ids():
    now = datetime.datetime.now()
    job_id       = now.strftime("%Y%m%d_%H%M%S")
    job_id_short = now.strftime("%H%M_%m%d")
    return job_id, job_id_short


# Build a new job folder structure and job metadata dict
# Consumes config, source node, selection; creates job directories
def new_job(cfg, node, selection):
    work_root = cfg.get("work_root", DEFAULT_WORK_ROOT)
    job_id, job_id_short = now_job_ids()

    job_dir = os.path.join(work_root, job_id)

    mbox_dir      = os.path.join(job_dir, "mbox")
    comfy_dir     = os.path.join(job_dir, "comfy")
    comfy_out_dir = os.path.join(job_dir, "comfy_out")

    os.makedirs(mbox_dir, exist_ok=True)
    os.makedirs(comfy_dir, exist_ok=True)
    os.makedirs(comfy_out_dir, exist_ok=True)

    mbox_setup_path = os.path.join(mbox_dir, "mbox_setup.matchbox_node")

    return {
        "cfg": cfg,
        "node": node,
        "selection": selection,

        "work_root": work_root,
        "job_id": job_id,
        "job_id_short": job_id_short,

        "job_dir": job_dir,
        "mbox_dir": mbox_dir,
        "comfy_dir": comfy_dir,
        "comfy_out_dir": comfy_out_dir,

        "mbox_setup_path": mbox_setup_path,
        "manifest_path": os.path.join(job_dir, "manifest.json"),
    }


# Create the initial manifest for a prepared job
# Consumes job metadata; returns manifest dict
def new_manifest(job):
    node = job["node"]
    return {
        "job_id": job["job_id"],
        "job_id_short": job["job_id_short"],
        "created": datetime.datetime.now().isoformat(timespec="seconds"),
        "status": "prepare_started",

        "node": str(node.name).strip("'\""),

        "seed": None,
        "template": None,
        "settings": None,
        "files": None,
        "geometry": None,
        "comfy_api": None,
    }


# Read a saved job manifest
# Consumes manifest path; returns manifest dict
def load_manifest(manifest_path):
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


# Write current manifest state to disk
# Consumes manifest path and dict; writes JSON
def save_manifest(manifest_path, manifest):
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, default=str)


#-------------------------------------
# Selection / Node helpers
#-------------------------------------


# Resolve a selected Batch node back to its BCE job folder
# Consumes selection; returns job_id, job_dir, node or Nones
def get_job_id(selection, quiet=False):
    node = None
    for item in (selection or []):
        if isinstance(item, flame.PyNode):
            node = item
            break

    if not node:
        if not quiet:
            msg("no node selected", "warning", 6)
        return None, None, None

    media_path = str(node.media_path).strip("'\"")
    p = PurePosixPath(media_path)

    parts = p.parts
    if "bce_jobs" not in parts:
        if not quiet:
            msg("Could not find BCE job folder", "warning", 6)
        return None, None, None

    i = parts.index("bce_jobs")
    job_index = None
    for idx in range(i + 1, len(parts)):
        name = parts[idx]
        if len(name) == 15 and name[8] == "_" and name.replace("_", "").isdigit():
            job_index = idx
            break

    if job_index is None:
        if not quiet:
            msg("Could not find BCE job id", "warning", 6)
        return None, None, None

    job_id = parts[job_index]

    job_dir = str(PurePosixPath(*parts[:job_index + 1]))

    return job_id, job_dir, node


# Render only the selected Write node while preserving bypass states
# Consumes Write node; mutates temporary bypass states and triggers Flame render
def render_write_node(node):
    nodes_bypass = []
    for n in flame.batch.nodes:
        if isinstance(n, (flame.PyRenderNode, flame.PyWriteFileNode)):
            nodes_bypass.append((n, n.bypass.get_value()))

    try:
        for n, _state in nodes_bypass:
            if n == node:
                n.bypass.set_value(False)
            else:
                n.bypass.set_value(True)

        dbg("rendering source Write node")
        flame.execute_shortcut("Render (Current Mode)")

    finally:
        for n, state in nodes_bypass:
            n.bypass.set_value(state)


# Return the BCE Matchbox node matching shader_name from the Flame selection
# Consumes Flame selection and shader name; returns PyNode or None
def find_matchbox_node(selection, shader_name):
    for obj in (selection or []):
        if not isinstance(obj, flame.PyNode):
            continue
        if obj.type != "Matchbox":
            continue
        if obj.shader_name == shader_name:
            return obj
    return None


def _transport_movie_path(job_dir, manifest):
    files = manifest.get("files") or {}
    result_name_base = files.get("result")
    transport_movie = files.get("transport_movie") or f"{result_name_base}_transport.mp4"
    source_video_dir = os.path.join(job_dir, "source_video")
    os.makedirs(source_video_dir, exist_ok=True)
    return os.path.join(source_video_dir, transport_movie)


def _transport_is_current(transport_path, source_dir):
    if not os.path.isfile(transport_path):
        return False

    jpgs = [
        name for name in os.listdir(source_dir)
        if name.lower().endswith(".jpg")
    ]
    if not jpgs:
        return True

    transport_mtime = os.path.getmtime(transport_path)

    for name in jpgs:
        path = os.path.join(source_dir, name)
        if os.path.isfile(path) and os.path.getmtime(path) > transport_mtime:
            return False

    return True


# Build the ffmpeg transport movie from the JPEG source sequence
# Consumes job_dir, manifest, fps; returns transport movie path
def build_transport_movie(job_dir, manifest, fps, fps_arg=None):
    source_dir = os.path.join(job_dir, "source_frame")
    transport_path = _transport_movie_path(job_dir, manifest)
    files = manifest.get("files") or {}
    source_name_base = files.get("source")
    pattern = os.path.join(source_dir, f"{source_name_base}.%04d.jpg")

    if _transport_is_current(transport_path, source_dir):
        dbg(f"SAM transport movie exists: {transport_path}")
        return transport_path

    if not os.path.isdir(source_dir):
        raise RuntimeError(f"source_frame dir missing: {source_dir}")

    jpgs = [name for name in os.listdir(source_dir) if name.lower().endswith(".jpg")]
    if not jpgs:
        raise RuntimeError(f"source JPEG sequence not found: {source_dir}")

    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", str(fps_arg or float(fps)),
        "-i", pattern,
        "-c:v", "libx264",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        transport_path,
    ]

    msg("building SAM transport movie...", "info", 6)
    dbg(" ".join(cmd))

    p = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if p.returncode != 0:
        raise RuntimeError("ffmpeg failed:\n" + (p.stderr or ""))

    if not os.path.isfile(transport_path):
        raise RuntimeError(f"SAM transport movie was not created: {transport_path}")

    deleted = 0
    for name in os.listdir(source_dir):
        if name.lower().endswith(".jpg"):
            os.remove(os.path.join(source_dir, name))
            deleted += 1

    dbg(f"deleted {deleted} SAM source JPEG frame(s)")

    dbg(f"SAM transport ready: {transport_path}")
    return transport_path


#-------------------------------------
# Job file checks
#-------------------------------------

# Validate required manifest and API files for launch/import
# Consumes job dir; returns manifest path and API JSON path or Nones
def check_files(job_dir):
    manifest_path = os.path.join(job_dir, "manifest.json")
    if not os.path.isfile(manifest_path):
        flame.messages.show_in_dialog(
            title="BCE Launch",
            message="Job folder is missing required files.\n\n"
                    "manifest.json not found.\n\n"
                    "Re-run BCE Prepare.",
            type="error",
            buttons=["Close"],
        )
        return None, None

    comfy_dir = os.path.join(job_dir, "comfy")
    if not os.path.isdir(comfy_dir):
        flame.messages.show_in_dialog(
            title="BCE Launch",
            message="Job folder is missing required files.\n\n"
                    "comfy/ folder not found.\n\n"
                    "Re-run BCE Prepare.",
            type="error",
            buttons=["Close"],
        )
        return None, None

    api_json = None
    for fname in os.listdir(comfy_dir):
        if fname.endswith("_API.json"):
            api_json = os.path.join(comfy_dir, fname)
            break

    if not api_json:
        flame.messages.show_in_dialog(
            title="BCE Launch",
            message="Job folder is missing required files.\n\n"
                    "No *_API.json found in comfy/.\n\n"
                    "Re-run BCE Prepare.",
            type="error",
            buttons=["Close"],
        )
        return None, None

    return manifest_path, api_json


#-------------------------------------
# Prepare helpers
#-------------------------------------

# Resolve the Write File export template for the active backend mode
# Consumes config and mode; returns template setup path
def get_export_template_path(cfg, backend_mode="local"):
    templates_dir = cfg.get("templates_dir", TEMPLATES_DIR)

    if backend_mode == "cloud":
        return os.path.join(templates_dir, "write_nodes", "bce_wf_tiff")

    return os.path.join(templates_dir, "write_nodes", "bce_wf_exr")


# Resolve the source-frame file extension for the active backend mode
# Consumes mode; returns extension without leading dot
def get_source_ext_for_backend(backend_mode="local"):
    if backend_mode == "cloud":
        return "tif"

    return "exr"


# Patch the saved Matchbox setup with the resolved seed value
# Consumes Matchbox setup path and seed; mutates the setup XML file
def patch_mbox_seed_value(mbox_setup_path, seed_value):
    with open(mbox_setup_path, "r", encoding="utf-8") as f:
        xml = f.read()

    m = re.search(r'(<Channel Name="Seed">.*?</Channel>)', xml, re.DOTALL)
    if not m:
        raise RuntimeError("Seed channel not found in Matchbox setup")

    block = m.group(1)

    if re.search(r"<Value>.*?</Value>", block, re.DOTALL):
        block_new = re.sub(
            r"<Value>.*?</Value>",
            f"<Value>{int(seed_value)}</Value>",
            block,
            count=1,
            flags=re.DOTALL,
        )
    else:
        if "</Channel>" not in block:
            raise RuntimeError("Malformed Seed channel in Matchbox setup")

        block_new = block.replace(
            "</Channel>",
            f"<Value>{int(seed_value)}</Value></Channel>",
            1,
        )

    xml = xml[:m.start()] + block_new + xml[m.end():]

    with open(mbox_setup_path, "w", encoding="utf-8") as f:
        f.write(xml)


# Patch a Write File export-node setup for this job's source-frame output
# Consumes template path, destination path, output path/name/frame; writes XML
def patch_export_node(src_export_node_path, dst_export_node_path, file_path, name_pattern, current_time):
    with open(src_export_node_path, "r", encoding="utf-8") as f:
        xml = f.read()

    frame = int(current_time)

    xml = re.sub(r"<FilePath>.*?</FilePath>", f"<FilePath>{file_path}</FilePath>", xml, count=1, flags=re.DOTALL)
    xml = re.sub(r"<NamePattern>.*?</NamePattern>", f"<NamePattern>{name_pattern}</NamePattern>", xml, count=1, flags=re.DOTALL)
    xml = re.sub(r"<Current_Time>.*?</Current_Time>", f"<Current_Time>{frame}</Current_Time>", xml, count=1, flags=re.DOTALL)

    with open(dst_export_node_path, "w", encoding="utf-8") as f:
        f.write(xml)


# Prepare source-frame export metadata before creating the Batch branch
# Consumes node callbacks and job paths; writes patched export setup and returns prep dict
def prepare_write_export(
    selection,
    cfg,
    job_dir,
    job_id_short,
    mbox_setup_path,
    render_mode,
    mbox_reader,
    source_finder,
    source_name_base=None,
    export_template_name=None,
):
    src = source_finder(selection)
    if not src:
        return None
    if not source_name_base:
        raise RuntimeError("missing source_name_base")

    if export_template_name:
        template_path = os.path.join(
            cfg.get("templates_dir", TEMPLATES_DIR),
            "write_nodes",
            export_template_name,
        )
    else:
        template_path = get_export_template_path(cfg, render_mode)

    out_dir = os.path.join(job_dir, "source_frame")
    os.makedirs(out_dir, exist_ok=True)

    probe = mbox_reader(mbox_setup_path)
    cur = probe["current_time"]

    patched_template_path = os.path.join(os.path.dirname(mbox_setup_path), "write_patched.export_node")
    name_pattern = f"{source_name_base}."

    patch_export_node(
        template_path,
        patched_template_path,
        out_dir + "/",
        name_pattern,
        cur,
    )

    return {
        "src": src,
        "frame": cur,
        "out_dir": out_dir,
        "probe": probe,
        "patched_template_path": patched_template_path,
        "source_name_base": source_name_base,
    }


# Build the frozen source-frame branch used by launch
# Consumes prep/job naming info; creates Mux, Write File, and Compass nodes
def add_write_branch(
    prep,
    job_id,
    job_id_short,
    mux_name_base="Node_on_frame",
    write_name_base="node_src",
    source_has_matte=False,
    freeze_current_frame=True,
    include_frame_in_mux_name=True,
):
    src = prep["src"]
    frame = prep["frame"]
    patched_template_path = prep["patched_template_path"]

    existing = [str(n.name)[1:-1] for n in flame.batch.nodes]

    mux = flame.batch.create_node("Mux")

    flame.batch.connect_nodes(src, "Default", mux, "Input_0")

    if source_has_matte:
        flame.batch.connect_nodes(src, "OutMatte", mux, "Matte_0")

    if freeze_current_frame:
        mux.range_active.set_value(True)
        mux.range_start.set_value(int(frame))
        mux.range_end.set_value(int(frame))
    else:
        mux.range_active.set_value(False)

    mux_name = mux_name_base
    if include_frame_in_mux_name:
        mux_name = f"{mux_name_base}_{frame}"

    mux.name = make_unique_name(existing, mux_name)
    existing.append(str(mux.name)[1:-1])

    mux.pos_x.set_value(src.pos_x.get_value() + 150)
    mux.pos_y.set_value(src.pos_y.get_value())

    mux.before_range = "Repeat First"
    mux.after_range = "Repeat Last"

    write_node = flame.batch.create_node("Write File")
    write_node.load_node_setup(patched_template_path)

    flame.batch.connect_nodes(mux, "Default", write_node, "Default")

    if source_has_matte:
        flame.batch.connect_nodes(mux, "OutMatte", write_node, "Matte")

    write_node.pos_x.set_value(mux.pos_x.get_value() + 250)
    write_node.pos_y.set_value(mux.pos_y.get_value() + 20)

    write_node.name = make_unique_name(existing, write_name_base)
    existing.append(str(write_node.name)[1:-1])

    comp = flame.batch.encompass_nodes([write_node])
    if not comp:
        return {"mux": mux, "write": write_node, "compass": None}

    comp.name = f"BCE Launch {job_id}"
    comp.colour = BCE_COLOR_PREP
    comp.width += 100
    comp.pos_x -= 50
    comp.height += 125
    comp.pos_y -= 150

    return {"mux": mux, "write": write_node, "compass": comp}


# Save current node setup as a Matchbox setup snapshot for this job
# Consumes job paths/node; writes setup file and mutates manifest status
def save_mbox_setup(job, manifest):
    p = job["mbox_setup_path"]
    dbg(f"Matchbox setup snapshot: {p}")
    job["node"].save_node_setup(p)
    manifest["status"] = "mbox_setup_saved"


# Return the Comfy API graph from either bare or wrapped API JSON
# Consumes loaded JSON; returns graph dict or raises for GUI/invalid templates
def api_graph_from_template(data):
    if not isinstance(data, dict):
        raise RuntimeError("Selected template is not a valid Comfy API JSON object.")

    if isinstance(data.get("nodes"), list):
        raise RuntimeError(
            "Selected template appears to be a Comfy GUI workflow, not API JSON. Use an API JSON template."
        )

    if isinstance(data.get("prompt"), dict):
        return data["prompt"]

    return data


# Iterate node-like API entries while safely skipping unrelated values
# Consumes API graph dict; yields (node_id, node) entries with class_type and/or inputs
def iter_api_items(graph):
    if not isinstance(graph, dict):
        raise RuntimeError("Selected template API graph is not a valid JSON object.")

    for node_id, node in graph.items():
        if not isinstance(node, dict):
            continue
        if "class_type" not in node and "inputs" not in node:
            continue
        yield str(node_id), node


# Iterate node-like API entries while safely skipping unrelated values
# Consumes API graph dict; yields node dicts with class_type and/or inputs
def iter_api_nodes(graph):
    for _node_id, node in iter_api_items(graph):
        yield node


# Record created Batch branch paths/nodes for later launch and manifest lookup
# Consumes shared prep info and created nodes; mutates job and manifest
def record_write_branch(job, manifest, prep, nodes):
    job["branch_info"] = {
        "template_used": prep["patched_template_path"],
        "out_dir": prep["out_dir"],
        "probe": prep["probe"],
        "write_node": nodes["write"],
        "mux_node": nodes["mux"],
        "compass_node": nodes["compass"],
    }
    job["probe"] = prep["probe"]

    manifest["settings"] = prep["probe"]
    manifest["status"] = "write_node_created"


# Find a tagged node in a Comfy API graph
# Consumes API dict and tag/class filter; returns (node_id, node) or (None, None)
def find_api_node_by_tag(wf, tag, class_type=None):
    for nid, node in (wf or {}).items():
        title = ((node.get("_meta") or {}).get("title") or "")
        if tag in title and (class_type is None or node.get("class_type") == class_type):
            return nid, node
    return None, None


# Mutate a tagged [BCE:LOAD] node in place for cloud mode.
# Consumes API node/image name; returns the same node with LoadImage inputs.
def mutate_load_node_for_cloud(node, image_name):
    meta = node.get("_meta")

    node["class_type"] = "LoadImage"
    node["inputs"] = {
        "image": image_name,
    }

    if meta is not None:
        node["_meta"] = meta

    title = ((node.get("_meta") or {}).get("title") or "")
    if "[BCE:LOAD]" not in title:
        node.setdefault("_meta", {})["title"] = "Load Image [BCE:LOAD]"

    return node


#-------------------------------------
# Image and result-size helpers
#-------------------------------------

# Read dimensions from supported image headers without loading pixels
# Consumes PNG/TIFF/EXR path; returns (width, height) or (None, None)
def read_image_size(path):
    p = path.lower()

    if p.endswith(".png"):
        with open(path, "rb") as f:
            if f.read(8) != b"\x89PNG\r\n\x1a\n":
                return None, None
            f.seek(16)
            w = struct.unpack(">I", f.read(4))[0]
            h = struct.unpack(">I", f.read(4))[0]
        return w, h

    if p.endswith(".tif") or p.endswith(".tiff"):
        with open(path, "rb") as f:
            header = f.read(8)
            if len(header) != 8:
                return None, None

            byte_order = header[:2]
            if byte_order == b"II":
                endian = "<"
            elif byte_order == b"MM":
                endian = ">"
            else:
                return None, None

            if struct.unpack(endian + "H", header[2:4])[0] != 42:
                return None, None

            ifd_offset = struct.unpack(endian + "I", header[4:8])[0]
            f.seek(ifd_offset)
            raw_count = f.read(2)
            if len(raw_count) != 2:
                return None, None

            count = struct.unpack(endian + "H", raw_count)[0]
            width = None
            height = None

            for _i in range(count):
                entry = f.read(12)
                if len(entry) != 12:
                    return None, None

                tag, field_type, value_count, value_offset = struct.unpack(endian + "HHII", entry)
                if tag not in (256, 257) or value_count < 1:
                    continue

                value = None
                if field_type == 3:
                    if endian == "<":
                        value = value_offset & 0xFFFF
                    else:
                        value = value_offset >> 16
                elif field_type == 4:
                    value = value_offset

                if tag == 256:
                    width = value
                elif tag == 257:
                    height = value

            if width and height:
                return int(width), int(height)

        return None, None

    if p.endswith(".exr"):
        with open(path, "rb") as f:
            if f.read(4) != b"\x76\x2f\x31\x01":
                return None, None

            f.seek(8)

            display_w = display_h = None
            data_w = data_h = None

            while True:
                name = bytearray()
                while True:
                    c = f.read(1)
                    if not c:
                        return None, None
                    if c == b"\x00":
                        break
                    name.extend(c)

                if not name:
                    break

                atype = bytearray()
                while True:
                    c = f.read(1)
                    if not c:
                        return None, None
                    if c == b"\x00":
                        break
                    atype.extend(c)

                size_bytes = f.read(4)
                if len(size_bytes) != 4:
                    return None, None
                size = struct.unpack("<I", size_bytes)[0]
                value = f.read(size)
                if len(value) != size:
                    return None, None

                if bytes(name) in (b"displayWindow", b"dataWindow"):
                    if size != 16:
                        continue
                    xmin, ymin, xmax, ymax = struct.unpack("<4i", value)
                    w = xmax - xmin + 1
                    h = ymax - ymin + 1

                    if bytes(name) == b"displayWindow":
                        display_w, display_h = w, h
                    else:
                        data_w, data_h = w, h

            if display_w and display_h:
                return display_w, display_h
            if data_w and data_h:
                return data_w, data_h

    return None, None


# Determine source/output extensions from tagged API load/save nodes
# Consumes Comfy API JSON path; returns source and output extensions
def read_api_io_exts(api_json):
    src_ext = "exr"
    out_ext = "png"

    try:
        with open(api_json, "r", encoding="utf-8") as f:
            wf = json.load(f)

        _nid, n_load = find_api_node_by_tag(wf, "[BCE:LOAD]")
        if n_load:
            load_type = str(n_load.get("class_type") or "")
            if load_type == "LoadEXR":
                src_ext = "exr"
            elif "RadianceDigitalCinemaRead" in load_type:
                src_ext = "exr"
            elif load_type == "LoadImage":
                src_ext = "tif"

        _nid, n_save = find_api_node_by_tag(wf, "[BCE:SAVE]")
        if n_save:
            save_type = str(n_save.get("class_type") or "")
            if save_type == "SaveEXR":
                out_ext = "exr"
            elif "RadianceDigitalCinemaWrite" in save_type:
                out_ext = "exr"
            elif save_type == "SaveImage":
                out_ext = "png"

    except Exception:
        pass

    return src_ext, out_ext


# Build the shared result-size payload used by launch/import helpers
# Consumes dimensions and offsets; returns normalized result_size dict
def build_result_size(src_w, src_h, out_w, out_h, x_offset=0.0, y_offset=0.0):
    src_w = int(src_w)
    src_h = int(src_h)
    out_w = int(out_w)
    out_h = int(out_h)

    src_mp = (src_w * src_h) / 1_000_000.0
    out_mp = (out_w * out_h) / 1_000_000.0

    return {
        "src_w": src_w,
        "src_h": src_h,
        "out_w": out_w,
        "out_h": out_h,
        "x_offset": float(x_offset),
        "y_offset": float(y_offset),
        "mp_delta": float(out_mp - src_mp),
        "same_size": (src_w == out_w and src_h == out_h),
    }


# Compute result sizing from manifest geometry
# Consumes job dir, manifest, and API JSON; returns result_size dict
def compute_result_size(job_dir, manifest, api_json):
    job_id_short = manifest.get("job_id_short")
    if not job_id_short:
        raise RuntimeError("missing job_id_short")

    files = manifest.get("files") or {}
    source_name_base = files.get("source")
    if not source_name_base:
        raise RuntimeError("missing files.source")

    src_ext = files.get("source_ext")
    if not src_ext:
        comfy_api = manifest.get("comfy_api") or {}
        comfy_source_media = str(comfy_api.get("comfy_source_media") or "")
        _root, ext = os.path.splitext(comfy_source_media)
        src_ext = ext.lstrip(".")
    if not src_ext:
        src_ext, _out_ext = read_api_io_exts(api_json)
    src_plate = os.path.join(
        job_dir,
        "source_frame",
        f"{source_name_base}.0001.{src_ext}",
    )

    src_w, src_h = read_image_size(src_plate)
    if not (src_w and src_h):
        raise RuntimeError(f"could not read source size: {src_plate}")

    policy = manifest.get("geometry") or {"mode": "same_as_source"}
    mode = str(policy.get("mode") or "same_as_source")

    if mode == "same_as_source":
        out_w = int(src_w)
        out_h = int(src_h)
        x_offset = 0.0
        y_offset = 0.0

    elif mode == "source_plus_padding":
        left = int(policy.get("left") or 0)
        right = int(policy.get("right") or 0)
        top = int(policy.get("top") or 0)
        bottom = int(policy.get("bottom") or 0)

        out_w = int(src_w) + left + right
        out_h = int(src_h) + top + bottom
        x_offset = (left - right) / 2.0
        y_offset = (bottom - top) / 2.0

    elif mode == "source_scale":
        scale_x = float(policy.get("scale_x") or 1.0)
        scale_y = float(policy.get("scale_y") or 1.0)

        out_w = int(round(int(src_w) * scale_x))
        out_h = int(round(int(src_h) * scale_y))
        x_offset = 0.0
        y_offset = 0.0

    elif mode == "explicit_size":
        out_w = int(policy.get("out_w") or 0)
        out_h = int(policy.get("out_h") or 0)
        x_offset = float(policy.get("x_offset") or 0.0)
        y_offset = float(policy.get("y_offset") or 0.0)

        if not (out_w and out_h):
            raise RuntimeError("explicit_size result_policy missing out_w/out_h")

    else:
        raise RuntimeError(f"unknown result_policy mode: {mode}")

    result_size = build_result_size(src_w, src_h, out_w, out_h, x_offset, y_offset)
    result_size["show_axis_offset"] = bool(policy.get("show_axis_offset", False))

    return result_size


# Show the launch confirmation, with result-size context when available
# Consumes optional result_size, node label, backend note; returns selected dialog button
def launch_dialog(result_size=None, node_name="BCE", launch_note=""):
    if result_size is not None:
        if result_size.get("same_size"):
            size_line = "           RESULT SIZE UNCHANGED\n\n"
        else:
            size_line = f"           ADDING {float(result_size.get('mp_delta', 0.0)):+.2f} MegaPixels \n\n"

        out_w = int(result_size.get("out_w") or 0)
        out_h = int(result_size.get("out_h") or 0)
        message = (
            size_line +
            f"{node_name} result: {out_w}×{out_h}\n\n" +
            "About to start BCE backend.\n\n" +
            launch_note +
            "\n\n\n"
            "Proceed?"
        )
    else:
        message = (
            "About to start BCE backend.\n\n" +
            launch_note +
            "\n\n\n"
            "Proceed?"
        )

    return flame.messages.show_in_dialog(
        title="BCE Launch",
        message=message,
        type="warning",
        buttons=["Cancel","Launch"],
    )


#-------------------------------------
# OpenClip patching for result import
#-------------------------------------

# Wait briefly for Flame-rendered files to appear on disk
# Consumes path/timeout; returns True when file exists
def _wait_for_file(path, timeout_s=3.0):
    t0 = time.time()
    while (time.time() - t0) < timeout_s:
        if os.path.exists(path):
            return True
        time.sleep(0.1)
    return False


# Read playback FPS from Flame's rendered source OpenClip.
# Used by SAM transport-movie generation after the Write node renders.
# Read a single numeric rate value from an OpenClip XML tag
# Consumes XML string and tag name; returns float or None
def _read_rate_value(xml, tag_name):
    m = re.search(
        rf"<{tag_name}[^>]*>\s*<numerator>([^<]+)</numerator>\s*<denominator>([^<]+)</denominator>\s*</{tag_name}>",
        xml,
        re.DOTALL,
    )
    if m:
        num_text = m.group(1).strip()
        den_text = m.group(2).strip()
        num = float(num_text)
        den = float(den_text)
        if den:
            return (num / den), f"{num_text}/{den_text}"

    m = re.search(rf"<{tag_name}[^>]*>([^<]+)</{tag_name}>", xml)
    if m:
        value_text = m.group(1).strip()
        return float(value_text), value_text

    return None, None


# Read the edit rate from a source OpenClip file
# Consumes clip path; returns (fps float, fps_arg string)
def read_clip_rate(clip_path):
    with open(clip_path, "r", encoding="utf-8") as f:
        xml = f.read()

    for tag_name in ("editRate", "sampleRate"):
        fps, fps_arg = _read_rate_value(xml, tag_name)
        if fps is not None:
            return fps, fps_arg

    return 24.0, "24"



# Render source, build transport movie, and start backend for a video job
# Consumes selection and meta key; drives render, ffmpeg, and runner
def launch_video_transport_job(selection, meta_key="sam", require_cloud=False, label="SAM"):
    try:
        job_id, job_dir, node = get_job_id(selection)
        if not job_dir:
            return

        manifest_path, api_json = check_files(job_dir)
        if not manifest_path:
            return

        cfg = load_config()
        render_mode = cfg.get("backend_mode", "local")

        if require_cloud and render_mode != "cloud":
            msg(f"BCE {label} currently supports Cloud mode only.", "error", 8)
            return

        if not preflight_backend(render_mode):
            return

        manifest = load_manifest(manifest_path)
        files = manifest.get("files") or {}
        source_name_base = files.get("source")
        if not source_name_base:
            msg(f"{label} manifest missing files.source", "error", 8)
            return

        transport_path = _transport_movie_path(job_dir, manifest)
        source_dir = os.path.join(job_dir, "source_frame")
        if not _transport_is_current(transport_path, source_dir):
            render_write_node(node)

        clip_path = os.path.join(job_dir, "source_frame", f"{source_name_base}.clip")
        if not os.path.isfile(clip_path):
            msg(f"{label} source .clip missing: {clip_path}", "error", 8)
            return

        fps, fps_arg = read_clip_rate(clip_path)
        manifest_fps = math.trunc(fps * 1000) / 1000

        manifest.setdefault(meta_key, {})["fps"] = manifest_fps
        manifest.setdefault(meta_key, {})["transport_path"] = transport_path
        save_manifest(manifest_path, manifest)

        transport_path = build_transport_movie(job_dir, manifest, fps, fps_arg=fps_arg)

        manifest = load_manifest(manifest_path)
        manifest.setdefault(meta_key, {})["fps"] = manifest_fps
        manifest.setdefault(meta_key, {})["transport_path"] = transport_path
        save_manifest(manifest_path, manifest)

        if not run_backend(api_json, cfg, node_name=label):
            return

        set_compass_color_for_job(job_id, BCE_COLOR_LAUNCHED)

        msg(f"{label} launch complete.", "info", 8)
        dbg(f"fps={fps}")
        dbg(f"transport={transport_path}")

    except Exception as e:
        msg(f"{label} launch failed: {e}", "error", 10)


# Create the result OpenClip expected by Flame import
# Consumes job paths/API/result_size; writes .clip and returns its path
def write_result_openclip(
    job_dir,
    job_id_short,
    iters,
    api_json,
    ext=None,
    node_name="BCE",
    result_size=None,
    source_name_base=None,
    result_name_base=None,
):
    _src_ext, out_ext = read_api_io_exts(api_json)
    if ext is None:
        ext = out_ext

    if not source_name_base:
        msg(f"{node_name} source_name_base is required before writing result .clip", "error", 8)
        return None
    if not result_name_base:
        msg(f"{node_name} result_name_base is required before writing result .clip", "error", 8)
        return None

    src_openclip = os.path.join(job_dir, "source_frame", f"{source_name_base}.clip")
    dst_clip     = os.path.join(job_dir, "comfy_out",   f"{result_name_base}.clip")

    if not _wait_for_file(src_openclip, timeout_s=3.0):
        msg(f"missing source .clip: {src_openclip}", "error", 8)
        return None

    if result_size is None:
        msg(f"could not determine {node_name} result size", "error", 8)
        return None

    out_w = int(result_size.get("out_w") or 0)
    out_h = int(result_size.get("out_h") or 0)

    with open(src_openclip, "r", encoding="utf-8") as f:
        xml = f.read()

    xml = re.sub(
        rf'(<name type="string">){re.escape(source_name_base)}(</name>)',
        lambda m: m.group(1) + result_name_base + m.group(2),
        xml
    )

    xml = re.sub(
        r'(<width type="uint">)\d+(</width>)',
        lambda m: m.group(1) + str(out_w) + m.group(2),
        xml,
        count=1
    )

    xml = re.sub(
        r'(<height type="uint">)\d+(</height>)',
        lambda m: m.group(1) + str(out_h) + m.group(2),
        xml,
        count=1
    )

    seq_path = os.path.join(job_dir, "comfy_out", f"{result_name_base}.[0001-{int(iters):04d}].{ext}")

    xml = re.sub(
        r'(<path encoding=")(file|pattern)(">).*?(</path>)',
        lambda m: m.group(1) + "pattern" + m.group(3) + seq_path + m.group(4),
        xml,
        count=1,
        flags=re.DOTALL
    )

    os.makedirs(os.path.dirname(dst_clip), exist_ok=True)
    with open(dst_clip, "w", encoding="utf-8") as f:
        f.write(xml)

    dbg(f"wrote result .clip: {dst_clip} ({out_w}x{out_h})")
    return dst_clip


#-------------------------------------
# Result import
#-------------------------------------

# Import completed BCE result clip and update job compass state
# Consumes selection/result_size; imports clip and mutates compass colour
def import_result(selection, node_name="BCE", result_size=None):
    job_id, job_dir, _node = get_job_id(selection)
    if not job_dir:
        return

    done_flag = os.path.join(job_dir, "comfy", "done.flag")
    if not os.path.exists(done_flag):
        msg("not ready (no done.flag)", "info", 5)
        return

    manifest_path = os.path.join(job_dir, "manifest.json")
    manifest = load_manifest(manifest_path)
    files = manifest.get("files") or {}
    result_name_base = files.get("result")
    if not result_name_base:
        msg("missing files.result", "error", 8)
        return

    clip = os.path.join(job_dir, "comfy_out", f"{result_name_base}.clip")
    if not os.path.exists(clip):
        msg(f"missing result .clip: {clip}", "error", 8)
        return

    reel_name = "BCE Renders"
    if reel_name not in [r.name for r in flame.batch.reels]:
        flame.batch.create_reel(reel_name)

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
        # BCE forces MediaHub cache during import and restores the user's setting afterward.
        names_before = {str(n.name) for n in flame.batch.nodes}
        try:
            flame.batch.import_clip(clip, reel_name)
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

        set_compass_color_for_job(job_id, BCE_COLOR_IMPORTED)

        if result_size and result_size.get("show_axis_offset"):
            x = float(result_size.get("x_offset") or 0.0)
            y = float(result_size.get("y_offset") or 0.0)
            msg(f"IMPORT DONE: AXIS OFFSET  X= {x:.0f}  Y= {y:.0f}", "info", 12)

    except Exception as e:
        msg(f"import failed: {e}", "error", 10)


#-------------------------------------
# Backend and Batch state helpers
#-------------------------------------

# Return whether a TCP port accepts a quick connection
# Check whether a TCP port is accepting connections
# Consumes host/port/timeout; returns bool
def _tcp_listening(host, port, timeout_s=1.0):
    try:
        with socket.create_connection((host, int(port)), timeout=timeout_s):
            return True
    except Exception:
        return False


# Check the selected backend is in a sane state before starting/submitting
# Verify the configured backend is reachable before launch
# Consumes render mode; shows error and returns False if not ready
def preflight_backend(render_mode):
    cfg = load_config()
    mode = (render_mode or cfg.get("backend_mode") or DEFAULT_BACKEND_MODE).strip().lower()

    if mode == "local":
        if _tcp_listening("127.0.0.1", 8188, timeout_s=0.5):
            msg("Local ComfyUI is already using port 8188.", "error", 8)
            msg("Close the existing ComfyUI process, or restart it cleanly, then try BCE again.", "error", 8)
            return False
        return True

    if mode == "lan":
        host = str(cfg.get("lan_host", "")).strip()
        port = str(cfg.get("lan_port", DEFAULT_LAN_PORT)).strip() or DEFAULT_LAN_PORT
        if not host or not _tcp_listening(host, int(port), timeout_s=2.0):
            msg(f"LAN ComfyUI is not reachable at {host}:{port}.", "error", 8)
            msg("Start or check the LAN ComfyUI server, then try BCE again.", "error", 8)
            return False
        return True

    if mode == "cloud":
        cloud_url = str(cfg.get("cloud_url", "")).strip()
        cloud_api_key = str(cfg.get("cloud_api_key", "")).strip()
        if not cloud_url or not cloud_api_key:
            msg("Cloud backend is not ready.", "error", 8)
            msg("Check the API key and backend settings in BCE Setup, then try again.", "error", 8)
            return False
        return True

    msg(f"Unknown backend mode: {mode}", "error", 8)
    return False

# Return a unique Batch node name based on existing names
# Consumes existing names and desired name; returns safe unique name
def make_unique_name(existing_names, new_name):
    if new_name not in existing_names:
        return new_name

    counter = 1
    while True:
        potential_name = f"{new_name}_{counter}"
        if potential_name not in existing_names:
            return potential_name
        counter += 1


# Locate the launch compass for a prepared job
# Consumes job_id; returns compass node or None
def find_compass_for_job(job_id):
    for n in flame.batch.nodes:
        try:
            name = str(n.name)[1:-1]
        except Exception:
            continue

        if job_id in name:
            return n

    return None


# Update the launch compass colour for job state feedback
# Consumes job_id and colour tuple; returns whether a compass was updated
def set_compass_color_for_job(job_id, colour):
    comp = find_compass_for_job(job_id)
    if not comp:
        return False

    try:
        comp.colour = colour
        return True
    except Exception:
        return False


# Confirm launch and start the BCE runner process for the API job
# Consumes API JSON/config/result_size; writes runner log and spawns backend
def run_backend(api_json, cfg=None, result_size=None, node_name="BCE"):
    if cfg is None:
        cfg = load_config()

    mode = cfg.get("backend_mode", "local")

    comfy_root = cfg.get("comfy_root") or cfg.get("comfy_dir") or ""
    comfy_py   = cfg.get("comfy_py") or ""
    runner_py  = cfg.get("runner_py") or RUNNER_PY

    cloud_url = str(cfg.get("cloud_url", "")).strip()
    cloud_api_key = str(cfg.get("cloud_api_key", "")).strip()

    if mode == "local":
        if not comfy_root or not comfy_py:
            msg(
                "Local backend is not configured.\n"
                "Open BCE Config and set Comfy Root and Comfy Python.",
                "error",
                8,
            )
            return False

    if mode == "cloud":
        launch_note = "Cloud render will use your configured hosted backend."
    elif mode == "lan":
        launch_note = "LAN render will use your configured network render node."
    else:
        launch_note = "Local Comfy will tax your GPU."

    resp = launch_dialog(result_size, node_name, launch_note)

    if resp != "Launch":
        msg("launch cancelled", "info", 5)
        return False

    job_dir = os.path.dirname(os.path.dirname(api_json))
    runner_log = os.path.join(job_dir, "comfy", "runner.log")

    dbg("launching BCE runner...")
    msg("BCE running in background — check Messages for progress", "info", 8)

    env = os.environ.copy()
    env["BCE_COMFY_ROOT"] = comfy_root
    env["BCE_COMFY_PY"] = comfy_py
    env["BCE_BACKEND_MODE"] = mode
    env["BCE_LAN_HOST"] = str(cfg.get("lan_host", "")).strip()
    env["BCE_LAN_PORT"] = str(cfg.get("lan_port", "8188")).strip()
    env["BCE_CLOUD_URL"] = cloud_url
    env["BCE_CLOUD_API_KEY"] = cloud_api_key

    try:
        f = open(runner_log, "w")
        f.write("[BCE] runner invoked\n")
        f.write(f"[BCE] api_json={api_json}\n")
        f.write(f"[BCE] BCE_COMFY_ROOT={env['BCE_COMFY_ROOT']}\n")
        f.write(f"[BCE] BCE_COMFY_PY={env['BCE_COMFY_PY']}\n")
        f.write(f"[BCE] BCE_BACKEND_MODE={env['BCE_BACKEND_MODE']}\n")
        f.write(f"[BCE] BCE_LAN_HOST={env['BCE_LAN_HOST']}\n")
        f.write(f"[BCE] BCE_LAN_PORT={env['BCE_LAN_PORT']}\n")
        f.write(f"[BCE] BCE_CLOUD_URL={env['BCE_CLOUD_URL']}\n")
        f.write(f"[BCE] BCE_CLOUD_API_KEY={'set' if env['BCE_CLOUD_API_KEY'] else ''}\n")
        f.flush()

        subprocess.Popen(
            [sys.executable, runner_py, api_json],
            env=env,
            cwd=job_dir,
            stdout=f,
            stderr=f,
        )

        dbg("runner started")
        return True

    except Exception as e:
        msg(f"runner failed to start: {e}", "error", 10)
        return False


#-------------------------------------
# Main Menu (Setup)
#-------------------------------------

# Confirm and purge BCE job folders from the configured jobs root
# Consumes menu invocation; deletes job folders after user confirmation
def cleanup_jobs_dir(selection=None, *args, **kwargs):
    cfg = load_config()
    work_root = cfg.get("work_root", DEFAULT_WORK_ROOT).strip()

    if not work_root:
        msg("no work root set", "warning", 6)
        return

    jobs_root = work_root

    resp = flame.messages.show_in_dialog(
        title="BCE",
        message="Delete all BCE temporary job folders under:\n\n"
                f"{jobs_root}\n\n"
                "This does not delete cached media.\n\n"
                "Proceed?",
        type="warning",
        buttons=["Cancel", "Remove"],
    )

    if resp != "Remove":
        msg("purge cancelled", "info", 5)
        return

    removed = purge_jobs(jobs_root)
    msg(f"purged {removed} job folder(s)", "info", 8)


# Register BCE main menu actions
# Consumed by Flame; returns setup and purge action descriptors
def get_main_menu_custom_ui_actions():
    return [
        {
            "name": "BCE",
            "hierarchy": [],
            "actions": [
                {
                    "name": "Setup and Config",
                    "execute": setup,
                    "minimumVersion": "2023.1"
                },
                {
                    "name": "Purge old Jobs...",
                    "execute": cleanup_jobs_dir,
                    "minimumVersion": "2023.1"
                },
            ]
        }
    ]
