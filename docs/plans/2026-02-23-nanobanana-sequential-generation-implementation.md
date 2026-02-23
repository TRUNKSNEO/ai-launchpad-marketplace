# Nanobanana Sequential Generation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add documented workflow patterns for sequential image generation with consistent styling to the nanobanana skill.

**Architecture:** Documentation-only enhancement. Add a "Sequential Generation" section to SKILL.md with 3 workflow patterns, a downstream integration pattern, expand prompts.md with matching prompt templates, and bump plugin version.

**Tech Stack:** Markdown only. No scripts or code changes.

**Design doc:** `docs/plans/2026-02-23-nanobanana-sequential-generation-design.md`

---

### Task 1: Add Sequential Generation section to SKILL.md

**Files:**
- Modify: `art/skills/nanobanana/SKILL.md:300` (insert after the SynthID Watermark Notice, before Best Practices)

**Step 1: Insert the Sequential Generation section**

Add the following after line 301 (after the SynthID paragraph, before `## Best Practices`):

```markdown
## Sequential Generation

Use sequential generation to maintain visual consistency across a series of images. The core technique: generate an anchor image first, then pass it as a reference (`-i`) for every subsequent image in the series.

### Pattern 1: Style-Board Anchoring

Generate a single anchor image that establishes the visual identity for a series. Reference it for all subsequent images.

**When to use:** Newsletter visual series, A/B thumbnail variants, brand-consistent image batches.

**Workflow:**

1. Generate the anchor image with a prompt emphasizing style, palette, and mood:
```bash
uv run <skill_dir>/scripts/generate.py \
  "modern flat illustration style, warm earth tones, soft gradients, clean lines, \
  minimal detail, cozy atmosphere" \
  --model pro -o anchor.png
```

2. Generate each subsequent image referencing the anchor:
```bash
uv run <skill_dir>/scripts/generate.py \
  "a laptop on a desk with coffee, matching the visual style, color palette, \
  and lighting of the reference image exactly" \
  -i anchor.png --model pro -o image_01.png
```

3. Repeat step 2 for each image in the series, always referencing the same anchor.

**Tip:** Use Flash to draft the anchor quickly, then regenerate with Pro once you find a style you like.

### Pattern 2: Subject Consistency

Keep the same character or subject looking consistent across different scenes and poses.

**When to use:** Mascot in multiple contexts, product photography series, recurring character.

**Workflow:**

1. Generate the initial subject with clear, detailed appearance description:
```bash
uv run <skill_dir>/scripts/generate.py \
  "a friendly robot mascot with round blue body, orange antenna, large expressive eyes, \
  simple geometric design, standing front-facing on white background" \
  --model pro -o subject_front.png
```

2. Generate new scenes referencing the subject:
```bash
uv run <skill_dir>/scripts/generate.py \
  "the same robot character from the reference image, now sitting at a desk typing, \
  same proportions and colors, office background" \
  -i subject_front.png --model pro -o subject_office.png
```

3. For stronger consistency, reference 2-3 of the best previous outputs:
```bash
uv run <skill_dir>/scripts/generate.py \
  "the same robot character from the reference images, now outdoors in a park, \
  same proportions and colors, waving at the viewer" \
  -i subject_front.png subject_office.png --model pro -o subject_park.png
```

### Pattern 3: Progressive Accumulation

Build a reference pool over a long series, adding each successful output as a reference for the next.

**When to use:** Series of 5+ images where consistency must compound across the full set.

**Workflow:**

1. Generate the anchor (same as Pattern 1, step 1).
2. Generate image 2 referencing the anchor.
3. Generate image 3 referencing anchor + image 2.
4. Continue, keeping the **3-4 strongest references** in the `-i` list. Drop weaker outputs.

**Why cap at 3-4 references:** More references dilute the style signal. The model averages across all inputs — too many and the result loses coherence. Keep only the images that best represent the target style.

**Reference ordering matters:** Place the style anchor first in the `-i` list. The model weights earlier references slightly more.
```

**Step 2: Verify SKILL.md line count**

Run: `wc -l art/skills/nanobanana/SKILL.md`
Expected: ~430 lines (under 500 limit)

**Step 3: Commit**

```bash
git add art/skills/nanobanana/SKILL.md
git commit -m "docs(nanobanana): add sequential generation patterns to SKILL.md"
```

---

### Task 2: Add downstream integration Pattern 4 to SKILL.md

**Files:**
- Modify: `art/skills/nanobanana/SKILL.md` (insert after Pattern 3: Batch with progress tracking in Downstream Skill Integration Guide, before Environment Variables)

**Step 1: Insert Pattern 4**

Add after the closing of Pattern 3's code block (after `successful = [r for r in results if r["success"]]`) and before `## Environment Variables`:

```markdown
### Pattern 4: Sequential generation for series

When a downstream skill needs multiple consistently-styled images (e.g., newsletter visuals, thumbnail A/B variants), use the anchor-and-reference pattern:

```python
from generate import generate_image

# Step 1: Generate the style anchor
anchor = generate_image(
    prompt="warm illustration style, earth tones, soft gradients, clean lines",
    output_path="anchor.png",
    model="pro",
)

# Step 2: Generate each image in the series, referencing the anchor
subjects = ["laptop on desk with coffee", "person reading a book", "sunrise over mountains"]
series_paths = [anchor["path"]]

for i, subject in enumerate(subjects):
    result = generate_image(
        prompt=f"{subject}, matching the visual style and color palette of the reference image exactly",
        input_paths=[anchor["path"]],  # always include the anchor
        output_path=f"series_{i+1:02d}.png",
        model="pro",
    )
    if result["success"]:
        series_paths.append(result["path"])
