#!/usr/bin/env python3
"""audit_report.py - validate findings.json, verify every quoted snippet at its cited location, render report.md.

findings.json: a list of findings (or {"scope": {...}, "coverage": [...], "findings": [...]}). Each finding needs:
id, title, class, severity, location, evidence, reproduction, impact, fix, confidence; false_positive_notes optional.
location "path:line" is checked against --root: the evidence (whitespace-normalized, first 10 lines) must occur in that
file within 5 lines of the cited line. Other locations (URLs, selectors, spec sections) are marked not-file.
coverage rows: {"class": ..., "method": ..., "covered": ..., "checked": true|false, "result": ..., "reason": ...}.
Exit 0 = all findings valid and all file citations verified, 1 = problems, 2 = usage error.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import emit, read_text  # noqa: E402

REQUIRED = ["id", "title", "class", "severity", "location", "evidence", "reproduction", "impact", "fix", "confidence"]
SEVERITY = ["critical", "high", "medium", "low", "info"]
CLASSES = ["security", "accessibility", "performance", "seo", "correctness", "dependencies", "privacy", "ux", "code-health", "spec"]
CONF = ["VERIFIED", "INFERRED", "UNVERIFIED"]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def verify_citation(root, loc, evidence):
    m = re.match(r"^(.+?):(\d+)(?:-\d+)?$", loc.strip())
    if not m or re.match(r"https?://", loc):
        return "not-file", ""
    path, line = os.path.join(root, m.group(1)), int(m.group(2))
    if not os.path.isfile(path):
        return "missing-file", m.group(1)
    lines = read_text(path).splitlines()
    snippet = norm("\n".join(evidence.splitlines()[:10]))
    if not snippet:
        return "empty-evidence", ""
    lo, hi = max(0, line - 6), min(len(lines), line + 5 + len(evidence.splitlines()))
    window = norm("\n".join(lines[lo:hi]))
    if snippet in window:
        return "verified", ""
    first = norm(evidence.splitlines()[0]) if evidence.splitlines() else ""
    if first and any(first in norm(l) for l in lines[lo:hi]):
        return "verified-first-line", ""
    return "not-found", "snippet not within 5 lines of %s:%d" % (m.group(1), line)


def render(doc, findings, checks):
    scope = doc.get("scope", {}) if isinstance(doc, dict) else {}
    cov = doc.get("coverage", []) if isinstance(doc, dict) else []
    counts = {s: sum(1 for f in findings if str(f.get("severity", "")).lower() == s) for s in SEVERITY}
    order = sorted(findings, key=lambda f: (SEVERITY.index(str(f.get("severity", "info")).lower()) if str(f.get("severity", "")).lower() in SEVERITY else 9, str(f.get("class")), str(f.get("id"))))
    out = ["# Audit report", ""]
    for k in ("target", "commit", "date", "in_scope", "out_of_scope", "method", "authorization"):
        if scope.get(k):
            out.append("- **%s**: %s" % (k.replace("_", " "), scope[k]))
    out += ["", "## Executive summary", "",
            "Findings: " + ", ".join("%s %d" % (s, counts[s]) for s in SEVERITY) + ".",
            "Citations verified: %d of %d file citations." % (sum(1 for c in checks if c["citation"].startswith("verified")), sum(1 for c in checks if c["citation"] != "not-file"))]
    top = [f for f in order if str(f.get("severity", "")).lower() in ("critical", "high")][:3] or order[:3]
    if top:
        out.append("Fix first: " + "; ".join("%s %s" % (f.get("id"), f.get("title")) for f in top) + ".")
    if cov:
        out += ["", "## Coverage", "", "| class | method | covered | checked | result |", "|---|---|---|---|---|"]
        for c in cov:
            out.append("| %s | %s | %s | %s | %s |" % (c.get("class"), c.get("method", ""), c.get("covered", ""), "yes" if c.get("checked") else "no", c.get("result", c.get("reason", ""))))
    out += ["", "## Findings", ""]
    for f in order:
        c = next((x for x in checks if x["id"] == f.get("id")), {})
        out += ["### %s %s (%s, %s, confidence %s)" % (f.get("id"), f.get("title"), f.get("severity"), f.get("class"), f.get("confidence")),
                "", "- Location: `%s` (citation: %s)" % (f.get("location"), c.get("citation", "?")),
                "- Evidence:", "", "```", str(f.get("evidence", "")).rstrip(), "```", "",
                "- Reproduction: %s" % f.get("reproduction"), "- Impact: %s" % f.get("impact"), "- Fix: %s" % f.get("fix")]
        if f.get("false_positive_notes"):
            out.append("- False-positive notes: %s" % f["false_positive_notes"])
        out.append("")
    nc = [c for c in cov if not c.get("checked")]
    out += ["## Not checked", ""] + (["- %s: %s" % (c.get("class"), c.get("reason", "no reason given")) for c in nc] or ["- (coverage list empty or every class checked)"])
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--findings", required=True)
    ap.add_argument("--root", default=".", help="folder that file citations are relative to")
    ap.add_argument("--out", help="write the rendered report here")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        doc = json.loads(read_text(a.findings))
    except (OSError, ValueError) as e:
        print("cannot read findings: %s" % e, file=sys.stderr)
        return 2
    findings = doc.get("findings", []) if isinstance(doc, dict) else doc
    problems, checks, ids = [], [], set()
    for i, f in enumerate(findings):
        fid = f.get("id") or "#%d" % i
        miss = [k for k in REQUIRED if not str(f.get(k, "")).strip()]
        if miss:
            problems.append("%s missing fields: %s" % (fid, ", ".join(miss)))
        if fid in ids:
            problems.append("%s duplicate id" % fid)
        ids.add(fid)
        if str(f.get("severity", "")).lower() not in SEVERITY:
            problems.append("%s severity not one of %s" % (fid, SEVERITY))
        if str(f.get("class", "")).lower() not in CLASSES:
            problems.append("%s class not one of %s" % (fid, CLASSES))
        if str(f.get("confidence", "")).upper() not in CONF:
            problems.append("%s confidence not one of %s" % (fid, CONF))
        status, why = verify_citation(a.root, str(f.get("location", "")), str(f.get("evidence", "")))
        checks.append({"id": fid, "citation": status, "detail": why})
        if status in ("not-found", "missing-file", "empty-evidence"):
            problems.append("%s citation %s %s" % (fid, status, why))
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(render(doc, findings, checks))
    return emit({"check": "audit_report", "findings": len(findings), "citations": checks, "problems": problems,
                 "report": a.out}, a.json, ok=not problems)


if __name__ == "__main__":
    sys.exit(main())
