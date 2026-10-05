#!/usr/bin/env python3
"""Resolve a color theme into diagram roles, list themes, or recolor an existing diagram.

  python theme.py                         # default theme (cool-classics), as a role table
  python theme.py earth-tones             # another theme (slug, name, or D2 id)
  python theme.py earth-tones --json      # same, as JSON
  python theme.py --list                  # all themes
  python theme.py --recolor in.excalidraw --to dark-mauve [--from cool-classics] [-o out.excalidraw]

Theme data (themes.json) comes from D2's open-source theme catalog (https://d2lang.com/tour/themes/).
Each theme is a slot palette: B1-B6 base shades (B1 strongest, B6 faintest), AA/AB accents, N1-N7 neutrals
(N1 text ... N7 canvas). Slots keep their meaning in dark themes, so one role mapping serves all themes.
"""
import argparse, colorsys, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = "cool-classics"
THEMES = json.load(open(os.path.join(HERE, "themes.json")))

# Status colors carry fixed meaning (new / changed / error), so they stay recognizable in every theme.
STATUS = {
    "light": {"new": ("#FED7AA", "#C2410C"), "changed": ("#FEF3C7", "#B45309"), "error": ("#FECACA", "#B91C1C")},
    "dark": {"new": ("#7C2D12", "#FB923C"), "changed": ("#78350F", "#FBBF24"), "error": ("#7F1D1D", "#F87171")},
}


def find(key):
    k = str(key).strip().lower().replace("_", "-").replace(" ", "-")
    if k in THEMES:
        return k
    for slug, t in THEMES.items():
        if k == str(t["id"]) or k == t["name"].lower().replace(" ", "-"):
            return slug
    matches = [s for s in THEMES if k in s]
    if len(matches) == 1:
        return matches[0]
    sys.exit(f"Unknown theme '{key}'. Run with --list. Close matches: {matches or 'none'}")


def _lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def _contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _darken(h, f=0.62):
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(hh, l * f, s)
    return "#%02X%02X%02X" % (round(r * 255), round(g * 255), round(b * 255))


def resolve(slug):
    t = THEMES[slug]
    s = {k: v.upper() for k, v in t["slots"].items()}
    st = STATUS[t["mode"]]

    def text_on(fill):
        return s["N1"] if _contrast(fill, s["N1"]) >= _contrast(fill, s["N7"]) else s["N7"]

    def role(fill, stroke, width=2, style="solid"):
        return {"fill": fill, "stroke": stroke, "text": text_on(fill), "strokeWidth": width, "strokeStyle": style}

    roles = {
        "canvas": {"background": s["N7"]},
        "title": {"text": s["B2"]},
        "text_body": {"text": s["N1"]},
        "text_muted": {"text": s["N2"]},
        # Blocks (fill + stroke + text inside)
        "group_light": role(s["B6"], s["B2"]),
        "group_mid": role(s["B4"], s["B2"]),
        "emphasis": role(s["B3"], s["B1"], 3),
        "accent": role(s["AB5"], _darken(s["AB4"])),
        "foundation": role(s["AA5"], s["AA2"]),
        "new": role(*st["new"], 3),
        "changed": role(*st["changed"]),
        "error": role(*st["error"]),
        "inverse": role(s["N1"], s["N1"]),
        "note": role(s["N6"], s["N3"]),
        # Lines and structure (stroke only)
        "arrow": {"stroke": s["N2"]},
        "divider": {"stroke": s["N4"], "strokeStyle": "dashed"},
        "spine": {"stroke": s["N3"]},
        "boundary": {"stroke": s["AA2"], "strokeWidth": 3},
        "group_border": {"stroke": s["B2"], "strokeStyle": "dashed", "fill": "transparent"},
        "dot": {"fill": s["B3"], "stroke": s["B3"]},
    }
    return {"theme": slug, "name": t["name"], "mode": t["mode"], "roles": roles, "slots": s}


