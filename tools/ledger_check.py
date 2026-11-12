#!/usr/bin/env python3
"""ledger_check.py - regenerate the expected source units and diff them against the ledger.

Modes:
  --gen DIR       write expected-unit listings (with titles) for extraction shards into DIR (outside the repo)
  --manifest      rewrite ledger/EXPECTED-UNITS.json (ids, line spans, hashes; no source text)
  (default)       check ledger/units/*.jsonl against the expected units, and field/*.jsonl rows

Expected units come from the raw sources when --src points at them (default /tmp/forge-src),
otherwise from ledger/EXPECTED-UNITS.json (reported as "manifest-only").
Standard library only, no network. Exit 0 = pass, 1 = fail, 2 = usage or environment error.
"""
import argparse, hashlib, json, os, re, sys, glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FATE_RE = re.compile(
    r"^(KEEP-CORE|KEEP-REFERENCE|QUARANTINE|QUARANTINE-DESIGN"
    r"|KEEP-MODE\((WEB|APP|PROMPT|AUDIT)(,(WEB|APP|PROMPT|AUDIT))*\)"
    r"|DROP\(.{3,}\)|CONFLICT\(.{2,}\))$")
FIELD_FATE_RE = re.compile(
    r"^(ADOPT-CORE|ADOPT-REFERENCE|ADOPT-MODE\((WEB|APP|PROMPT|AUDIT)(,(WEB|APP|PROMPT|AUDIT))*\)|REJECT\(.{3,}\))$")
SPLIT_SPAN = 120  # an S2 unit longer than this is split at its 4-space-indented child tags


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def read_lines(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read().split("\n")


def close_units(starts, total, lines, src):
    """starts: list of (line_index, id, title). Returns unit dicts with 1-based inclusive spans."""
    out = []
    for n, (idx, uid, title) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else total
        text = "\n".join(lines[idx:end])
        out.append({"id": uid, "src": src, "lines": [idx + 1, end], "sha": sha(text), "title": title})
    return out


def units_s1(path):
    """Markdown source: one unit per '### ' heading and per '## ' banner group, outside code fences."""
    L = read_lines(path)
    starts = [(0, "S1-0001", "front matter and title banner")]
    fence = False
    prev_banner = False
    for i, line in enumerate(L):
        if line.lstrip().startswith("```"):
            fence = not fence
            prev_banner = False
            continue
        if fence:
            prev_banner = False
            continue
        if line.startswith("### "):
            starts.append((i, "S1-%04d" % (i + 1), line[4:].strip()))
            prev_banner = False
        elif line.startswith("## "):
            has_text = bool(re.search(r"[A-Za-z]", line))
            if has_text and not prev_banner:
                # a banner may open with a rule line; start the unit at the rule line above if present
                start = i - 1 if i > 0 and L[i - 1].startswith("## ") and not re.search(r"[A-Za-z]", L[i - 1]) else i
                starts.append((start, "S1-%04d" % (i + 1), line[3:].strip()))
            prev_banner = prev_banner or has_text
        else:
            prev_banner = False
    return close_units(starts, len(L), L, "S1")


def units_s2(path):
    """XML source: one unit per 2-space-indented child tag of each part; long units split at 4-space children."""
    L = read_lines(path)
    part_starts = [i for i, l in enumerate(L) if l.startswith("<omni_builder_master_prompt")]
    bounds = [0] + part_starts + [len(L)]
    cdata = [False] * len(L)
    inside = False
    for i, l in enumerate(L):
        cdata[i] = inside
        if "<![CDATA[" in l:
            inside = True
        if "]]>" in l:
            inside = False
    starts = []
    for p in range(len(bounds) - 1):
        a, b = bounds[p], bounds[p + 1]
        tags = [i for i in range(a, b) if re.match(r"^  <[A-Za-z_]", L[i]) and not cdata[i]]
        if not tags or tags[0] != a:
            starts.append((a, "S2-P%02d-%04d" % (p, a + 1), "part %d preamble" % p))
        for n, t in enumerate(tags):
            end = tags[n + 1] if n + 1 < len(tags) else b
            kids = [i for i in range(t + 1, end) if re.match(r"^    <[A-Za-z_]", L[i]) and not cdata[i]]
            if end - t > SPLIT_SPAN and len(kids) > 1:
                first = True
                for k in kids:
                    idx = t if first else k
                    title = L[t].strip()[:60] + " :: " + L[k].strip()[:90] if first else L[k].strip()[:150]
                    starts.append((idx, "S2-P%02d-%04d" % (p, k + 1), title))
                    first = False
            else:
                starts.append((t, "S2-P%02d-%04d" % (p, t + 1), L[t].strip()[:150]))
    starts.sort(key=lambda s: s[0])
    return close_units(starts, len(L), L, "S2")


def units_s3(root):
    """Archive source: one unit per file, except the decision-rule XML, which is split per top-level child tag."""
    out = []
    files = []
    for d, _, fs in os.walk(root):
        for f in fs:
            files.append(os.path.join(d, f))
    files.sort()
    for p in files:
        rel = os.path.relpath(p, root)
        if rel.endswith("master-prompt.xml"):
            L = read_lines(p)
            tags = [i for i, l in enumerate(L) if re.match(r"^  <[A-Za-z_]", l)]
            starts = [(0, "S3-B-0001", "xml prolog and root open")] if tags and tags[0] != 0 else []
            for t in tags:
                starts.append((t, "S3-B-%04d" % (t + 1), L[t].strip()[:150]))
            for u in close_units(starts, len(L), L, "S3"):
                u["file"] = rel
                out.append(u)
        else:
            with open(p, "rb") as f:
                data = f.read()
            out.append({"id": "S3-F:" + rel, "src": "S3", "lines": [1, data.count(b"\n") + 1],
                        "sha": hashlib.sha256(data).hexdigest()[:12], "title": rel, "bytes": len(data)})
    return out


def expected_from_sources(src):
    s1 = os.path.join(src, "prose", "S1.md")
    s2 = os.path.join(src, "prose", "S2.xml")
    s3 = os.path.join(src, "skill")
    if not (os.path.isfile(s1) and os.path.isfile(s2) and os.path.isdir(s3)):
        return None
    return units_s1(s1) + units_s2(s2) + units_s3(s3)


def load_manifest():
    p = os.path.join(REPO, "ledger", "EXPECTED-UNITS.json")
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)["units"]


