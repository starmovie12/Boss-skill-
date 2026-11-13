# s2d digest: S2 lines 4419-5959 (method only; every number is the source's own claim unless marked "mine")
Range is two parts of canon for one named product plus a closing activation block. Only the method below transfers.

## 1. A product module that keeps later sessions consistent [CORE unless tagged]
- [S2-P24-4432, S2-P25-5356] Pin a truth order inside the module: live code > main spec > in-repo docs and constants > task cards > older docs. Review personas and lenses are process only; they never outrank product facts.
- [S2-P24-4432] Name the small fixed set of context files that enters every session, and re-read the live repo on top of them each time; memory of an earlier session is not evidence.
- [S2-P24-4675, S2-P25-5438] Put every user-visible label for statuses and titles in one constants file; a hardcoded copy anywhere else fails review.
- [S2-P24-4824] Once a price or other business constant is confirmed, centralize it in exactly one file; until then mark it OPEN and ask.
- [S2-P24-5307] Keep a divergence ledger: each code-vs-spec conflict carries a status (code wins / constants win / open, ask owner / migrate only when touching the file). Never build out features the spec has cut without confirmation.
- [S2-P24-4662] When an owner's standing rule contradicts a spec number, record both values and apply the owner's rule until told otherwise.
- [S2-P24-4704] Record the stack as verified from the repo; mark spec-only stacks dead and planned services not-yet-wired; log library traps found in real code with a verify marker.
- [S2-P24-4472, S2-P25-5496 | APP,WEB] Pick one existing exemplary screen as the quality reference for new screens (depth, spacing, color use) and ignore legacy screens.
- [S2-P24-4472] Lock app-content language separately from conversation language; rewrite wrong-language legacy strings whenever their file is touched. Rename legacy names only in files already being edited.
- [S2-P24-4472, S2-P25-5754] Suggest only tools the owner can actually run; check each new dependency works in their build path before adding it.
- [S2-P24-5279] Ask only for a closed list of owner decisions (data-model direction, open pricing, scope of legacy features, a real business-rule conflict); otherwise execute.
- [S2-P24-5291] Keep a per-project veto list where any single hit rejects the whole output; run it as the last pass.

## 2. Resolving canon conflicts [CORE]
- [S2-P24-4572, S2-P25-5888] Collision order: safety and legal floor > user's explicit instruction > security veto > performance budget over looks > accessibility AA > project design canon > platform conventions > token definitions > general practice.
- [S2-P25-5888, S2-P24-4432] Repo, spec and documents disagree: the repo wins for what exists, and the disagreement is flagged to the owner; never pick silently on a load-bearing point.
- [S2-P24-4869, S2-P24-5307] When an engagement tactic conflicts with the user-wellbeing rule, wellbeing wins; write that resolution down so the tension is not re-argued.
- [S2-P25-5792] A document that promises something a core invariant forbids is treated as a stale bug, not as a second source of truth.
- [S2-P24-4852, S2-P25-5768] Scale target vs current reality: honor the principles now, defer heavy scale pieces until a limit nears, and always state which pieces are stubbed and which are live.

## 3. Pre-build checklist [CORE; APP,WEB for the UI steps]
- [S2-P24-4572] Before emitting: restate the true intent; read target files and imports (data layer and access rules first if touched); pick the winning source and name conflicts; choose container (full screen, sheet, or full takeover), zones and thumb path; then stress-test.
- [S2-P24-4572] Stress over time: check the design at first second, mid-cycle, after many cycles, after a week; trace each mechanic's incentives two hops out; hunt the empty room, dropped connection, hostile actor, bored heavy user.
- [S2-P24-4626, S2-P24-5279] Design gate only for new major screens or systems: offer up to three options that differ in core mechanism (fewer if fewer are real), propose once, then defer. Small or scoped edits execute directly.
- [S2-P24-4939] Spec states testable acceptance criteria, numeric non-functional targets, edge/error/empty/offline cases and named abuse threats; plan resolves the riskiest unknown first with one-line decision records; work in small verifiable tasks.

## 4. Screen-spec format [APP, WEB]
- [S2-P24-4921] Order: intent; zones with sizes; thumb path (core action within 2 taps); components, each with interaction record and state matrix; copy; feedback per element; sad path and trust handling; what the spec forgot; honest reason to return; wellbeing check; reviewer sign-off.
- [S2-P24-4921] Interaction record: trigger; haptic type and timing; animation phases with named curve or spring and ms; visual feedback; which thread runs it; resulting state; abuse signal.
- [S2-P24-4921] State list to cover where applicable: idle, loading, empty, partial, success, error, offline, retrying, focus, pressed, disabled, throttled, cooldown, blocked, optimistic-pending, reconciled, permission-denied, failure-with-reason.
- [S2-P24-4532, S2-P25-5393] Screen vetoes: more than one decision per screen; primary action outside the thumb zone; more than 2 taps to the core action; tutorials; generic labels (Submit, OK, Item); a status change with no visible event.
- [S2-P24-4532] Continuity: a pending critical decision follows the user across screens until resolved; no critical decision is lost by navigating away.

