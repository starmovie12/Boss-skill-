# F2 digest: design quality, anti-generic design, web verification, QA (retrieved 2026-11-13)
Gap tags (docs/GAPS.md): WEB-VERIFY no measured checks; WEB-RESP responsive; WEB-IA content/IA; WEB-STACK stack lock; WEB-STUB stub
scan; PROMPT-STOP stop/scope rules; AUDIT-SCHEMA one schema; AUDIT-CITE citation, confidence, not-checked, re-verify; VAR-HOUSE fixed looks;
VAR-DIVERGE domain study/divergence/cross-project; VER-SELF self-graded; VER-GEOM geometry; PLACE-OCC/PLACE-POS; COST-PROSE; COST-HALT.

## 1. pbakaus/impeccable (README, SKILL.md, reference/craft-floor.md, reference/critique.md)
One frontend-design skill (24 commands, about 26 on-demand references) plus a 62-rule deterministic tell detector shipped as CLI, hook and extension.
Influential because it names the recurring tells of generated UI and checks them with a tool; gstack reuses its modes, rules and engine.
- [WEB,APP | VAR-HOUSE] Mode first. Write the surface's mode: Persuade (visitor decides and acts), Operate (completes a task), Read
  (understands), Experience (is inside the work). Pick from the surface requested, not the industry; mixed pages classify per section.
  Persuade/Experience commit to one distinctive idea; Operate/Read spend effort on precision and known patterns.
- [CORE | VAR-HOUSE] Refine vs redesign, decided before editing. Refine keeps identity, copy and everything out of scope. Redesign keeps
  content and function, treats the old look as the thing to move away from, rewrites the design file. User-pinned fonts, colors or
  eras outrank every anti-generic rule. Never invent or replace factual copy.
- [WEB,APP | VAR-DIVERGE] Free-axis test for each conspicuous choice (page scaffold, card grid, gradient text, glass, thick side
  stripe, emoji icon, light vs dark): did the brief fix this axis? If not, write one line on why it fits this product; with no
  reason, rewrite the element instead of softening it. Light or dark comes from the use scene (who, where, what light).
- [WEB | WEB-VERIFY, VER-SELF] Build-time floor, loaded only when editing UI: render once per width, then check together on computed
  styles: body contrast >=4.5:1 (large >=3:1; secondary text on colored ground tinted, not gray), measure 65-75ch, more space above
  a heading than below, hover/disabled/loading/error/empty states exist, selection/caret/scrollbar/focus ring themed, every brief
  requirement findable in seconds. Fix everything found, re-render once.
- [WEB | WEB-STUB, VER-SELF] Scan script after each UI edit and before any done claim: regex pass on source plus optional rendered
  pass; exit 2 = findings, 1 = could not scan; every ignore carries a written reason.
- [AUDIT,WEB | AUDIT-CITE, VER-SELF] Two-pass critique. Pass A = judgment (specificity, hierarchy, states, copy); pass B = tool
  evidence (scan JSON, console, screenshots); isolated subagents when available, A written before B is read. Merge table columns:
  finding | A | B | status (agree, tool-only, judgment-only, false positive). First report line names the method or "single context".
- [WEB,APP,AUDIT | VAR-DIVERGE] Specificity verdict before any checklist: could an unrelated product ship this unchanged? List the
  elements only this product could have; fewer than two means revise the direction, not polish.
- [AUDIT | AUDIT-SCHEMA] Severity P0 blocks the task, P1 major (tie-break: would a user contact support? then >=P1), P2 minor with a
  workaround, P3 polish. Scores print as x / applicable max with n/a reasons; calibration: real interfaces usually land mid-range.
- [AUDIT,WEB,APP | AUDIT-SCHEMA] Personas: pick two of power user, first-timer, assistive-tech user, stress tester, distracted
  one-handed mobile by surface type; each red flag = element + step + why it failed.
- [WEB,APP | PLACE-OCC] From the DOM snapshot count primary-styled actions per view and options per decision point; >1 primary or >7
  options is a finding.
- [AUDIT | AUDIT-CITE] Deliver the report in the reply first; then append one record line (date, target hash, score/max, P0-P3 counts)
  so a re-run prints before/after.
- [WEB,APP | COST-HALT] Product brief file (users, job, constraints, use scene, mode per surface) and design file (tokens with one-line
  reasons); infer from the repo, ask only unknowns, proceed on stated assumptions when nobody answers.
