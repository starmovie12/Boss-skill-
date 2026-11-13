# s3a review: decision-rule Brain (S3-B-*) + 11 reference files (S3-F:...)
File-unit shorthand: F:name = S3-F:references/name.md; F:SKILL = S3-F:SKILL.md.

## STRENGTHS
- Size router with an explicit required/optional/forbidden matrix stops over-output on small tasks and under-delivery on big ones (S3-B-0067, S3-B-0287). CORE.
- Honest-claims system: four evidence labels, three never-averaged layers, the "spec-approved, render-unverified" verdict and a three-list receipt (S3-B-0089, F:scorecard-and-evidence). CORE, AUDIT.
- Placement is decided in text before any styling: frequency grading, one main action, five questions per element, a color-stripped check (S3-B-0166, S3-B-0185, S3-B-0204, S3-B-0230). WEB, APP.
- No-shortcut zone for money, identity, consent, destructive and security flows, with concrete payment rules (exact amount, confirm, idempotency, server-confirmed success) (S3-B-0098, S3-B-0204). CORE.
- Checkable platform artefacts: 7 edge cases, 10 responsive checks, 9+5 states, 7-part gesture record, transition-map row format (F:layout-platform). WEB, APP.
- Gate stack: acceptance test written first, 9-row stress matrix, touched/untouched regression list, severity-ranked fix loop capped at 3, 31-question veto list (S3-B-0189, F:tests-gates, S3-B-0230, S3-B-0253). CORE.
- Safety floor, inputs-as-data rule and a six-level priority order that settles rule conflicts (S3-B-0036, S3-B-0046, S3-B-0166). CORE.
- Verify-first handling of non-Latin fonts and heuristics-with-exception-notes instead of universal visual laws (S3-B-0213, S3-B-0148, F:SKILL). WEB, APP.

## FLAWS
- Self-graded scorecard: the maker scores its own work; thresholds (80%, 3/5) are self-declared unverified; "no evidence = 0" sits outside the 1-5 scale; the SPEC layer demands "observed" evidence a spec cannot supply; fail line is "<3" in one place and "3 or below" in another (F:scorecard-and-evidence, F:tests-gates, S3-B-0089).
- By its own admission never field-tested; every spatial share, breakpoint and score threshold is an unverified author heuristic (S3-B-0003, F:SKILL, F:tests-gates part F, F:layout-platform).
- Heavy repetition against its own single-source rule: evidence labels, receipt lists and the no-shortcut list each restated 4-6 times; the summary unit and veto list duplicate the steps almost 1:1 (S3-B-0019, S3-B-0067, S3-B-0089, S3-B-0253, F:SKILL, F:scorecard-and-evidence).
- Single-source breaches: the first-glance window is said to live in one file yet "3s/5s" is hardcoded elsewhere; the touch floor is stated three ways (48 everywhere; 44/48 per platform; "do not reuse one unit across platforms") (F:tests-gates, F:scorecard-and-evidence, F:icons-tokens-states, F:pro-rules-and-predelivery, F:ux-rules-full).
- Rigid universal prescriptions: forced single-workspace-with-pills template and its 40/30/30 split, offline queue everywhere, "zero blocking popups" beside mandatory confirms (S3-B-0098 rules 3-4, S3-B-0253 item 1, F:layout-platform).
- Contradictions: dark mode conditional (S3-B-0148, S3-B-0213) vs "both themes tested" and "design light/dark together" (F:pro-rules-and-predelivery, F:ux-rules-full); uniform durations banned (S3-B-0148) vs "unify duration tokens globally" and fixed 150/200ms (F:ux-rules-full, F:icons-tokens-states).
- Domain ranking is inconsistent: navigation labelled high yet ranked ninth under medium items; layout ranked below style selection although placement is said to outrank styling (S3-B-0157 vs S3-B-0166).
- Unrealistic for a text-only run: checklist lines say "tested on" devices, orientations and both themes; most RENDER/INTERACT items can only end not-tested, so the big M/L deliverable set is mostly spec-only bulk (F:pro-rules-and-predelivery, S3-B-0230, S3-B-0287).
- Ceremony and blanket claims: a required sentence declaring every placement "perfect", persona with brand-name benchmarks, undefined internal id jargon (letter-number rule ids), near-duplicate checklist lines (S3-B-0213, S3-B-0018, F:pro-rules-and-predelivery).
- Possibly stale or locale-bound facts: 300ms tap-delay fix, auto-zoom under 16px, fixed viewport sizes, one country's privacy act, named OS gestures and hardware cut-outs, accessibility-standard clause numbers (F:ux-rules-full, S3-B-0036, F:layout-platform, F:tests-gates).

## GAPS
- WEB: page patterns are 16 frozen section orders with no stated decision logic; nothing on desktop-first density, semantic structure or content strategy; the pre-delivery list is native-only (F:page-patterns, F:pro-rules-and-predelivery).
- APP: no method for choosing navigation architecture (tabs vs stack vs drawer, depth); tablet/foldable is one line; permission flows are a single sentence (S3-B-0194, F:layout-platform).
- PROMPT: nothing on writing prompts or work orders; only an intake field list and an output order (S3-B-0305, S3-B-0287).
- AUDIT: defined only by its output list; no procedure for gathering evidence from screenshots or code, sampling, or calibrating severity with examples (S3-B-0067, S3-B-0287).
- Occlusion: no single "nothing covers the primary action or required control" check; coverage rules are scattered (keyboard, safe areas, sticky insets, focus-not-obscured); no rule for conventional positions of close/search/back icons (F:layout-platform, F:tests-gates, F:pro-rules-and-predelivery).
- Design variety: the anti-generic audit depends on a file outside the shard; one-direction and single-workspace rules push sameness (S3-B-0148, S3-B-0098).
- Verification: no concrete steps to obtain a render; scripts are named but not in the shard; no worked example of an evidence line or receipt (S3-B-0089, F:SKILL).
- Token cost: 74 KB logic file with long repeated lists; kit-gate and changelog text are large; 221-rule index overlaps the other checklists (S3-B-0003, S3-B-0055, F:ux-rules-full).

