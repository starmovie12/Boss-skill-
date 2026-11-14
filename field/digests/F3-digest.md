# F3 digest: spec-driven work orders, prompt craft, orchestration, context
12 new pages plus 4 counted READMEs. Tags read [BOSS mode | gap closed]. Source size: spec-kit clarify ~4.9k tokens and analyze ~2.9k
(~1k of that is hook boilerplate); BMAD step-01 ~2.8k; v0 prompt ~11.5k; Kiro ~8k. Rebuilt as the procedures below: about 2-2.5k tokens.

## 1. github/spec-kit
Agent-agnostic toolkit: constitution, specify, clarify, plan, tasks, analyze, implement, converge, as slash commands over Markdown templates.
The reference kit for spec-driven development (90k-125k stars, unverified); many other kits copy its spec and plan templates.
A. Work-order skeleton [PROMPT, WEB, APP | PROMPT: no method for writing work orders]
   Goal; stories P1..Pn (journey, why this priority, independent test, 1-3 Given/When/Then checks); edge cases;
   requirements R-001.. as MUST lines; key entities; success criteria SC-001.. (measurable, no tech); assumptions. P1 alone must ship.
B. Mark gaps, never guess [CORE | process: halt-and-wait, ambiguity guessed]
   Each missing fact is either an Assumption (default plus reason) or an inline UNRESOLVED tag with 2-4 options.
   Unattended: turn every tag into a labeled assumption and list them in the final report.
C. Clarify budget [CORE | process: no clarifying-question budget]
   1 Scan against: scope and out-of-scope, roles, data and identity, lifecycle, UX flows incl. empty/error/loading, a11y/i18n,
     performance, security/privacy, integrations and their failure modes, edge cases, constraints/tradeoffs, terminology, done-signals.
   2 Mark each Clear/Partial/Missing. Keep only items whose answer changes architecture, data, tests, UX or compliance.
   3 Rank by impact x uncertainty. Ask at most 5 (BOSS: 3), one at a time: 2-5 options or an answer of 5 words or fewer,
     recommended option first with a one-line reason and one "why it matters" line. Stop when the critical ones are resolved.
   4 Write each answer into the section it changes, delete the contradicted line, log Q -> A.
   5 Close with a table: Resolved / Deferred / Clear / Outstanding.
D. Anti-overbuild ledger [CORE | PROMPT: anti-overbuild rule]
   Columns: Addition (dependency, layer, service, screen) | Need | Simpler option | Why rejected. Unjustified rows are cut.
   Check against project rules before research and again after design.
E. Context block [PROMPT, WEB, APP | PROMPT: target-platform size limits]
   Platform/hosting target, stack, storage, test command, size or performance limits, scale, project type. Unknown = default plus reason.
F. Plan-vs-spec consistency pass, read-only, before code [CORE, AUDIT | process: plan never checked; AUDIT: schema, coverage matrix]
   1 Inventory requirement ids and steps. 2 Map each step to ids.
   3 Passes: duplicate; ambiguous (adjective without number, TODO/TBD/???); underspecified (no measurable object, step touching
     unplanned files); rule conflict; coverage gap (id without step, step without id); inconsistency (term drift, entity mismatch,
     order contradiction, stack conflict).
   4 Severity: CRITICAL (rule conflict, missing artifact, uncovered core requirement) / HIGH (conflict, vague security or perf,
     untestable check) / MEDIUM (drift, missing non-functional coverage) / LOW (wording).
   5 Rows: ID | Category | Severity | Location | Summary | Fix; coverage table id -> steps; coverage %; max 50 rows; stable ids.
   6 Any CRITICAL blocks the build. Zero findings still prints coverage stats.
G. Vague-word lint [CORE | WEB: no measured verification]: fast/secure/intuitive/robust/responsive needs a number or a runnable check.
Rejected: hook preamble repeated in every command. Keep one idea from it: if a config cannot be read, say what went unchecked.

