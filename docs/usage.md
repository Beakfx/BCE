# Using BCE

This doc covers the universal "how to use BCE" stuff that applies
across all node categories — the prep/render/import lifecycle, where
parameters live, how seeds work, what to expect when switching
backends, and how to recover a render from an archived Batch setup.

For per-template guidance — which prompt syntax Flux 2 prefers, how
many steps the 4-step LoRA wants, what the SAM preview-then-mattes
flow does — see [workflows.md](workflows.md).

---

## The lifecycle

Every BCE render goes through three steps. Each is a right-click
action on the BCE node:

1. **Prepare Job.** Reads the Matchbox UI, snapshots the setup,
   creates a job folder under `~/bce/bce_jobs/<category>/<job_id>/`,
   creates a Write File branch in Batch to render source media, and
   patches the Comfy API JSON with your parameters. Nothing runs yet.
2. **Launch.** Starts the backend. For local, this spawns Comfy if it
   isn't already running. For LAN, it submits to your render node.
   For cloud, it uploads the source and submits to Comfy Cloud.
3. **Import Result.** Imports the finished render back into Flame as
   a cached clip.

> **Changed a parameter? Re-prep.** Prepare Job snapshots the Matchbox
> UI at the moment it runs. Adjusting a value after prep has no effect
> at Launch — re-prep to pick up the change. (The intent is that prep
> will eventually fold into launch and this step disappears.)

For SAM specifically, the menu shows **Render Preview** and **Render
Mattes** instead of a single Launch — see [workflows.md](workflows.md).

### Compass colors

BCE wraps each prepared job in a Compass node in your Batch tree.
The color tells you where the job stands at a glance:

| Color | State |
|-------|-------|
| Blue | Prepared — job folder and patched workflow ready, nothing sent yet. |
| Yellow | Launched — job has been sent to Comfy, result not yet imported. |
| Grey | Done — result imported into Flame. |

If you open a Batch setup and see yellow Compass nodes, there are
results waiting to import.

---

## Monitoring a running render

BCE can't update Flame while Comfy is running — Comfy has to run as
a separate process or it locks (and crashes) Flame while waiting for
a result. There's no progress bar in the UI.

**Best option: leave a browser tab open.**

- **Local:** open Comfy's web UI before or after Launch. If Comfy
  isn't running yet, the tab will show "error reconnecting" or
  similar. When BCE launches Comfy, the tab connects automatically
  and shows the queue and per-node progress for the active job.
- **Cloud:** leave a tab open at `platform.comfy.org`. When BCE
  submits a job, the queue manager shows "1 active" and a per-frame
  percentage as it runs.

**Fallback: `runner.log`.** Every job folder has a log at
`~/bce/bce_jobs/<category>/<job_id>/comfy/runner.log`. If a render
silently fails, this is the first place to look.

### Killing a stuck render

If it's clearly going to take forever (RAW 4K through a slow workflow,
wrong resolution, wrong backend) — cancel it in the ComfyUI browser
tab. There's an **X** button next to the active job readout beside the
Run button. This works for both local and cloud.

For local, if the tab isn't reachable, you can also kill the process:
```
kill $(lsof -ti :8188)
```

Re-prep with different settings, maybe try a different rez, or do a crop. Maybe switch render modes, local can get testy while fighting Flame's VRAM usage. Consider lan or cloud for huge jobs.

---

## Where parameters live

Three places. The node UI controls are patched directly into the
ComfyUI workflow at prep time — what you see is what gets sent.

**The node UI.** Sliders, toggles, dropdowns, thresholds — everything
visible on the BCE node. Read at Prepare Job. Changes after prep are
ignored until you re-prep.

**The Prompt goes in the Note!** Double-click the BCE note to see the default as loaded. In some cases (like outpaint) the default prompt works. Others must be changed. Shooting a SAM job with "mask prompt here" can go wrong quickly :) Paste your prompt there. This is a standard Note widget that is part of Flame/Matchbox — BCE uses it because it's the only place that holds arbitrary text, survives copy/paste and node cloning, and saves with the Batch setup.
Long prompts are fine; there's no length limit, beyond what Comfy might not like. The prompt is sent verbatim into whatever Comfy node is expecting it, the one labeled [BCE:PROMPT] in the Comfy workflow.

