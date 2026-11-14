#!/usr/bin/env python3
"""placement_check.py - heuristic geometry lint for rendered pages (PL gate).

At each width (default 360 and 1280 px) it reports: horizontal scroll, overlapping interactive elements, interactive
elements outside the viewport, clipped text, targets under 44 px (48 px for the primary action below 600 px; inline
text links exempt), elements covered at every scroll position by another layer (fixed bars, banners), and whether the
primary action named in _boss/layout-plan.md (line `primary: "<label>" zone=<top|middle|bottom>`) exists, is
uncovered and sits in the planned zone. Optional: axe-core accessibility scan (--axe PATH) and full-page screenshots.

The script is standard library; it drives the preinstalled Playwright through `node` as an external tool. Without
node or Playwright it falls back to a static HTML check and labels the result static-only.
It is a lint, not a verdict: fix or justify each hit, and still look at the screenshots.
Exit 0 = no hits, 1 = hits, 2 = usage or environment error.
"""
import argparse
import functools
import html.parser
import http.server
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import emit, read_text  # noqa: E402

NODE_SCRIPT = r"""
const { chromium } = require(process.env.BOSS_PW || 'playwright');
const fs = require('fs');
const [,, url, widthsCsv, primaryLabel, shotDir, axePath, blockExternal] = process.argv;
(async () => {
  const browser = await chromium.launch();
  const out = [];
  for (const w of widthsCsv.split(',').map(Number)) {
    const page = await browser.newPage({ viewport: { width: w, height: w < 600 ? 780 : 800 }, deviceScaleFactor: 1 });
    const errors = [];
    page.on('pageerror', e => errors.push('pageerror: ' + String(e.message || e)));
    page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text().slice(0, 200)); });
    if (blockExternal === '1') {
      await page.route('**/*', r => { const u = r.request().url();
        if (/^(https?:\/\/(127\.0\.0\.1|localhost)|file:|data:|blob:)/.test(u)) r.continue(); else r.abort(); });
    }
    try { await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 }); } catch (e) { errors.push('goto: ' + e.message); }
    await page.waitForTimeout(400);
    const res = await page.evaluate(async ([primaryLabel]) => {
      const vw = document.documentElement.clientWidth, vh = window.innerHeight;
      const SEL = 'a[href],button,input:not([type=hidden]),select,textarea,summary,[role=button],[role=link],[role=tab],[role=checkbox],[role=switch],[role=menuitem],[onclick],[tabindex]:not([tabindex="-1"])';
      const vis = el => { const s = getComputedStyle(el); if (s.visibility === 'hidden' || s.display === 'none' || +s.opacity === 0) return false;
        const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
      const label = el => ((el.getAttribute('aria-label') || el.innerText || el.value || el.getAttribute('title') || el.getAttribute('alt') || '') + '').trim().replace(/\s+/g, ' ');
      const desc = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (label(el) ? ' "' + label(el).slice(0, 40) + '"' : '');
      const els = [...document.querySelectorAll(SEL)].filter(vis).slice(0, 600);
      const page = el => { const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; };
      const inlineLink = el => el.tagName === 'A' && getComputedStyle(el).display === 'inline' && el.parentElement && /^(P|LI|SPAN|TD|LABEL|SMALL|DD|EM|STRONG)$/.test(el.parentElement.tagName);
      const target = el => { let r = page(el); if (el.labels && el.labels.length) { for (const l of el.labels) { const q = page(l);
          const x1 = Math.min(r.x, q.x), y1 = Math.min(r.y, q.y), x2 = Math.max(r.x + r.w, q.x + q.w), y2 = Math.max(r.y + r.h, q.y + q.h);
          r = { x: x1, y: y1, w: x2 - x1, h: y2 - y1 }; } } return r; };
      const hscroll = document.documentElement.scrollWidth > vw + 1;
      const norm = s => s.toLowerCase().replace(/\s+/g, ' ').trim();
      let primary = null;
      if (primaryLabel) { const want = norm(primaryLabel); primary = els.find(e => norm(label(e)) === want) || els.find(e => norm(label(e)).includes(want)) || null; }
      const P = els.map(page);
      const overlaps = [];
      for (let i = 0; i < els.length && overlaps.length < 40; i++) for (let j = i + 1; j < els.length; j++) {
        const a = els[i], b = els[j]; if (a.contains(b) || b.contains(a)) continue;
        const A = P[i], B = P[j]; const ix = Math.min(A.x + A.w, B.x + B.w) - Math.max(A.x, B.x), iy = Math.min(A.y + A.h, B.y + B.h) - Math.max(A.y, B.y);
        if (ix > 2 && iy > 2 && ix * iy > 0.1 * Math.min(A.w * A.h, B.w * B.h)) overlaps.push([desc(a), desc(b)]); }
      const offscreen = els.filter((e, i) => P[i].x + P[i].w > vw + 1 || P[i].x < -1).map(desc).slice(0, 40);
      const small = []; els.forEach(e => { if (inlineLink(e)) return; const t = target(e); const min = (e === primary && vw < 600) ? 48 : 44;
        if (Math.min(t.w, t.h) < min - 0.5) small.push(desc(e) + ' ' + Math.round(t.w) + 'x' + Math.round(t.h)); });
      const clipped = []; for (const el of document.querySelectorAll('body *')) { if (clipped.length >= 40) break;
        if (!vis(el) || ![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue; const s = getComputedStyle(el);
        const hx = /(hidden|clip)/.test(s.overflowX) && s.textOverflow !== 'ellipsis' && el.scrollWidth > el.clientWidth + 1;
        const hy = /(hidden|clip)/.test(s.overflowY) && s.webkitLineClamp === 'none' && el.scrollHeight > el.clientHeight + 2;
        if (hx || hy) clipped.push(desc(el)); }
      const maxY = Math.max(0, document.documentElement.scrollHeight - vh); const seen = new Map();
      for (let y = 0; ; y = Math.min(maxY, y + Math.max(120, Math.floor(vh / 3)))) { window.scrollTo(0, y); await new Promise(r => requestAnimationFrame(() => r()));
        els.forEach((el, i) => { const r = el.getBoundingClientRect(); if (r.top < 0 || r.bottom > vh || r.left < 0 || r.right > vw || r.height > vh) return;
          const cx = r.left + r.width / 2, cy = r.top + r.height / 2; const top = document.elementFromPoint(cx, cy);
          const ok = !!top && (top === el || el.contains(top) || top.contains(el) || (el.labels && [...el.labels].some(l => l.contains(top))));
          const prev = seen.get(i) || { visible: false, clear: false, by: null }; prev.visible = true; if (ok) prev.clear = true; else if (!prev.by && top) prev.by = desc(top); seen.set(i, prev); });
        if (y >= maxY) break; }
      window.scrollTo(0, 0);
      const covered = []; seen.forEach((v, i) => { if (v.visible && !v.clear) covered.push(desc(els[i]) + ' covered by ' + v.by); });
      let prim = null;
      if (primaryLabel) { if (!primary) prim = { found: false };
        else { const s = getComputedStyle(primary); let fixedAnc = null; for (let n = primary; n && n !== document.body; n = n.parentElement) { const p = getComputedStyle(n).position; if (p === 'fixed' || p === 'sticky') { fixedAnc = p; break; } }
          const r = primary.getBoundingClientRect(); const y = fixedAnc ? r.top + r.height / 2 : r.top + scrollY + r.height / 2;
          const zone = y > vh && !fixedAnc ? 'below-fold' : (y < vh / 3 ? 'top' : (y < 2 * vh / 3 ? 'middle' : 'bottom'));
          const i = els.indexOf(primary); const cov = seen.get(i);
          prim = { found: true, label: label(primary).slice(0, 60), zone, pinned: fixedAnc, size: Math.round(r.width) + 'x' + Math.round(r.height), covered: !!(cov && cov.visible && !cov.clear) }; } }
      return { vw, vh, interactive: els.length, hscroll, scrollWidth: document.documentElement.scrollWidth, overlaps, offscreen, small, clipped, covered, primary: prim };
    }, [primaryLabel || '']);
    if (axePath) { try { await page.addScriptTag({ content: fs.readFileSync(axePath, 'utf8') });
        const ax = await page.evaluate(async () => { const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'] } });
          return r.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, help: v.help })); });
        res.axe = ax; } catch (e) { res.axe_error = String(e.message || e); } }
    if (shotDir) { fs.mkdirSync(shotDir, { recursive: true }); await page.screenshot({ path: shotDir + '/shot-' + w + '.png', fullPage: true }); res.screenshot = shotDir + '/shot-' + w + '.png'; }
    res.width = w; res.errors = errors; out.push(res); await page.close(); }
  await browser.close(); process.stdout.write(JSON.stringify(out));
})().catch(e => { console.error(String(e && e.stack || e)); process.exit(3); });
"""


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve_dir(path):
    """Serve a folder on 127.0.0.1 in a daemon thread; return (server, base_url)."""
    handler = functools.partial(_Quiet, directory=path)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, "http://127.0.0.1:%d/" % srv.server_address[1]


