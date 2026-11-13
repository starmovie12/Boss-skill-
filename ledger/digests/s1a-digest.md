# s1a digest: S1 lines 1-1667 (own words; every number is the source's own claim unless marked "mine")

## 1. Planning before output
- [S1-0213 | CORE] Name the deliverable type plus modifiers (realtime, offline, multi-tenant, localized, edge) before planning; an unclassified task is not started.
- [S1-0213 | CORE] Decompose first: list every section, component, state, variant, edge case, route, table, access rule, error boundary, loading/empty/skeleton state, shortcut, label, test name, env var. Source floor: 16 items for full-stack, 10 for UI-only. Exit check: every listed item is present in the output.
- [S1-0213 | CORE] Conflict order: 1 explicit user instruction, 2 security, 3 performance budget, 4 accessibility AA floor, 5 house UX rules, 6 platform guidelines, 7 token definitions, 8 general practice. Write each resolution down; a clash that cannot be settled without hurting security or accessibility is declared as a hard constraint at the top of the output.
- [S1-0213 | CORE] A planning step that does not apply (threat model on UI-only work, concurrency on single-user features, observability, AI) is written as "not applicable" with a reason, never silently skipped.
- [S1-0213 | CORE] Flag truncation-prone sections up front (state tables, access rules, type definitions, animation specs, error handling, tests) and commit to writing them in full.
- [S1-0213 | WEB,APP] Architecture is declared, not implied: server/client split per component, cache policy per route, runtime per endpoint, schema + indexes + access rules, navigation stack, realtime provider/channels/reconnect/ordering, AI model + budget + fallback; full-stack work gets an ASCII data-flow diagram.
- [S1-0213 | WEB,APP] Shared-state plan: partition key, channel naming pattern, target concurrent users (100 / 1K / 10K / 100K) with backpressure, race class (counter, balance, seat claim, queue) and its fix (transaction, sharded counter, optimistic lock, ordered consumer), presence heartbeat + stale cutoff, write coalescing or sharding for any record written more than once per second.
- [S1-0213 | WEB,APP] Observability plan: error tracking with personal-data scrubbing, structured logs with correlation ids, funnel metrics, health endpoint with dependency checks, alert thresholds.
- [S1-0696 | CORE] Placeholder scan before delivery: ellipsis, "etc.", TODO, bracketed stubs, "same as above", "similar to", "rest of implementation". Complete each hit or declare it out of scope. (Source says length is never a reason to cut; mine: treat as a default, not an absolute.)
- [S1-0480 | WEB,APP,PROMPT] Exact-value rule: size with unit; timing in ms; easing as a full curve; springs as mass/stiffness/damping; haptic by named type; numeric font weight; decimal opacity; layer from a named scale; blur in px; contrast as N:1; cache time in seconds; rate limit as N per M seconds; bundle delta in KB gzip; concurrency and partition counts as integers. Vague words (fast, large, rounded, readable, scalable, reasonable, lightweight) fail review. Mine: only state numbers that were measured or deliberately chosen, never invented.

## 2. Review lenses and veto list  [S1-0050 | WEB,APP,AUDIT]
- Four lenses (design, security, delivery weight, data); one veto blocks release until fixed (source demands a full restart).
- Design veto: cluttered hierarchy; raw color values; desktop-first layout; animation without curve or spring spec; contrast under 4.5:1; touch target under 44x44px.
- Security veto: race conditions; missing rate limits; missing CSRF or CSP; prompt-injection paths; object-ownership holes; security decisions trusted to the client; session token in browser local storage; no audit log on financial operations; unvalidated webhooks; SSRF surfaces.
- Delivery veto: bundle growth over 20KB gzip without reason; server-only APIs in edge routes; cold start over 50ms; interaction delay risk over 200ms; unoptimized image or font loading; a dependency over 50KB that does not earn its weight.
- Data veto: read-modify-write races; single-record hot writes; missing indexes; N+1 queries; unbounded queries; wildcard access rules; cross-region writes lacking a conflict strategy; serial awaits that should run in parallel.
- Extra floor items: each form field has four validation states (idle, focus, valid, error); keyboard equivalent for every action; interaction response under 150ms; retries use exponential backoff and circuit breakers; personal data collection justified, retention bounded, deletion and consent paths present.