**The seed.** A numeric field in the UI. See
[Seeds and iterations](#seeds-and-iterations) below.

---

## Seeds and iterations

**Seed = 0:** BCE generates a random seed (1–9,999,999) at prep time
and writes it back into the node UI. You'll see it update after
Prepare Job.

**Non-zero seed:** BCE uses it as-is. The value in the field is the value
sent to Comfy.

When you render multiple iterations, each frame gets an incremented
seed:

- Iteration 1 → base seed
- Iteration 2 → base seed + 1
- Iteration 3 → base seed + 2
- ...

### Determinism

Comfy and PyTorch are deterministic. Same workflow, same seed, same
prompt, same parameters → pixel-for-pixel identical result, every
time. This is what makes iteration recovery possible.

**Important:** the seed alone isn't enough. If anything else changed
— prompt, model, resolution, node UI values — the result will differ.
Determinism requires the full matching setup.

### Re-running a specific iteration

Say you rendered 10 iterations, imported iteration 6, and deleted the
job folder. Client comes back needing to re-render it:

1. Load the archived Batch setup (seed is still there).
2. In the node UI, increment the Seed field 5 times
   (iteration 6 = base + 5). Flame's arrow-key does this cleanly.
3. Re-prep and launch.

Same result as the original.

### Cloning or reusing a node

If you copy a BCE node or load an old Batch setup for a new render,
**set the seed back to 0** before prepping. Otherwise you'll get the
same result as the original render. Zero = fresh seed on next prep.

---

## Switching backends

Backend Mode is a toggle in BCE Setup. Switching it changes where the
render runs, but nothing else about the BCE node or its parameters.

- **Local → Cloud:** the same prep produces the same render, with
  source media transported as TIFF instead of EXR.
  Results come back as EXR either way.
- **Local → LAN:** identical behavior if Work Root is set to a path
  both machines see (see [install.md](install.md) section 4b).
- **Cloud → Local:** works, with one caveat — workflows authored
  around custom nodes available only on cloud (or only locally) may
  fail. See [workflows.md](workflows.md) for which templates run
  where.

You don't need to re-prep when switching backends. An already-prepped
job will run on whichever backend is active at Launch time.

---

## Job folders

Every prepared job lives at:

```
~/bce/bce_jobs/<category>/<job_id>/
```

Inside, you'll find:

- `manifest.json` — the contract for this job (paths, parameters,
  state)
- `comfy/` — the patched API JSON and runner log
- `source_frame/` or `source_video/` — the media rendered out of
  Flame as Comfy's input
- `comfy_out/` — the finished render (EXR sequence or MP4)
- `mbox/` — the Matchbox setup snapshot and Write File template

### Safe to delete

Once you've imported a result, the job folder is **safe to delete**.
BCE forces MediaHub cache mode during import, so the imported clip
is fully cached in Flame and doesn't need the source media on disk.

Bulk cleanup of old jobs is fine:

```
rm -rf ~/bce/bce_jobs/inpaint/2025*
```

You won't lose any Flame timeline media. Re-running the job would
require re-prep, but the cached clip stays.

---

## AI pixels — always comp your plate

Every AI model in BCE will alter your source pixels to some degree. Colors shift, edges soften or sharpen, fine grain disappears. This is not a bug — it's how diffusion works. The result is a *fill*, not a faithful extension of your plate.

**Always comp your original back over the result.** Inpaint, Outpaint, all of it. Use the result for what it's good at — filling the gap — and let your original carry anything it already covered.

---

## Archive recovery

Because every BCE parameter lives in the Flame Batch setup — Matchbox
values, the seed, and the prompt in the Note — you can archive a
project, restore it months later, and re-render the same result.

What you need on restore:

1. The Batch setup (in the archive).
2. The same BCE template available at `~/bce/templates/` on the
   restoring machine. *If you've updated BCE since the render, the
   template may have changed — keep a copy of the exact template if
   long-term reproducibility matters.*
3. The same model (if local/LAN) or working API key (if cloud).
4. A working BCE install with the right backend configured.
5. The source media.

What you do **not** need:

- The original job folder (BCE recreates it on Prepare Job).
- Anything from the old prep/launch cycle.

### The "long-term reproducibility" caveat

Comfy itself, custom nodes, and model weights are not frozen by BCE.
A model update, custom-node update, or template change could produce
a different result. If a project needs to render exactly as it did
on a specific date, archive the BCE template alongside the Batch
setup, and ideally pin the Comfy environment.

For most production work, "same prompt, same seed, same parameters →
same result" is true and reliable. The caveats above only matter when
you need bit-exact reproducibility across years.
