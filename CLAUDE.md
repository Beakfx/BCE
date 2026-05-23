# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

# CLAUDE.md — Batch Comfy Extensions (BCE)

Context for AI assistants working in this repo. Read top to bottom before
editing code.

A companion file, `GLOSSARY.md`, defines terms, the job folder layout,
naming conventions, and the per-category `[BCE:*]` tag details. This file
is rules and rationale; the glossary is reference.

---

## What this is

Batch Comfy Extensions (BCE) is a Flame python hook system. A BCE node in
Flame Batch reads values from a Matchbox UI, patches a ComfyUI workflow
template against those values, and renders through one of three backends:
local Comfy, LAN Comfy, or Comfy Cloud. The result is imported back into
Flame.

Author: Beak. Throughout this repo, the author is referred to as Beak, not Pete.

Current categories: Outpaint, Inpaint, SAM.

The project started as a single Outpaint node, then grew into a system.
The "BCE" acronym reads as Batch Comfy Extensions in public; Flame artists
who know the author (Beak) will also read it as Beak's Comfy Extension.
Both are fine.

**Audience for the code:** Flame artists who can read Python. Not Python
engineers who happen to use Flame.


---

## Quality bar

v1 quality bar: a Flame TD opens `bce_outpaint.py` on a Sunday and follows
it end to end without Python expertise.

This outranks elegance, DRY, and abstraction. Flame is one controlled
platform. Do not write code as if it has to run on forty.

---

## Coding style

- Minimal.
- Linear top-to-bottom where possible.
- Clear over clever.
- Not overly defensive. Don't wrap everything in try/except; let real
  errors surface.
- No LLM-style abstraction sprawl. No three-line helpers that exist only
  to name one expression.
- No helper-function confetti. A helper has to genuinely improve
  readability or be reused at least twice.
- Comments explain *why*. Code says *what*.
- Prefer flat data (dicts, manifest JSON) over classes.

Reference style: the python hooks on the Logik Portal (e.g. Michael V's
`import_write_node.py`, also present in this repo). When in doubt, match
their shape.

---

## What you may edit

| File type                              | Rule                                                       |
|----------------------------------------|------------------------------------------------------------|
| `bce_*.py`                             | Edit freely within the style rules.                        |
| `pyflame_lib_bce.py`                   | **Do not edit.** Vendored PyFlame UI library (Michael Vaglienty). Treat like a dependency. |
| Matchbox files (`.xml`, `.glsl`)       | **Do not edit without asking.** Authored by the dev. `.mx` is a compiled/closed-source matchbox shader — not used or wanted here; BCE uses plain `.xml` menus and pass-through `.glsl` shaders only. |
| ComfyUI templates (`*_API.json`, GUI versions) | **Do not edit without asking.** Workflow-author territory. |
| `.clip` / OpenClip files               | **Do not edit.** Flame-generated.                          |

If a Python change appears to require an edit to one of the protected
file types, stop and surface it. Explain the why, name the file, propose
the change, and wait for confirmation.

---

## How verification works

Flame python only runs inside Flame. There is no headless test harness
and none is planned for v1.

What the agent can do:

- Syntax-check / compile-check Python:
  ```
  for f in flame_python/bce_*.py; do python3 -c "import ast; ast.parse(open('$f').read())" && echo "OK: $f"; done
  ```
- Logic-review code paths.
- Dry-run API JSON patching against a captured manifest if one is provided.
- Read logs and `tree` output when the dev attaches them.

What the agent cannot do:

- Render, prep, launch, or import. Those all require the dev clicking
  through Flame.

When the dev is debugging, expect to receive:

