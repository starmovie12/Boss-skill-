# s1b review (S1 lines 1668-3770)

## STRENGTHS
- Audit finding record with location, exploit scenario, impact, proof, complete fix and a test proving the fix; severity counts by band up front (S1-2603, S1-3343) [AUDIT].
- Seventeen concrete attacker questions per state-changing route, answerable by reading code (S1-2380) [AUDIT, WEB, APP].
- Stress plan shape: named cohorts with counts and behavior, numeric pass criteria, observation list, rollback rule (S1-2340, S1-2813) [AUDIT].
- Blueprint section template that forces exact sizes, safe-area edges, breakpoint deltas, edge-case records, dark-mode delta and contrast per pair (S1-2436) [WEB, APP].
- Single-file site order and stylesheet layer order; component file order (S1-2498, S1-2514) [WEB, APP].
- Native app spec: permission-with-purpose table, build profiles, deep links, secure storage, size and cold-start budgets (S1-2769, S1-3585) [APP].
- Work-order skeleton with requester-only slots, numbered measurable requirements, count gate, output and acceptance clause (S1-3281, S1-3373, S1-3318) [PROMPT].
- Many scan-checkable checklist items, plus the explicit "skipped with reason" manifest rule and the realtime publish pipeline (S1-2938, S1-2529, S1-2243) [CORE, REF].

## FLAWS
- Invisible self-grading: 100-item audit must run silently and never be printed; latency percentiles are "passed" by mental simulation; persona consensus is a check (S1-2938, S1-2340, S1-3677).
- Heavy repetition: the header/profile-image rule appears about twelve times (S1-2071, S1-2410, S1-2436, S1-2498, S1-2938 twice, S1-3083, S1-3281, S1-3318, S1-3373, S1-3499, S1-3558, S1-3677); templates 9, 10, 13, 14 restate laws and schemas number for number.
- Contradictions: three channel-naming patterns (S1-1673 has two, S1-2938 check 78 a third); subscriber/presence caps 10K vs 5K vs 1K (S1-1673, S1-2243, S1-2639); six ban rules vs seven, and non-appealable bans vs an appeal list (S1-1812 vs S1-2718); 403 in code vs "404 not 403" check (S1-1673 vs S1-2938).
- Spec arithmetic errors: "18-state" matrix has 19 rows; 56px targets inside a 64px bar with 8px padding; jitter comment says plus-or-minus but code only adds and can exceed the stated cap (S1-3083, S1-1673).
- Defects in the "law" code: score written by subject but read by user id, window argument ignored, "moving average" comment over a plain sum, nonexistent store command, CSRF check passes when both origin headers are absent (S1-1975, S1-1812).
- Safety: mandates decoy endpoints with fake errors, deliberate stalling, and single-hit permanent non-appealable bans on user/IP/device (one decoy path is hit by ordinary bots), then makes them audit requirements (S1-1812, S1-2718, S1-3530, S1-2938 checks 48-51).
- Rigid universal rules: every multi-user feature geo-partitioned; one mandatory nav skin, font trio and motion default; 21-file manifest; 18+ states including "banned" on every component; forced 400ms loading hold; compositor hint on every animated property; ARIA attributes on every interactive element (S1-1673, S1-2071, S1-2529, S1-2938, S1-2498).
- Blanket or unverifiable claims: deployable first attempt, zero-bug, top assurance level, "zero exceptions / zero truncation", 100% attacker detection with zero false positives (S1-3677, S1-3226, S1-2340, S1-2813).
- Possibly stale or wrong facts: year label on the web top-ten taxonomy; edge free-tier limits; pinned model ids and framework/SDK versions; a storage plugin listed as encrypted; limited browser support for the reduced-transparency query (S1-2603, S1-2314, S1-3400, S1-3585, S1-2769, S1-2498).
- Self-contradicting hygiene checks: "zero raw values" while tokens must be defined with raw values and the laws' own CSS uses raw px, blur and bezier numbers; placeholder scan bans ordinary words (S1-2938 checks 1-2 vs S1-2071).

