## BCE Glossary of Terms

### BCE

**BCE**
The overall Flame-to-Comfy bridge project. BCE nodes live in Flame Batch, prepare source media, run Comfy workflows locally/LAN/cloud, and import the result back into Flame.

**BCE Node**
A Matchbox-based UI node in Flame Batch, such as `BCE Outpaint`, `BCE Inpaint`, or `BCE SAM`. The Matchbox node is the artist-facing control panel.

**BCE Category**
A family of BCE behavior, usually mapped to one Python prep hook and one Matchbox UI. Current examples:

```
Outpaint
Inpaint
SAM
```

---

## Flame / Batch Terms

**Matchbox Node**
The Flame Batch node that provides the BCE UI. It usually does little or no image processing. It acts as a parameter carrier.

**Matchbox Setup Snapshot**
The saved `.matchbox_node` file captured during **Prepare Job**. BCE reads this file to extract prompt, sliders, toggles, thresholds, mask selections, etc.

**Write File Node / Write Node**
The Flame node BCE creates during preparation to render source media into the job folder. BCE uses its generated name to classify job type:

```
op_<short>_src   = Outpaint
ip_<short>_src   = Inpaint
sam_<short>_src  = SAM
```

**Mux Node**
The node BCE inserts between the source and the Write File node. For Outpaint/Inpaint it may freeze one frame. For SAM it renders the full sequence.

**Compass Node**
The Flame Batch visual grouping BCE creates around the Write File node. It marks the prepared job and changes color as the job state changes.

**Frame Code Mode / FCM**
Flame/OpenClip frame-rate mode. For BCE SAM, the JPEG Write File template should use:

```
<FCM>-3</FCM>
```

Meaning: conform/match the Batch frame rate.

---

## Job Terms

**Job**
One prepared BCE render package on disk.

Example:

```
~/bce/bce_jobs/sam/20260516_133719/
```

**Job ID**
The timestamp folder name for a job.

```
20260516_133719
```

**Job Short ID**
Shorter ID used in filenames.

```
1337_0516
```

**Job Folder**
The root directory for one prepared BCE job. Contains `manifest.json`, source media, Comfy API JSON, output media, and setup snapshots.

**Prepared Job**
A job after **Prepare Job** has run successfully. It has a manifest, patched API JSON, Matchbox setup snapshot, and Write File branch.

**Manifest**
`manifest.json`. The job contract. It records paths, filenames, user settings, workflow choice, SAM state, output state, and import targets.

**API JSON**
The ComfyUI API-format workflow JSON patched by BCE. This is what the runner submits to Comfy.

**Template**
A reusable Comfy API JSON or Flame Write File setup used as a starting point. BCE patches templates per job.

---

## Job Folder Layout

**`mbox/`**
Stores the saved Matchbox setup and patched Write File setup.

```
mbox_setup.matchbox_node
mbox_setup.xml
mbox_setup.1.glsl
write_patched.export_node
```

**`comfy/`**
Stores the patched Comfy API JSON and runner status files.

```
sam_<short>_API.json
runner.log
done.flag
```

**`source_frame/`**
Source frames rendered by Flame. For SAM, this is a temporary JPEG sequence plus the source `.clip`.

```
sam_<short>_src.0001.jpg
sam_<short>_src.0002.jpg
sam_<short>_src.clip
```

For SAM, JPEGs may be deleted after the transport movie is built. The `.clip` should remain.

**`source_video/`**
Stores the SAM transport movie.

```
sam_<short>_transport.mp4
```

**`comfy_out/`**
Stores final or preview results from Comfy.

```
sam_<short>_preview.mp4
sam_<short>_matte.mp4
```

---

## Media Terms

**Source Frame / Source Plate**
The image or sequence exported from Flame for Comfy to process.

**Transport Movie**
The temporary MP4 created from the SAM JPEG sequence and sent to Comfy.

Important: this is **not** a Flame proxy, proxy render, or deliverable.

```
source JPEG sequence -> transport movie -> Comfy
```

**Preview Movie**
A one-frame SAM preview MP4 showing colored overlay/object IDs.

```
sam_<short>_preview.mp4
```

**Matte Movie**
The final SAM mask/matte MP4 output.

```
sam_<short>_matte.mp4
```

**Result Movie**
Generic term for whatever SAM most recently produced: preview or matte.

**Last Result Movie**
Manifest field pointing to the movie BCE should import.

```
"last_result_movie": "/path/to/sam_<short>_preview.mp4"
```

---

## SAM Terms

**BCE SAM**
The BCE category for SAM video segmentation / tracking workflows.

**SAM3**
The current SAM implementation being used. BCE naming stays general enough to allow SAM2/SAM4/RMBG/etc. later.

**Render Preview**
The SAM menu action that runs a one-frame ID preview. It patches the video load to process only one frame.

