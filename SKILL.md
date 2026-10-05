---
name: excalidraw-diagram
description: Create clean block-style Excalidraw diagrams (.excalidraw JSON) — architecture, pipelines, data flows, layered stacks, before/after deltas. Boxes carry 1-3 word labels, arrows carry tiny captions, colour carries meaning. Use whenever the user asks to diagram, draw, visualize, or map out a system, workflow, or architecture, even if they don't say "Excalidraw".
---

# Excalidraw Block Diagrams

Generate `.excalidraw` files that read at a glance: **simple colored blocks, very little text, arrows that show flow.** The viewer should get the structure in ten seconds without reading anything long. Detail belongs in the surrounding doc, not in the diagram.

**Setup:** for renderer/dependency setup see `README.md`. **Changing the theme of an existing diagram:** `python3 references/theme.py --recolor <file> --to <theme>`, then re-render.
**Theme:** colors come from a theme. Default is **Cool Classics**; the user can ask for any other (`python3 references/theme.py --list`). Details in `references/color-palette.md`.
**Layouts:** `references/layouts.md` lists layout options (flow, hub-and-spoke, cycle, tree, comparison, timeline, swimlane/stack). Read it to pick one.

## Why so little text

A diagram earns its place by showing shape: what sits above what, what talks to what, what changed. Sentences in boxes turn it into a slide of bullets that nobody reads and that breaks on resize. So every piece of text must be a label, not an explanation.

## Text budget (hard limits)

| Where | Limit |
|---|---|
| Block label | 1-3 words, at most 2 lines. Use the name the user's domain already uses, never a description |
| Arrow caption | 1-4 words, only when the arrow's meaning isn't obvious. Most arrows get none |
| Group / lane header | 1-3 words, UPPERCASE |
| Title | one line, no subtitle |
| Legend | one entry per color/line style used, 1-2 words each |

Never put sentences, bullets, code snippets, JSON, or parenthetical explanations in a block. If something needs explaining, drop it or tell the user in chat. When tempted to add a note box, ask whether the structure already shows it; if not, a 2-4 word grey note block is the maximum (e.g. `app side unchanged`).

## Building blocks

The vocabulary is small and shared by every layout:

- **Block** = `rectangle` with rounded corners, filled, text bound inside. The default for every component.
- **Start/actor** = `ellipse`. **Decision** = `diamond`. Use sparingly, only where the shape adds meaning.
- **Group** = large dashed, unfilled rectangle with a small label in its top-left corner, around blocks that belong together.
- **Arrow** = a relationship or flow (see Arrows).
- **Legend** = optional small swatches + 1-2 word names. Add one whenever color or line style carries meaning a reader couldn't guess; skip it for tiny diagrams where labels already say everything.

Choose the layout from the *shape of the idea*, not from habit: see `references/layouts.md`. A 4-block flow should look like a 4-block flow, not a lane diagram. Whatever the layout, prefer a regular grid: equal-size blocks, equal gaps (~25-40px), aligned edges. Regularity is what makes sparse text legible.

## Color = meaning

Colors are theme *roles* (`group_light`, `group_mid`, `accent`, `foundation`, `new`, `changed`, ...), resolved to hex by `theme.py`. Pick the role by what the block is, keep each role consistent across the diagram, and take fill, stroke and text from the same role row. Use a dashed stroke for optional/alternate paths and the `emphasis` role (stroke 3) for the one thing the diagram is about. `new` / `changed` is the standard way to show a delta; the rest stays in calm family colors. Always `opacity: 100`, `roughness: 0`.

## Arrows

- One arrow per real relationship; bind both ends (`startBinding`/`endBinding`) and mirror the binding in each shape's `boundElements`.
- Color the arrow like its source's family; use orange for the path the diagram is highlighting, dashed for feedback/async/alternate.
- Route with elbow points to avoid crossing blocks. Keep arrows within a group unless the crossing is the point.
- Caption sparingly, in small monospace, in the arrow's color.

## Sizing (so text is readable when the whole diagram is viewed)

Diagrams are viewed zoomed out, so go big: block text `fontSize` 26-36, headers 36, region labels 24-26, arrow captions 22-24, title 56-60. Blocks ~360-780px wide, 70-115px tall. `fontFamily: 3`, `textAlign: "center"`, bound via `containerId`. Short labels are what let you use big fonts; if a label doesn't fit, shorten the label, don't shrink the font.

## Process

1. **Pick the theme and resolve it:** `cd ~/.claude/skills/excalidraw-diagram/references && python3 theme.py [theme]` (no argument = Cool Classics). Use the printed hex values for everything, and the canvas background for `appState.viewBackgroundColor`.
2. **List the blocks and links** in your head: name each component with its short real name, pick a layout, mark what is new/changed if it's a delta. If you're about to write a long label, you're describing instead of naming — cut it.
3. **Lay out on a grid** following the chosen layout in `references/layouts.md`.
4. **Write the JSON** using `references/element-templates.md`. For more than ~40 elements, build it in sections (e.g. title and frame, then each group, then cross-group arrows, then legend) with one Edit per section; don't try to emit the whole file in one response. Use descriptive string IDs (`g_comp`, `a_sink_to_comp`) and write the JSON by hand — a generator script adds indirection that makes fixes harder.
5. **Render and look** (below). Fix and re-render until it's clean.

## JSON skeleton

```json
{ "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
  "elements": [], "appState": { "viewBackgroundColor": "<canvas from theme>", "gridSize": 20 }, "files": {} }
```

## Render & validate (required)

JSON can't show overlap or clipping, so render and view the PNG:

```bash
cd ~/.claude/skills/excalidraw-diagram/references && uv run python render_excalidraw.py <path-to-file.excalidraw>
```

Read the PNG, then check: text fits its block; nothing overlaps; arrows land on the intended blocks and don't cut through others; spacing and alignment are even; the colors are the theme's (no stray hex values); the legend has an entry for every color **and line style** used (a dashed arrow with no legend entry is a mystery); **and the text is sparse** — if any block reads like a sentence, shorten it. Fix and re-render (usually 2-3 passes).

First-time setup: `cd references && uv sync && uv run playwright install chromium`.
