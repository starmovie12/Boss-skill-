"""Tests for the BOSS scripts. Run: python3 -m unittest discover -s tests -v"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(REPO, "src", "boss-skill", "scripts")
TOOLS = os.path.join(REPO, "tools")


def run(script, *args, folder=SCRIPTS):
    p = subprocess.run([sys.executable, os.path.join(folder, script), *args], capture_output=True, text=True, timeout=300)
    data = None
    if "--json" in args:
        try:
            data = json.loads(p.stdout)
        except ValueError:
            pass
    return p.returncode, data, p.stdout + p.stderr


def have_browser():
    node = shutil.which("node")
    if not node:
        return False
    r = subprocess.run([node, "-p", "require.resolve('playwright')"], capture_output=True, text=True)
    return r.returncode == 0


def write(d, rel, text):
    p = os.path.join(d, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    return p


CLEAN = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Clean</title><style>body{margin:0;font:16px sans-serif}main{padding:16px 16px 96px}button{min-height:48px;min-width:48px}
.bar{position:fixed;bottom:0;left:0;right:0;height:72px;display:flex;align-items:center;padding:0 16px;background:#eee}</style></head>
<body><main><h1>Shop</h1><p>Read the <a href="/terms">terms</a> first.</p><button>Details</button><div style="height:900px"></div>
<button>Last</button></main><div class="bar"><button>Place order</button></div></body></html>"""
BAD = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bad</title><style>body{margin:0}button{height:48px}</style></head><body>
<button style="position:absolute;top:10px;left:10px;width:120px">One</button><button style="position:absolute;top:20px;left:40px;width:120px">Two</button>
<button style="position:absolute;top:100px;left:420px;width:100px">Off</button><button style="width:20px;height:20px;padding:0">x</button></body></html>"""


class TestBudgetAndDoctor(unittest.TestCase):
    def test_token_budget_passes_on_skill(self):
        code, data, _ = run("token_budget.py", "--json")
        self.assertEqual(code, 0)
        self.assertLessEqual(data["total_tokens"], 27000)

    def test_doctor_passes_on_skill(self):
        code, data, out = run("boss_doctor.py", "--json")
        self.assertEqual(code, 0, out)

    def test_doctor_catches_color_literal_and_missing_path(self):
        with tempfile.TemporaryDirectory() as d:
            shutil.copytree(os.path.join(REPO, "src", "boss-skill"), os.path.join(d, "s"))
            with open(os.path.join(d, "s", "modes", "web.md"), "a") as fh:
                fh.write("\nUse #ff0000 and see `references/nope.md`.\n")
            code, data, _ = run("boss_doctor.py", "--root", os.path.join(d, "s"), "--skip-help", "--json")
            self.assertEqual(code, 1)
            joined = " ".join(data["problems"])
            self.assertIn("color literal", joined)
            self.assertIn("references/nope.md", joined)


class TestSecrets(unittest.TestCase):
    def test_finds_named_secret_and_respects_fixture_marker(self):
        with tempfile.TemporaryDirectory() as d:
            value = "q8" + "Zr4Lm2Vx9Tb7Kw3Hn6Pd1Fs5"
            write(d, "src/config.js", "const API_SECRET = '%s';\n" % value)
            write(d, "src/fixture.js", "const API_SECRET = 'FIXTURE_SECRET_not_a_real_key_0001';\n")
            code, data, _ = run("secrets_scan.py", "--root", d, "--json")
            self.assertEqual(code, 1)
            self.assertEqual([f["file"] for f in data["findings"]], [os.path.join("src", "config.js")])
            self.assertNotIn(value, json.dumps(data))

    def test_clean_project(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "index.html", "<p>hello</p>")
            self.assertEqual(run("secrets_scan.py", "--root", d, "--json")[0], 0)


class TestSeedAndFingerprint(unittest.TestCase):
    def test_seed_reproducible_and_has_no_colors(self):
        a = run("design_seed.py", "--seed", "42", "--json")[1]
        b = run("design_seed.py", "--seed", "42", "--json")[1]
        self.assertEqual(a["roll"], b["roll"])
        self.assertNotRegex(json.dumps(a), r"#[0-9a-fA-F]{6}")

    def test_fingerprint_too_close_then_distinct(self):
        with tempfile.TemporaryDirectory() as d:
            hist = os.path.join(d, "hist.json")
            css1 = ":root{--bg:#f7f5ef;--accent:#1f6f5c}h1{font-family:'Fraunces',serif}body{font-family:'Work Sans',sans-serif}"
            page1 = "<body><header></header><section class='hero'></section><section class='features'></section><footer></footer></body>"
            write(d, "p1/index.html", page1); write(d, "p1/style.css", css1)
            write(d, "p2/index.html", page1.replace("features", "features")); write(d, "p2/style.css", css1.replace("1f6f5c", "1f705d"))
            css3 = ":root{--bg:#101318;--accent:#e0663a}h1{font-family:'Archivo Black',sans-serif}body{font-family:'IBM Plex Sans',sans-serif}"
            page3 = "<body><nav></nav><main><aside class='sidebar'></aside><table></table><form></form></main></body>"
            write(d, "p3/index.html", page3); write(d, "p3/style.css", css3)
            self.assertEqual(run("design_fingerprint.py", "--root", os.path.join(d, "p1"), "--history", hist, "--append", "--json")[0], 0)
            code, data, _ = run("design_fingerprint.py", "--root", os.path.join(d, "p2"), "--history", hist, "--json")
            self.assertEqual(code, 1, data)
            code, data, _ = run("design_fingerprint.py", "--root", os.path.join(d, "p3"), "--history", hist, "--json")
            self.assertEqual(code, 0, data)
            self.assertEqual(data["comparisons"][0]["axes_differing"], 3)


@unittest.skipUnless(have_browser(), "node + Playwright not available")
class TestPlacement(unittest.TestCase):
    def test_clean_page_passes(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "index.html", CLEAN)
            plan = write(d, "plan.md", 'primary: "Place order" zone=bottom\n')
            code, data, out = run("placement_check.py", "--site", d, "--plan", plan, "--json")
            self.assertEqual(code, 0, out)

    def test_planted_defects_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "index.html", BAD)
            code, data, _ = run("placement_check.py", "--site", d, "--json")
            self.assertEqual(code, 1)
            hits = " ".join(data["hits"])
            self.assertIn("overlap", hits)
            self.assertIn("outside viewport", hits)
            self.assertIn("small target", hits)
            self.assertIn("horizontal scroll", hits)


class TestStaticPlacementFallback(unittest.TestCase):
    def test_static_only_flags_unlabeled_button(self):
        with tempfile.TemporaryDirectory() as d:
            p = write(d, "index.html", "<html><head></head><body><button></button><img src='a.png'></body></html>")
            code, data, _ = run("placement_check.py", "--url", p, "--static-only", "--json")
            self.assertEqual(code, 1)
            self.assertEqual(data["mode"], "static-only")


class TestVerify(unittest.TestCase):
    def test_static_site_gates(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "index.html", CLEAN.replace("Details", "Details <!-- TODO later -->"))
            code, data, _ = run("boss_verify.py", "--root", d, "--json")
            self.assertEqual(code, 1)
            st = {r["check"]: r["status"] for r in data["results"]}
            self.assertEqual(st["design_gate"], "FAIL")
            self.assertEqual(st["substance"], "FAIL")
            self.assertEqual(st["js_budget"], "PASS")

    def test_palette_recomputes_ratios(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "index.html", "<p>x</p>")
            write(d, "_boss/tokens.md", "| body | #111111 | #ffffff | 18.88:1 | 4.5 |\n| muted | #999999 | #ffffff | 4.6:1 | 4.5 |\n")
            data = run("boss_verify.py", "--root", d, "--no-build", "--json")[1]
            pal = next(r for r in data["results"] if r["check"] == "palette")
            self.assertEqual(pal["status"], "FAIL")
            self.assertIn("#999999", " ".join(pal["detail"]))


class TestAuditReport(unittest.TestCase):
    def test_verifies_snippets_and_flags_fabrication(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "app/server.js", "const a = 1;\napp.get('/u/:id', (req, res) => {\n  res.json(db.users[req.params.id]);\n});\n")
            good = {"id": "SEC-001", "title": "No ownership check", "class": "security", "severity": "high", "location": "app/server.js:3",
                    "evidence": "res.json(db.users[req.params.id]);", "reproduction": "GET /u/2 as user 1", "impact": "reads other users",
                    "fix": "check req.user.id", "confidence": "INFERRED"}
            bad = dict(good, id="SEC-002", location="app/server.js:1", evidence="eval(req.body)")
            f = write(d, "findings.json", json.dumps({"findings": [good, bad], "coverage": [{"class": "privacy", "checked": False, "reason": "no data flows in scope"}]}))
            code, data, _ = run("audit_report.py", "--findings", f, "--root", d, "--out", os.path.join(d, "report.md"), "--json")
            self.assertEqual(code, 1)
            st = {c["id"]: c["citation"] for c in data["citations"]}
            self.assertTrue(st["SEC-001"].startswith("verified"))
            self.assertEqual(st["SEC-002"], "not-found")
            with open(os.path.join(d, "report.md")) as fh:
                report = fh.read()
            self.assertIn("## Not checked", report)
            self.assertIn("privacy", report)


class TestPromptLint(unittest.TestCase):
    def test_flags_vague_placeholder_and_halting(self):
        with tempfile.TemporaryDirectory() as d:
            p = write(d, "p.md", "Make it fast and modern.\nName: [insert name]\nWait for my approval before each step.\n")
            data = run("prompt_lint.py", p, "--json")[1]
            kinds = {f["kind"] for f in data["flags"]}
            self.assertTrue({"vague-word", "placeholder", "halting-trap", "missing-part"} <= kinds)
            self.assertEqual(run("prompt_lint.py", p, "--strict", "--json")[0], 1)


class TestForgeTools(unittest.TestCase):
    def test_isolation_check_catches_planted_token(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "shipped/a.md", "a GlassIsland navigation\n")
            code = subprocess.run([sys.executable, os.path.join(TOOLS, "isolation_check.py"), "--roots", os.path.join(d, "shipped"),
                                   "--src", "/nonexistent", "--json"], capture_output=True, text=True).returncode
            self.assertEqual(code, 1)

    def test_build_editions_reproducible(self):
        p = subprocess.run([sys.executable, os.path.join(TOOLS, "build_editions.py"), "--check", "--json"], capture_output=True, text=True, timeout=120)
        self.assertEqual(p.returncode, 0, p.stdout[-800:])

    def test_ledger_check_runs(self):
        p = subprocess.run([sys.executable, os.path.join(TOOLS, "ledger_check.py"), "--json"], capture_output=True, text=True, timeout=120)
        self.assertEqual(p.returncode, 0, p.stdout[-800:])


if __name__ == "__main__":
    unittest.main()