```

The full sequential generation patterns are documented in the [Sequential Generation](#sequential-generation) section above.
```

**Step 2: Verify line count**

Run: `wc -l art/skills/nanobanana/SKILL.md`
Expected: ~460 lines (under 500 limit)

**Step 3: Commit**

```bash
git add art/skills/nanobanana/SKILL.md
git commit -m "docs(nanobanana): add sequential generation downstream integration pattern"
```

---

### Task 3: Add sequential generation prompts to prompts.md

**Files:**
- Modify: `art/skills/nanobanana/references/prompts.md` (append after line 267, end of file)

**Step 1: Append the Sequential Generation Prompts section**

Add at the end of `references/prompts.md`:

```markdown
## Sequential Generation Prompts

Prompt templates for maintaining visual consistency across a series of images using the `-i` reference flag.

### Style-Board Anchor Prompts

Generate the anchor image that establishes the visual identity for a series:

```
{style} style, {color palette} color palette, {lighting} lighting,
{mood} atmosphere, {texture/detail level}, cohesive visual identity
```

**Examples:**
```
Modern flat illustration, warm earth tones and muted pastels,
soft ambient lighting, cozy inviting atmosphere, clean lines with
subtle gradients, cohesive visual identity

Dark moody photography style, deep blues and amber highlights,
dramatic side lighting, cinematic atmosphere, high contrast with
film grain, cohesive visual identity
```

### Referencing an Anchor

When generating subsequent images that reference the anchor:

```
{subject description}, matching the visual style, color palette,
and lighting of the reference image exactly
```

**Key phrasing patterns:**
- "matching the visual style of the reference image exactly"
- "using the same color palette and artistic style as the reference"
- "in the same style as the first image, with identical lighting and color treatment"

**Be explicit about what to preserve vs. change:**
```
# Good — clear about what changes and what stays
"a mountain landscape at sunset, using the exact same illustration style,
color palette, and line weight as the reference image"

# Bad — ambiguous about style preservation
"a mountain landscape at sunset, similar to the reference"
```

### Subject Consistency Prompts

Establish the subject with detailed, reusable appearance description:

```
{subject} with {distinguishing features}, {colors/materials},
{proportions}, {expression/pose}, on {simple background}
```

Reference the subject in new scenes:

```
the same {subject} from the reference image, now {new action/pose},
same proportions and colors, {new background/setting}
```

**Tip:** Include "same proportions and colors" explicitly — without it, the model may drift on physical attributes across scenes.

### A/B Variant Prompts

Generate multiple compositions sharing the same style for split-testing:

```bash
# Variant A: Close-up with text space on right
uv run generate.py "close-up portrait composition with negative space on the right, \
  matching the style of the reference image" -i anchor.png -o variant_a.png

# Variant B: Wide shot with centered subject
uv run generate.py "wide shot with centered subject and blurred background, \
  matching the style of the reference image" -i anchor.png -o variant_b.png

# Variant C: Dynamic angle with high energy
uv run generate.py "dynamic low-angle shot with dramatic perspective, \
  matching the style of the reference image" -i anchor.png -o variant_c.png
```

### Newsletter Series Prompts

Generate a set of visuals for a single newsletter issue with consistent styling:

```bash
# Anchor: Establish the issue's visual identity
uv run generate.py "minimalist tech illustration, teal and coral accents, \
  clean vector style, light gray background, cohesive identity" \
  --model pro -o newsletter_anchor.png

# Hero image
uv run generate.py "wide banner showing AI workflow automation concept, \
  matching the style of the reference image exactly" \
  -i newsletter_anchor.png --ratio 21:9 -o hero.png

# Section illustration 1
uv run generate.py "person collaborating with AI assistant on laptop, \
  matching the style of the reference image exactly" \
  -i newsletter_anchor.png --ratio 16:9 -o section_1.png

# Section illustration 2
uv run generate.py "abstract data flow visualization, \
  matching the style of the reference image exactly" \
  -i newsletter_anchor.png --ratio 16:9 -o section_2.png
```

### Sequential Prompting Tips

1. **Reference ordering matters** — Put the style anchor as the first `-i` argument. The model gives slightly more weight to earlier references.

2. **Be specific about preservation** — "matching the visual style" is okay; "matching the visual style, color palette, lighting, and line weight" is better.

3. **Describe what changes, not just what stays** — The model handles conflicting signals better when you clearly separate "keep X" from "change Y."

4. **Cap your reference pool** — 3-4 images is the sweet spot. Beyond that, the model averages too many inputs and the result loses character.

5. **Use consistent terminology** — If you called it "warm earth tones" in the anchor prompt, use "warm earth tones" (not "natural colors") in follow-up prompts.
```

**Step 2: Commit**

```bash
git add art/skills/nanobanana/references/prompts.md
git commit -m "docs(nanobanana): add sequential generation prompt templates"
```

---

### Task 4: Bump plugin version

**Files:**
- Modify: `art/.claude-plugin/plugin.json`

**Step 1: Update version**

Change `"version": "1.0.1"` to `"version": "1.1.0"`.

**Step 2: Commit**

```bash
git add art/.claude-plugin/plugin.json
git commit -m "chore(art): bump version to 1.1.0 for sequential generation docs"
```

---

### Task 5: Final validation

**Step 1: Verify SKILL.md line count**

Run: `wc -l art/skills/nanobanana/SKILL.md`
Expected: Under 500 lines

**Step 2: Verify no broken markdown**

Read through the final SKILL.md and prompts.md to confirm:
- All code blocks are properly closed
- Internal links work (e.g., `#sequential-generation` anchor)
- No placeholder content
- Consistent formatting with existing sections

**Step 3: Verify plugin.json**

Read `art/.claude-plugin/plugin.json` and confirm version is `1.1.0`.