## 3. State matrix  [S1-0710 | WEB,APP]
- One table per interactive component. Columns: state | visual change (tokens + dimensions) | haptic (type + timing, or none) | animation (curve + ms, or none).
- Rows (heading says 18 minimum, table lists 19): 1 default/idle; 2 hover (web only); 3 keyboard focus (ring, 2px offset); 4 press-in (scale); 5 press-release (bounce); 6 long-press; 7 drag-active (shadow, scale, layer); 8 loading (shimmer or spinner); 9 streaming output (cursor blink); 10 live-update pulse (1500ms loop); 11 success; 12 error (shake); 13 warning; 14 throttled (message, warning haptic); 15 banned (banner + lock, error haptic); 16 disabled (dedicated tokens, not lowered opacity); 17 empty/zero-data (illustration + copy); 18 skeleton (1500ms shimmer); 19 offline/stale (banner). Domain-specific states are appended in the same columns.
- Mine: rows 9, 10, 14, 15 are situational; the universal set is idle, hover, focus, pressed, loading, success, error, warning, disabled, empty, skeleton, offline/stale.

## 4. Interaction record  [S1-0745 | WEB,APP]: seven parts per gesture
- 1 Trigger: type (tap, long-press, swipe direction, pinch, scroll, drag, hover, focus, blur, key), threshold in px/ms/force, target size, debounce or throttle in ms.
- 2 Haptic: named type; fire timing (start, at N ms, completion, overshoot peak, none); platform (iOS, Android, none on web).
- 3 Animation phases: per phase the property, start and end, duration, easing; spring phase with overshoot and mass/stiffness/damping; total duration; native-driver flag on React Native; will-change property.
- 4 Visual feedback: change type (highlight, ripple, glow, scale, rotation, border flash, or a shift of color, shadow or blur); token before and after; transition; reduced-motion fallback.
- 5 Performance path: compositor, main thread, native UI thread, or GPU-composited, with a cost note.
- 6 State result: final UI state; navigation side effect; API side effect (endpoint, method, optimistic or confirmed); state mutation; follow-on haptics.
- 7 Behavior signal: logged event name, risk weight 0 to 1, anomaly flags, throttle hook. Abuse-detection add-on; mine: optional outside sensitive surfaces.

## 5. Accessibility thresholds  [S1-0810, S1-0050 | WEB,APP,AUDIT]
- Targets: at least 44x44px (Apple guidance) or 48x48dp (Material guidance).
- Contrast: body text at least 4.5:1 (AA floor), 7:1 as AAA aim; large text (18px regular or 14px bold and up) at least 3:1; state the measured ratio.
- Focus: visible outline 2px wide with 2px offset; the outline is never removed without a replacement.
- Semantics: label on icon-only buttons; roles where needed; disabled state exposed to assistive tech; polite live region on dynamic areas; busy flag while loading; expanded and controls attributes on toggles; errors tied to inputs by a description attribute.
- Keyboard: Tab reaches every control; Enter/Space activate; Escape dismisses; arrows move within lists and menus; Home/End jump to first/last; a command-palette shortcut.
- Motion: every animation has a reduced-motion branch with a concrete static alternative.
- Every async state change is announced through a live region. Color is never the only carrier of meaning (pair it with icon, label or pattern).
- Focus management: dialog open -> first element; dialog close -> back to the trigger; route change -> page heading.

## 6. Performance thresholds  [S1-0050, S1-0213, S1-0841 | WEB,APP]
- Field targets at p75: largest paint at most 2.5s, interaction-to-next-paint at most 200ms, layout shift at most 0.1. Bundle regression cap 20KB gzip unless justified; edge cold start at most 50ms; interaction response aim under 150ms.
- Pre-check per deliverable: name the largest-paint element and its load path; list interaction-delay risks (heavy script, slow handlers); list shift risks (images without dimensions, late-injected content); estimate bundle delta; pick image formats and lazy boundary; font loading strategy; reconnect with exponential backoff plus jitter; cap or partition fan-out above 1K subscribers.
- Render-path rule: animate transform and opacity (compositor); avoid animating height, background or shadow (layout or repaint); blur is GPU-costly, test on low-end devices; the above-fold hero image gets load priority; prefer server-side data fetch over client waterfalls; wrap non-urgent updates in a transition.

