# Excalidraw Diagram Skill

A coding agent skill that generates beautiful and practical Excalidraw diagrams from natural language descriptions. Clean block-style diagrams: colored blocks, 1-3 word labels, short arrow captions, in whichever layout fits (flow, hub, cycle, tree, comparison, timeline, stack, swimlane).

Compatible with any coding agent that supports skills. For agents that read from `.claude/skills/` (like [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [OpenCode](https://github.com/nicepkg/OpenCode)), just drop it in and go.

## What Makes This Different

- **Simple blocks, minimal text.** Labels are names, not sentences; the layout is picked to match the idea. See `references/layouts.md`.
- **Color carries meaning.** Palette roles for groups, new vs changed, infrastructure, and so on.
- **Built-in visual validation.** A Playwright-based render pipeline lets the agent see its own output, catch layout issues (overlapping text, misaligned arrows, unbalanced spacing), and fix them in a loop before delivering.
- **Color themes.** 20 themes from [D2's catalog](https://d2lang.com/tour/themes/), default **Cool Classics**. Ask for another by name ("use earth tones", "dark mode"), or restyle an existing diagram with `theme.py --recolor`.

## Installation

Clone or download this repo, then copy it into your project's `.claude/skills/` directory:

```bash
git clone https://github.com/coleam00/excalidraw-diagram-skill.git
cp -r excalidraw-diagram-skill .claude/skills/excalidraw-diagram
```

## Setup

The skill includes a render pipeline that lets the agent visually validate its diagrams. There are two ways to set it up:

**Option A: Ask your coding agent (easiest)**

Just tell your agent: *"Set up the Excalidraw diagram skill renderer by following the instructions in SKILL.md."* It will run the commands for you.

**Option B: Manual**

```bash
cd .claude/skills/excalidraw-diagram/references
uv sync
uv run playwright install chromium
```

## Usage

Ask your coding agent to create a diagram:

> "Create an Excalidraw diagram showing how the AG-UI protocol streams events from an AI agent to a frontend UI"

The skill handles the rest — concept mapping, layout, JSON generation, rendering, and visual validation.

## Themes

```bash
cd references
python3 theme.py --list                       # all themes (default: cool-classics)
python3 theme.py earth-tones                  # resolved role colors for a theme
python3 theme.py --recolor my.excalidraw --to dark-mauve   # restyle an existing diagram
```

Or just tell the agent: "draw this in the grape soda theme". To add your own theme, add an entry to `references/themes.json` with the same slots (B1-B6, AA2/4/5, AB4/5, N1-N7).

## File Structure

```
excalidraw-diagram/
  SKILL.md                          # Design methodology + workflow
  references/
    color-palette.md                # Theme roles and how to switch themes
    themes.json                     # Theme palettes (from D2's catalog)
    theme.py                        # Resolve / list / recolor themes
    layouts.md                      # Layout options
    element-templates.md            # JSON templates for each element type
    json-schema.md                  # Excalidraw JSON format reference
    render_excalidraw.py            # Render .excalidraw to PNG
    render_template.html            # Browser template for rendering
    pyproject.toml                  # Python dependencies (playwright)
```
