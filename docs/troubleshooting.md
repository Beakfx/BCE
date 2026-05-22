# Troubleshooting

"I installed BCE and it won't run — why?" Start here.

Most fresh-install failures fall into one of four buckets: install
state, BCE Setup, the backend (local/LAN/cloud), or ComfyUI itself.
This doc covers getting a working install to actually run a job.

For "it ran but the output looks wrong," per-template quirks, and
issues you hit after editing a template, see [workflows.md](workflows.md).
If ComfyUI itself is broken (missing models, custom nodes failing,
Python env issues), see the [ComfyUI side](#comfyui-side) section near
the bottom.

---

## Before debugging BCE: test the workflow in Comfy first

The fastest way to rule out a Comfy dependency problem is to load the
template directly in ComfyUI and run it standalone — before BCE is in
the picture.

BCE ships tested workflows, but custom nodes and models both need to
be in place locally. Temporarily swap the load node for a standard
LoadImage, feed it any test PNG, and run it. Fix whatever Manager and
missing model errors throw at you until you get a clean render, then
close without saving.

If it doesn't run standalone, it won't run through BCE. See
[install.md](install.md) section 5 for the full walkthrough.

---

## Quick checks

Before reading logs, try these:

1. **Restart Flame.** Python hooks load at startup; if you installed
   or updated BCE while Flame was running, restart.
2. **BCE menu visible?** Right-click in Batch — you should see a BCE
   submenu. If not, BCE isn't installed correctly. See
   [BCE menu doesn't appear](#bce-menu-doesnt-appear-in-flame).
3. **Setup run?** Go to BCE → Setup and Config. If the dialog is blank
   on first open, that's expected — fill it in and save.
4. **Backend reachable?** For local, can you load Comfy at
   `http://127.0.0.1:8188` standalone? For cloud, does your API key
   work in a browser test? If not, fix that first.

---

## Reading the BCE log

Every BCE log line is prefixed `[BCE]`, so you can filter Flame's app
log:

**Linux:**
```
grep -F "[BCE]" ~/.flame*/flame*_app.log | tail -50
```

**Mac:**
```
grep -F "[BCE]" ~/Library/Logs/Autodesk/Flame/*/flame*_app.log | tail -50
```

Lines like `[BCE] ERROR: ...` and `[BCE] prepare failed` are usually
where to start. The 20 lines above an error often contain useful
context (what job, what backend, what template).

For backend-side detail (Comfy itself), check the job's runner log:

```
~/bce/bce_jobs/<category>/<job_id>/comfy/runner.log
```

---

## Common BCE errors

### BCE menu doesn't appear in Flame

**Cause:** BCE Python hooks aren't installed or aren't being loaded.

**Fix:**
- Confirm `/opt/Autodesk/shared/python/BCE/` exists and contains files
  starting with `bce_` (e.g. `bce_outpaint.py`).
- If it doesn't, re-run `./install_bce.sh`.
- Restart Flame after install.

---

### "No BCE config found"

**Cause:** First-run state. BCE config is created by the user, not the
installer.

**Fix:** Go to BCE → Setup and Config, fill in the fields, click Save.
See [install.md](install.md) section 3.

---

### "Selected API template is missing required BCE tag(s)"

**Cause:** You picked a Comfy *GUI* template, not an *API* template.
The two formats look similar but aren't interchangeable: a **GUI
template** is the node graph you open and edit in Comfy's web UI; an
**API template** is the flattened version BCE patches and submits at
render time. BCE can only drive API templates.

**Fix:** In the BCE node's Matchbox UI, set the workflow to one of the
`*_API.json` files in `~/bce/templates/`. The `gui_versions/` subfolder
holds the same workflows in GUI format — those are well laid out for
opening and experimenting in Comfy directly, but BCE won't load them.

---

### Local render fails with `FileNotFoundError`

**Symptom:** Log shows:
```
FileNotFoundError: [Errno 2] No such file or directory: '...miniconda3/python'
```

**Cause:** Wrong Comfy Python path. You pointed at Miniconda root, not
the env Python.

**Fix:** In BCE Setup, set Comfy Python to:
```
/path/to/miniconda3/envs/<your-env>/bin/python
```
Test it in a terminal: `/path/to/python --version` should print
Python 3.x without error.

---

### Launch fails: "Local ComfyUI is already using port 8188"

**Cause:** Local mode launches its own ComfyUI on port 8188, but
something is already listening there — usually a Comfy instance you
started by hand, or a previous one that didn't shut down cleanly.

**Fix:** Kill whatever's holding the port, then run BCE again:
```
kill $(lsof -ti :8188)
```

---

### Launch fails: "LAN ComfyUI is not reachable at HOST:PORT"

**Cause:** LAN mode can't open a TCP connection to the LAN ComfyUI
server at the configured host/port (server down, wrong host/port, or
firewall).

**Fix:**
- Confirm the LAN Comfy server is actually running and serving on that
  host and port.
- In BCE Setup, check **LAN Host** and **LAN Port** match the server.
- From the Flame box, test reachability: `curl http://HOST:PORT/`
  should respond.

---

### Launch fails: "Cloud backend is not ready"

**Cause:** Cloud mode needs both a Cloud URL and a Cloud API Key, and
one of them is blank.

**Fix:** In BCE Setup, confirm **Cloud API Key** is filled in. The
**Cloud URL** defaults to `https://cloud.comfy.org`; if you cleared it,
restore it. Save, then try again. (If the key is set but the render
still fails with `401`, see the next entry.)

---

### Cloud render fails with `401 Unauthorized`

**Cause:** API key missing, wrong, or expired.

**Fix:** Go to [platform.comfy.org](https://platform.comfy.org) → account
settings → generate a new API key. Paste it into BCE Setup → Cloud API
Key. Save.

---

## Job folder things

### Job folder is huge / disk filling up

**Cause:** Normal. Each job keeps its source media, intermediate
files, and outputs.

**Fix:** Delete old job folders from `~/bce/bce_jobs/`. Imported
clips are fully cached in Flame; deleting the job folder won't lose
your timeline media. See README → "Imports stay."

---

### Want to re-run a finished job

For SAM specifically, the transport movie is kept after prep — you
can re-run Render Mattes with different Mask_N toggles without
re-prepping. Set the new toggles in the Matchbox UI and right-click
→ Render Mattes again.

For Outpaint and Inpaint, re-prep is required if Matchbox values
change.

---

### Local render produces black output or crashes mid-job

**Cause:** VRAM exhausted. Large renders — 4K Inpaint especially —
can exceed what's available locally.

**Fix:** Reduce resolution, or switch to cloud for heavy jobs.

---

## ComfyUI side

If BCE prep succeeded but Comfy is failing (missing models, custom
node errors), that's a Comfy issue, not BCE. Check `runner.log` for
the error and consult ComfyUI's docs.

---

## Escalating

If none of the above apply, post in [Logik](https://forum.logik.tv) or
open a repo issue. Include:

- Flame version and OS
- BCE backend mode (local / LAN / cloud)
- The last 50 `[BCE]`-filtered log lines
- The relevant runner.log if the failure was backend-side
- A description of what you were trying to do