def load_jsonl(pattern):
    rows, errors = [], []
    for p in sorted(glob.glob(pattern)):
        with open(p, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    r["_file"] = os.path.relpath(p, REPO)
                    r["_line"] = n
                    rows.append(r)
                except ValueError as e:
                    errors.append("%s:%d bad json: %s" % (os.path.relpath(p, REPO), n, e))
    return rows, errors


def check_ledger(expected, mode):
    rows, errors = load_jsonl(os.path.join(REPO, "ledger", "units", "*.jsonl"))
    exp = {u["id"]: u for u in expected}
    seen = {}
    no_fate, bad_fate, sha_mismatch, long_summary = [], [], [], []
    for r in rows:
        uid = r.get("id")
        if uid in seen:
            errors.append("duplicate unit %s (%s:%d)" % (uid, r["_file"], r["_line"]))
        seen[uid] = r
        fate = (r.get("fate") or "").strip()
        if not fate:
            no_fate.append(uid)
        elif not FATE_RE.match(fate):
            bad_fate.append("%s: %s" % (uid, fate))
        if uid in exp and r.get("sha") and r["sha"] != exp[uid]["sha"]:
            sha_mismatch.append(uid)
        if len((r.get("summary") or "").split()) > 40 or not (r.get("summary") or "").strip():
            long_summary.append(uid)
    missing = sorted(set(exp) - set(seen))
    extra = sorted(set(seen) - set(exp))
    fates = {}
    for r in rows:
        key = re.sub(r"\(.*", "", (r.get("fate") or "NONE"))
        fates[key] = fates.get(key, 0) + 1
    per_src = {}
    for u in expected:
        per_src[u["src"]] = per_src.get(u["src"], 0) + 1
    ok = not (missing or extra or no_fate or bad_fate or errors or sha_mismatch or long_summary)
    return {"check": "ledger", "expected_mode": mode, "expected_units": len(exp), "ledger_rows": len(rows),
            "per_source": per_src, "missing": missing, "extra": extra, "no_fate": no_fate, "bad_fate": bad_fate,
            "sha_mismatch": sha_mismatch, "bad_summary": long_summary, "errors": errors, "fates": fates,
            "pass": ok}


def check_field():
    rows, errors = load_jsonl(os.path.join(REPO, "field", "*.jsonl"))
    bad = []
    repos = {}
    for r in rows:
        where = "%s:%d" % (r["_file"], r["_line"])
        url = r.get("repo") or ""
        if not url.startswith("http"):
            bad.append(where + " missing repo url")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(r.get("retrieved") or "")):
            bad.append(where + " missing retrieved date")
        fr = r.get("files_read")
        if not (isinstance(fr, list) and fr and all(isinstance(x, str) and x for x in fr)):
            bad.append(where + " missing files_read")
        if not (r.get("mechanism") or "").strip():
            bad.append(where + " missing mechanism")
        if not FIELD_FATE_RE.match((r.get("fate") or "").strip()):
            bad.append(where + " bad fate: %r" % r.get("fate"))
        d = repos.setdefault(url, {"rows": 0, "files": set()})
        d["rows"] += 1
        d["files"].update(fr if isinstance(fr, list) else [])
    thin = sorted(u for u, d in repos.items() if d["rows"] < 3 or len(d["files"]) < 3)
    synth = os.path.join(REPO, "docs", "FIELD-SYNTHESIS.md")
    synth_text = open(synth, encoding="utf-8").read() if os.path.isfile(synth) else ""
    thin_unexplained = [u for u in thin if u.rstrip("/").split("/")[-1] not in synth_text or "thin" not in synth_text.lower()]
    skipped = os.path.join(REPO, "field", "SKIPPED.md")
    skip_lines = []
    if os.path.isfile(skipped):
        skip_lines = [l for l in open(skipped, encoding="utf-8").read().split("\n") if l.strip().startswith("- ")]
    bad_skip = [l for l in skip_lines if re.search(r"\b(too (big|large|complex)|size|complexity|low value|not worth)\b", l, re.I)]
    blocked = os.path.isfile(os.path.join(REPO, "field", "BLOCKED-BY-ENV.md"))
    ok = (not bad and not errors and not thin_unexplained and len(skip_lines) <= 4 and not bad_skip and (rows or blocked))
    return {"check": "field", "rows": len(rows), "repos": len(repos), "bad_rows": bad, "errors": errors,
            "thin_repos": thin, "thin_unexplained": thin_unexplained, "skipped": len(skip_lines),
            "bad_skip_reasons": bad_skip, "blocked_by_env": blocked, "pass": bool(ok)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="/tmp/forge-src", help="directory holding the unpacked raw sources")
    ap.add_argument("--gen", metavar="DIR", help="write expected-unit listings with titles into DIR")
    ap.add_argument("--manifest", action="store_true", help="rewrite ledger/EXPECTED-UNITS.json from the raw sources")
    ap.add_argument("--skip-field", action="store_true", help="do not validate field/*.jsonl")
    ap.add_argument("--json", action="store_true", help="print machine-readable JSON")
    a = ap.parse_args()

    expected = expected_from_sources(a.src)
    mode = "raw-sources"
    if a.gen or a.manifest:
        if expected is None:
            print("raw sources not found under %s" % a.src, file=sys.stderr)
            return 2
        if a.gen:
            os.makedirs(a.gen, exist_ok=True)
            with open(os.path.join(a.gen, "units.tsv"), "w", encoding="utf-8") as f:
                for u in expected:
                    f.write("\t".join([u["id"], u["src"], "%d-%d" % tuple(u["lines"]), u["sha"],
                                       u.get("file", ""), u["title"]]) + "\n")
            print("wrote %d units to %s/units.tsv" % (len(expected), a.gen))
        if a.manifest:
            slim = [{"id": u["id"], "src": u["src"], "lines": u["lines"], "sha": u["sha"]} for u in expected]
            p = os.path.join(REPO, "ledger", "EXPECTED-UNITS.json")
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"rule": "see ledger/UNIT-RULES.md", "count": len(slim), "units": slim}, f, indent=0)
                f.write("\n")
            print("wrote manifest with %d units" % len(slim))
        return 0
    if expected is None:
        expected = load_manifest()
        mode = "manifest-only"
        if expected is None:
            print("no raw sources and no manifest", file=sys.stderr)
            return 2
    results = [check_ledger(expected, mode)]
    if not a.skip_field:
        results.append(check_field())
    ok = all(r["pass"] for r in results)
    if a.json:
        print(json.dumps({"pass": ok, "results": results}, indent=1))
    else:
        for r in results:
            print("[%s] %s" % ("PASS" if r["pass"] else "FAIL", r["check"]))
            for k, v in r.items():
                if k in ("check", "pass"):
                    continue
                if isinstance(v, list) and len(v) > 12:
                    v = v[:12] + ["... %d more" % (len(v) - 12)]
                print("   %s: %s" % (k, v))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