- `tree <job_id>/` output of a real job folder.
- `grep -F "[BCE]" flame.app.log` (Flame's app log, filtered).
- `runner.log` from the job's `comfy/` directory.
- Comfy Cloud history / asset / error responses when the snag is on cloud.

Do **not** claim a change is "tested." Say "compile-checks clean, logic
looks right, ready for a prep/launch when you can run it."

---

## Logging

Every log line from BCE Python uses the `[BCE]` prefix. That makes the
filtered grep above work. Keep new log statements consistent with this.

Flame provides two channels and BCE uses both deliberately:

- `flame.messages.show_in_console(...)` — appears in the artist's
  message console *and* lands in the app log. Use for things the
  artist must see (job prepared, render failed, missing config).
- `print(...)` — app log only (Flame captures stdout into
  `flame*_app.log`). Use for diagnostic detail that would just be
  noise in the artist's UI.

`bce_lib` provides `msg()` for artist-facing output. A `log()`
helper (print-only, no console) may be added to bce_lib during the
cleanup pass to give callers a way to write diagnostic detail without
cluttering the artist's message console.

The codebase is currently in a *dev storm* — log volume is high and
noisy, and many existing calls are `msg()` when they should probably
be `log()`. A cleanup pass is pending before publish. **Do not
refactor existing calls unprompted.** The dev will lead that triage.
When adding new log lines, match the volume of surrounding code — do
not "tidy" while you're nearby.

---

## Search order for Flame / Matchbox / Batch / PyNode / socket / Mux questions

When you need to verify Flame-side behavior, search in this order. Stop
as soon as you have a real executable example.

1. `logik-portal/python` GitHub repo (community scripts — *executable
   examples*).
2. `forum.logik.tv` (Flame community Q&A).
3. Autodesk Flame forum.
4. Official Autodesk Flame docs.

Prioritize community scripts over docs/speculation. If you can't find an
example, say so rather than guessing at an API.

For ComfyUI questions, vanilla Comfy docs are fine. For anything Comfy
Cloud-specific (asset upload, history_v2 download, available custom nodes,
output `type=temp` vs `type=output`), the `cloud.comfy.org` docs are also
a primary source — cloud behavior differs from local.

---

## Repo / install layout

In this repo all Python lives under `flame_python/`. The installer copies
those files to `/opt/Autodesk/shared/python/BCE/`. User assets live under
`~/bce`. Code and user data are deliberately separate.

```
flame_python/                           # dev source tree (edit here)
    bce_lib.py
    bce_launch.py
    bce_runner.py
    bce_outpaint.py
    bce_inpaint.py
    bce_SAM.py
    pyflame_lib_bce.py                  # vendored — do not edit
```

Install destinations:

```
/opt/Autodesk/shared/python/BCE/        # code (the hook)
    bce_lib.py
    bce_launch.py
    bce_runner.py
    bce_outpaint.py
    bce_inpaint.py
    bce_SAM.py
    ...

~/bce/                                  # user space, created by installer
    config/         config.json (user-created via Flame Setup UI)
    templates/      ComfyUI API + GUI JSON templates
    matchbox/       Matchbox node files (.xml, .glsl)
    docs/
    bce_jobs/<category>/<job_id>/      job working dirs (safe to delete; see Caching)
```

Installer copies code to `/opt/...` and assets to `~/bce`. It does **not**
create `config.json` — the user creates that through Flame's `BCE > Setup
and Config` UI. Missing config is a warning, not a fatal error.

---

## File responsibilities

Four-file pattern, repeated per node category:

| File                  | Owns                                                                 |
|-----------------------|----------------------------------------------------------------------|
| `bce_<node>.py`       | Node category definition. Prep, manifest fields, API JSON patching, cloud flags. **This is the editable file for new node types.** |
| `bce_launch.py`       | Runtime orchestration. Render source, build manifest, create result OpenClip, spawn runner, drive Flame-side menu visibility. |
| `bce_lib.py`          | Shared Flame-side helpers — config, OpenClip/import, write-template selection, Matchbox snapshot read, result-size math. |
| `bce_runner.py`       | Backend execution. Detached process. Launches local Comfy, talks to LAN Comfy or Comfy Cloud, downloads results. Stdlib only. |

`bce_runner.py` runs as a detached child process so Flame is not blocked.
Treat it as a separate program — it has its own logging and minimal imports.

### MES (Minimum Editable Stuff)

`bce_<node>.py` is the *one file an artist edits to make a new node
category*. It should contain only what is genuinely category-specific.
Everything else goes in `bce_lib.py`. When `bce_inpaint.py` or
`bce_outpaint.py` drifts above ~500 lines, something belongs in lib.

---

## Adding a new node category

This is the canonical workflow. Don't invent a new shape.

1. Pick the ComfyUI workflow. Test it standalone in Comfy first — and on
   Comfy Cloud, per the cloud constraint below.
2. Tag the Comfy nodes with `[BCE:*]` markers in their titles (see
   glossary for the full tag list).
3. Save two templates under `~/bce/templates/`: `<name>_API.json` for
   runtime, plus a GUI version under `templates/gui_versions/` for
   artists to inspect/copy.
4. Build the Matchbox UI (`.xml` + `.glsl`). Use `BCE_Outpaint.xml`
   or `BCE_Inpaint.xml` as the style reference — match indentation, line
   width, parameter ordering. Set the workflow display title in the XML to
   include the model, step count, and any notable characteristics — e.g.
   "Flux.1 - 12 steps no guide". The steps slider default is fixed in the
   XML and doesn't change when the artist switches templates; the title is
   their only in-UI hint about what the template expects.
5. Copy `bce_outpaint.py` to `bce_<newname>.py` and edit. The constants
   block at the top (`SHADER_NAME`, `WORK_SUBDIR`, `ARTIFACT_PREFIX`,
   etc.) is the first thing to change.
6. Patch the API JSON in the category file's prep function — read values
   from the Matchbox setup snapshot, substitute into tagged nodes.

If the new workflow looks like an existing category, copy that category.
If it's a new shape (video, multi-output), expect to extend `bce_lib.py`
and `bce_runner.py` as well.

---

## The `[BCE:*]` tag contract

BCE finds and patches Comfy nodes by reading tags embedded in node
titles. Tags split into two groups:

- **Common tags** appear (or potentially appear) across categories:
  `LOAD`, `SAVE`, `PROMPT`, `SEED`, `STEPS`, `SAMPLER` / `KSAMPLER`.
- **Category-specific tags** exist in one category only — e.g. `PAD`
  and `GUIDE` are Outpaint; `VIDTRACK`, `PREVIEW`, `INDEX` are SAM.

Full tag-by-tag detail (what each patches, which node type, which
inputs) lives in `GLOSSARY.md`. The actual `bce_<category>.py` is the
source of truth — verify against it.

### Radiance Read / Write conventions

```
[BCE:LOAD]  RadianceDigitalCinemaRead
            inputs["source_path"] = source path
            (SAM uses [BCE:LOAD] differently — patches a video field.
             See glossary.)

[BCE:SAVE]  RadianceDigitalCinemaWrite
            inputs["filename_prefix"] = <comfy_out>/<result_name_base>  (no trailing dot)
            inputs["output_path"]     = ""
            inputs["write_mode"]      = "Sequence"
            inputs["start_frame"]     = <patched per iteration>
            inputs["bit_depth"]       = "16-bit Half Float"
            inputs["compression"]     = "ZIP"
```

`Sequence` mode produces `<base>.0001.exr`. `Single Image` mode produces
`<base>..exr` — wrong.

### Cloud-only mutations

The cloud runner does two graph surgeries, both scoped to the tagged
`[BCE:LOAD]` node only — never to every LoadImage in the graph (Qwen,
SAM, and future workflows have multiple loaders):

1. `[BCE:LOAD]` is mutated to LoadImage, pointing at the uploaded TIFF.
2. An `InvertMask` is spliced between the LoadImage MASK output and
   downstream mask consumers.

`[BCE:SAVE]` stays as RadianceDigitalCinemaWrite on cloud. The old
`RadianceSaveEXR` cloud mutation is obsolete — do not reintroduce it.

---

## Backends

| Backend | Source transport        | Result transport             | Notes                          |
|---------|-------------------------|------------------------------|--------------------------------|
| local   | EXR via Radiance Read   | EXR via Radiance Write       | Direct disk.                   |
| LAN     | EXR via Radiance Read   | EXR via Radiance Write       | Shared filesystem. CPU-bound in practice; SAM deferred. |
| cloud   | 16-bit RGBA TIFF upload | EXR download via `/api/view` | LoadImage substitution + mask invert; output filename from `history_v2`. |

### The cloud constraint (read this before designing a new template)

**A single Comfy workflow template must run on local, LAN, and cloud.**

Comfy Cloud runs a fixed set of custom nodes — usually not the
interesting/useful ones. If a custom node appears in a BCE-shipped
template, it has been verified working on cloud. When designing a new
workflow:

- Prefer nodes that exist on Comfy Cloud.
- If a node is local-only, the whole template is local-only — label it
  that way and don't try to make it cloud-portable with runtime patching.
- The cloud-side mutations BCE *will* do are already listed above
  (LoadImage substitution, InvertMask splice). Do not add more.

### Cloud asset filenames

Comfy Cloud writes output assets with hashed (asset hash / blob) names,
not the friendly display name. Do **not** assume the blob filename
equals `<result_name_base>.0001.exr`. The cloud runner must:

```
submit prompt
wait for status success
fetch history_v2
recursively find the actual output filename/type/subfolder
download via /api/view
save locally as canonical:
    comfy_out/<result_name_base>.<iter:04d>.exr
```

### Local completion

Radiance Write may not surface normal save-node image metadata in local
`/history`. Poll `/history` only until `prompt_id` appears, then check
the expected output path once. Do not scan directories — Flame may be
playing back a heavy timeline while this runs.

---

## Footguns — do not do these

Every one of these has been paid for in commits. Don't repay them.

- **Do not** rewire every LoadImage on cloud. Only the `[BCE:LOAD]`-
  tagged node. Multi-loader workflows (Qwen, SAM) break if you scan
  globally.
- **Do not** put Radiance Write in `Single Image` mode. Use `Sequence`.
  `filename_prefix` must have no trailing dot.
- **Do not** add `--force-fp16` to the local Comfy launch. It makes
  Flux.2 and Qwen render black.
- **Do not** patch `SamplerCustomAdvanced.seed`. On modern split graphs
  the real noise source is `RandomNoise.noise_seed` — tag and patch that
  (`[BCE:SEED]`).
- **Do not** assume cloud output blob filename matches `<base>.0001.exr`.
  Get it from `history_v2`.
- **Do not** apply runner-side mask inversion on local/LAN. That fix is
  cloud-only.
- **Do not** require LanPaint UI values. LanPaint nodes are not
  available on Comfy Cloud; treat `LanPaint_NumSteps` as optional
  legacy.
- **Do not** auto-create `config.json` at install time. Missing config
  is a warning that routes the user to `BCE > Setup and Config`.
- **Do not** validate `comfy_root` / `comfy_py` strictly at save time —
  cloud-only users legitimately have neither.
- **Comfy Python gotcha:** users (and the dev) will set `comfy_py` to
  the miniconda root. It must be the env Python:
  `.../miniconda3/envs/<env>/bin/python`. Docs and tooltip must say so.
- **Do not** propose new features for v1. Cleanup and ship is the entire
  v1 mandate. Feature ideas go in the dev's notes, not the code.

---

## Caching

`~/bce/bce_jobs/<category>/<job_id>/` is safe to delete between jobs —
Flame imports are fully cached because BCE forces MediaHub `cache_mode`
on during import and restores it after. This fixed the long-standing
"missing media after purge" issue. **Do not change the cache-mode
handling without understanding that history.**

The SAM transport movie under `<job>/source_video/` is kept after prep
on purpose, so re-renders against the same source clip don't re-export
the JPEG stream. The JPEG sequence itself is disposable after the
transport movie is built.

---

## Current state (v1 RC)

Working: Outpaint, Inpaint, and SAM categories render local and cloud.
Radiance Read/Write refactor complete across templates. Cloud transport
(TIFF source, EXR or MP4 result via history_v2) working. SAM transport
movie + Render Preview / Render Mattes flow working. Match the Batch
FPS via `.clip` editRate. Installer and user-created config flow in
place.

Mandate from here to publish: **cleanup and ship.** No new features.

Known debt (post-v1, not for this pass unless explicitly asked):


- Inpaint+SAM work. Trim toward MES is in scope for cleanup.
- Logging volume (dev storm) — dev-led cleanup pending.
- SAM `preview_mode` bool is positional/fragile in the Matchbox channel
  list.
- `max_objects` can exceed the six exposed `Mask_N` toggles. Acceptable
  for v1.
- Import/result handling for video should eventually become shared with
  still-image import.
- LAN backend not smoke-tested since Radiance refactor.
- Flux.2 Outpaint: green frame vs black frame, prompt sensitivity, color
  shift — needs another pass.

- `probe` is still the internal dict name for the Matchbox setup
  snapshot. Rename candidate: `mbox_values`. Not urgent.

---

## References

- `GLOSSARY.md` (this repo) — terms, naming, job folder layout, full
  `[BCE:*]` tag detail.
- Logik Portal Python script library — reference for Flame python style
  and APIs. Michael V's `import_write_node.py` is a representative
  example and is also vendored in this repo.
- `forum.logik.tv` — Flame community Q&A.
- `cloud.comfy.org` docs — Comfy Cloud-specific reference.
