# Phone test (manual, per edition)

The same three prompts for every edition. Expected markers are what a working install visibly does.

| # | Prompt | Expected markers |
|---|---|---|
| T1 | "Make a landing page for a small Hindi-and-English tiffin service in Pune." | first line names the size (M); an acceptance list; a domain study with keep/avoid/depart; three directions with one chosen; a layout plan with one primary action; Hindi text with lang="hi" and a font-coverage note; no lorem ipsum; a phone deploy path; a report with verified / inferred / not done |
| T2 | "Write a prompt for Claude Code to build a habit-tracker app, I will be away for hours." | a ten-part work order with stop rules and measurable checks; no "wait for approval"; five-line note with test inputs |
| T3 | "Audit this code: app.get('/u/:id', (req,res)=>res.json(db[req.params.id]))" | scope line; a finding with class security, severity high, file:line or snippet, reproduction, fix, confidence INFERRED; a "Not checked" section |

## E1 Claude Code on the web
1. Install per README E1; start a new session on the repo.
2. Ask T1; confirm `_boss/` files appear before any UI file is written.
3. Confirm the session runs `boss_verify.py` and pastes its PASS/FAIL lines.
4. Ask T2 and T3; compare with the markers.
5. Any missing marker: open an issue with the transcript link.

## E2 Claude.ai
1. Install per README E2 (Project or paste route).
2. Ask T1; confirm the markers (scripts are replaced by manual checklists; renders are labeled UNVERIFIED).
3. Ask T2; confirm no halting instruction appears in the work order.
4. Ask T3; confirm the finding schema.
5. Note any marker that is missing.

## E3 Gemini
1. Install per README E3.
2. Ask "Boss: WEB" plus T1; confirm the design steps happen before code.
3. Ask T2 and T3.
4. Confirm the answer cites knowledge files (mode-web.md, ref-placement.md) when it uses them.
5. Record the instruction-length and file-count limits your account actually shows (they are UNVERIFIED in docs/FRESH-FACTS.md).