## 7. Security checklist an auditor can run  [S1-0864, S1-0213, S1-1370 | AUDIT,WEB,APP]
- [ ] Handler order: server-side auth on every request -> (optional abuse or ban check) -> rate limit -> safe body parse -> strict schema validation that rejects unknown keys (blocks mass assignment) -> logic on validated data only.
- [ ] Status codes: 401 unauthenticated, 403 banned, 429 with limit, remaining and retry-after headers, 400 for bad JSON or failed validation with field issues.
- [ ] Concurrency: every change to a shared balance, stock, seat or counter runs in a transaction, an atomic server-side function, or an atomic batch; hot counters (over 1 write/sec) are sharded and summed on read. A separate read followed by an update on shared data is a finding.
- [ ] Value creation: every balance increase traces to an allowed source (verified payment webhook handled idempotently, peer transfer with both sides in one transaction, server-verified admin grant, server-triggered reward with idempotency key).
- [ ] Audit trail: each balance change writes an immutable entry (id, actor, counterparty, type, direction, amount, balance before and after, source reference, IP, truncated user agent, server timestamp); the audit store is unreadable and unwritable from clients.
- [ ] Access rules (least privilege): owner-only reads; updates limited to an allow-list of editable fields; privileged fields (balance, role, email, ban flag, risk score) never client-writable; create and delete denied unless needed; no wildcard rules.
- [ ] Rate-limit profiles exist per action class. Source values: read 60/60s, write 10/10s, financial 5/60s, auth 5/15min fixed window, AI 10/min token bucket, realtime messages 100/60s.
- [ ] Headers: HSTS with long max-age and subdomains; frame restriction; no-sniff; strict-origin-when-cross-origin referrer policy; permissions policy disabling unused device APIs; CSP with default self, nonce-based scripts, no objects or frames, restricted base-uri and form-action, explicit connect and image origins. (Source also sets the legacy XSS header and allows inline styles: both are weak spots.)
- [ ] LLM input: untrusted text only in the user role inside delimiters, never concatenated into the system prompt; length cap; model output validated against a schema with an enumerated action; per-user rate limit; fixed output-token cap. (The source's regex stripping is a weak supplementary layer.)
- [ ] Object ownership: every client-supplied id is checked against the session user; a mismatch returns not-found (not forbidden) and is logged as an abuse signal.
- [ ] Threat-model table per input, write and external call: vector (XSS, injection, CSRF, SSRF, broken object or function auth, mass assignment, race, replay, token tampering, path traversal, privilege escalation, data exposure, credential stuffing, bot abuse) -> named defense -> confirmation that no surface is unprotected.
- [ ] Active-defense plan (optional): slow responses for suspicious callers, decoy endpoints that flag callers, auto-ban thresholds (source example: 5 failed logins in 60s -> 24h ban), replay nonce or timestamp window, bot challenge, reputation per IP, user and device.

## 8. Testing, CI, secrets  [S1-1443, S1-1517, S1-1548, S1-0213 | WEB,APP]
- Tests per handler: one per rejection path (401, 403, 429, each 400 variant such as invalid payload, self-target, insufficient balance) plus a success test asserting the side effect (audit entry created). Schema unit tests: negative, over max, unknown field, valid. End-to-end: main flow and one graceful failure.
- Coverage floor (source): every happy path, every defined error path, every veto item. Security tests: auth bypass, injection payloads, ownership bypass, replay.
- Load thresholds (source): p95 request time under 500ms, failure rate under 1%. Source also demands a 10K-user / 1K-attacker / 60s simulation; unverifiable without real infrastructure.
- CI order on push and pull request: clean install -> type-check -> lint -> unit -> integration -> build -> end-to-end -> stress -> security regression -> page-performance audit. Any failure blocks.
- Secrets: parse the whole environment through a schema at startup (format checks such as key prefix, URL shape, minimum secret length 32) and crash on failure; server-only values kept apart from public-prefixed ones; no admin service key in the repo; no payment secret in the client bundle.

## 9. Reference patterns (load on demand)
- [S1-1170 | WEB] Server by default; client only for local state, effects, handlers, browser APIs, realtime, canvas or charts. Dynamic regions behind a loading boundary with content-shaped skeleton. Utility scale only; arbitrary values only to reference tokens.
- [S1-1266 | WEB,APP] Async state as a discriminated union; never cast external data (parse with schema, infer type); catch as unknown; named constants; strict compiler flags.
- [S1-1582 | WEB,APP] Optimistic update: cancel reads, snapshot, apply, roll back on error, refetch on settle (mine: not for money).
- [S1-1414 | WEB] Cache strategy per resource class; pending state for offline writes; sync on reconnect.
- [S1-1481 | WEB,APP] Scrub personal fields from error reports; structured JSON logs with a security level; funnel events with reason codes.
- [S1-1607 | WEB,APP] No hard-coded user-facing strings; complete message file per locale; locale-aware date, number and currency formatting.
- [S1-1622 | WEB,APP] Token change log: type, old -> new, reason, migration, breaking flag, affected components.
- [S1-1640 | WEB,APP] Doc block: purpose, params with constraints, thrown errors, return, security notes.

## 10. Design tokens: reasoning only (names and values are QUARANTINE-DESIGN)  [S1-0509]
- Role-named color tokens (surface levels, text levels, on-color text, status + subtle partner, borders, shadows, overlays) make contrast pairs auditable and theming a one-place change; grep for raw literals outside the token definition file.
- Closed scales: spacing on a 4px grid, radius steps, five motion durations (0 to 600ms), named easing curves, named layer order (base < raised < floating nav < dropdown < sticky < overlay < modal < notification < tooltip < command palette).
