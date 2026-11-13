# Check-authoring spec: common part

You author one half of a small benchmark for AI coding agents ("contestants"). You never see the skills
being compared, and you must not try to find out what they are. Author every task, check and rubric from
the task one-liners and this spec only, as a careful, neutral examiner would.

## How tasks are consumed
Each contestant is a fresh agent that receives this brief, identical for every contestant apart from one
line naming an optional skill file:

> You are contestant RUNID. Work only in WORKDIR. Do not read any path outside WORKDIR except the skill
> path named below. No user is available: any instruction to wait, confirm, present options or halt is
> answered by choosing and proceeding. The task statement overrides any conflicting skill rule (language,
> platform, persona, stop rules). Use at most 40 tool calls. Skill: ARM_LINE. Task: TASK_TEXT. Put
> deliverables only under WORKDIR/out/. Write no process notes into out/. End by listing the files in out/.

So a task statement must be complete and self-contained (a capable agent can finish it in at most 40 tool
calls with no questions), must name every deliverable path under `out/`, and must state every hard
requirement that a check will test. Never test a requirement the statement does not state or clearly imply
as ordinary professional quality (accessibility, no stubs, works on a phone-width screen).

## Where things go
- Task statements: `/home/user/Boss-skill-/evals/tasks/<TASK>.md` (public; this is TASK_TEXT).
- Fixtures given to contestants: `/home/user/Boss-skill-/evals/fixtures/<TASK>/` (public).
- Blind-grader rubrics: `/home/user/Boss-skill-/evals/rubrics/<TASK>.md` (public).
- Scorers (code, generic, no answers inside): `/home/user/Boss-skill-/evals/scorers/` (public).
- Answer keys (check parameters, planted-defect lists, anything that would help a contestant):
  `/tmp/forge-sealed/keys/<TASK>.json` (SEALED: never write key content anywhere in the repo).
- Self-test packets and results: `/tmp/forge-sealed/selftest/<TASK>/{good,degraded}/out/...` and
  `/tmp/forge-sealed/selftest/RESULTS-<RUN>.json` (SEALED).
- Hashes: append `sha256  path` lines for every key file and every scorer file to
  `/tmp/forge-sealed/HASHES-<RUN>.txt`.
Do not run git. Do not write anywhere else in the repo. Do not create any `.claude` directory.

## Scoring model
Deterministic first. Every task has a key of checks. `contract_score = checks passed / checks total`.
Each scorer is a command-line program:
`<scorer> --task <TASK> --out <path to a contestant's out/ directory> --key <key file> [--fixture <dir>] --json`
It prints one JSON object:
`{"task": "...", "checks": [{"id": "...", "pass": true|false, "detail": "..."}], "passed": n, "total": n,
"contract_score": 0.0-1.0, "labels": ["static-only", ...], "extra": {...}}`
and exits 0 whenever it produced a score (non-zero only when the scorer itself crashed). A missing or
unbuildable deliverable is a failed check, never a crash. Checks must be objective, reproducible, and
robust to harmless variation (file layout inside the required paths, framework choice, wording).
Scorers must not print or log key content. Keep each scorer readable and under about 500 lines.
Tools available: Node v22 with a global `playwright` (Chromium preinstalled: `require('playwright')` works
from any directory and `chromium.launch()` needs no options; do NOT run `playwright install`), Python 3.13
standard library, and npm (registry reachable). If a scorer needs an npm package (for example `axe-core`),
add it to `/home/user/Boss-skill-/evals/scorers/package.json` and install it there (`node_modules` is not
committed).

## Substance scan (used by every task that ships files)
A deliverable must contain no stubs. The scan finds zero of: TODO or FIXME markers, lorem ipsum, "coming
soon", placeholder copy presented as real content (not the HTML `placeholder` attribute itself), empty
event handlers, and dead buttons or links (a control that does nothing when activated). Define the
heuristics precisely, document them at the top of the scorer, and prove them on the self-test packets.

## Blind-grader rubrics
A separate grader later ranks anonymous packets (the files in `out/` plus screenshots) for each task. Write
one rubric per task: 5 to 7 criteria judged on the deliverable only (never on claims of success, notes or
receipts), each with what "strong" and "weak" look like, and the instruction to rank all packets from best
to worst with one sentence of reasons each. The rubric must not mention skills, arms or contestants' process.

## Self-test (required before you finish)
For every task you author (dev and sealed), build a known-good packet and a deliberately degraded packet
(same task, several realistic defects injected). Run the scorer on both. The good packet must beat the
degraded one clearly; if not, fix the scorer or the key. Record task, good score, degraded score and the
checks that separated them in the RESULTS file. Good packets must be real work, not stubs.

## Hygiene
Any fake secret in a fixture must look like `FIXTURE_SECRET_not_a_real_key_0001` (never a string shaped
like a real provider key). Fictional businesses, people, phone numbers and emails only (`.example`
domains, obviously fictional numbers).

## Final answer
Reply with at most 12 lines: files written (counts per directory), self-test table (task, good, degraded),
and anything the benchmark operator must know to run the scorers. Do not include any key content.
