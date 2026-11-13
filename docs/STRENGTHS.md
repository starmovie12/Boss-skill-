# Strongest capabilities of each source (BOSS must match or beat every row; see docs/OVERMATCH.md)

## S1 (markdown skill)
- ST-S1-1 Per-component state table with visual, haptic and motion columns, including empty, skeleton, offline (S1-0710) [WEB, APP]
- ST-S1-2 Seven-part interaction record from trigger to resulting state and side effect (S1-0745) [WEB, APP]
- ST-S1-3 Accessibility checklist with numeric floors and focus-return rules (dialog open, close, route change) (S1-0810) [WEB, APP, AUDIT]
- ST-S1-4 Mutation-handler order, atomic writes, ownership check answering not-found, immutable audit entry (S1-0864) [WEB, APP, AUDIT]
- ST-S1-5 Exact-value table turning vague words into unit-bearing values (S1-0480) [PROMPT, WEB, APP]
- ST-S1-6 Audit finding record: location, exploit scenario, impact, proof, complete fix, regression test; severity counts up front (S1-2603, S1-3343) [AUDIT]
- ST-S1-7 Seventeen attacker questions per state-changing route (S1-2380) [AUDIT]
- ST-S1-8 Stress-plan shape: cohorts with counts and behavior, numeric pass criteria, rollback rule (S1-2340, S1-2813) [AUDIT]
- ST-S1-9 Native app spec: permission-with-purpose table, build profiles, deep links, secure storage, size and cold-start budgets (S1-2769) [APP]
- ST-S1-10 Work-order skeleton with numbered measurable requirements and a skipped-with-reason manifest (S1-3281, S1-2529) [PROMPT, CORE]

## S2 (25-part XML)
- ST-S2-1 Project ingestion: read all, source-of-truth order, conflict map with OPEN items, gap hunt, report of live vs stubbed vs assumed (S2-P01-0504) [CORE]
- ST-S2-2 Shelf-life law for dated facts and epistemic labels for confidence (S2-P02-0883, S2-P04-1498) [CORE]
- ST-S2-3 Nine-lens adversarial audit plus compound scan and four stress passes (S2-P04-1239 to S2-P04-1483) [AUDIT]
- ST-S2-4 Prompt craft: order of parts, literal reading, long-context sandwich, machine-read output contracts (S2-P05-1731) [PROMPT]
- ST-S2-5 Requirement tests (atomic, testable, unambiguous, necessary) and a 14-check completeness gate (S2-P08-2441, S2-P08-2453) [PROMPT, AUDIT]
- ST-S2-6 Spec audit: 20-class defect taxonomy, severity with written criteria, seven-field fix protocol, report order (S2-P09-2534, S2-P09-2606, S2-P09-2615, S2-P09-2627) [AUDIT]
- ST-S2-7 Diverge-then-converge: options must differ in core mechanism, never padded to a count (S2-P10-2673, S2-P10-2757) [WEB, APP, PROMPT]
- ST-S2-8 Execution loop with stop condition and failure signals written before looping; risk-tiered confirmation (S2-P11-2860, S2-P11-2887) [CORE]
- ST-S2-9 Delegation brief contract, separate grader, five-item handoff (S2-P12-2974, S2-P12-2984, S2-P15-3178) [CORE, PROMPT]
- ST-S2-10 Eval-first grading ladder (deterministic before model judge) and verification gauntlet finding schema with ship bar (S2-P13-3046, S2-P18-3455, S2-P18-3462) [CORE, AUDIT]