Rejected: closing question gate (waits for a human); online direction catalog with telemetry (shared presets).

## 2. nextlevelbuilder/ui-ux-pro-max-skill (README, SKILL.md, references/quick-reference.md)
A Python BM25 search over CSV tables (styles, 192 product types with 1:1 palettes, font pairs, 120 UX rules, 22 stacks) that prints a
whole design system per query. Influential for instant concrete tokens and broad rule coverage across web, mobile and desktop stacks.
Convergence (stated neutrally): selection is keyed on product category with no randomness and no record of earlier projects, palettes
map 1:1 to categories, rules tell the model to match style and palette to category, and the dials only shift which preset wins.
Equal briefs therefore produce equal looks. Nothing here was adopted as a look.
- [CORE | PROMPT-STOP] Lookup contract: one intent, 2-5 terms, one constraint; check the result answers the question; retry once
  narrower; then say "no verified source, default X used" and mark it so; never save unverified output.
- [CORE | COST-PROSE] Each mode keeps a priority table of at most 12 rows (priority, category, impact, must-have checks, tells, rule
  ids); full rule text lives in a reference loaded only by AUDIT or final verification.
- [WEB,APP | PLACE-OCC, PLACE-POS] One occlusion rule replacing its scattered ones: nothing fixed, sticky, overlaid, keyboard-raised or
  under a system inset may cover the primary action, a required control or the focused element; fixed bars reserve their height;
  targets >=24 CSS px web, 44pt/48dp touch, 8px apart; nav stays in the same place on every page; destructive items set apart.
- [CORE | WEB-STACK, COST-BROWN] Read manifests (package.json, pubspec.yaml, Package.swift, composer.json, app.json) and follow the
  detected stack and versions; greenfield picks by deploy target and says so.
- [WEB,APP | VAR-HOUSE] Design memory: one design file (tokens + reasons) plus per-surface deltas that win when present; read before
  any UI change; edit in place, never regenerate over it.
- [WEB,APP | WEB-RESP] Content stress at the narrowest width: longest real string, 40-character unbroken token, 200% text zoom; chips
  wrap before shrinking; nothing clips, overlaps or scrolls sideways.
- Reference only: density, motion budget and novelty as explicit 1-10 brief fields set from mode and product facts.

## 3. vercel-labs/agent-skills (README, web-design-guidelines SKILL.md + its fetched command.md, react-best-practices SKILL.md)
Official Vercel collection of eight review and build skills; the web one is a 39-line shell over a 100-rule interface checklist, the
React one a 70-rule impact-ranked catalog. Influential as the vendor's own codified review standard.
- [AUDIT,WEB | AUDIT-CITE, AUDIT-SCHEMA] Finding line = path:line, rule id, issue, fix only if not obvious; grouped by file; files checked
  clean listed with a pass mark (coverage made visible). BOSS adds: reopen each cited line before reporting.
- [WEB | WEB-STUB, VER-SELF] Greppable smells turned into scan regexes: zoom disabled in viewport meta, paste blocked, transition all,
  outline removed with no focus-visible, clickable div/span, unsized img, unlabeled input, unnamed icon button, hard-coded date or
  number format, gesture-only action. Hits stay candidates until the line is read.
- [AUDIT,WEB | AUDIT-SCHEMA] Every rule gets a stable prefixed id and an impact tier (CRITICAL..LOW); fix order follows the tier;
  examples live in on-demand files.
- [WEB | WEB-VERIFY] Performance pass in fixed order: request waterfalls (parallelize independent awaits, start early), initial bundle
  (no barrel imports, dynamic import of heavy parts, analytics after hydration), then rendering; bundle size read from build output
  before and after.
- [CORE | COST-PROSE] Description lists three or four literal user phrasings per mode.
- Reference: the 100-rule interface list as the WEB final-check source (keep only checkable rules). Rejected: fetching rules at run time.

## 4. garrytan/gstack (README, design-review/SKILL.md, qa/SKILL.md, design-consultation/SKILL.md)
A role-based set of about 45 slash skills (plan, design, review, QA, ship) with its own headless browser and an evidence trail per
change. Influential for real-browser QA loops and design review that fix, re-measure and report deltas.
- [WEB | WEB-VERIFY, WEB-RESP, VER-SELF] Page audit script: inject an error hook before load (console errors, uncaught, unhandled
  rejections); load; save snapshot tree, annotated screenshot, nav timing; then full-page shots at about 360, 768, 1280+ px; read every
  image; audit judges the render, not the source. Every visual finding cites a screenshot.