def read_plan(plan_path):
    """Return [(label, zone)] from `primary: "<label>" zone=<zone>` lines."""
    out = []
    if plan_path and os.path.isfile(plan_path):
        for m in re.finditer(r'primary:\s*"([^"]+)"(?:\s*zone=(top|middle|bottom))?', read_text(plan_path)):
            out.append((m.group(1), m.group(2)))
    return out


def find_playwright():
    node = shutil.which("node")
    if not node:
        return None, None
    for cwd in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
        try:
            p = subprocess.run([node, "-p", "require.resolve('playwright')"], cwd=cwd, capture_output=True, text=True, timeout=20)
            if p.returncode == 0 and p.stdout.strip():
                return node, os.path.dirname(p.stdout.strip())
        except Exception:
            pass
    return node, None


def run_browser(url, widths, primary, shot_dir=None, axe=None, block_external=True, timeout=180):
    node, pw = find_playwright()
    if not node or not pw:
        return None, "node or Playwright not available"
    with tempfile.TemporaryDirectory() as td:
        js = os.path.join(td, "probe.cjs")
        with open(js, "w") as fh:
            fh.write(NODE_SCRIPT)
        env = dict(os.environ, BOSS_PW=pw)
        try:
            p = subprocess.run([node, js, url, ",".join(map(str, widths)), primary or "", shot_dir or "", axe or "", "1" if block_external else "0"],
                               capture_output=True, text=True, timeout=timeout, env=env)
        except subprocess.TimeoutExpired:
            return None, "browser probe timed out"
    if p.returncode != 0:
        return None, (p.stderr or "probe failed").strip()[-400:]
    return json.loads(p.stdout), None