## 5. Honest system states [CORE, APP]
- [S2-P24-4869] Every sent item ends in one visible state: delivered, rejected with reason, visibly queued, or visibly cooling down. Nothing is dropped silently.
- [S2-P24-4869] No shadow penalties: any restriction appears on the affected user's own screen with reason and appeal; rate limits trigger only at machine speed and are enforced server-side.
- [S2-P24-4892] Under bursts keep everything in local memory and throttle only rendering: batch the display, pause auto-scroll when the user scrolls up and show a new-items chip, keep visible position on arrival.
- [S2-P24-4892] Backpressure is shown: a visible send countdown first, then a rare visible "full, retry in N seconds".
- [S2-P24-4800] Show users the real math behind visibility or ranking (count reached, tier, time left); no hidden ranking.

## 6. Mobile engineering checks [APP]
- [S2-P25-5545] Leaks: every subscription, listener, timer and animation is cleaned up in the effect cleanup; channels unsubscribed on unmount; memory stays flat under a sustained burst.
- [S2-P25-5545] Offline-first: optimistic writes with guaranteed rollback; cache as read source; visible offline state; drafts and send queue persisted; idempotent retries; never a blank screen (labelled demo data while seeding).
- [S2-P24-4852] Live delivery over a pub/sub socket, never a database listener, with no synchronous DB read in the delivery path. Reconnect: subscribe and buffer first; fetch snapshot with server time; gap-fill from that time with no upper bound; merge, dedupe by id, sort by server time; render; release buffer; jitter reconnects.
- [S2-P24-5067, S2-P25-5545] Long lists: virtualized, memoized rows with custom equality, stable keys, capped mounted window with paging, sized and cached images; no inline object or function props into memoized rows. Mine: fixed row height only fits uniform rows.
- [S2-P24-4991, S2-P25-5665] Shared counters via atomic increment with server time; balances change only in a transaction that checks funds and writes an immutable ledger entry; the client never sets balance, score or role.
- [S2-P24-5238] Idempotent writes: the client mints an id per action and the server uses it as the record key (mine: a separate lookup-then-insert is racy).
- [S2-P24-4991] Exhaustive switch over a union with a never-typed default so a new case cannot go unhandled; validate external data with a strict schema and infer the type from it.
- [S2-P25-5732, S2-P25-5751, S2-P24-4721] Springs given as mass/stiffness/damping on the UI thread; bursts via refs, not state; reduce-motion fade fallback; haptics through one hook keyed by semantic intent; monospaced digits for changing numbers.
- [S2-P24-5067] Always test unhappy paths: offline, failed send rolled back, permission denied, empty, burst re-render; query components by accessibility label; mock backends at the boundary.

## 7. Verification, receipts, anti-regression [CORE, AUDIT]
- [S2-P25-5864 | APP] Before presenting UI code, walk its life: what mounts, held state, re-render triggers and memoization, UI vs JS thread work, data flow to reconcile, every reachable state, where a leak or dropped frame could occur.
- [S2-P24-5254, S2-P25-5864] Receipt: sections applied; gates run with headline result; stubbed vs live, named; assumptions where sources were silent; honest confidence with dated facts to re-verify.
- [S2-P24-4959] Review passes: static, security mapped to CWE, dynamic and race, performance and UX, final gate. Severity blocker / critical / major / minor / nit; ship at zero blocker and zero critical. Finding: file:line, category, severity, CWE, problem, impact, fix, proving test.
- [S2-P24-5211] Add one gate tier that checks the project's own non-negotiables next to the generic engineering tiers; any failure means fix and restart the gate.
- [S2-P24-5322] Never call a feature done from a document; open the real routes and modules and report what exists.

## 8. Safety and fairness method [CORE]
- [S2-P24-4869, S2-P25-5839] Engagement allowed, compulsion banned: cap emotional pushes per user per day server-side (source's claim: 3), dropping the excess rather than queueing; no hidden exits; no loss-pressure on real-money surfaces.
- [S2-P24-4869] Minors: block under-13 sign-up; protective defaults for teens (limited reach, no payouts, off public leaderboards, private location); refuse and flag any request that targets minors.
- [S2-P25-5839] Decide explicitly how an immutable financial ledger coexists with erasure and export rights before building either.
- [S2-P24-4824, S2-P25-5438] The platform never mints currency; promotions grant badges. Status grants ceremony, never moderation power. Inaction defaults to the user-safe outcome; transfers need an explicit tap.
- [S2-P24-4902] Paid cosmetics have fixed visible prices, never randomized crates; AI content always labelled, never ranked, and AI hosts go quiet once enough real users are present.
