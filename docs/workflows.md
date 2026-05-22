# BCE Workflows

This doc covers per-template guidance for the workflows BCE ships
with — recommended step counts, prompt quirks, known limitations,
and which backends each template runs on.

For the universal "how to use BCE" stuff (prep/launch/import, seeds,
the Note field), see [usage.md](usage.md).

For the contract that lets you bring your own workflow or build a
new node category, see [glossary.md](glossary.md) and
[claude.md](claude.md).

---

## How to pick a template

Each BCE node category ships with one or more API templates under
`~/bce/templates/`. Pick the template in the BCE node's UI
via the workflow selector.

**API templates vs GUI templates.** BCE patches *API* templates at
render time. The `gui_versions/` subfolder contains the same
workflows in Comfy's GUI format — those are for inspection and
copy-paste into Comfy itself, not for BCE to load. If BCE says
"missing required BCE tag(s)," you probably picked a GUI template
by mistake.

**Read the template title — steps don't necessarily follow the template.** The workflow selector shows the title as set in the BCE/Matchbox XML, e.g.
"Flux.2 Klein - 4 steps" or "Flux.1 Fill - 12 steps". That title is
your only in-UI hint about what the template actually wants. The steps
slider default is baked into the XML and doesn't change when you
switch templates — if you switch from a 12-step template to a 4-step
LoRA and leave the slider alone, you're running 12 steps on a workflow
that expects 4. It'll look bad and take three times as long. Check the
title, match your slider.

