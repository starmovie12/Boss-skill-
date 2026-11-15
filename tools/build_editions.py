#!/usr/bin/env python3
"""build_editions.py - compile the three BOSS editions from src/boss-skill (deterministic, byte-identical rebuilds).

E1 editions/e1-plugin/      Claude Code plugin (manifest + skills/boss/) and boss-skill.zip for upload on claude.ai.
E2 editions/e2-claude-free/ project-instructions.md (core), knowledge/ (mode-*.md, ref-*.md), paste/ (single-message
                            fallback files), all script-free.
E3 editions/e3-gemini-free/ gem-instructions.txt (from editions-src, <= 4,000 characters) and gem-knowledge/ (10 files).
Edition markers in src: <!--e1-->...<!--/e1--> is E1-only text; <!-- e23: text --> is the E2/E3 replacement.
Also writes .claude-plugin/marketplace.json at the repo root so the repo can be added as a plugin marketplace.
--check rebuilds into a temp folder and compares with the committed editions (exit 1 on any difference).
Exit 0 = built (or identical), 1 = budget breach or difference, 2 = usage error.
"""
import argparse
import filecmp
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "src", "boss-skill")
VERSION = "1.0.0"
E1_BLOCK = re.compile(r"<!--e1-->(.*?)<!--/e1-->", re.S)
E23 = re.compile(r"<!-- e23: ?(.*?) ?-->", re.S)
RENAME = {"modes/web.md": "mode-web.md", "modes/app.md": "mode-app.md", "modes/prompt.md": "mode-prompt.md",
          "modes/audit.md": "mode-audit.md", "references/placement.md": "ref-placement.md",
          "references/design-system.md": "ref-design-system.md", "references/quality-gates.md": "ref-quality-gates.md",
          "references/stacks.md": "ref-stacks.md", "references/india.md": "ref-india.md", "references/audit-checklists.md": "ref-audit-checklists.md",
          "references/domains/fintech-trading.md": "ref-fintech-trading.md"}


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def tidy(text):
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def for_e1(text):
    return tidy(E23.sub("", text.replace("<!--e1-->", "").replace("<!--/e1-->", "")))


def for_e23(text):
    text = E1_BLOCK.sub("", text)
    text = E23.sub(lambda m: m.group(1), text)
    for src, dst in sorted(RENAME.items(), key=lambda kv: -len(kv[0])):
        text = text.replace("`%s`" % src, "`%s`" % dst).replace(src, dst)
    text = re.sub(r"(?m)^---\n.*?\n---\n", "", text, count=1, flags=re.S) if text.startswith("---") else text
    text = text.replace("Load exactly one mode file per task", "Use exactly one mode file per task")
    return tidy(text)


