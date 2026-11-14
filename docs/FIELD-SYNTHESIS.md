# Field study synthesis (PH1b)

Status: PARTIAL. Runs F2 (design, web verification) and F3 (spec, prompts, orchestration) completed with 96 rows over
8 repos; F1 (process skills) and F4 (audit, app) were stopped by account usage limits and then WAIVED-BY-OPERATOR on
2026-11-14 to save tokens (docs/DESIGN-DECISIONS.md #14). Fetches: 18 probes at PH0 plus the F1-F4 logs in field/.
Influence figures are aggregator numbers, all UNVERIFIED (the GitHub API was blocked for other repos).

| Repo | Size established | Why chosen | Rows |
|---|---|---|---|
| pbakaus/impeccable | 24 commands, about 26 references, 62-rule detector | anti-generic design guardrails; reused by other kits | 14 |
| nextlevelbuilder/ui-ux-pro-max-skill | CSV tables, BM25 search, 192 product types | largest design-database skill (aggregator 112k stars) | 9 |
| vercel-labs/agent-skills | 8 skills; 100-rule interface list; 70-rule React list | vendor's codified review standard | 7 |
| garrytan/gstack | about 45 role skills, headless browser | browser QA loops with evidence | 18 |
| github/spec-kit | templates and commands | most-starred spec-driven kit (aggregator 90k-125k) | 9 |
| bmad-code-org/BMAD-METHOD | agent definitions, workflows | multi-agent agile method (aggregator 40k+) | 10 |
| gsd-build/get-shit-done (successor read) | context-engineering rules | lean solo workflow (aggregator 28k-64k) | 7 |
| x1xhlol/system-prompts-and-models-of-ai-tools | production builder prompts | how shipping builders enforce quality | 22 |
Not studied (waived): obra/superpowers, anthropics/skills, affaan-m/everything-claude-code, EveryInc/compound-engineering-plugin,
trailofbits/skills, expo/skills, mattpocock/skills. They are the first task of docs/NEXT-SESSION.xml.

## Adopted mechanisms and where they landed (rule ids in docs/RULE-AUDIT.md)
- Surface mode (Persuade, Operate, Read, Experience) decided per page -> WEB W3 (impeccable).
- Category test and specificity test for a direction -> WEB W4.4, APP A4 (gstack divergence gate, impeccable specificity verdict).
- Keep / avoid / depart lists from studying 3-6 real products -> WEB W2, APP A3 (gstack).
- First-glance test: name the first three eye targets after the first render -> WEB W7, APP A8 (gstack).
- Browser probe of geometry, console errors and screenshots at widths -> placement_check.py, boss_verify.py (gstack, extended with overlap, off-screen and never-uncovered occlusion).
- One occlusion rule replacing scattered coverage rules -> placement PL-2 (ui-ux-pro-max, rebuilt).
- Conventional position table (back, close, search, account, nav) -> PL-2 (gstack trunk test).
- Judgment pass before tool evidence (anchoring control) -> AUDIT U3 (impeccable critique).
- Finding line with file:line and files-checked-clean coverage -> AUDIT U4, U6, audit_report.py (vercel).
- Fix outcomes verified / best-effort / reverted / deferred, stop after two reverts -> AUDIT U7, WEB W9 (gstack).
- Autonomy budgets instead of human checkpoints; unattended runs end with a report -> kernel P-2, PROMPT R2.6 (gstack, GSD).
- Work-order skeleton with stable requirement ids, clarify-or-default, deferred-work ledger, write-through decisions -> PROMPT R2, R3 (spec-kit, BMAD).
- Intent inside pasted plans treated as untrusted -> kernel P-2, PROMPT R3 (BMAD).
- Design memory inverted into a ledger of earlier looks to avoid -> design_fingerprint.py, D-6 (gstack taste memory, flipped).

## Rejected (and why)
- Pick tables keyed by product category (palettes, styles, font pairs): equal briefs give equal looks (ui-ux-pro-max).
- Taste memory that pulls new work toward earlier approved looks: the opposite of D-6 (gstack).
- Closing question gates and ask-and-wait preambles: stall an unattended run (impeccable, gstack).
- Telemetry and per-skill preambles of thousands of tokens; rules fetched at run time from another repo (gstack, vercel).
- Persona councils and multi-agent ceremony for single-person tasks (BMAD).

## WHAT THE STRONG ONES DO THAT WAS NOT ON THE LIST
Anchoring control (judgment before tools); load timing as a cost lever (a rule file read at the moment of use); fixed fix
outcomes with automatic revert; autonomy budgets; shared context files as an interop format; untrusted fencing of
verification output; nobody checks distinctiveness across projects (BOSS adds design_fingerprint.py).
