# Install BCE

Batch Comfy Extensions for Autodesk Flame.

This guide walks you through installing BCE and picking a backend.
Most artists need 10 minutes for local install plus however long Comfy
takes to download models.

---

## 1. What you need

- Autodesk Flame 2023.1 or later, Linux or Mac
- One of:
  - **Local backend** — a workstation with an NVIDIA GPU and ComfyUI installed
  - **LAN backend** — a render node on your network with ComfyUI installed, plus a shared filesystem
  - **Cloud backend** — a Comfy Cloud account ([platform.comfy.org](https://platform.comfy.org)) and API key. *Recommended default for Mac users — see section 4c.*

You can use more than one. Switching is a toggle in BCE Setup.

---

## 2. Install BCE

Download the BCE release zip and unzip it somewhere. From the unzipped
folder, run the installer:

```
./install_bce.sh
```

The installer will prompt for `sudo` (Flame's shared python folder is
owned by root). It copies code to `/opt/Autodesk/shared/python/BCE/`
and user files to `~/bce/`. The Matchbox shaders that drive the BCE
Batch nodes land in `~/bce/matchbox/` — you'll load them in section 5.

When the installer finishes, restart Flame.

If you can't run the installer, see [Manual install](#manual-install) at
the end of this doc.

---

## 3. Run Setup

In Flame: **BCE → Setup and Config**.

Fill in:

- **Work Root** — where BCE writes job folders. Default `~/bce/bce_jobs` is
  fine for local use. LAN users see section 4b.
- **Templates Dir** — `~/bce/templates` (the installer puts them there).
- **Comfy Root** — path to your ComfyUI install (local/LAN only).
- **Comfy Python** — the Python *executable* inside your Comfy env
  (local/LAN only). **This is the most common setup mistake** — see
  the gotcha below.
- **Cloud API Key** — paste from [platform.comfy.org](https://platform.comfy.org)
  (cloud only).
- **Backend Mode** — `local`, `lan`, or `cloud`.

Click Save.

### The Comfy Python gotcha

`Comfy Python` is the Python **inside the Comfy environment**, not the
Miniconda install folder. It usually looks like:

```
/path/to/miniconda3/envs/comfy/bin/python
```

It is **not** usually:

```
/path/to/miniconda3/python
```

Wrong path → BCE will fail to launch local Comfy with a `FileNotFoundError`.

Test it in a terminal first:

```
/path/to/python /path/to/ComfyUI/main.py --help
```

If that prints Comfy's help, the path is right.

---

## 4. Pick a backend

### 4a. Local

You need ComfyUI installed and working on the same workstation as Flame.

If you don't have ComfyUI yet, see [comfy_install.md](comfy_install.md)
for a Miniconda-based setup that doesn't touch your system Python.

**Mac users:** that guide is Linux-only. For Apple Silicon, this
[community install guide](https://github.com/vincyb/Installing-Comfyui-for-Apple-Mac-Silicon)
is a reasonable starting point — PyTorch and launch flags differ enough
that BCE doesn't ship a Mac guide. See section 4c for the cloud alternative.

Once Comfy runs standalone (browse to `http://127.0.0.1:8188` and load
the default workflow), set BCE Setup:

- Backend Mode → `local`
- Comfy Root → your ComfyUI folder
- Comfy Python → the env Python (see gotcha above)

BCE launches Comfy for you when you render. You do not need to start it
manually.

### 4b. LAN

LAN render uses a shared filesystem so the artist workstation and the
render node see job folders at the same absolute path. Once the mounts
are in place, it behaves the same as local — ComfyUI is a web server
either way.

**On the artist workstation:**

1. Share `~/bce/bce_jobs` over the network (Samba, NFS, whatever your
   shop uses).
2. Bind-mount `~/bce/bce_jobs` to `/mnt/bce_jobs` so the artist machine
   sees its own files at the canonical LAN path. On Linux:
   ```
   sudo mkdir -p /mnt/bce_jobs
   sudo mount --bind ~/bce/bce_jobs /mnt/bce_jobs
   ```
   On Mac, use the equivalent (bindfs, or a symlink as a simpler
   substitute). Make it persistent however your OS handles boot-time
   mounts.
3. In BCE Setup, set Work Root to `/mnt/bce_jobs`.

**On the LAN render node:**

1. Mount the artist's share at `/mnt/bce_jobs`.
2. Install ComfyUI on the render node (see [comfy_install.md](comfy_install.md)).
3. In BCE Setup, set Work Root to `/mnt/bce_jobs`, Backend Mode to
   `lan`, and LAN Host to the render node's hostname or IP.

Both machines now see the same jobs at the same path. Manifest paths
written by the prep machine resolve on the render node.

**Switching between local and LAN:** leave Work Root on the LAN path
permanently. The bind mount means local renders still hit `~/bce/bce_jobs`
physically, so switching modes is just the Backend Mode toggle — no
path juggling. If the render farm is down, switch to cloud as the
fallback.

### 4c. Cloud

The easiest backend to set up — no Comfy install needed.

> [!WARNING]
> **Two sites, no link between them:** [cloud.comfy.org](https://cloud.comfy.org)
> is where you run workflows. Account management and API keys are at
> [platform.comfy.org](https://platform.comfy.org) — and there is no navigation
> between them. Go to platform.comfy.org first.

1. Sign up and get your API key at [platform.comfy.org](https://platform.comfy.org).
2. In BCE Setup:
   - Backend Mode → `cloud`
   - Cloud API Key → paste the key
   - Comfy Root and Comfy Python can stay blank
3. Click Save.

Cloud is also a good fallback when your local GPU is busy or your LAN
render farm is down.

**Mac:** Local Comfy works on Apple Silicon, but if MPS isn't cutting it,
cloud is the way — Comfy Cloud runs on RTX 6000s.

**Linux:** Worth noting - Flame and PyTorch both compete for VRAM. Cloud keeps
your GPU from exploding when you're hitting it hard.

---

## 5. Get the templates running in Comfy first

Before BCE, confirm the workflow dependencies are in place on your
local Comfy.

The shipped load nodes are EXR-based and don't have a file browser —
they're built for BCE, not manual use. For a quick dependency check,
temporarily swap the load node for a standard LoadImage, feed it any
test PNG, and run the workflow. Fix whatever ComfyUI Manager and model
errors throw at you until you get a clean render. Then close without
saving — you're just shaking out missing pieces, not changing the
workflow.

Cloud skips this step entirely.

---

## 6. Load the BCE Matchbox nodes in Flame

After running the installer and BCE Setup, the Matchbox files live at
`~/bce/matchbox/`.

To use one in Batch:

1. Add a Matchbox node to your batch schematic.
2. Right-click → **Change Shader**.
3. Navigate to `~/bce/matchbox/` and load `BCE_Outpaint`,
   `BCE_Inpaint`, or `BCE_SAM`.

How you organize Matchbox nodes long-term — node bins, favorites,
shelves, project templates — is up to you and your studio's
conventions. The files in `~/bce/matchbox/` are the source; copy or
link them wherever suits your workflow.

If something goes wrong, every BCE log line is prefixed `[BCE]`, so you
can filter the Flame app log:

```
grep -F "[BCE]" ~/.flame*/flame*_app.log | tail -50
```

---

## Manual install

If you can't or don't want to run the installer:

**Code (requires sudo):**

```
sudo mkdir -p /opt/Autodesk/shared/python/BCE
sudo cp -r flame_python/* /opt/Autodesk/shared/python/BCE/
```

**User files:**

```
mkdir -p ~/bce/{config,docs,matchbox,templates,bce_jobs}
cp -r docs/*      ~/bce/docs/
cp -r matchbox/*  ~/bce/matchbox/
cp -r templates/* ~/bce/templates/
```

Restart Flame. Continue from section 3.

---

## Troubleshooting

The most common issues:

- **BCE menu doesn't appear in Flame** — check that
  `/opt/Autodesk/shared/python/BCE/` exists and contains `bce_*.py`
  files. Restart Flame.
- **"No BCE config found"** — expected on first run. Go to
  BCE → Setup and Config and fill it in.
- **Local render fails with `FileNotFoundError`** — your Comfy Python
  path is wrong. See the gotcha in section 3.
- **Cloud render fails with `401 Unauthorized`** — API key is missing
  or wrong. Re-paste from [platform.comfy.org](https://platform.comfy.org).

If you hit something not listed here, check the app log (`grep "[BCE]"`
as shown above) and open an issue.