## PLACEMENT
- Placement before styling: position, size and order of every element fixed in text before any color, font, shadow or motion (S3-B-0166, S3-B-0204, S3-B-0019).
- Color-stripped check gates the visual step: layout must read clearly with all color removed (S3-B-0213, S3-B-0230 check 6.1).
- Platform identified first; unknown platform = phone, labelled assumed (S3-B-0204).
- Five ordered questions per element (where, how big, beside/after what, why here, label) plus rank tag hero/second/quiet (S3-B-0204).
- Screen written as proportional parts totalling 100%, floating elements listed separately (S3-B-0204, F:layout-platform part A).
- Frequency grading: frequent in prime position, occasional one tap away, rare in a menu; features never removed (S3-B-0185).
- Exactly one main action per screen; no twin primary buttons (S3-B-0185, F:ux-rules-full, F:scorecard-and-evidence criterion 1).
- Thumb zone: frequent actions bottom/middle, rare ones top or in menu/sheet (F:layout-platform part A).
- Proximity and order: related controls close, groups far apart, on-screen order = task order, balanced top/middle/bottom weight (F:layout-platform part A).
- No habitual cards or boxes where spacing and type can separate (S3-B-0148, F:layout-platform part A, F:scorecard-and-evidence criterion 5).
- Full-screen content: small floating controls clustered low, main button pinned, others auto-hide (F:layout-platform part A).
- Keyboard and long forms: active field and primary action stay above the keyboard; summary and action sticky at bottom (F:layout-platform parts A and D item 7).
- Data screens: one largest key number with context; lists: compact filters so the first result sits high (F:layout-platform part A).
- Destructive actions kept out of the easy zone and away from the primary action; undo for small, explicit confirm for account-level (S3-B-0204, F:ux-rules-full, S3-B-0253 item 9).
- Money actions: exact amount on the button, confirm, idempotency id, success only after server confirmation, failure states whether money moved (S3-B-0204, S3-B-0253 item 17).
- Hiding vs pinned bars on scroll; pinned input and primary action never hide (S3-B-0194, F:layout-platform part D item 4).
- New page only when the task cannot be done on the current screen; inline preview, tab or sheet first (S3-B-0194).
- Login/permission asked in context with a skip route; state restored on reopen (S3-B-0194).
- Familiar interaction patterns without cloning whole screens (S3-B-0201).
- Lost-feature guard: every required feature present in layout; missing one is a blocker defect (S3-B-0166, S3-B-0230 check 6.1, S3-B-0253 item 12, F:tests-gates part E).
- Exit path of full touch size in every popup, sheet, flow and state; no dead ends (S3-B-0036, S3-B-0098 rule 4, F:layout-platform part C, S3-B-0253 item 3).
- Seven per-screen platform edge cases, one line each (F:layout-platform part B; required at M/L by S3-B-0204).
- Safe areas, system bars, gesture-indicator clearance and content insets under fixed bars (F:pro-rules-and-predelivery, F:icons-tokens-states, F:ux-rules-full, F:layout-platform part D item 8).
- Gesture discipline: one primary gesture per region, system gestures never blocked, visible control for every critical gesture (F:pro-rules-and-predelivery, F:ux-rules-full).
- State transition map row format and standard chain from empty to success/error/offline (F:layout-platform part C, S3-B-0204).
- Nine mandatory + five contextual component states, with a fixed priority when several apply (F:layout-platform part E, F:icons-tokens-states).
- Seven-part gesture record including undo path and accessible alternative (F:layout-platform part E, S3-B-0213 sub-step 5.7).
- No fake progress: progress and "done" tied to real state (S3-B-0230 check 6.10, S3-B-0253 item 17).
- Icon discipline: one vector family, one stroke, no emoji, token sizes, official logos, expanded hit area, icon + label in navigation (F:icons-tokens-states, F:pro-rules-and-predelivery, S3-B-0253 item 19).
- Ten responsive checks with pass/fail/spec-only/not-tested, each width with its own composition (F:layout-platform part D).
- Navigation form by width, same placement on every page, no mixed patterns at one level (F:layout-platform part D item 3, F:ux-rules-full).
- Touch floor, gap and focus rules: target size, spacing, focus order = visual order, focus never covered by sticky UI (F:tests-gates part C items 2, 4, 5).
- Stress matrix keeps placement stable under extreme content: sibling buttons do not move, primary action stays in view on small screens and at largest font (F:tests-gates part A1).
- Regression list (touched vs untouched) and cross-screen consistency matrix including primary action height and position (F:tests-gates part B).
- Acceptance test declared up front with tap counts, target/contrast floors and exit path (S3-B-0189).
- Severity loop and veto gate force placement defects to be fixed before delivery (S3-B-0230, S3-B-0253, F:tests-gates part E).
- Visual heuristics (hero, anchor) are not forced onto dashboards, forms, settings or dialogs; exceptions need a one-line note (S3-B-0148, S3-B-0253 item 28).
- Landing pages: main action placed beside the convincing content; capture form above the fold; sticky action on long or priced pages (F:page-patterns).
