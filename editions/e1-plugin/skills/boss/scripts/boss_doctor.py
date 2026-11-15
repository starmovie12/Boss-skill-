#!/usr/bin/env python3
"""boss_doctor.py - structural health check of the BOSS skill itself.

Checks: SKILL.md front matter (name, description <= 1,536 characters); every path the prose names (modes/, references/,
scripts/) exists; every mode file has an output contract heading; every script has a module docstring and --help works;
no color literals (hex, rgb, hsl) or preset palettes in prose; named fonts appear only inside a "Habits to avoid" block
of at most 120 words; token budgets (token_budget.py).
Exit 0 = healthy, 1 = problems, 2 = usage error.
"""
import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import SKILL_DIR, emit, read_text  # noqa: E402
import token_budget  # noqa: E402

FONT_NAMES = r"\b(Inter|Roboto|Arial|Helvetica|Open Sans|Lato|Montserrat|Poppins|Playfair|Georgia|Times New Roman|Source Sans|Noto Sans|Nunito|Raleway|Merriweather|Space Grotesk|DM Sans|Manrope|Outfit)\b"
COLOR = r"(?<![\w&])#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b|\brgba?\(\s*\d|\bhsla?\(\s*\d"


def prose_files(root):
    out = []
    for d, _, fs in os.walk(root):
        if "/scripts" in d.replace(os.sep, "/"):
            continue
        out += [os.path.join(d, f) for f in sorted(fs) if f.endswith(".md")]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=SKILL_DIR)
    ap.add_argument("--skip-help", action="store_true", help="do not run each script's --help")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    root = a.root
    sk = os.path.join(root, "SKILL.md")
    if not os.path.isfile(sk):
        print("no SKILL.md under %s" % root, file=sys.stderr)
        return 2
    problems = []
    text = read_text(sk)
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm:
        problems.append("SKILL.md has no front matter")
    else:
        if not re.search(r"^name:\s*\S+", fm.group(1), re.M):
            problems.append("front matter has no name")
        d = re.search(r"^description:\s*(.+)$", fm.group(1), re.M)
        if not d:
            problems.append("front matter has no description")
        elif len(d.group(1)) > 1536:
            problems.append("description is %d characters (limit 1,536)" % len(d.group(1)))
    for p in prose_files(root):
        rel = os.path.relpath(p, root)
        body = read_text(p)
        for m in re.finditer(r"`((?:modes|references|scripts)/[\w./-]+?)`|`python3 (scripts/[\w.]+)", body):
            path = (m.group(1) or m.group(2)).split(" ")[0]
            if not os.path.exists(os.path.join(root, path)):
                problems.append("%s names missing path %s" % (rel, path))
        for n, line in enumerate(body.splitlines(), 1):
            if re.search(COLOR, line):
                problems.append("%s:%d color literal in prose" % (rel, n))
        habits = re.search(r"## Habits to avoid[^\n]*\n(.*?)(?=\n## |\Z)", body, re.S)
        outside = body.replace(habits.group(0), "") if habits else body
        for m in re.finditer(FONT_NAMES, outside):
            problems.append("%s names a font outside the habits list: %s" % (rel, m.group(0)))
        if habits and len(habits.group(1).split()) > 120:
            problems.append("%s habits list is %d words (limit 120)" % (rel, len(habits.group(1).split())))
        if rel.startswith("modes" + os.sep) and not re.search(r"(?im)^#+ .*output contract", body):
            problems.append("%s has no output contract heading" % rel)
    sdir = os.path.join(root, "scripts")
    for f in sorted(os.listdir(sdir)) if os.path.isdir(sdir) else []:
        if not f.endswith(".py") or f.startswith("_"):
            continue
        src = read_text(os.path.join(sdir, f))
        if not re.match(r'(#!.*\n)?"""', src):
            problems.append("scripts/%s has no module docstring" % f)
        if "--json" not in src:
            problems.append("scripts/%s has no --json option" % f)
        if not a.skip_help:
            r = subprocess.run([sys.executable, os.path.join(sdir, f), "--help"], capture_output=True, text=True, timeout=60)
            if r.returncode != 0:
                problems.append("scripts/%s --help exits %d" % (f, r.returncode))
    tb = token_budget.check_skill(root)
    if not tb["pass"]:
        problems.append("token budget exceeded: %s" % [r["file"] for r in tb["files"] if not r["pass"]] or "total")
    return emit({"check": "boss_doctor", "root": root, "problems": problems, "total_tokens": tb["total_tokens"]}, a.json, ok=not problems)


if __name__ == "__main__":
    sys.exit(main())
