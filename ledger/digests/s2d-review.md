# s2d review: S2 lines 4419-5959

## STRENGTHS
- Project-module discipline: truth order, context kit, one constants file for labels, a divergence ledger with statuses, a closed owner-only ask list (S2-P24-4432, S2-P24-4675, S2-P24-5307, S2-P24-5279) | CORE.
- Honest-state design: four visible end states for a sent item, no shadow penalties, visible backpressure, render throttling instead of dropping (S2-P24-4869, S2-P24-4892) | CORE, APP.
- Screen-spec format with sized zones, thumb path, per-component interaction record and state list (S2-P24-4921) | APP, WEB.
- Render-cycle walk before presenting UI code, plus a stubbed-vs-live receipt (S2-P25-5864, S2-P24-5254) | APP, CORE.
- Mobile resilience checks: leak cleanup, offline-first, buffered reconnect, atomic counters, idempotent writes (S2-P25-5545, S2-P24-4852, S2-P24-4991) | APP.
- Pragmatic bridge: honor principles now, defer scale pieces, always disclose what is stubbed (S2-P24-4852, S2-P25-5768) | CORE.
- Wellbeing and fairness rules stated as checkable server-side limits, with a written resolution of the engagement-vs-wellbeing tension (S2-P24-4869, S2-P24-5307) | CORE.

## FLAWS
- Two councils both declared binding: thirteen chairs with a 13/13 sign-off (S2-P24-4532, S2-P24-4921, S2-P24-5262) vs seven minds with 7/7 (S2-P25-5393, S2-P25-5864).
- Two "final" code gates: a hundred checks (S2-P24-5211) vs a "thousand points" (S2-P25-5545); each domain lists only about a dozen checks, so the count is self-graded and inflated; both run silently and are never printed, so neither can be verified.
- The mobile-only and single-product locks (S2-P25-5356, S2-P25-5468) contradict the source's own web standards (S2-P22-3790) and the closing reminder that applies the file to any task (S2-P25-5932).
- Code bugs in the patterns: idempotent send looks up the id in a different collection than it writes to, and lookup-then-insert is racy; the limiter is labelled sliding window but is a fixed window (S2-P24-5238).
- More bugs: fixed row height assumed for variable-height messages (S2-P24-5067, S2-P25-5643); optimistic send uses the phone clock for id and time while the refusal list bans phone-clock ordering (S2-P25-5712).
- Heavy repetition: the final part restates almost all of the previous one, and both restate Parts 10 and 17-23 with product wording; the codebook appears twice.
- Unrealistic targets stated as pass criteria: every malicious actor flagged within a minute and banned within minutes with zero false positives (S2-P24-4991, source's claim).
- Dated facts: library versions, vendor channel limits, batch sizes, store rules (S2-P24-4704, S2-P24-4852); only some carry a verify marker.
- A fixed halting line in a non-English language and a "nothing ships without unanimous personas" rule are ceremony, not verifiable method (S2-P24-4626, S2-P24-4532).
- Private details embedded: the owner's name, a public repo path, a bundle id and a backend project id (S2-P24-4432, S2-P24-4704).

## GAPS
- WEB: nothing usable; this range forbids web output outright.
- PROMPT: only governance, receipt and ask-vs-proceed rules; no method for writing prompts or work orders.
- AUDIT: finding format and severity repeat earlier parts; no method for auditing a product canon for internal contradictions, though the range needed one.
- Design variety: one locked palette, font set and reference screen; no way to choose or vary a visual direction.
- Verification: every gate is silent; the receipt is the only visible evidence, and running tools (type-check, tests) is mentioned only once (S2-P24-5279).
- APP: strong on chat lists and real-time sync; thin on navigation structure, deep links, permission prompts, store submission.
- Token cost: about 1,500 lines, of which perhaps 60 lines of method transfer; loading it outside its product wastes context.

## PLACEMENT
- One decision per screen; primary action in the thumb zone; core action within 2 taps; no tutorials (S2-P24-4532, S2-P25-5393, S2-P25-5545).
- Choose the container (full screen, sheet, full takeover) plus zones and thumb path before building (S2-P24-4572).
- Screen spec lists sized zones, thumb path and every component's states and interaction record (S2-P24-4921).
- A pending critical decision stays visible across screens until resolved; every screen has an honest reason to reopen (S2-P24-4532).
- Use one exemplary existing screen as the reference for depth and spacing; ignore legacy screens (S2-P24-4472, S2-P25-5496).
- Depth: at least three elevation levels, separate shadow roles for content and for chrome (S2-P24-4721).
- Spacing on an 8pt grid with a banned list of off-grid values; touch targets at least 44pt iOS / 48dp Android (S2-P24-4721, S2-P25-5496).
- Monospaced digits for changing numbers so counters cause no layout shift (S2-P24-4721, S2-P25-5545).
- Native edges: safe areas on every edge, no pull-to-refresh or double-tap zoom on chat, dedicated keyboard handling, status bar follows theme (S2-P24-4721, S2-P25-5751, S2-P25-5759).
- Lists keep visible position when items arrive, pause on scroll-up with a new-items chip, throttle rendering rather than dropping (S2-P24-4892, S2-P24-5067).
- Visible states for offline, backpressure, cooldown and restriction-with-reason (S2-P24-4869, S2-P24-4892, S2-P25-5545).
- Vetoes: generic labels, contrast below AA, meaning by color alone, missing reduce-motion fallback (S2-P24-4532, S2-P24-4991).