**Render Mattes**
The SAM menu action that renders the selected SAM mask IDs over the full clip.

**Preview Mode**
A Matchbox bool/toggle that makes the first SAM run produce a preview before full matte rendering.

**`next_action`**
SAM manifest state that controls which SAM menu action appears next.

```
"next_action": "preview"
```

or:

```
"next_action": "render"
```

**Object ID / Mask ID**
The numeric ID assigned by SAM to a detected/tracked object in the preview overlay.

**Mask Toggles**
The Matchbox controls `Mask_0` through `Mask_5`. They build the `object_indices` string sent to `SAM3_TrackToMask`.

```
Mask_1 = 1
```

becomes:

```
"object_indices": "1"
```

**Max Objects**
The maximum number of objects SAM is allowed to detect/track. This can be higher than the number of exposed Mask toggles.

**Threshold**
Detection threshold for SAM. Higher is stricter; lower is more permissive.

**`object_indices`**
The Comfy SAM input string listing which IDs to extract.

```
"0,3,5"
```

Blank means all available tracked objects.

---

## Comfy / Runner Terms

**Runner**
`bce_runner.py`. The detached process that submits the patched API JSON to Comfy, waits for completion, downloads/copies results, updates manifest, and writes `done.flag`.

**Backend**
Where Comfy runs.

```
local
lan
cloud
```

**Local Backend**
Comfy runs on the same workstation. BCE starts Comfy and points it at the job folders.

**LAN Backend**
Comfy runs on another machine using the shared BCE job folder. Deferred for SAM until the shared mount is updated.

**Cloud Backend**
Comfy runs on Comfy Cloud ([cloud.comfy.org](https://cloud.comfy.org)). BCE uploads source media as an asset and downloads the result via `/api/view`. Account management and API keys are at [platform.comfy.org](https://platform.comfy.org) — separate site, no direct link.

**Asset Hash / Blob Name**
Cloud’s storage filename, usually a hash-like name ending in `.mp4`. This is what the API needs, not the friendly display name.

**Display Name**
Cloud/UI-friendly name shown to humans. Do not rely on this for API download.

**Temp Output**
Cloud/Comfy output type used by SAM preview. Usually downloaded with:

```
type=temp
```

**Output Output**
Cloud/Comfy output type used by final saved results. Usually downloaded with:

```
type=output
```

**`done.flag`**
Small file written when the runner completes successfully. Import checks for it.

---

## Workflow Terms

**Prepare Job**
Reads the BCE Matchbox node, snapshots the setup, creates the job folder, creates the Write File branch, and patches the Comfy API JSON.

**Launch / Render**
Starts the backend process. For SAM, this builds/reuses the transport movie and runs preview or matte rendering.

**Import Result**
Imports the most recent completed result back into Flame.

**Match the Batch**
BCE SAM’s frame-rate rule: derive timing from Flame’s rendered `.clip`, preserving rational rates like:

```
24000/1001
```

for ffmpeg transport creation and Comfy video settings.

---

## BCE Tags in API JSON

**`[BCE:LOAD]`**
The Comfy node BCE patches with the source input.

For SAM:

```
"video": "<uploaded-or-local-transport.mp4>"
```

**`[BCE:PROMPT]`**
The prompt text node.

**`[BCE:VIDTRACK]`**
SAM3 video tracking node. BCE patches threshold and max objects.

**`[BCE:PREVIEW]`**
SAM3 preview node. Produces the colored object-ID preview movie.

**`[BCE:INDEX]`**
SAM3 Track-to-Mask node. BCE patches `object_indices`.

**`[BCE:SAVE]`**
Final save/output node. For SAM, this is usually VHS Video Combine.

---

## Naming Conventions

**Outpaint prefix**

```
op_
```

**Inpaint prefix**

```
ip_
```

**SAM prefix**

```
sam_
```

**Source Write node**

```
sam_<short>_src
```

**Transport movie**

```
sam_<short>_transport.mp4
```

**Preview result**

```
sam_<short>_preview.mp4
```

**Matte result**

```
sam_<short>_matte.mp4
```

---

## Current Known Debt

**Runner size**
`bce_runner.py` is getting too large. Future refactor should make runner behavior more data-driven.

**SAM preview mode storage**
The Matchbox bool currently saves positionally in `ShaderParameters`. This works, but it is fragile.

**Preview-to-mask workflow**
Current v1 workflow may require re-prep after preview to select specific mask IDs. Future version should update existing job mask IDs without re-prepping.

**LAN SAM**
Deferred until shared mount layout is updated from old `bce_work` convention to current `~/bce/work` / `/mnt/bce` layout.

**Mask selection limit**
SAM can detect more than six objects, but BCE v1 only exposes Mask\_0 through Mask\_5.

**Transport lifecycle**
Transport movie is durable within the job. JPEG sequence is disposable after transport creation.
