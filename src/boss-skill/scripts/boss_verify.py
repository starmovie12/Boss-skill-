#!/usr/bin/env python3
"""boss_verify.py - run every applicable BOSS gate on a project and report evidence.

Checks (each ends PASS, FAIL, NOT-RUN with the reason, or STATIC-ONLY):
  design_gate      _boss/acceptance.md, design-brief.md, layout-plan.md exist (and craft-log.md with --final)
  substance        no TODO/FIXME, lorem ipsum, "coming soon", dead links (href="#", javascript:void), empty handlers,
                   placeholder copy in source files
  secrets          secrets_scan over the project (including built output)
  palette          every row of _boss/tokens.md with two colors and a ratio: recomputed WCAG contrast meets the floor
                   (4.5, or 3 when the row says large, ui, icon, border or focus) and matches the claimed ratio within 0.2
  token_match      colors defined as tokens in the code also appear in _boss/tokens.md (at least 80 percent)
  build            `npm run build` when package.json has a build script and dependencies are installed (or --install)
  typecheck/lint   for TypeScript and Expo projects when dependencies are installed
  js_budget        gzip size of local scripts referenced by the built index.html <= --js-budget KB (default 170)
  placement        placement_check at 360 and 1280 px with the layout plan's primary action (browser or static-only)
  axe              axe-core serious and critical violations = 0 (when axe-core is resolvable from the project)
  permissions      (Expo) every permission requested in code is declared with a rationale in app config
Screenshots go to _boss/shots/. --shots-only takes screenshots and stops.
Exit 0 = no FAIL, 1 = at least one FAIL, 2 = usage error.
"""
import argparse
import gzip
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import emit, iter_files, read_text  # noqa: E402
import placement_check  # noqa: E402
import secrets_scan  # noqa: E402

SRC_EXT = {".html", ".htm", ".css", ".scss", ".js", ".jsx", ".mjs", ".ts", ".tsx", ".vue", ".svelte", ".astro", ".md", ".json"}
SUBSTANCE = [
    (re.compile(r"(?://|/\*|<!--|#)\s*(TODO|FIXME|XXX)\b"), "TODO/FIXME marker"),
    (re.compile(r"(?i)lorem ipsum|dolor sit amet"), "lorem ipsum"),
    (re.compile(r"(?i)coming soon|under construction"), "coming-soon text"),
    (re.compile(r"""href\s*=\s*["']#["']"""), "dead link href=\"#\""),
    (re.compile(r"(?i)javascript:\s*void\(0\)"), "javascript:void(0) link"),
    (re.compile(r"on(?:Click|Press|Submit|Change)\s*=\s*\{\s*\(\s*\w*\s*\)\s*=>\s*\{\s*\}\s*\}"), "empty event handler"),
    (re.compile(r"""onclick\s*=\s*["']\s*["']"""), "empty onclick"),
    (re.compile(r"(?i)\b(your company|company name|your name here|insert [a-z ]+ here|placeholder text)\b"), "placeholder copy"),
]


def contrast(c1, c2):
    def lum(h):
        h = h.lstrip("#")
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        ch = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        ch = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
        return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]
    a, b = sorted([lum(c1), lum(c2)], reverse=True)
    return (a + 0.05) / (b + 0.05)


def check(name, status, detail=""):
    return {"check": name, "status": status, "detail": detail}


def design_gate(root, final):
    need = ["acceptance.md", "design-brief.md", "layout-plan.md"] + (["craft-log.md"] if final else [])
    missing = [n for n in need if not os.path.isfile(os.path.join(root, "_boss", n))]
    return check("design_gate", "FAIL" if missing else "PASS", "missing: " + ", ".join(missing) if missing else "all present")


def substance(root):
    hits = []
    for p in iter_files(root, SRC_EXT, skip_dirs={"dist", "build", "out", ".output", "public/vendor"}):
        rel = os.path.relpath(p, root)
        if os.path.basename(p) in ("package.json", "package-lock.json", "tsconfig.json") or rel.endswith(".min.js"):
            continue
        for n, line in enumerate(read_text(p).splitlines(), 1):
            for rx, kind in SUBSTANCE:
                if rx.search(line):
                    hits.append("%s:%d %s" % (rel, n, kind))
                    break
    return check("substance", "FAIL" if hits else "PASS", hits[:40] if hits else "no stubs found")


