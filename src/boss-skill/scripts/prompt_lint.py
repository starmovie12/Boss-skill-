#!/usr/bin/env python3
"""prompt_lint.py - ADVISORY structural lint for prompts and agent work orders (a heuristic, not a quality score).

Flags: missing parts (goal or done, constraints, acceptance or success criteria, output format, stop or blocked handling
for long work orders), vague words with no number nearby, unresolved placeholders, shouting (runs of ALL-CAPS words),
"use your judgment" with no default, halting traps (wait for approval, ask the user) in unattended work orders, and
lines that repeat. Always exits 0 unless --strict is given (then 1 when anything is flagged); 2 on usage error.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import emit, read_text  # noqa: E402

PARTS = {
    "goal_or_done": r"(?i)\b(goal|objective|definition of done|done (means|when)|outcome)\b",
    "constraints": r"(?i)\b(constraint|must not|never|do not|don't|limit|only)\b",
    "acceptance": r"(?i)\b(acceptance|success criteria|pass(es)? (if|when)|check(ed)? (by|with)|verify|test)\b",
    "output_format": r"(?i)\b(output|deliverable|return|format|respond (only )?(as|with)|json|schema)\b",
}
LONG_PARTS = {"stop_or_blocked": r"(?i)\b(stop|blocked|if .{0,30} fails|when .{0,30} fails|cannot|unreachable)\b",
              "context": r"(?i)\b(context|background|repo|environment|you have|available)\b"}
VAGUE = r"(?i)\b(fast|quick(ly)?|robust|scalable|seamless|intuitive|clean|modern|nice|good|better|best|appropriate|reasonable|various|some|many|etc\.?|user[- ]friendly|high[- ]quality|optimi[sz]ed|lightweight|soon)\b"
PLACEHOLDER = r"(\bTBD\b|\bTODO\b|\[\s*(insert|your|name|x+)[^\]]*\]|<\s*(insert|your)[^>]*>|\{\{\s*\w+\s*\}\}|\?\?\?)"
HALT = r"(?i)\b(wait for (my|the user's|user) (approval|confirmation)|ask (me|the user) before (each|every)|present (\w+ )?options and (stop|wait|halt)|do not proceed until)\b"


def lint(text):
    flags = []
    lines = text.splitlines()
    words = len(re.findall(r"\w+", text))
    long_form = words > 400
    for k, rx in dict(PARTS, **(LONG_PARTS if long_form else {})).items():
        if not re.search(rx, text):
            flags.append({"kind": "missing-part", "detail": k})
    for n, line in enumerate(lines, 1):
        for m in re.finditer(VAGUE, line):
            if not re.search(r"\d", line):
                flags.append({"kind": "vague-word", "line": n, "detail": m.group(0)})
                break
        if re.search(PLACEHOLDER, line):
            flags.append({"kind": "placeholder", "line": n, "detail": line.strip()[:80]})
        if re.search(r"\b(?:[A-Z]{3,}\s+){3,}[A-Z]{3,}\b", line):
            flags.append({"kind": "shouting", "line": n, "detail": line.strip()[:80]})
        if re.search(r"(?i)use your (best )?judg(e)?ment", line) and not re.search(r"(?i)default|if unsure|otherwise", line):
            flags.append({"kind": "judgment-without-default", "line": n})
        if re.search(HALT, line):
            flags.append({"kind": "halting-trap", "line": n, "detail": line.strip()[:80]})
    seen = {}
    for n, line in enumerate(lines, 1):
        key = re.sub(r"\W+", " ", line.lower()).strip()
        if len(key) > 40:
            if key in seen:
                flags.append({"kind": "repeated-line", "line": n, "detail": "same as line %d" % seen[key]})
            seen.setdefault(key, n)
    return {"words": words, "form": "long work order" if long_form else "short prompt", "flags": flags}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--strict", action="store_true", help="exit 1 when anything is flagged")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isfile(a.file):
        print("no such file: %s" % a.file, file=sys.stderr)
        return 2
    r = lint(read_text(a.file))
    r.update({"check": "prompt_lint", "label": "advisory heuristic, not a quality score", "count": len(r["flags"])})
    code = emit(r, a.json, ok=not r["flags"])
    return code if a.strict else 0


if __name__ == "__main__":
    sys.exit(main())