## GAPS
- WEB: no content, copy, SEO or asset guidance beyond meta tags; no real-browser verification (render, console, screenshots at each width, measured performance).
- APP: native spec stops at configuration; nothing on platform navigation patterns (back gesture, stack vs tabs), permission-request UX, store review, native accessibility (text scaling, screen readers), device test matrix.
- PROMPT: templates are stack-locked orders addressed to this one engine; nothing on audience, context to include, examples, success criteria, evaluation of a prompt, or non-code prompts.
- AUDIT: only a security report shape; no UX, accessibility, performance or content audit shape; no evidence standard (how verified, confidence, what was not checked), no prioritization, effort or executive summary.
- Design variety: a fixed 16-name menu plus one mandatory nav/font/motion baseline (S1-2901 vs S1-2071) drives every output toward the same look.
- Verification: every gate is internal assertion; nothing requires running code, tests or scans or separating verified from assumed.
- Token cost: about 2,100 lines, large single-stack code blocks, each law restated in schemas, audit, templates and summary (three to five times); 14 templates share one skeleton.
- No scope sizing (when 21 files or 100 checks are overkill), no clarifying questions, no handling of an existing codebase or design system beyond one change-log line.

## PLACEMENT
- Zone allowlist/denylist: header holds brand, title, back, search, notifications, one contextual action; account identity lives once, at the end of the bottom bar, in thumb reach; reason: one predictable "self" anchor, no competing identity surfaces; verified by scan (S1-2071, S1-2410, S1-2938 checks 88-89).
- Fixed bottom bar geometry: centered, side margins, max width, bottom offset = spacing + bottom safe-area inset; same result on notch, home-indicator and gesture-bar devices (S1-2071, S1-3083, S1-2938 check 90).
- Mobile-first: base at narrowest target (source 380px; then 414/768/1280), min-width steps up, tablet/desktop as deltas (S1-2071, S1-3373, S1-3558, S1-2938 check 86).
- Blueprint dimension block per section: min/max sizes, per-side padding/margin, safe-area edges, z-layer from a named scale, per-breakpoint layout delta, max lines with truncation (S1-2436; S1-2938 checks 5, 11).
- Tab order method: fixed slot order, emphasized primary action in the middle, unread badge on activity, self last; focus order left to right; active item flagged for assistive tech (S1-3083; the specific order is quarantined).
- States and transitions: full state list per component with explicit N/A; press-in/release, focus ring, hover, loading, disabled, skeleton, offline; blocked state replaces the bar; offline pill 8px above the bar, auto-dismiss 3s after reconnect (S1-3083; S1-2938 checks 21, 30-33).
- Focus placement: dialog open -> first focusable; close -> back to trigger; route change -> heading; async changes announced in a live region (S1-2938 checks 27-28).
- Hit areas and rhythm: targets >= 44x44px / 48x48dp verified per element, whole tab is the hit area; spacing on a 4px grid; radius, shadow, z from scales (S1-2938 checks 12, 15-17; S1-3318; S1-3083).
- Motion placement: animate transform/opacity only; each phase has property, range, ms, easing; reduced-motion = instant; blur = solid fallback (S1-3083, S1-2071, S1-2938 checks 23-24).
- Page structure order: semantic landmarks header/nav/main/section/article/footer; stylesheet layers in fixed order with responsive rules last, mobile-first (S1-2498).
- Route-level states: each async page ships loading (content-matched skeleton), error (retry) and not-found (way back) siblings (S1-2529; S1-2938 checks 30, 32, 67).
- Native insets and gate: per-platform safe-area handling, nav adapted to insets (S1-2769, S1-3585); any failed placement check blocks delivery, and vetoes are checked by scan rather than assertion (S1-2938, S1-3677).
