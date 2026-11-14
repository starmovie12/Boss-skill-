#!/usr/bin/env python3
"""design_fingerprint.py - fingerprint a project's design and compare it with earlier designs (D-6).

Three axes, extracted statically from the project's source and built files:
  palette   chromatic hue families (12 bins of 30 degrees, weighted by use) plus background luminance class
  type      heading family and body family (first non-generic family in each font stack)
  skeleton  ordered landmark and section types of the main page (web) or screen list and navigation type (app)
Axis differs from an earlier entry when: palette hue-family Jaccard < 0.5 or background class differs; either font
family differs; skeleton sequence similarity < 0.7. A design is "too close" when fewer than 2 axes differ from ANY
entry in the history file. --append adds this design to the history after the comparison.
Exit 0 = distinct enough (or empty history), 1 = too close, 2 = usage error.
"""
import argparse
import colorsys
import datetime
import difflib
import html.parser
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import emit, iter_files, read_text  # noqa: E402

HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
FUNC = re.compile(r"(rgba?|hsla?)\(\s*([0-9.]+)(deg)?[\s,]+([0-9.]+)%?[\s,]+([0-9.]+)%?")
GENERIC = {"sans-serif", "serif", "monospace", "system-ui", "ui-sans-serif", "ui-serif", "ui-monospace", "-apple-system",
           "blinkmacsystemfont", "cursive", "fantasy", "inherit", "initial", "var", "emoji", "math"}
SECTION_WORDS = ["hero", "nav", "header", "feature", "pricing", "plan", "testimonial", "review", "faq", "cta", "gallery", "menu",
                 "contact", "about", "stat", "chart", "watchlist", "portfolio", "order", "ticket", "table", "form", "story", "team",
                 "timeline", "map", "footer", "sidebar", "card", "grid", "list", "search", "banner", "logo", "blog", "event"]
STYLE_EXT = {".css", ".scss", ".html", ".htm", ".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte", ".astro", ".json"}


def to_rgb(m_hex=None, m_fn=None):
    if m_hex:
        h = m_hex
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    kind, a, _, b, c = m_fn
    if kind.startswith("rgb"):
        return tuple(min(255, float(x)) / 255 for x in (a, b, c))
    r, g, bb = colorsys.hls_to_rgb(float(a) % 360 / 360, float(c) / 100, float(b) / 100)
    return (r, g, bb)


def palette_axis(texts):
    bins, bg_l = {}, None
    for t in texts:
        for m in HEX.finditer(t):
            add_color(bins, to_rgb(m_hex=m.group(1)))
        for m in FUNC.finditer(t):
            try:
                add_color(bins, to_rgb(m_fn=m.groups()))
            except ValueError:
                pass
        for m in re.finditer(r"(?:--(?:color-)?(?:bg|background|surface|canvas)[\w-]*|background(?:-color)?|backgroundColor)\s*[:=]\s*['\"]?(#[0-9a-fA-F]{3,6})", t):
            if bg_l is None:
                r, g, b = to_rgb(m_hex=m.group(1)[1:])
                bg_l = colorsys.rgb_to_hls(r, g, b)[1]
    total = sum(bins.values()) or 1
    fams = sorted(k for k, v in bins.items() if v / total >= 0.1)
    bg = "unknown" if bg_l is None else ("dark" if bg_l < 0.3 else "light" if bg_l > 0.7 else "mid")
    return {"hue_families": fams, "background": bg}