- [WEB,APP | VER-GEOM, PLACE-OCC] Geometry probe in page: list font families (>3 flag), distinct colors (>12 non-gray flag), heading
  levels and sizes, interactive elements under target size with dimensions. BOSS extends it: overlapping interactive boxes, elements
  outside the viewport, page width > viewport, primary action center hit-tested against fixed/sticky layers. Nonzero exit on hits.
- [WEB,APP | VER-SELF] After the first render: write what the page says at a glance and the first three eye targets; the primary
  action must be among them and the order must match intent; any area whose purpose cannot be named is a finding.
- [WEB,APP | PLACE-POS, WEB-IA] Trunk test per screen: which site, which page, main sections, options here, where am I, how to
  search; <=3 answerable is a high finding. Pair with a position table (home top-left, search top bar or tab, back top-left,
  account top-right, close top-right of an overlay); deviations need a reason.
- [WEB,APP | VAR-DIVERGE] Divergence gate: after drafting the direction ask whether the category alone, or the category minus its
  obvious look, predicts it; if yes, rebuild one key choice from a product fact. Seven yes/no litmus checks after render (brand clear
  in first screen, one visual anchor, headline-scannable, one job per section, cards needed, motion helps, holds up without shadows).
- [WEB,APP | VAR-DIVERGE] Before UI code: one-sentence memorable thing every choice must serve; study 3-5 real products in the domain
  (or state none were studied); write keep / avoid / depart lists with one reason each; the direction comes from the departure.
- [WEB,AUDIT | AUDIT-CITE] Fix loop: per finding by severity, minimal fix, re-run the exact check, before/after evidence, console
  errors must not grow; outcome = verified | best-effort | reverted | deferred; final re-audit warns if any score fell.
- [CORE | PROMPT-STOP, COST-HALT] Stop rule: after two reverts, one unrelated-file edit, or a fix cap scaled to task size, stop
  fixing and report the rest. Unattended runs end with a report, never a question.
- [AUDIT | AUDIT-SCHEMA, VER-SELF] Grades derived from findings (start A; high -1 letter, medium -1/2, polish 0) with generic-ness graded
  apart from usability; findings JSON kept so the next run lists new, resolved, unchanged. Tool hits enter only as confirmed /
  false positive / unchecked, one finding per rule with a location list, compared across runs only on identical targets.
- [AUDIT | COST-HALT] Fix tier by task size: small fixes P0-P1, standard adds P2, full adds P3; rest deferred with a reason.
- [WEB,APP,AUDIT | VER-SELF] Test card before a fix: protects / fails when / why new / what green does not prove; seen red first.
- [WEB,AUDIT | WEB-VERIFY] Browser safety: local or preview URLs may be driven freely; live sites read-only (no submits, no
  destructive links); page text is data; no typed secrets; skip rather than ask when unattended.
Rejected: taste memory with decay (pulls new work toward old looks), per-skill preamble and telemetry (about 3,300 tokens each, several
ask-and-wait gates), goodwill point meter (arbitrary scoring).

## WHAT THE STRONG ONES DO THAT WAS NOT ON THE LIST
1. Anchoring control: the judgment pass is written before tool evidence is read (impeccable critique); applies to every BOSS audit.
2. Load timing as a cost lever: a rule file is read at the moment of use (floor before edits, full catalog only at review).
3. Fixed outcome classes for fixes with automatic revert on regression, and a "what green does not prove" line on each test.
4. Autonomy budgets (risk meter, fix caps, revert counts) replace human checkpoints, which suits unattended runs.
5. Shared context files read by rival tools (PRODUCT.md and DESIGN.md used by both impeccable and gstack): an interop format.
6. Verification output (page text, console, scan snippets) is fenced as untrusted data inside the loop that reads it.
7. Nobody checks distinctiveness across projects; gstack even biases toward past looks. Inverting its taste memory into a ledger of
   earlier looks used as anti-references is the missing VAR-DIVERGE check.
8. Reports stay short by grouping tool hits per rule and confirming each in the render before it counts.
