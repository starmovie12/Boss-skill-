# s1a review (S1 lines 1-1667)

## STRENGTHS
- Per-component state table with visual, haptic and animation columns, including empty, skeleton and offline rows (S1-0710) [WEB,APP]
- Seven-part interaction record tying gesture -> feedback -> render path -> resulting state and API effect (S1-0745) [WEB,APP]
- Concrete accessibility checklist with numeric floors and explicit focus-return rules (S1-0810) [WEB,APP,AUDIT]
- Security handler order, atomic-write requirement, ownership check answering not-found, immutable audit entry (S1-0864) [AUDIT,WEB,APP]
- Pre-work decomposition list with exit check, fixed conflict order, and not-applicable-with-reason habit (S1-0213) [CORE]
- Exact-value table that turns vague spec words into unit-bearing values (S1-0480) [PROMPT,WEB,APP]
- One-test-per-rejection-path naming and fail-fast environment schema (S1-1443, S1-1548) [WEB,APP]
- Veto lists grouped by review lens give a fast final gate (S1-0050) [WEB,APP,AUDIT]

## FLAWS
- Self-praise and impossible blanket claims: best in existence, zero defects of every kind, simultaneous compliance with many certifications (S1-0001, S1-0050).
- The planning protocol is told to run silently and never be shown, so none of it can be verified; any miss demands full regeneration (S1-0213).
- Internal contradictions: user instruction and security veto are both called un-overridable (S1-0213); 18 states announced, 19 listed (S1-0710); keyword easing banned yet used in the skeleton snippet (S1-0480 vs S1-1170); placeholders banned yet test bodies and a handler are stubs (S1-0696 vs S1-1443, S1-0864).
- Raw-color ban has no exception for the place where tokens are defined, and the protocol's own style step names a raw-alpha surface (S1-0509, S1-0213).
- Demands exact contrast ratios, bundle deltas and cold-start times with no measuring step, which invites invented precision (S1-0480, S1-0213, S1-0841).
- Rigid universals: every component gets all states, every gesture a full record with haptics and abuse scoring, nothing may be shortened; heavy token cost on small tasks (S1-0696, S1-0710, S1-0745).
- Possibly stale or wrong facts: web top-ten list dated 2023, legacy XSS header, inline styles allowed in CSP, hard-coded model id, pinned framework versions, browser online flag treated as truth (S1-0864, S1-1370, S1-1170, S1-1414).
- Example code breaks its own rules: the atomic batch option has no balance check, clients may create transfer records directly, optimistic update on a money balance, AI route accepts client-written assistant turns, regex blacklist as injection defense (S1-0864, S1-1582, S1-1370).
- Unrealistic targets: 10K-user plus 1K-attacker stress run inside every CI push, 50ms cold start, AAA contrast named beside AA with no clear gate (S1-1517, S1-1443, S1-0050, S1-0810).
- One stack, one CI vendor and one house visual style are stated as immutable law; the banner promises 30 laws and the text cross-references laws outside this range (S1-0476, S1-1170 to S1-1640, S1-0213).

## GAPS
- WEB: no content, information-architecture, SEO or copy method; responsive breakpoints never specified beyond one narrow-phone baseline.
- APP: mobile appears only as haptic columns and target sizes; nothing on safe areas, keyboard avoidance, navigation patterns, permissions or store rules.
- PROMPT: nothing on writing prompts or work orders beyond the exact-value table and an injection snippet.
- AUDIT: no report format, severity scale, evidence standard or reproduction steps; the checks live inside build templates.
- Design variety: a single fixed look is mandated; the only choice step is a one-line rationale declaration.
- Verification: nearly all gates are self-attested in hidden reasoning; no run-the-tool-and-show-output step.
- Token cost: about 1,650 always-loaded lines, most of it stack code that belongs in on-demand reference.
- No scope triage (tiny tasks get the full ceremony), no clarifying-question step, no way to state unknowns.

## PLACEMENT
- Named layer scale fixes stacking order: base, raised, floating nav, dropdown, sticky, overlay, modal, notification, tooltip, command palette; pick by name (S1-0509). Oddity: floating nav sits below dropdown and sticky.
- State table places feedback per state: focus ring offset, banner for offline and banned, illustration + copy for empty, skeleton shaped like the content (S1-0710).
- Interaction record requires final UI state and navigation side effect for each gesture, so transitions are specified end to end (S1-0745).
- Focus placement: dialog open -> first element, close -> trigger, route change -> heading (S1-0810).
- Minimum target 44x44px / 48dp appears as veto, exact-value row, trigger field and accessibility rule (S1-0050, S1-0480, S1-0745, S1-0810).
- Narrow-phone-first baseline (source: 380px or less as primary target); desktop-first only on explicit request (S1-0213, S1-0050).
- Fixed house rule (quarantined): profile avatar only in bottom navigation, never in the header; floating elements need an elevation shadow. Method residue: one home per element, floating layers must read as raised (S1-0050, S1-0213).
- Layout-shift guards: images carry dimensions, no late-injected content, dynamic regions behind content-matched skeletons (S1-0213, S1-0050, S1-1170).
- Spacing on a 4px grid and a closed radius scale; framework utilities only, no arbitrary pixel values (S1-0509, S1-1170).
- Form fields carry four validation states; errors are tied to their input; status never by color alone (S1-0050, S1-0810).
- Above-fold hero image flagged as largest-paint candidate and prioritized (S1-0841).
- Final gate: veto list by lens plus a conflict order in which performance and accessibility outrank aesthetics (S1-0050, S1-0213).