**Backend compatibility.** All templates BCE ships with run on local,
LAN, and cloud. Templates that rely on nodes outside Comfy Cloud's
supported set (LanPaint, or anything else cloud won't run) are not
included — if one is added, its title should say so explicitly.

---

## Outpaint

Outpaint extends a single frame beyond its original borders, filling
in new pixels via diffusion. Inputs: one image. Outputs: one image
at the requested padded size.

**Comping the offset.** After each Outpaint render, BCE prints axis offset values to the console — X and Y distances to shift your comp node's axis so your original plate lands square in the center of the new frame. Read those values before you start pushing and cursing in the action node.

### Flux.1

**Model:** `flux1-fill-dev.safetensors`

Good at preserving texture in the extended area. Can struggle on large adds. Default 12 steps is fine — with guidance at 29 and a descriptive prompt, diminishing returns kick in early.

**Prompt:** Start with *"extend the image naturally…"* then describe the scene. The mechanical opener suppresses hallucination (random objects, sea monsters) that guidance alone doesn't always catch.

**Resolution limit.** Flux.1 gets unreliable above ~1.0 MP total output size. The launch dialog shows the calculated megapixel count so you can catch this before you launch. Try to keep your added area within that budget.

**Pixel shift.** Like all Flux models, Flux.1 will move your source pixels slightly. Always comp the original back over the result. The BCE console message gives you the axis offset values to use as a cheat for your comp.

### Flux.2

**Model:** `flux-2-klein-9b.safetensors`

A general-purpose image edit model repurposed for outpainting — the same model as Flux.2 Inpaint, with different masking, output size, and prompt. BCE fills the pad area with a black border and the prompt tells the model to replace it. It's a hack, but it works well.

**Prompt.** The default *"replace the border by extending the image naturally…"* is load-bearing. Skip it and the model may leave black patches at the edges. Add your scene description after it.

**Strengths.** Better than Flux.1 at adding objects and features that look like they belong. Faster, and fewer random artifacts. It does soften and shift source pixels a bit more than Flux.1, but the results are hard to compare directly — different training data, different character. Expect a "feels different" takeaway rather than a measurable quality delta. Probably the future default, since BFL doesn't appear to be shipping a dedicated Flux.2 Fill.

**Resolution limit.** Handles up to ~4 MP — significantly more headroom than Flux.1's 1.0 MP ceiling.

**Steps.** 4 is the default and holds up well at that count. Up to 8 to get a 'crisper, more baked' result.

**Known quirk — black border artifact.** Occasionally one or more edges will have a residual black outline — a side effect of the border-replacement approach. First try adding *"extend the image into the black border"* to your prompt — that often clears it. If not, rerun with a different seed; most renders come out clean.

---

## Inpaint

Inpaint replaces or removes content within a frame using a matte.
Inputs: front image + matte. Outputs: one image at source resolution.

**Matte required.** The BCE inpaint node won't prep without a matte connected. No exceptions.

**Change the prompt — the default is a placeholder.** The Note field loads with *"inpaint prompt"* as a reminder. It does nothing on its own. Replace it with what you actually want: `"remove girl"` or something as detailed as `"add graffiti to wall — artistic tags, some sloppy gang lettering, old peeling paint, faded"`. A more descriptive prompt can be better when generating new content.

**Mask softness.** Hard mattes can make blending rough at the edges. A little softness helps the model blend; comping your original back over the result helps more. BCE workflows ship with all feathering and blending parameters off — Comfy is not a comp tool,  especially if you're sitting on a Flame :).

### Flux.2 Klein 9B

**Model:** `flux-2-klein-9b.safetensors`

The same model as Flux.2 Outpaint, here used for inpaint. Default 4 steps. Beyond that — try it and find out. The two inpaint models have different character; which one works better depends on the shot.

### Qwen Edit 2509

**Model:** `qwen_image_edit_2509_fp8_e4m3fn.safetensors` + Lightning LoRA (4-step distilled)

Newer model, only recently in use. Different character from Flux.2 Klein — hard to measure directly, but you'll feel it. Qwen can shift and twist pixels harder than Klein, so comping your original plate back in matters even more here.

**Steps.** 4 is the default (Lightning LoRA, distilled for low step counts).

---

## SAM

SAM does video segmentation and tracking. Input: video clip. Output:
either a preview movie (colored object IDs) or a matte movie
(selected object IDs as a mask).

The SAM flow is different from the other categories — see "The
preview-then-mattes flow" below before reading the per-template
sections.

### The preview-then-mattes flow

SAM has two render actions on the right-click menu instead of one
Launch:

- **Render Preview** — runs SAM on one frame of the source, outputs
  a colored overlay showing detected/tracked object IDs. Use this
  first to see what SAM found and which IDs to keep.
- **Render Mattes** — runs SAM on the full clip, outputs a mask
  movie for the IDs you selected via the Mask_N toggles.

**Workflow:**

1. Enable Preview Mode in the Matchbox UI, enter a prompt (or leave
   blank to see all detected objects), Prepare Job, Render Preview.
2. Import the preview, identify which object IDs you want.
3. Set the Mask_N toggles for those IDs.
4. Re-prep (this is the v1 limitation — selecting new IDs requires
   re-prep), Render Mattes, Import Result.

**v1 limitations:**

- Re-prep required to change selected mask IDs.
- Only Mask_0 through Mask_5 exposed in the UI. Max Objects can be
  higher (useful for previewing crowds), but you can only directly
  extract the first six. To extract IDs above 5, render all masks
  and isolate in Flame.
- Transport movie is kept after prep — re-running Render Mattes
  against the same source skips JPEG re-export.

### If the matte is blank or wrong

Most common causes, in order of likelihood:

1. The prompt doesn't match anything in the clip. Run Preview Mode
   with an empty prompt to see everything SAM detects, then prompt
   for what's actually there.
2. The wrong Mask_N toggles are set for the IDs you want. Re-check
   the IDs from the preview and re-prep.
3. Threshold too high (nothing detected) or too low (everything
   detected). Adjust and re-render.

Fix is the same loop in each case: adjust the Matchbox settings,
re-prep, re-render.

### SAM3

**Model:** `sam3.1_multiplex_fp16.safetensors`

The most experimental of the BCE nodes, and also BCE's proof of concept for video transport. It works, but expect rough edges.

**You must change the prompt.** SAM3 is text-prompted. Simple nouns work well: `"people"`, `"chairs"`, `"car tires"`, `"windshields"`. You can also prompt for multiple object types at once — `"apples, wine bottles, bananas"` will pull all three, each as its own mask ID. Be specific when the scene has multiple candidate objects of the same type.

**Two ways to work it:**

*You know what you want.* Prompt directly, skip preview, render mattes. Fine when the subject is unambiguous.

*You have a crowd or multiple candidates.* Run preview first. The preview frame shows colored object IDs with confidence values overlaid. Use those to dial in your settings: set Threshold just below your target mask's confidence value, enable only the Mask_N toggles you want, set Max Objects to match, then re-prep with Preview Mode off and render mattes.

If the preview looks exactly right as-is, skip the re-prep — right-click the node and the menu will have changed to **Render Mattes**. Go straight to it. Re-prep is only needed if you changed any settings.

Example: target is mask ID 4, confidence 0.76 → Mask_4 = on, all others off, Threshold = 0.70, re-prep, render mattes.

**Max Objects.** Default is 6. Higher values are useful in preview to see everything SAM found in a crowd — but you can only extract IDs 0–5 directly. For higher IDs, render all masks and isolate in Flame.

---

## Color space on import

BCE preserves the source clip's tagged color space when it imports a
result back into Batch — the result inherits whatever the source was
tagged as. If a result imports as "Unknown," something broke in the
import path rather than the workflow: re-import manually via
right-click → Results Import on the BCE node, and if it's still wrong,
check the source clip's tagged color space in Flame.

---

## Bring your own workflow

### Level 1 — new template, existing category

If your workflow fits an existing BCE category (Outpaint, Inpaint, SAM), swapping in a custom template is straightforward.

1. Build and test the workflow standalone in ComfyUI first.
2. Tag the relevant nodes with `[BCE:*]` markers in their titles (see [glossary.md](glossary.md)). Easiest approach: copy the Load and Save nodes directly from an existing BCE API template — they're already tagged and wired correctly.
3. Save the API JSON to `~/bce/templates/` using the existing naming conventions. The GUI version goes in `gui_versions/` for your reference — BCE only loads API JSON.
4. Add a menu entry in the Matchbox XML for the new template.
5. Edit the top of the matching `bce_<category>.py` — one line, the template filename — to point at your new file.

The node category determines which tags BCE expects. Mismatches surface as "missing required BCE tag(s)" at Prepare Job time.

### Level 2 — new category

New Matchbox UI, new Python category file, possibly new runner logic. See [claude.md](claude.md). Or ask your neighborhood robot.
