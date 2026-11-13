#!/usr/bin/env python3
"""isolation_check.py - prove that shipped files carry no source canon and no pasted text.

Checks (each reported separately in JSON):
  tokens    case-sensitive search of the shipped trees for every product token in
            docs/ISOLATION-TOKENS.txt plus a fixed list; one hit fails.
  copies    no tracked file (git ls-files) has the sha256 of a raw source file.
  verbatim  no run of N or more consecutive words (default 21, i.e. "above 20 words") in a shipped
            file also occurs in a reference corpus (the raw sources, and any extra --against dir such
            as fetched third-party files). Skipped with a label when no corpus is present.

Shipped trees default to: src/boss-skill (examples/ excepted), editions/, .claude/.
Standard library only, no network. Exit 0 = pass, 1 = fail, 2 = usage error.
"""
import argparse, hashlib, json, os, re, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXED = ["CROWN", "GlassIsland", "Glass-Era", "avatar-bottom-nav", "city-shard", "hyper-local", "LAW-ENGLISH"]
TEXT_EXT = {".md", ".txt", ".py", ".json", ".xml", ".html", ".css", ".js", ".mjs", ".ts", ".tsx", ".sh", ".yml", ".yaml", ".csv"}
WORD = re.compile(r"[A-Za-z0-9ऀ-ॿ']+")


def shipped_files(roots, exclude):
    out = []
    for r in roots:
        base = os.path.join(REPO, r)
        if os.path.isfile(base):
            out.append(base)
            continue
        for d, dirs, fs in os.walk(base):
            rel = os.path.relpath(d, REPO)
            if any(rel == e or rel.startswith(e + os.sep) for e in exclude):
                dirs[:] = []
                continue
            dirs[:] = [x for x in dirs if x not in ("node_modules", "__pycache__", ".git")]
            for f in fs:
                if os.path.splitext(f)[1].lower() in TEXT_EXT:
                    out.append(os.path.join(d, f))
    return sorted(out)


def read(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def load_tokens(path):
    toks = list(FIXED)
    if os.path.isfile(path):
        for line in read(path).split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                toks.append(line)
    seen, out = set(), []
    for t in toks:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def check_tokens(files, tokens):
    hits = []
    for p in files:
        text = read(p)
        for t in tokens:
            # whole-token match where the token starts/ends with a word character
            pat = (r"(?<![A-Za-z0-9_])" if t[0].isalnum() else "") + re.escape(t) + (r"(?![A-Za-z0-9_])" if t[-1].isalnum() else "")
            for m in re.finditer(pat, text):
                line = text.count("\n", 0, m.start()) + 1
                hits.append({"file": os.path.relpath(p, REPO), "line": line, "token": t})
    return {"check": "tokens", "tokens": len(tokens), "files": len(files), "hits": hits[:200],
            "hit_count": len(hits), "pass": not hits}


def check_copies(src_files):
    try:
        tracked = subprocess.run(["git", "-C", REPO, "ls-files"], capture_output=True, text=True, check=True).stdout.split("\n")
    except Exception as e:  # git missing is an environment problem, reported not hidden
        return {"check": "copies", "pass": False, "error": str(e)}
    want = {}
    for s in src_files:
        with open(s, "rb") as f:
            want[hashlib.sha256(f.read()).hexdigest()] = os.path.basename(s)
    found = []
    for t in tracked:
        p = os.path.join(REPO, t)
        if t and os.path.isfile(p):
            with open(p, "rb") as f:
                if hashlib.sha256(f.read()).hexdigest() in want:
                    found.append(t)
    return {"check": "copies", "tracked": len([t for t in tracked if t]), "source_hashes": len(want),
            "copies": found, "pass": not found}


def words(text):
    return [w.lower() for w in WORD.findall(text)]


def shingles(ws, n):
    return {" ".join(ws[i:i + n]) for i in range(0, max(0, len(ws) - n + 1))}


def corpus_files(dirs):
    out = []
    for d in dirs:
        if os.path.isfile(d):
            out.append(d)
        elif os.path.isdir(d):
            for root, _, fs in os.walk(d):
                for f in fs:
                    if os.path.splitext(f)[1].lower() in TEXT_EXT:
                        out.append(os.path.join(root, f))
    return out


def check_verbatim(files, corpus, n):
    if not corpus:
        return {"check": "verbatim", "pass": True, "label": "NOT-RUN: no reference corpus present", "n": n}
    ref = set()
    for c in corpus:
        ref |= shingles(words(read(c)), n)
    hits = []
    for p in files:
        ws = words(read(p))
        for i in range(0, max(0, len(ws) - n + 1)):
            s = " ".join(ws[i:i + n])
            if s in ref:
                hits.append({"file": os.path.relpath(p, REPO), "words": s[:160]})
                break
    return {"check": "verbatim", "n": n, "corpus_files": len(corpus), "files": len(files), "hits": hits, "pass": not hits}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--roots", nargs="*", default=["src/boss-skill", "editions", ".claude"], help="shipped trees")
    ap.add_argument("--exclude", nargs="*", default=["src/boss-skill/examples"], help="repo-relative dirs to skip")
    ap.add_argument("--tokens", default=os.path.join(REPO, "docs", "ISOLATION-TOKENS.txt"))
    ap.add_argument("--src", default="/tmp/forge-src", help="raw sources: prose/*.md|xml and skill/ (optional)")
    ap.add_argument("--against", nargs="*", default=[], help="extra corpus dirs for the verbatim check (e.g. fetched field files)")
    ap.add_argument("--words", type=int, default=21, help="verbatim run length that fails (default 21 = above 20 words)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    files = shipped_files(a.roots, a.exclude)
    raw = [os.path.join(a.src, "prose", f) for f in ("S1.md", "S2.xml")]
    raw = [p for p in raw if os.path.isfile(p)]
    corpus = raw + corpus_files([os.path.join(a.src, "skill")] if os.path.isdir(os.path.join(a.src, "skill")) else []) + corpus_files(a.against)
    corpus = [c for c in corpus if not c.endswith(".csv") and os.path.getsize(c) < 2_000_000]
    results = [check_tokens(files, load_tokens(a.tokens)),
               check_copies([p for p in raw]) if raw else {"check": "copies", "pass": True, "label": "NOT-RUN: raw sources absent"},
               check_verbatim(files, corpus, a.words)]
    ok = all(r["pass"] for r in results)
    if a.json:
        print(json.dumps({"pass": ok, "shipped_files": len(files), "results": results}, indent=1))
    else:
        for r in results:
            print("[%s] %s %s" % ("PASS" if r["pass"] else "FAIL", r["check"], r.get("label", "")))
            for k in ("hit_count", "copies", "hits"):
                if r.get(k):
                    print("   %s: %s" % (k, r[k] if not isinstance(r[k], list) else r[k][:10]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
