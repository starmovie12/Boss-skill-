"""Shared helpers for BOSS scripts. Standard library only."""
import json
import os
import sys

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".expo", ".next", ".turbo", ".cache", "coverage", "_boss", ".venv", "venv"}
TEXT_EXT = {".html", ".htm", ".css", ".scss", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".vue", ".svelte", ".astro",
            ".json", ".md", ".py", ".txt", ".yml", ".yaml", ".env", ".toml", ".xml", ".svg", ".sh", ".ini", ".cfg"}
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def iter_files(root, exts=None, skip_dirs=None, max_bytes=2_000_000):
    """Yield file paths under root, skipping vendor and build caches."""
    skip = SKIP_DIRS | set(skip_dirs or ())
    if os.path.isfile(root):
        yield root
        return
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in skip)
        for f in sorted(files):
            p = os.path.join(d, f)
            ext = os.path.splitext(f)[1].lower()
            if exts is not None and ext not in exts and f not in exts:
                continue
            try:
                if os.path.getsize(p) > max_bytes:
                    continue
            except OSError:
                continue
            yield p


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def emit(result, as_json, ok=None):
    """Print the result and return the process exit code (0 pass, 1 fail)."""
    if ok is None:
        ok = bool(result.get("pass", True))
    result.setdefault("pass", ok)
    if as_json:
        print(json.dumps(result, indent=1, ensure_ascii=False))
    else:
        print("[%s] %s" % ("PASS" if ok else "FAIL", result.get("check", "")))
        for k, v in result.items():
            if k in ("check", "pass"):
                continue
            if isinstance(v, list) and len(v) > 15:
                v = v[:15] + ["... %d more" % (len(v) - 15)]
            print("  %s: %s" % (k, v))
    return 0 if ok else 1


def die(msg, code=2):
    print(msg, file=sys.stderr)
    sys.exit(code)
