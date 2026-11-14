#!/usr/bin/env python3
"""secrets_scan.py - find likely secrets in a project (generic: key names, known prefixes, entropy).

Reports file:line with the value redacted. Allowlist: lines containing FIXTURE_SECRET or "boss-allow-secret",
and paths listed (one glob per line) in a .boss-secrets-allow file at the root. Skips node_modules, .git, build caches.
Exit 0 = nothing found, 1 = findings, 2 = usage error.
"""
import argparse
import fnmatch
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import TEXT_EXT, emit, iter_files, read_text  # noqa: E402

PREFIXES = [
    (r"AKIA[0-9A-Z]{16}", "cloud access key id"),
    (r"(?:sk|rk)_(?:live|test)_[0-9A-Za-z]{16,}", "payment secret key"),
    (r"sk-[A-Za-z0-9_-]{20,}", "API secret key"),
    (r"gh[pousr]_[A-Za-z0-9]{30,}", "git host token"),
    (r"xox[abpr]-[A-Za-z0-9-]{10,}", "chat bot token"),
    (r"AIza[0-9A-Za-z_-]{35}", "browser API key (often public, check restrictions)"),
    (r"-----BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY-----", "private key"),
    (r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}", "JSON web token"),
]
NAME_RE = re.compile(r"""(?i)\b([A-Z0-9_]*(?:SECRET|TOKEN|PASSWORD|PASSWD|API_?KEY|PRIVATE_?KEY|ACCESS_?KEY|AUTH)[A-Z0-9_]*)\b\s*[:=]\s*["']?([^"'\s,;]{8,})""")
PLACEHOLDER = re.compile(r"(?i)^(x+|\*+|changeme|your[_-]?|example|dummy|test|placeholder|<|\$\{|process\.env|os\.environ|import\.meta)")


def entropy(s):
    if not s:
        return 0.0
    freq = {c: s.count(c) for c in set(s)}
    return -sum(n / len(s) * math.log2(n / len(s)) for n in freq.values())


def redact(v):
    return v[:4] + "..." + ("%d chars" % len(v))


def load_allow(root):
    p = os.path.join(root, ".boss-secrets-allow")
    if os.path.isfile(p):
        return [l.strip() for l in read_text(p).splitlines() if l.strip() and not l.startswith("#")]
    return []


def scan(root):
    allow = load_allow(root)
    findings = []
    for p in iter_files(root, TEXT_EXT | {".env", ".env.local", ".env.production"}):
        rel = os.path.relpath(p, root) if os.path.isdir(root) else os.path.basename(p)
        if any(fnmatch.fnmatch(rel, g) for g in allow):
            continue
        name = os.path.basename(p)
        if name.endswith((".lock", "-lock.json")) or name == "package-lock.json":
            continue
        for n, line in enumerate(read_text(p).splitlines(), 1):
            if "FIXTURE_SECRET" in line or "boss-allow-secret" in line or len(line) > 2000:
                continue
            for pat, kind in PREFIXES:
                m = re.search(pat, line)
                if m:
                    findings.append({"file": rel, "line": n, "kind": kind, "value": redact(m.group(0))})
                    break
            else:
                m = NAME_RE.search(line)
                if m and not PLACEHOLDER.match(m.group(2)) and entropy(m.group(2)) >= 3.0:
                    findings.append({"file": rel, "line": n, "kind": "secret-named value (%s)" % m.group(1),
                                     "value": redact(m.group(2))})
        if name.startswith(".env") and name not in (".env.example", ".env.sample") and os.path.getsize(p) > 0:
            findings.append({"file": rel, "line": 1, "kind": "environment file present (should not be committed or shipped)", "value": ""})
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, help="project folder or single file")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.exists(a.root):
        print("no such path: %s" % a.root, file=sys.stderr)
        return 2
    f = scan(a.root)
    return emit({"check": "secrets_scan", "root": a.root, "findings": f, "count": len(f)}, a.json, ok=not f)


if __name__ == "__main__":
    sys.exit(main())