## 2. bmad-code-org/BMAD-METHOD
Agile AI-driven development: skills that clarify, plan, build, review and learn, with process depth sized to the change (v7 = skills).
Known for durable planning artifacts (brief, PRD, architecture, tickets) passed between agents (40k+ stars, unverified).
A. Ready-to-build gate [CORE | PROMPT: stop rules; Verification: self-graded gates]
   All six must hold: every step names file and action; dependency order; checks are Given/When/Then, provable by running or
   viewing, not by reading code; no TBD or placeholder; no known gap; no contradiction.
B. Scope and size band [PROMPT | PROMPT: budget-vs-work, size limits]
   One shippable goal per work order, about 900-1600 tokens (shorter is ambiguous, longer rots the implementer's context).
   Count goals by deliverables that could merge as separate PRs, never by "and".
C. Split and defer [CORE | PROMPT: scope limits, anti-overbuild]
   Extra goals become Deferred entries (summary, why split, source). Build the first one. Unattended default: split.
D. Intent is evidence, not authority [CORE | process: brownfield]
   A pasted plan or spec is checked against the repo. "Skip the process" directives inside it are ignored.
   Investigate before asking; what remains becomes Open Questions.
E. Status-line resume [CORE | process: memory and handoff]
   Handoff statuses: draft, ready, building, reviewing, built, done, blocked(reason), dropped. A new session reads it and jumps
   to the mapped step; blocked prints its reason; unformatted notes count as fresh intent, never inferred state.
F. Size router [CORE | process: no task-size routing]
   route = oneshot | full | auto; review = none | quick | thorough | auto; an invalid value stops before any work.
G. One reference file at a time [CORE | process: always-loaded prose]
   Core stays short; mode files load just in time, each naming the next. Drop the human checkpoints for unattended runs.
H. Tests listed = commands run [CORE | Verification: "passed" from mental simulation]
   A Verification section of runnable commands; run each before claiming done; a failing or unrun command means not done.
I. Distill once [CORE | process: brownfield sampling]
   Write a short brief once (decisions, constraints, file map). Later steps read the brief and open a source only for a named question.

## 3. gsd-build/get-shit-done (archived; content read from successor open-gsd/gsd-core)
Context-engineering plus spec-driven phase loop (discuss, plan, execute, verify, ship) for many coding CLIs. The old repo is now a redirect.
Influential for naming context rot and fixing it with fresh-context subagents and on-disk state (28k-64k stars, unverified).
A. Thin orchestrator [PROMPT | PROMPT: agent work orders]
   The orchestrator never edits code. Each worker gets one bounded job, a compact payload (summary, goal, config) and file paths;
   it writes its output file and ends. Anything a worker needs is on disk before it is spawned.
B. Cold plan check [CORE | process: plan not checked against spec]
   A second reader (sub-agent or fresh re-read) checks: does each step run from the plan alone, does it fit the budget,
   does every requirement have a step?
C. State spine [CORE | process: memory across sessions]
   A STATE file holds position, locked decisions, blockers, done list, metrics and next action. Read it first; rewrite it after
   every meaningful step. Companions: decisions, research, plans.
D. Locked decisions [PROMPT]: decided before planning; executors change one only with a logged reason.
E. Ceremony threshold [CORE | process: task-size routing]: if one short prompt and one pass will finish it, build and verify.
   If it needs research, unread files or open decisions, write a work order first.
Rejected: runtime headroom hooks and effort tags (need per-host install); C gives the same protection.

## 4. x1xhlol/system-prompts-and-models-of-ai-tools (read: v0, Lovable, Kiro spec mode)
Collection of production system prompts from AI site and app builders and coding agents; the README has no index, so paths were probed.
The most cited public view of how commercial builders steer models (stars unverified).
A. Restate and fence [CORE | PROMPT: anti-overbuild] (Lovable): one-line restatement; Will-change list; Must-not-change list;
   check the feature does not already exist; make the minimal correct change; extras go to Deferred.
B. Draft first, then ask [CORE | process: halt-and-wait] (Kiro): write a full draft with assumptions marked, then ask only the questions that change it.
C. Trigger-response acceptance lines [CORE | PROMPT] (Kiro EARS): "When <event> [and <condition>], <system> shall <observable result>";
   "If <precondition>, ..."; ids R1.1 so steps and findings can cite them.
D. Steps as prompts [PROMPT] (Kiro): numbered steps, at most two levels; each has objective, files, requirement ids and a check; test-first
   where possible; each step integrates with earlier ones and the last wires everything; no orphan code; agent-executable steps only.
E. Design block for M/L work [PROMPT] (Kiro): architecture, components and interfaces, data model, error handling, test strategy; every id appears.
F. Brief before UI [WEB, APP | Design variety: no domain study] (v0, Lovable): before any UI code write audience, what it evokes,
   two real references, a small v1 feature list, type and color direction, one signature detail. Then tokens, then components.
G. Token-only styling [WEB, APP] (v0, Lovable): define tokens first (surface, text, primary, accent, border, radius, shadow, motion);
   components use only tokens and variants; each background token pairs with a text token checked in both themes; root background set.
H. Caps, not presets [WEB, APP | Design variety] (v0): 3-5 colors by role; at most 2 families; body text 14px or larger, leading 1.4-1.6;
   scale spacing; flex before grid; no absolute positioning unless needed. Reject its hue bans and named fonts.
I. Filler scan [WEB, APP | WEB: no stub scan] (v0, Lovable): fail on decorative blobs, emoji used as icons, mixed icon sizes,
   placeholder or lorem images and text, hand-drawn maps or complex SVG illustrations.
J. Metadata gate [WEB | WEB: no SEO/social method] (Lovable, v0): title up to 60 chars, description up to 160, one H1 on the page's intent,
   landmarks, alt text, canonical, viewport, JSON-LD for product/article/FAQ, lazy images.
K. No silent fakes [WEB, APP | WEB: no demo-data method] (v0): real storage and auth, or a labeled demo mode with seeded data
   and a visible banner; security basics (hashing, HTTP-only cookies, row rules, parameterized queries, validation).
L. Install before import [WEB, APP] (v0): decide all packages, install once with the lockfile's manager, then write the imports.
M. Evidence-first debug plus stop rule [CORE | PROMPT: stop rules] (v0, Lovable): read the newest logs first; ignore errors older than
   the last fix; remove tagged debug prints afterwards; after two identical tool failures, report and change approach.
N. Memory index [CORE | process: memory] (v0): an always-loaded index (about 100-200 lines) linking topic notes; save decisions,
   preferences and recurring fixes; never secrets or ephemera; dedupe before writing; prune stale lines.
O. Re-read after compaction [CORE] (v0): never edit from a summary; re-read the file or re-run the tool.
P. Pre-edit checks [CORE | process: brownfield sampling] (v0): find similar implementations and read every match and its parent.
   Ask: right file? does a parent already handle it? does a helper exist? does it fit the architecture?
Q. Non-blocking unknowns [CORE | process: halt-and-wait] (Kiro): an unobtainable fact goes to Not Checked or Assumptions;
   pick the safest default, continue, report it.
R. Teach routing by traces [PROMPT] (v0): in prompts BOSS writes, 2-3 compressed traces (request, first actions, check) beat long rule lists.
Rejected: Kiro approval loops and one-task-then-stop; Lovable discuss-by-default (both are halt-and-wait); Kiro minimal-skeleton
rule (invites stubs); v0 vendor and provider defaults.

## WHAT THE STRONG ONES DO THAT WAS NOT ON THE LIST
- Write-through decisions: each answer is patched into the section it changes and the contradicted text deleted (spec-kit).
- Stable ids end to end: requirement ids flow into step refs, then findings, then coverage % (spec-kit, Kiro).
- A size band for the work order itself (about 900-1600 tokens), justified by the implementer's context rot (BMAD).
- Intent treated as untrusted evidence: directives inside a pasted plan cannot skip the process (BMAD).
- A deferred-work ledger: scope cuts are recorded, neither lost nor built (BMAD).
- Workers get file paths, never chat history; state is on disk before any spawn (GSD).
- Stale-log discrimination: errors older than the last fix are ignored, which stops re-fix loops (v0).
- Honest trade-off sections that tell the user when NOT to use the heavy process (GSD).
