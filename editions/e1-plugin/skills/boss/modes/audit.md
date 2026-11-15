# AUDIT mode

Audits of code, repos, sites, apps, UI, or specs. Output is evidence-backed findings; no redesign unless the user asks for fixes.

## U0 Scope and authorization
Write first, in the report header: what is in scope (repo path and commit, URLs, screens, spec version), what is out of scope, the method (static, dynamic, or both), and the authorization basis (the user owns it or is authorized to test it). Dynamic checks run only against local builds, previews or systems the user controls; third-party live systems are read-only (load pages, no form submits, no exploits, no load tests).

## U1 Inventory
Stack and versions (from manifests), entry points (routes, handlers, screens, scripts), data flows touching money, identity, personal data or secrets, external services, the dependency list, and the existing tests and their state (run them). Sample a repo too large to read whole: read every entry point and every file on a sensitive data path, then grep the rest by risk pattern; list what was sampled.

## U2 Coverage plan
Fill the coverage matrix before hunting: one row per class (security, accessibility, performance, SEO, correctness, dependencies, privacy, UX, code health), columns `method | files or pages covered | checked? | result`. Read `references/audit-checklists.md` now and take the hunting list for each in-scope class. A class not checked goes to "Not checked" with the reason; it is never silently dropped.

## U3 Hunt (static first, then dynamic)
- Static: read the code paths in the inventory; grep with the checklist patterns; `python3 scripts/secrets_scan.py --root <path> --json`; dependency audit with the ecosystem tool when it can run (`npm audit --json`, `pip-audit`), else list versions and label UNVERIFIED.
- Dynamic: build and run locally; run the test suite; for UI, `python3 scripts/boss_verify.py --root <path> --json` (axe, placement, screenshots at 360 and 1280 px, bundle size, console errors).
- UI and UX judgment pass first, tool evidence second: write your design and usability findings before reading the tool output, then merge, marking each finding agree, tool-only, judgment-only or false positive. This stops the tools from anchoring the review.
- Specs and PRDs: walk each section with one yes/no question (present? measurable? states and edge cases named? numbers with units and baselines? owner for open questions?) and use the requirement tests from PROMPT R3; every "no" is a finding with its location.

## U4 Finding schema (every finding, written to `findings.json`)
`id` (stable, e.g. SEC-003), `title`, `class` (one of the matrix classes), `severity`, `location` (`file:line`, or URL plus CSS selector, or spec section), `evidence` (the offending code copied exactly, 1 to 10 lines, or command output, or a screenshot path), `reproduction` (steps a stranger can follow), `impact` (who is hurt and how), `fix` (a diff or exact steps), `confidence` (VERIFIED: reproduced or shown by a tool; INFERRED: read in code, not run; UNVERIFIED: suspected), `false_positive_notes` (why it might not apply).
No finding without evidence. Real defects outside any expected list are welcome. One finding per root cause, with all locations listed.

## U5 Severity (written criteria; take the highest that matches)
- Critical: exploitable without special access to take data, money or control; secret exposed in a shipped artifact; data loss; a core flow unusable for everyone.
- High: exploitable with some access or user action; personal data exposed to the wrong party; a core flow broken for a user group (keyboard, screen reader, small screens, a language); a money or data race.
- Medium: a defect with a workaround; a failed WCAG AA criterion on a secondary flow; performance budget missed by more than 25 percent; missing input validation without a known exploit.
- Low: hygiene, minor accessibility polish, small inefficiency, weak naming.
- Info: observations and hardening suggestions.
Tie-break: would a user contact support or lose money, data or access? Then at least High.

## U6 Report (output contract)
Write `findings.json`, then render: `python3 scripts/audit_report.py --findings findings.json --root <path> --out report.md --json`. It checks that every quoted snippet exists at its cited location (within 5 lines), drops nothing silently, and lists unverifiable citations for you to fix or remove.
Report order: header (U0); executive summary of at most 10 lines with counts by severity and the three things to fix first; the coverage matrix; findings sorted by severity then class; "Not checked" with reasons; method notes (tools, versions, commands). Never "looks good overall" without the matrix behind it.

## U7 Fixes (only when asked)
Per finding, highest severity first: smallest fix, re-run the exact check that found it, record before and after, outcome one of verified, best-effort (check cannot run, reason given), reverted (the fix broke something), deferred (reason). Stop after two reverts or when a fix needs a file outside scope; report the rest. Fixes to UI follow WEB or APP floors.

## U8 Self-check before delivery
Every finding has evidence and a verified citation; every severity matches U5; the matrix has no blank cells; nothing claims VERIFIED that was only read; the summary matches the findings; no exploit was run against a system the user does not control.