def build_e1(out):
    skill = os.path.join(out, "e1-plugin", "skills", "boss")
    for d, dirs, files in os.walk(SRC):
        dirs[:] = sorted(x for x in dirs if x != "__pycache__")
        for f in sorted(files):
            p = os.path.join(d, f)
            rel = os.path.relpath(p, SRC)
            dst = os.path.join(skill, rel)
            if f.endswith(".md"):
                write(dst, for_e1(read(p)))
            elif f.endswith(".py"):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(p, dst)
    manifest = {"name": "boss", "version": VERSION,
                "description": "BOSS: build websites and apps with a fresh, domain-fitted design and verified placement, write agent work orders, and audit with verified citations.",
                "license": "MIT"}
    write(os.path.join(out, "e1-plugin", ".claude-plugin", "plugin.json"), json.dumps(manifest, indent=2) + "\n")
    zpath = os.path.join(out, "e1-plugin", "boss-skill.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for d, dirs, files in os.walk(skill):
            dirs.sort()
            for f in sorted(files):
                p = os.path.join(d, f)
                info = zipfile.ZipInfo(os.path.join("boss", os.path.relpath(p, skill)).replace(os.sep, "/"), date_time=(2026, 1, 1, 0, 0, 0))
                info.external_attr = (0o755 if f.endswith(".py") else 0o644) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                with open(p, "rb") as fh:
                    z.writestr(info, fh.read())


def build_e2(out):
    base = os.path.join(out, "e2-claude-free")
    core = for_e23(read(os.path.join(SRC, "SKILL.md")))
    core = core.replace("# BOSS\n", "# BOSS (Claude.ai edition: no scripts; every check is a manual checklist)\n", 1)
    write(os.path.join(base, "project-instructions.md"), core)
    for src, dst in RENAME.items():
        write(os.path.join(base, "knowledge", dst), for_e23(read(os.path.join(SRC, src))))
    for mode in ("web", "app", "prompt", "audit"):
        pack = "Paste this whole message, then describe your task.\n\n" + core + "\n---\n\n" + read(os.path.join(base, "knowledge", "mode-%s.md" % mode))
        write(os.path.join(base, "paste", "boss-%s.md" % mode), tidy(pack))
    write(os.path.join(base, "README.md"), tidy("""# BOSS for Claude.ai (free or paid), no scripts

Project route (best): create a Project, paste `project-instructions.md` into the project instructions, upload every
file in `knowledge/`, then chat normally or start with "Boss: WEB", "Boss: APP", "Boss: PROMPT" or "Boss: AUDIT".

Paste route (no Projects): open `paste/boss-<mode>.md` on GitHub, copy all, paste it as your first message, then
describe the task. When the mode names a reference (for example ref-placement.md), paste that file from `knowledge/` too.
"""))


def build_e3(out):
    base = os.path.join(out, "e3-gemini-free")
    write(os.path.join(base, "gem-instructions.txt"), read(os.path.join(REPO, "editions-src", "gem-instructions.txt")))
    k = os.path.join(base, "gem-knowledge")
    write(os.path.join(k, "core.md"), for_e23(read(os.path.join(SRC, "SKILL.md"))))
    for src, dst in RENAME.items():
        if dst in ("ref-stacks.md", "ref-fintech-trading.md", "ref-india.md"):
            continue
        write(os.path.join(k, dst), for_e23(read(os.path.join(SRC, src))))
    merged = "\n".join(for_e23(read(os.path.join(SRC, r))) for r in ("references/stacks.md", "references/domains/fintech-trading.md", "references/india.md"))
    for old in ("ref-stacks.md", "ref-fintech-trading.md", "ref-india.md"):
        merged = merged.replace(old, "ref-stacks-fintech-india.md")
    write(os.path.join(k, "ref-stacks-fintech-india.md"), tidy(merged))
    for p in sorted(os.listdir(k)):
        fp = os.path.join(k, p)
        t = read(fp)
        for old in ("ref-stacks.md", "ref-fintech-trading.md", "ref-india.md"):
            t = t.replace(old, "ref-stacks-fintech-india.md")
        write(fp, t)
    write(os.path.join(base, "README.md"), tidy("""# BOSS for Gemini (Gem), no scripts

1. Gemini app or gemini.google.com: Gems, New Gem (if your account shows "skills" instead of Gems, use the same text there).
2. Name it BOSS. Paste all of `gem-instructions.txt` into the instructions box.
3. Add the 10 files in `gem-knowledge/` as knowledge files. Save.
4. Test with the three prompts in docs/PHONE-TEST.md. Limits (instruction length, file count) are UNVERIFIED and may change.
"""))


def build(out):
    if os.path.isdir(out):
        shutil.rmtree(out)
    build_e1(out)
    build_e2(out)
    build_e3(out)
    write(os.path.join(REPO, ".claude-plugin", "marketplace.json"), json.dumps({
        "name": "boss-skill", "owner": {"name": "BOSS maintainers"},
        "plugins": [{"name": "boss", "source": "./editions/e1-plugin", "description": "BOSS skill: WEB, APP, PROMPT and AUDIT modes", "version": VERSION}]}, indent=2) + "\n")


def budgets(out):
    sys.path.insert(0, os.path.join(SRC, "scripts"))
    import token_budget
    res = []
    e2 = os.path.join(out, "e2-claude-free")
    res.append(("e2 core", token_budget.est(read(os.path.join(e2, "project-instructions.md"))), 2500))
    for f in sorted(os.listdir(os.path.join(e2, "knowledge"))):
        if f.startswith("mode-"):
            res.append(("e2 " + f, token_budget.est(read(os.path.join(e2, "knowledge", f))), 3500))
    gem = read(os.path.join(out, "e3-gemini-free", "gem-instructions.txt"))
    res.append(("e3 gem-instructions.txt (chars)", len(gem), 4000))
    res.append(("e3 knowledge files (count)", len(os.listdir(os.path.join(out, "e3-gemini-free", "gem-knowledge"))), 10))
    leaks = []
    for d in ("e2-claude-free", "e3-gemini-free"):
        for root, _, fs in os.walk(os.path.join(out, d)):
            for f in fs:
                t = read(os.path.join(root, f))
                if "scripts/" in t or "<!--" in t:
                    leaks.append(os.path.relpath(os.path.join(root, f), out))
    return res, leaks


def same_tree(a, b):
    diffs = []
    for root, _, fs in os.walk(a):
        for f in fs:
            pa = os.path.join(root, f)
            pb = os.path.join(b, os.path.relpath(pa, a))
            if not os.path.isfile(pb) or not filecmp.cmp(pa, pb, shallow=False):
                diffs.append(os.path.relpath(pa, a))
    for root, _, fs in os.walk(b):
        for f in fs:
            if not os.path.exists(os.path.join(a, os.path.relpath(os.path.join(root, f), b))):
                diffs.append(os.path.relpath(os.path.join(root, f), b))
    return diffs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=os.path.join(REPO, "editions"))
    ap.add_argument("--check", action="store_true", help="rebuild in a temp folder and compare with --out")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.check:
        with tempfile.TemporaryDirectory() as td:
            build(os.path.join(td, "e"))
            diffs = same_tree(os.path.join(td, "e"), a.out)
        res = {"check": "build_editions --check", "identical": not diffs, "differences": diffs, "pass": not diffs}
    else:
        build(a.out)
        rows, leaks = budgets(a.out)
        res = {"check": "build_editions", "out": a.out, "budgets": [{"item": n, "value": v, "limit": l, "pass": v <= l} for n, v, l in rows],
               "script_or_marker_leaks": leaks}
        res["pass"] = all(r["pass"] for r in res["budgets"]) and not leaks
    print(json.dumps(res, indent=1) if a.json else "\n".join("%s: %s" % kv for kv in res.items()))
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
