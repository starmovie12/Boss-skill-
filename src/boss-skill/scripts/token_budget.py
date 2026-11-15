#!/usr/bin/env python3
"""token_budget.py - check BOSS prose against its size budgets.

Method: tokens are estimated as characters / 3.5 (conservative for English prose and markdown).
Budgets (tokens): SKILL.md 2,500; each mode file 5,000; each reference 2,500; each domain reference 1,500;
total prose 30,000. A file passes only with 10 percent headroom (estimate <= 0.9 x budget).
Edition mode (--editions DIR): E2/E3 core 2,500, each E2/E3 mode pack 3,500, Gem instructions 4,000 characters.
Exit 0 = all within budget, 1 = over budget, 2 = usage error.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import SKILL_DIR, emit, read_text  # noqa: E402

CHARS_PER_TOKEN = 3.5
HEADROOM = 0.9


def est(text):
    return int(round(len(text) / CHARS_PER_TOKEN))


def budget_for(rel):
    rel = rel.replace(os.sep, "/")
    if rel == "SKILL.md":
        return 2500
    if rel.startswith("modes/"):
        return 5000
    if rel.startswith("references/domains/"):
        return 1500
    if rel.startswith("references/"):
        return 2500
    return None


def check_skill(root):
    rows, total = [], 0
    for d, _, files in os.walk(root):
        if "/scripts" in d.replace(os.sep, "/") or "/tests" in d.replace(os.sep, "/"):
            continue
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            p = os.path.join(d, f)
            rel = os.path.relpath(p, root)
            b = budget_for(rel)
            t = est(read_text(p))
            total += t
            rows.append({"file": rel, "tokens": t, "budget": b, "limit_with_headroom": int(b * HEADROOM) if b else None,
                         "pass": b is None or t <= b * HEADROOM})
    rows.sort(key=lambda r: r["file"])
    total_ok = total <= 30000 * HEADROOM
    return {"check": "token_budget", "method": "chars/3.5, 10% headroom", "files": rows, "total_tokens": total,
            "total_limit_with_headroom": int(30000 * HEADROOM), "pass": total_ok and all(r["pass"] for r in rows)}


def check_editions(root):
    rows = []
    for d, _, files in os.walk(root):
        for f in sorted(files):
            p = os.path.join(d, f)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            text = read_text(p) if f.endswith((".md", ".txt")) else ""
            if not text:
                continue
            if f == "gem-instructions.txt":
                rows.append({"file": rel, "chars": len(text), "limit": 4000, "pass": len(text) <= 4000})
            elif f in ("project-instructions.md", "core.md"):
                t = est(text)
                rows.append({"file": rel, "tokens": t, "limit": 2500, "pass": t <= 2500})
            elif "/packs/" in "/" + rel or f.startswith("mode-"):
                t = est(text)
                rows.append({"file": rel, "tokens": t, "limit": 3500, "pass": t <= 3500})
    return {"check": "edition_budget", "files": rows, "pass": all(r["pass"] for r in rows)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=SKILL_DIR, help="skill folder (default: this skill)")
    ap.add_argument("--editions", help="check an editions folder instead")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args()
    if a.editions:
        if not os.path.isdir(a.editions):
            print("no such folder: %s" % a.editions, file=sys.stderr)
            return 2
        return emit(check_editions(a.editions), a.json)
    if not os.path.isfile(os.path.join(a.root, "SKILL.md")):
        print("no SKILL.md under %s" % a.root, file=sys.stderr)
        return 2
    return emit(check_skill(a.root), a.json)


if __name__ == "__main__":
    sys.exit(main())
