# Color Themes

**Colors come from a theme, never from memory.** Run the resolver once per diagram and use its hex values for every shape, text and line:

```bash
cd ~/.claude/skills/excalidraw-diagram/references && python3 theme.py            # default theme
python3 theme.py earth-tones                                                      # a named theme
python3 theme.py --list                                                           # all themes
```

The resolver prints a table of **roles** (fill / stroke / text / strokeWidth / style) plus the canvas background to put in `appState.viewBackgroundColor`. Always `opacity: 100`.

## Default and switching

- **Default theme: Cool Classics** (`cool-classics`), a blue family with teal and violet accents. Use it unless the user asks otherwise.
- The user can pick any theme by name ("use earth tones", "dark mode", "make it warm") — run `theme.py <name>`. For a vague request ("change the theme"), run `theme.py --list` and ask which one; "dark" means `dark-mauve` or `dark-flagship-terrastruct`, "warm" means one of `earth-tones`, `vanilla-nitro-cola`, `buttered-toast`, `orange-creamsicle`.
- To restyle an **existing** diagram without redrawing it: `python3 theme.py --recolor diagram.excalidraw --to <theme> [--from <current theme>] [-o out.excalidraw]`, then re-render. `--from` defaults to Cool Classics.
- Themes are D2's catalog (https://d2lang.com/tour/themes/), stored in `themes.json`. To add a custom theme, add an entry with the same slots (B1-B6, AA2/4/5, AB4/5, N1-N7) and it appears in `--list`.

## Roles (what each means)

| Role | Use for |
|---|---|
| `title` | Diagram title, section headings (text only) |
| `text_body` / `text_muted` | Free-floating labels / captions and secondary notes |
| `group_light` | Default block; first lane or family |
| `group_mid` | Second lane or family; secondary blocks |
| `emphasis` | The one thing the diagram is about (strokeWidth 3) |
| `accent` | A third family (control, service, external actor) |
| `foundation` | Lowest layer: storage, hardware, platform, infrastructure |
| `new` / `changed` / `error` | Status highlights for a delta or failure. Same hues in every theme so they stay recognizable |
| `inverse` | A dark block that should pop (channel, queue, store) |
| `note` | Neutral aside ("unchanged"), 2-4 words |
| `arrow` | Default arrow color; or use the source block's `stroke` |
| `divider` / `spine` / `boundary` | Lane dividers (dashed) / tier spine / hard boundary line |
| `group_border` | Dashed unfilled group rectangle (fill stays transparent) |
| `dot` | Timeline and spine marker dots |

**Rules:** pair each fill with its own `stroke` and `text` from the same role row (text is chosen for contrast, so it stays readable on dark themes). Keep each role consistent across a diagram. Do not invent colors; if nothing fits, use `group_light`. A legend entry per role used makes meaning explicit.