## S3 (archive with the Brain)
- ST-S3-1 Task-size router with a required / optional / forbidden deliverable matrix (S3-B-0067, S3-B-0287) [CORE]
- ST-S3-2 Four evidence labels, three never-averaged layers (spec, render, interact), "spec-approved, render-unverified" verdict, three-list receipt (S3-B-0089) [CORE, AUDIT]
- ST-S3-3 Acceptance test written before design, never bent afterwards (S3-B-0189) [CORE]
- ST-S3-4 Text-only placement plan before styling: five questions per element, frequency grading, one main action, color-stripped check (S3-B-0185, S3-B-0204, S3-B-0213) [WEB, APP]
- ST-S3-5 No-shortcut zone for money, identity, consent, destructive and security flows (idempotent money actions), under a safety floor, inputs-as-data rule and six-level priority order (S3-B-0098, S3-B-0204, S3-B-0036, S3-B-0046, S3-B-0166) [CORE]
- ST-S3-6 Seven platform edge cases, ten responsive checks, nine plus five states, transition-map rows (S3-F:references/layout-platform.md) [WEB, APP]
- ST-S3-7 Gate stack: stress matrix, recovery cases, regression list, consistency matrix, P0-P3 fix loop capped at 3, 31-question veto list (S3-F:references/tests-gates.md, S3-B-0230, S3-B-0253) [CORE]
- ST-S3-8 Three genuinely different paths for large new screens and the anti-generic rule that two layers beyond color must change (S3-B-0132, S3-B-0148) [WEB, APP]
- ST-S3-9 Verify-first handling of non-Latin fonts with five rendering checks; visual heuristics scoped by screen archetype with an autopilot-sign list and exception notes (S3-B-0213, S3-F:references/visual-craft.md) [WEB, APP]
- ST-S3-10 Three-tier token method (primitive, semantic, component) with dark mode as a semantic-only delta, paired on-color roles and a measured palette table; full state model with precedence (S3-F:references/design-system/token-architecture.md, S3-F:references/design-system/states-and-variants.md) [WEB, APP]

## PLACEMENT (every mechanism the sources use to put elements in the right place and keep them there)
- PL-S-1 Layout decided in text before any styling; color-stripped readability check (S3-B-0166, S3-B-0204, S3-B-0213)
- PL-S-2 Platform first; unknown platform = phone, labeled assumed (S3-B-0204)
- PL-S-3 Five ordered questions per element plus visual rank; screen as proportional parts with floating elements listed (S3-B-0204)
- PL-S-4 Frequency grading A/B/C: frequent in prime position, occasional one tap away, rare in a menu; features never removed (S3-B-0185)
- PL-S-5 One primary decision and one main action per screen; core action within two taps (S3-B-0185, S2-P03-0989)
- PL-S-6 Thumb zone; proximity (related close, groups apart); on-screen order = task order (S3-F:references/layout-platform.md, S2-P03-0989)
- PL-S-7 Fixed corner conventions (back top-left, at most two contextual actions top-right); one home per element (S2-P03-0989, S1-2410 method only)
- PL-S-8 Destructive actions away from the primary action and the easy zone; undo for small, confirm for large; money shows the exact amount, confirms, is idempotent, succeeds only on server confirmation (S3-B-0204, S3-B-0253)
- PL-S-9 Container by stakes: full screen for high-stakes input, sheet for quick picks, takeover for pending critical decisions that follow the user (S2-P03-1096, S2-P24-4532)
- PL-S-10 Hiding vs pinned bars on scroll; keyboard keeps active field and primary action visible; sticky summary in long forms (S3-B-0194, S3-F:references/layout-platform.md)
- PL-S-11 Seven per-screen platform edge cases; safe areas and insets under fixed bars; system gestures never blocked (S3-F:references/layout-platform.md, S2-P03-1057)
- PL-S-12 Ten responsive checks, each width its own composition; navigation form by width; zero horizontal scroll (S3-F:references/layout-platform.md, S1-2071)
- PL-S-13 State lists and transition-map rows with exit paths; route-level loading, error and not-found siblings (S3-F:references/layout-platform.md, S1-2529, S1-0710)
- PL-S-14 Icon discipline: one vector family and stroke, no emoji, icon + label in navigation, official logos, enlarged hit areas (S3-F:references/icons-tokens-states.md, S2-P03-1087)
- PL-S-15 Touch floor and gaps; focus order = visual order; focus return rules; focus never covered by sticky UI (S1-0810, S3-F:references/tests-gates.md)
- PL-S-16 Named layer scale for stacking; blueprint dimension block per section with safe-area edges and per-breakpoint deltas (S1-0509, S1-2436)
- PL-S-17 Stress matrix keeps placement stable under long text, empty data, huge volume, small screens, large font (S3-F:references/tests-gates.md)
- PL-S-18 Lost-feature guard and veto list: a required feature missing from the layout or a dead end blocks delivery (S3-B-0253, S3-B-0230)
- PL-S-19 Regression list and cross-screen consistency matrix including primary-action height and position (S3-F:references/tests-gates.md)
- PL-S-20 Landing pages: main action beside the convincing content; heuristics never forced onto dashboards, forms, settings or dialogs (S3-F:references/page-patterns.md, S3-B-0148)