class _Static(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.issues, self.viewport, self.stack = [], False, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and a.get("name") == "viewport":
            self.viewport = True
            if re.search(r"user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(\.0)?\b", a.get("content", "")):
                self.issues.append("viewport disables zoom")
        if tag in ("button", "a") and not a.get("aria-label") and not a.get("title"):
            self.stack.append([tag, ""])
        if tag == "img" and not (a.get("width") and a.get("height")) and "aspect-ratio" not in (a.get("style") or ""):
            self.issues.append("img without width and height: %s" % (a.get("src") or "")[:60])
        m = re.search(r"width\s*:\s*(\d{3,})px", a.get("style") or "")
        if m and int(m.group(1)) > 360:
            self.issues.append("fixed inline width %spx on <%s> (overflows 360 px)" % (m.group(1), tag))

    def handle_data(self, data):
        if self.stack:
            self.stack[-1][1] += data.strip()

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1][0] == tag:
            t, text = self.stack.pop()
            if not text:
                self.issues.append("<%s> with no text and no aria-label" % t)


def static_check(html_path):
    p = _Static()
    p.feed(read_text(html_path))
    if not p.viewport:
        p.issues.append("no viewport meta")
    return p.issues


def evaluate(results, plan):
    hits = []
    for r in results:
        w = r["width"]
        if r.get("hscroll"):
            hits.append("%dpx: horizontal scroll (page %dpx wide)" % (w, r["scrollWidth"]))
        for a, b in r.get("overlaps", []):
            hits.append("%dpx: overlap %s / %s" % (w, a, b))
        hits += ["%dpx: outside viewport %s" % (w, x) for x in r.get("offscreen", [])]
        hits += ["%dpx: small target %s" % (w, x) for x in r.get("small", [])]
        hits += ["%dpx: clipped text %s" % (w, x) for x in r.get("clipped", [])]
        hits += ["%dpx: %s" % (w, x) for x in r.get("covered", [])]
        p = r.get("primary")
        if plan and p is not None:
            label, zone = plan[0]
            if not p.get("found"):
                hits.append('%dpx: primary action "%s" not found' % (w, label))
            else:
                if p.get("covered"):
                    hits.append("%dpx: primary action covered" % w)
                if zone and w < 600 and p.get("zone") != zone:
                    hits.append("%dpx: primary action in zone %s, plan says %s" % (w, p.get("zone"), zone))
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--url", help="page URL (http://...) or a local .html file")
    g.add_argument("--site", help="folder with index.html; served on 127.0.0.1")
    ap.add_argument("--page", default="", help="path under --site to check (default index)")
    ap.add_argument("--plan", help="_boss/layout-plan.md with a primary: line")
    ap.add_argument("--widths", default="360,1280")
    ap.add_argument("--shots", help="folder for full-page screenshots")
    ap.add_argument("--axe", help="path to axe.min.js to also run an accessibility scan")
    ap.add_argument("--allow-external", action="store_true", help="do not block non-local requests")
    ap.add_argument("--static-only", action="store_true", help="skip the browser")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    widths = [int(x) for x in a.widths.split(",") if x.strip()]
    plan = read_plan(a.plan)
    srv, url, html_file = None, a.url, None
    if a.site:
        if not os.path.isfile(os.path.join(a.site, a.page or "index.html")):
            print("no %s under %s" % (a.page or "index.html", a.site), file=sys.stderr)
            return 2
        html_file = os.path.join(a.site, a.page or "index.html")
        srv, base = serve_dir(a.site)
        url = base + a.page
    elif a.url and not re.match(r"https?://", a.url):
        if not os.path.isfile(a.url):
            print("no such file: %s" % a.url, file=sys.stderr)
            return 2
        html_file = os.path.abspath(a.url)
        srv, base = serve_dir(os.path.dirname(html_file))
        url = base + os.path.basename(html_file)
    results, err = (None, "static-only requested") if a.static_only else run_browser(
        url, widths, plan[0][0] if plan else "", a.shots, a.axe, not a.allow_external)
    if srv:
        srv.shutdown()
    if results is None:
        if not html_file:
            print("browser unavailable (%s) and no local HTML for a static check" % err, file=sys.stderr)
            return 2
        issues = static_check(html_file)
        return emit({"check": "placement_check", "mode": "static-only", "reason": err, "hits": issues}, a.json, ok=not issues)
    hits = evaluate(results, plan)
    axe = [v for r in results for v in r.get("axe", []) if v.get("impact") in ("serious", "critical")]
    out = {"check": "placement_check", "mode": "browser", "url": url, "widths": widths, "hits": hits,
           "primary_plan": plan[0] if plan else None, "per_width": [{k: r.get(k) for k in ("width", "interactive", "primary", "screenshot", "errors")} for r in results]}
    if a.axe:
        out["axe_serious_critical"] = axe
    return emit(out, a.json, ok=not hits and not axe)


if __name__ == "__main__":
    sys.exit(main())
