# Layouts

Pick the layout that mirrors the idea. All layouts share the same rules: filled rounded blocks, 1-3 word names, tiny arrow captions, palette colors, regular grid. Mix layouts inside one diagram only when it helps (e.g. a flow inside one group of a stack).

| If the idea is... | Use | Sketch |
|---|---|---|
| A sequence of steps / pipeline | **Flow** (row or column of blocks) | `[A] → [B] → [C] → [D]` |
| A branch on a condition | **Flow + diamond** | `[A] → ◇ → [B] / [C]` |
| One thing talking to many (or many to one) | **Hub-and-spoke** (center block, ring or fan of blocks) | `[hub]` with arrows out/in |
| A loop / feedback process | **Cycle** (blocks around a ring, arrows clockwise) | `A → B → C ↺ A` |
| Parent/child structure | **Tree** (top-down blocks, elbow lines) | root → children → leaves |
| Two states or options side by side | **Comparison / before-after** (two columns, same rows, differences colored) | `[old] │ [new]` |
| Things over time, ordered messages | **Timeline / sequence** (a line with dots, or actor columns with horizontal arrows down) | `● ─ ● ─ ●` |
| Layers (top-level consumers down to foundations) | **Stack** (full-width rows, top to bottom) | stacked bars |
| Parallel concerns, each with its own stack | **Swimlane** (columns with header blocks, rows are shared tiers) | see below |
| Which things belong to which boundary | **Groups** (dashed regions around blocks) | can be added to any layout |

If nothing fits, use a plain flow. Simple beats clever.

## Common to all

- **Title** left-aligned, 56-60px, deep blue (`#1e40af`). Skip it when the diagram is a small illustration for a doc that already has a heading.
- **Spacing:** ~25-40px between blocks, ~60-100px between rows/columns that carry arrows (room for captions).
- **Flow direction:** left→right or top→bottom. One direction per diagram unless it's a cycle or hub.
- **Size scales with the idea:** 3-6 blocks → large blocks (~300x100) and big whitespace; 30+ blocks → smaller blocks (~360x70) on a tight grid. Keep font size at the readable end of the range either way by shortening labels.
- **Block content:** good → a short proper name or role (`Gateway`, `Order DB`, `Retry`). Bad → a clause that explains what it does, bullets, code, parentheticals. Two lines max; the second line is usually a path or sub-name.
- **Delta (what changed):** keep everything in calm family colors, then NEW in orange (`#fed7aa` / `#c2410c`, stroke 3) and CHANGED in yellow (`#fef3c7` / `#b45309`), carried by orange arrows. The legend says what they mean. Use this only when the diagram is actually about a change.
- **Arrow captions:** small monospace (22-24px), in the arrow's color, beside the line (`retry`, `on fail`, `async`). Skip when obvious.
- **Groups:** dashed unfilled rectangle, family-color stroke, label top-left (24-26px), inner blocks inset ~22px. Connect arrows to blocks, not to the group border.

## Swimlane / stack details

For parallel concerns that each have layers (columns = concerns, rows = shared tiers):

1. **Lane headers:** one rounded block per column, ~66px tall, UPPERCASE 36px, each lane its own family color. ~50px gaps between lanes with a dashed vertical divider (`#cbd5e1`) down the gap.
2. **Rows:** each lane is a column of blocks sharing x and width; side-by-side pairs split the width evenly. The entry point (ellipse) goes at the top.
3. **Tier spine (optional):** thin slate line at the far left with 16px dots and 22px tier labels, aligned to the rows. Use the tier names the user's domain uses.
4. **Hard boundary (optional):** a solid line (`#047857`, stroke 3) across the width with tiny labels naming the two sides, when the diagram has a real divide (public/private, client/server, trusted/untrusted). Foundation blocks sit below it.
5. **Legend:** bottom row of swatches, one per color and line style used.

Use this layout only when there are genuinely parallel stacks. A single stack is just rows; a single pipeline is just a flow.