def palette(root):
    p = os.path.join(root, "_boss", "tokens.md")
    if not os.path.isfile(p):
        return check("palette", "NOT-RUN", "no _boss/tokens.md palette table")
    bad, rows = [], 0
    for line in read_text(p).splitlines():
        cols = re.findall(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", line)
        ratio = re.search(r"(\d+(?:\.\d+)?)\s*:\s*1", line)
        if len(cols) >= 2 and ratio:
            rows += 1
            real = contrast(cols[0], cols[1])
            floor = 3.0 if re.search(r"(?i)\b(large|ui|icon|border|focus|non-text)\b", line) else 4.5
            claimed = float(ratio.group(1))
            if real + 1e-9 < floor or abs(real - claimed) > 0.2:
                bad.append("%s on %s: claimed %.2f, computed %.2f, floor %.1f" % (cols[0], cols[1], claimed, real, floor))
    if not rows:
        return check("palette", "FAIL", "tokens.md has no rows with two colors and a ratio")
    return check("palette", "FAIL" if bad else "PASS", bad or "%d pairs recomputed" % rows)


def token_match(root):
    p = os.path.join(root, "_boss", "tokens.md")
    if not os.path.isfile(p):
        return check("token_match", "NOT-RUN", "no _boss/tokens.md")
    brief = {h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}\b", read_text(p))}
    built = set()
    for f in iter_files(root, {".css", ".scss", ".ts", ".tsx", ".js", ".jsx", ".html"}, skip_dirs={"dist", "build", "out"}):
        for m in re.finditer(r"(?:--[\w-]+|\b\w*(?:color|colour|bg|background|surface|text|primary|accent)\w*)\s*[:=]\s*['\"]?(#[0-9a-fA-F]{6})\b", read_text(f)):
            built.add(m.group(1).lower())
    if not built:
        return check("token_match", "NOT-RUN", "no color tokens found in code")
    share = len(built & brief) / len(built)
    return check("token_match", "PASS" if share >= 0.8 else "FAIL", "%d of %d code token colors are in tokens.md" % (len(built & brief), len(built)))


def run(cmd, cwd, timeout=600):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        tail = (p.stdout + p.stderr).strip().splitlines()[-3:]
        return p.returncode, " | ".join(tail)[-300:]
    except (OSError, subprocess.TimeoutExpired) as e:
        return 99, str(e)[:200]


def site_dir(root):
    for d in ("dist", "build", "out", "_site", "public", "."):
        if os.path.isfile(os.path.join(root, d, "index.html")):
            return os.path.normpath(os.path.join(root, d))
    return None


def js_budget(site, budget_kb):
    idx = read_text(os.path.join(site, "index.html"))
    total, files = 0, []
    for src in re.findall(r"""<script[^>]+src=["']([^"'#?]+)""", idx) + re.findall(r"""<link[^>]+rel=["']modulepreload["'][^>]+href=["']([^"'#?]+)""", idx):
        if re.match(r"https?:", src):
            files.append(src + " (external, not counted)")
            continue
        p = os.path.join(site, src.lstrip("/"))
        if os.path.isfile(p):
            with open(p, "rb") as fh:
                total += len(gzip.compress(fh.read(), 9))
            files.append(src)
    inline = sum(len(gzip.compress(m.encode(), 9)) for m in re.findall(r"<script(?![^>]*src)[^>]*>(.*?)</script>", idx, re.S))
    kb = (total + inline) / 1024
    return check("js_budget", "PASS" if kb <= budget_kb else "FAIL", "%.1f KB gzip initial JS (budget %d KB); %s" % (kb, budget_kb, ", ".join(files[:6]) or "no scripts"))


def axe_path(root):
    node = shutil.which("node")
    if not node:
        return None
    for cwd in (root, os.path.dirname(os.path.abspath(__file__))):
        code, out = run([node, "-p", "require.resolve('axe-core/axe.min.js')"], cwd, 30)
        if code == 0 and out.strip().endswith("axe.min.js"):
            return out.strip().split(" | ")[-1]
    return None


def permissions(root):
    cfg = ""
    for n in ("app.json", "app.config.js", "app.config.ts"):
        if os.path.isfile(os.path.join(root, n)):
            cfg += read_text(os.path.join(root, n))
    if not cfg:
        return None
    used = set()
    for f in iter_files(root, {".ts", ".tsx", ".js", ".jsx"}):
        for m in re.finditer(r"(Camera|Location|MediaLibrary|Notifications|Contacts|Calendar|ImagePicker|Microphone|Audio)\w*\.request\w*Permissions?Async", read_text(f)):
            used.add(m.group(1))
    hints = {"Camera": "camera", "Location": "location", "MediaLibrary": "photo", "ImagePicker": "photo", "Notifications": "notification",
             "Contacts": "contacts", "Calendar": "calendar", "Microphone": "microphone", "Audio": "microphone"}
    missing = [u for u in sorted(used) if not re.search(hints[u], cfg, re.I)]
    return check("permissions", "FAIL" if missing else "PASS", ("requested in code but not declared with a rationale in app config: %s" % missing) if missing else ("declared: %s" % sorted(used) or "none requested"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, help="project folder")
    ap.add_argument("--final", action="store_true", help="also require _boss/craft-log.md")
    ap.add_argument("--install", action="store_true", help="run npm install when node_modules is missing")
    ap.add_argument("--no-build", action="store_true")
    ap.add_argument("--js-budget", type=int, default=170)
    ap.add_argument("--shots-only", action="store_true", help="only take screenshots at 360 and 1280 px")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        print("no such folder: %s" % root, file=sys.stderr)
        return 2
    shots = os.path.join(root, "_boss", "shots")
    plan = os.path.join(root, "_boss", "layout-plan.md")
    pkg = json.loads(read_text(os.path.join(root, "package.json"))) if os.path.isfile(os.path.join(root, "package.json")) else {}
    deps = dict(pkg.get("dependencies", {}), **pkg.get("devDependencies", {}))
    kind = "app" if "expo" in deps or "react-native" in deps else ("node-web" if pkg else "static")
    results = []
    if not a.shots_only:
        results += [design_gate(root, a.final), substance(root)]
        sec = secrets_scan.scan(root)
        results.append(check("secrets", "FAIL" if sec else "PASS", ["%s:%d %s" % (f["file"], f["line"], f["kind"]) for f in sec][:20] or "none found"))
        results += [palette(root), token_match(root)]
        if pkg and not a.no_build:
            has_nm = os.path.isdir(os.path.join(root, "node_modules"))
            if not has_nm and a.install:
                code, tail = run(["npm", "install", "--no-audit", "--no-fund"], root, 900)
                has_nm = code == 0
                results.append(check("install", "PASS" if code == 0 else "FAIL", tail))
            if not has_nm:
                results.append(check("build", "NOT-RUN", "dependencies not installed (use --install)"))
            else:
                if "typescript" in deps and os.path.isfile(os.path.join(root, "tsconfig.json")):
                    code, tail = run(["npx", "--no-install", "tsc", "--noEmit"], root)
                    results.append(check("typecheck", "PASS" if code == 0 else "FAIL", tail))
                if "lint" in pkg.get("scripts", {}):
                    code, tail = run(["npm", "run", "lint", "--silent"], root)
                    results.append(check("lint", "PASS" if code == 0 else "FAIL", tail))
                if kind == "app":
                    code, tail = run(["npx", "--no-install", "expo", "export", "--platform", "web", "--output-dir", "dist"], root, 900)
                    results.append(check("web_export", "PASS" if code == 0 else "FAIL", tail))
                elif "build" in pkg.get("scripts", {}):
                    code, tail = run(["npm", "run", "build", "--silent"], root, 900)
                    results.append(check("build", "PASS" if code == 0 else "FAIL", tail))
        if kind == "app":
            perm = permissions(root)
            if perm:
                results.append(perm)
    site = site_dir(root)
    if site:
        if not a.shots_only:
            results.append(js_budget(site, a.js_budget))
        axe = None if a.shots_only else axe_path(root)
        srv, base = placement_check.serve_dir(site)
        prim = placement_check.read_plan(plan)
        res, err = placement_check.run_browser(base, [360, 1280], prim[0][0] if prim else "", shots, axe)
        srv.shutdown()
        if res is None:
            issues = placement_check.static_check(os.path.join(site, "index.html"))
            results.append(check("placement", "STATIC-ONLY" if not issues else "FAIL", issues or "static checks clean (%s)" % err))
            results.append(check("axe", "NOT-RUN", err))
        else:
            hits = placement_check.evaluate(res, prim)
            results.append(check("screenshots", "PASS", [r.get("screenshot") for r in res]))
            if not a.shots_only:
                results.append(check("placement", "FAIL" if hits else "PASS", hits[:30] or "no geometry hits at 360 and 1280 px"))
                errs = [e for r in res for e in r.get("errors", [])]
                results.append(check("console", "FAIL" if errs else "PASS", errs[:10] or "no console errors"))
                axe_err = [r["axe_error"] for r in res if r.get("axe_error")]
                if axe and axe_err:
                    results.append(check("axe", "NOT-RUN", "axe could not run: %s" % axe_err[0]))
                elif axe:
                    v = [x for r in res for x in r.get("axe", []) if x.get("impact") in ("serious", "critical")]
                    ran = sum(1 for r in res if "axe" in r)
                    results.append(check("axe", "FAIL" if v else "PASS", ["%s (%s) x%d: %s" % (x["id"], x["impact"], x["nodes"], x["help"]) for x in v][:20] or "0 serious or critical at %d widths" % ran))
                else:
                    results.append(check("axe", "NOT-RUN", "axe-core not resolvable; add it as a dev dependency to enable"))
    elif not a.shots_only:
        results.append(check("placement", "NOT-RUN", "no built index.html found (dist, build, out, public or root)"))
    failed = [r["check"] for r in results if r["status"] == "FAIL"]
    return emit({"check": "boss_verify", "root": root, "kind": kind, "results": results, "failed": failed}, a.json, ok=not failed)


if __name__ == "__main__":
    sys.exit(main())