def add_color(bins, rgb):
    h, l, s = colorsys.rgb_to_hls(*rgb)
    if s < 0.12 or l < 0.08 or l > 0.96:
        return
    k = int((h * 360) // 30) * 30
    bins[k] = bins.get(k, 0) + 1


def first_family(stack):
    for f in stack.split(","):
        f = f.strip().strip("'\"").strip()
        if f and f.lower() not in GENERIC and not f.startswith("var("):
            return f.lower()
    return None


def type_axis(texts):
    heading = body = None
    for t in texts:
        for m in re.finditer(r"([^{}]+)\{[^{}]*?font-family\s*:\s*([^;}{]+)", t):
            sel, fam = m.group(1).lower(), first_family(m.group(2))
            if not fam:
                continue
            if heading is None and re.search(r"\bh[1-3]\b|heading|title|display", sel):
                heading = fam
            if body is None and re.search(r"\bbody\b|\bhtml\b|:root|\bp\b", sel):
                body = fam
        for m in re.finditer(r"--(?:font|family|typeface|ff)[\w-]*\s*:\s*([^;}{]+)", t):
            name, fam = m.group(0).split(":")[0].lower(), first_family(m.group(1))
            if not fam or fam.startswith("#") or re.match(r"[\d.]", fam):
                continue
            if re.search(r"heading|display|title|head", name):
                heading = heading or fam
            elif not re.search(r"mono|code|hindi|deva|script", name):
                body = body or fam
        for m in re.finditer(r"fontFamily\s*:\s*['\"]([^'\"]+)['\"]", t):
            fam = first_family(m.group(1))
            if fam:
                body = body or fam
    return {"heading": heading or body or "system", "body": body or heading or "system"}


class _Skel(html.parser.HTMLParser):
    TAGS = {"header", "nav", "main", "section", "article", "aside", "footer", "form", "table", "figure", "dialog"}

    def __init__(self):
        super().__init__()
        self.seq, self.depth = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("br", "img", "input", "meta", "link", "hr", "source"):
            return
        self.depth += 1
        if self.depth > 6:
            return
        a = dict(attrs)
        words = ((a.get("class") or "") + " " + (a.get("id") or "") + " " + (a.get("aria-label") or "")).lower()
        kind = next((w for w in SECTION_WORDS if w in words), None)
        if tag in self.TAGS or (kind and tag in ("div", "ul", "ol")):
            tok = kind or tag
            if not self.seq or self.seq[-1] != tok:
                self.seq.append(tok)

    def handle_endtag(self, tag):
        if tag not in ("br", "img", "input", "meta", "link", "hr", "source"):
            self.depth = max(0, self.depth - 1)


def skeleton_axis(root, files):
    idx = [p for p in files if os.path.basename(p) in ("index.html", "index.htm")]
    idx.sort(key=lambda p: (("dist" not in p and "build" not in p), len(p)))
    if idx:
        s = _Skel()
        s.feed(read_text(idx[0]))
        return {"kind": "web", "sequence": s.seq[:40]}
    screens = sorted(os.path.splitext(os.path.basename(p))[0].lower() for p in files
                     if re.search(r"(^|/)(app|screens|src/screens)/", os.path.relpath(p, root).replace(os.sep, "/")) and p.endswith((".tsx", ".jsx", ".ts", ".js")))
    nav = "tabs" if any("tabs" in os.path.relpath(p, root) or "createBottomTabNavigator" in read_text(p) for p in files if p.endswith((".tsx", ".jsx"))) else "stack"
    return {"kind": "app", "sequence": [nav] + screens[:40]}


def fingerprint(root):
    files = list(iter_files(root, STYLE_EXT))
    texts = [read_text(p) for p in files if not p.endswith("package-lock.json")]
    return {"palette": palette_axis(texts), "type": type_axis(texts), "skeleton": skeleton_axis(root, files)}


def compare(a, b):
    pa, pb = set(a["palette"]["hue_families"]), set(b["palette"]["hue_families"])
    jac = len(pa & pb) / len(pa | pb) if (pa | pb) else 1.0
    pal_diff = jac < 0.5 or a["palette"]["background"] != b["palette"]["background"]
    type_diff = a["type"]["heading"] != b["type"]["heading"] or a["type"]["body"] != b["type"]["body"]
    ratio = difflib.SequenceMatcher(None, a["skeleton"]["sequence"], b["skeleton"]["sequence"]).ratio()
    skel_diff = ratio < 0.7
    return {"palette_jaccard": round(jac, 2), "palette_differs": pal_diff, "type_differs": type_diff,
            "skeleton_similarity": round(ratio, 2), "skeleton_differs": skel_diff, "axes_differing": pal_diff + type_diff + skel_diff}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, help="project folder")
    ap.add_argument("--history", help="design-history JSON (default <root>/_boss/design-history.json)")
    ap.add_argument("--name", help="name for this entry (default: folder name)")
    ap.add_argument("--append", action="store_true", help="append this fingerprint to the history")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.root):
        print("no such folder: %s" % a.root, file=sys.stderr)
        return 2
    hist_path = a.history or os.path.join(a.root, "_boss", "design-history.json")
    hist = {"entries": []}
    if os.path.isfile(hist_path):
        try:
            hist = json.loads(read_text(hist_path))
        except ValueError:
            print("history file is not valid JSON: %s" % hist_path, file=sys.stderr)
            return 2
    fp = fingerprint(a.root)
    name = a.name or os.path.basename(os.path.abspath(a.root))
    comps = [dict(compare(fp, e), against=e.get("name")) for e in hist.get("entries", []) if e.get("name") != name]
    too_close = [c for c in comps if c["axes_differing"] < 2]
    if a.append:
        hist.setdefault("entries", [])
        hist["entries"] = [e for e in hist["entries"] if e.get("name") != name] + [dict(fp, name=name, date=datetime.date.today().isoformat())]
        os.makedirs(os.path.dirname(os.path.abspath(hist_path)), exist_ok=True)
        with open(hist_path, "w", encoding="utf-8") as fh:
            json.dump(hist, fh, indent=1)
    return emit({"check": "design_fingerprint", "name": name, "fingerprint": fp, "compared": len(comps),
                 "too_close_to": [c["against"] for c in too_close], "comparisons": comps, "appended": a.append}, a.json, ok=not too_close)


if __name__ == "__main__":
    sys.exit(main())
