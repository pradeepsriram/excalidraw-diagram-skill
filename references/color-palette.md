# Color Palette & Brand Style

**This is the single source of truth for all colors and brand-specific styles.** To customize diagrams for your own brand, edit this file — everything else in the skill is universal.

---

## Shape Colors (Semantic)

Colors encode meaning, not decoration. Each semantic purpose has a fill/stroke pair.

| Semantic Purpose | Fill | Stroke |
|------------------|------|--------|
| Primary/Neutral | `#3b82f6` | `#1e3a5f` |
| Secondary | `#60a5fa` | `#1e3a5f` |
| Tertiary | `#93c5fd` | `#1e3a5f` |
| Start/Trigger | `#fed7aa` | `#c2410c` |
| End/Success | `#a7f3d0` | `#047857` |
| Warning/Reset | `#fee2e2` | `#dc2626` |
| Decision | `#fef3c7` | `#b45309` |
| AI/LLM | `#ddd6fe` | `#6d28d9` |
| Inactive/Disabled | `#dbeafe` | `#1e40af` (use dashed stroke) |
| Error | `#fecaca` | `#b91c1c` |

**Rule**: Always pair a darker stroke with a lighter fill for contrast.

### Block-diagram roles

| Role | Fill | Stroke |
|------|------|--------|
| Lane A / default family (light) | `#dbeafe` | `#1e40af` |
| Lane B family (mid) | `#93c5fd` | `#1e3a5f` |
| Emphasis block in a family | `#60a5fa` | `#1e3a5f` (strokeWidth 3) |
| Lane C family (control/service) | `#ddd6fe` | `#6d28d9` |
| NEW | `#fed7aa` | `#c2410c` (strokeWidth 3) |
| CHANGED | `#fef3c7` | `#b45309` |
| Foundation / infrastructure (lowest layer, storage, hardware, platform) | `#a7f3d0` | `#047857` |
| Dark accent (a channel, store or queue worth standing out) | `#1e293b` | `#1e293b`, text `#93c5fd` |
| Note (unchanged/aside) | `#f1f5f9` | `#64748b` |

Text inside blocks: `#374151` on light fills, or the family's dark stroke color (`#1e3a5f`, `#7c2d12` on orange/yellow, `#4c1d95` on lavender). Region boxes: no fill, dashed, family stroke. Lane dividers: `#cbd5e1` dashed.

---

## Text Colors (Hierarchy)

Use color on free-floating text to create visual hierarchy without containers.

| Level | Color | Use For |
|-------|-------|---------|
| Title | `#1e40af` | Section headings, major labels |
| Subtitle | `#3b82f6` | Subheadings, secondary labels |
| Body/Detail | `#64748b` | Descriptions, annotations, metadata |
| On light fills | `#374151` | Text inside light-colored shapes |
| On dark fills | `#ffffff` | Text inside dark-colored shapes |

---

## Dark Block Colors

Used for a dark "data/socket/queue" block (short label only; no code or JSON in diagrams).

| Artifact | Background | Text Color |
|----------|-----------|------------|
| Code snippet | `#1e293b` | Syntax-colored (language-appropriate) |
| JSON/data example | `#1e293b` | `#22c55e` (green) |

---

## Default Stroke & Line Colors

| Element | Color |
|---------|-------|
| Arrows | Use the stroke color of the source element's semantic purpose |
| Structural lines (dividers, trees, timelines) | Primary stroke (`#1e3a5f`) or Slate (`#64748b`) |
| Marker dots (fill + stroke) | Primary fill (`#3b82f6`) |

---

## Background

| Property | Value |
|----------|-------|
| Canvas background | `#ffffff` |