def color_map(slug):
    """Every concrete color a theme can emit -> its slot name or role-field key (used for recoloring)."""
    r = resolve(slug)
    m = {}
    for k, v in r["slots"].items():
        m.setdefault(v, k)
    m.setdefault(_darken(r["slots"]["AB4"]), "AB_DARK")
    for kind in ("new", "changed", "error"):
        fill, stroke = STATUS[r["mode"]][kind]
        m.setdefault(fill, kind + "_fill")
        m.setdefault(stroke, kind + "_stroke")
    return m, r


def slot_values(slug):
    r = resolve(slug)
    vals = dict(r["slots"])
    vals["AB_DARK"] = _darken(r["slots"]["AB4"])
    for kind in ("new", "changed", "error"):
        vals[kind + "_fill"], vals[kind + "_stroke"] = STATUS[r["mode"]][kind]
    return vals


def recolor(path, src, dst, out):
    data = json.load(open(path))
    old_map, _ = color_map(src)
    new_vals = slot_values(dst)
    new_res = resolve(dst)
    mapping = {old.upper(): new_vals[key] for old, key in old_map.items() if key in new_vals}
    changed = unknown = 0
    by_id = {e["id"]: e for e in data["elements"]}
    for e in data["elements"]:
        for f in ("strokeColor", "backgroundColor"):
            c = (e.get(f) or "").upper()
            if c in mapping:
                e[f] = mapping[c]; changed += 1
            elif c and c != "TRANSPARENT":
                unknown += 1
    # keep text readable after light<->dark swaps: recompute text color inside filled containers
    n1, n7 = new_res["slots"]["N1"], new_res["slots"]["N7"]
    for e in data["elements"]:
        cont = by_id.get(e.get("containerId") or "")
        if e["type"] == "text" and cont and (cont.get("backgroundColor") or "").startswith("#"):
            bg = cont["backgroundColor"]
            e["strokeColor"] = n1 if _contrast(bg, n1) >= _contrast(bg, n7) else n7
    data.setdefault("appState", {})["viewBackgroundColor"] = new_res["roles"]["canvas"]["background"]
    json.dump(data, open(out, "w"), indent=1)
    print(f"recolored {path} ({src} -> {dst}) -> {out}: {changed} colors mapped, {unknown} left as-is (not from '{src}')")


def table(r):
    lines = [f"# Theme: {r['name']} ({r['theme']}, {r['mode']})", "",
             f"canvas background: {r['roles']['canvas']['background']}  (appState.viewBackgroundColor)", "",
             "| role | fill | stroke | text | strokeWidth / style |", "|---|---|---|---|---|"]
    for name, v in r["roles"].items():
        if name == "canvas":
            continue
        style = f"{v.get('strokeWidth', 2)} / {v.get('strokeStyle', 'solid')}" if "stroke" in v else "-"
        lines.append(f"| {name} | {v.get('fill', '-')} | {v.get('stroke', '-')} | {v.get('text', '-')} | {style} |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("theme", nargs="?", default=DEFAULT)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--recolor", metavar="FILE")
    ap.add_argument("--from", dest="src", default=DEFAULT)
    ap.add_argument("--to")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    if a.list:
        for slug, t in sorted(THEMES.items(), key=lambda kv: (kv[1]["mode"], kv[1]["id"])):
            print(f"{slug:28} {t['mode']:5} id={t['id']:<3} {t['name']}" + ("   (default)" if slug == DEFAULT else ""))
        return
    if a.recolor:
        if not a.to:
            sys.exit("--recolor needs --to <theme>")
        out = a.out or os.path.splitext(a.recolor)[0] + f".{find(a.to)}.excalidraw"
        recolor(a.recolor, find(a.src), find(a.to), out)
        return
    r = resolve(find(a.theme))
    print(json.dumps(r["roles"] | {"theme": r["theme"], "mode": r["mode"]}, indent=1) if a.json else table(r))


if __name__ == "__main__":
    main()
