# s2c review (S2 lines 2857-4418, Parts 11-23)

## STRENGTHS
- Execution loop with a stop condition and failure signals set before starting, plus risk-tiered confirmation (S2-P11-2860, S2-P11-2887) [CORE]
- Delegation contract: five-field brief, nothing assumed across the boundary, least privilege, separate grader with pre-written rubric, fan-out criteria (S2-P11-2899, S2-P12-2966 to S2-P12-3001) [CORE, PROMPT]
- Eval-first rules with a grading ladder and a rubric-agreement test (S2-P13-3038 to S2-P13-3066) [CORE, AUDIT]
- Zero-trust reading: instruction-shaped data reported, embedded claims not trusted, pre-action goal check, structural separation (S2-P14-3105 to S2-P14-3130) [CORE]
- Five-item compaction/handoff contract plus decision-log habit (S2-P15-3169, S2-P15-3178, S2-P11-2874) [CORE]
- Complete audit apparatus: six review passes, defect taxonomy, severity scale, eight-field finding, report schema with explicit ship bar (S2-P18-3431 to S2-P18-3462) [AUDIT]
- Router plus short proof-of-work receipt (modules, checks, stubbed vs live, assumptions, confidence) (S2-P21-3578, S2-P21-3591) [CORE]
- Fixed mutation-route order and a twelve-line done bar (S2-P22-3882, S2-P22-3979) [WEB, APP, AUDIT]

## FLAWS
- Self-graded superlatives: repeated claims that the system beats any single execution file or generic engine (S2-P20-3513, S2-P21-3613, S2-P22-3625, S2-P22-3995, S2-P23-4398).
- Contradiction: the final gate must run silently and not be printed (S2-P20-3521), yet the receipt must show which gates ran (S2-P21-3591). The restart-from-check-one-on-any-failure rule cannot be checked from outside.
- Unrealistic universal targets: a ten-thousand-user load test at a times-fifty multiplier, with malicious cohorts, for every concurrent feature (S2-P22-3759, S2-P20-3533). The 60fps-on-3GB and p95 budgets are presented as fixed law (S2-P22-3750).
- Unsafe content carried forward: honeypots, tarpits and instant permanent bans (S2-P20-3533, S2-P20-3521 tier 3).
- Example code bugs: a limiter called sliding-window that is actually fixed-window; an idempotent create that checks and then inserts with no unique constraint, so it can race (S2-P22-3930). The TS config example uses a non-null assertion that the rules next to it ban (S2-P22-3683 vs S2-P22-3639).
- Stale-prone pins: framework and library major versions, a database client API gotcha, a batch size set by the founder (S2-P22-3790, S2-P22-3817, S2-P23-4014, S2-P23-4204). Uncited "2026 studies" statistics (S2-P17-3353, S2-P18-3421).
- Repetition: maker/checker appears 3 times (S2-P11-2920, S2-P12-2984, S2-P22-3912). Just-in-time loading appears 3 times (S2-P11-2874, S2-P15-3197, S2-P21-3578). Real-time rules appear 3 times (S2-P22-3864, S2-P23-4245, S2-P23-4204). The stress test appears twice (S2-P20-3533, S2-P22-3759).
- Four persona lenses repeat an earlier four-role council (S2-P22-3912 vs S1-0050).
- Product stack lock-in is presented as universal: no styling library, no list library, cloud-only builds, a palette contrast note (S2-P23-4014, S2-P23-4064, S2-P23-4379).

## GAPS
- WEB: strong on security and performance, but there is no method for SEO, content, routing or information architecture, and no responsive breakpoint checks.
- APP: permissions are not covered (request timing, denial recovery). Deep links, back-stack behavior, push notification consent, store review rules and app size are also missing.
- PROMPT: the brief contract exists (S2-P11-2899), but there is no template for a full work order or for how to test a prompt.
- AUDIT: there is no evidence standard (repro steps, screenshots) and no rule for findings that cannot be verified. The report does not separate findings from recommendations.
- Verification: the dynamic pass is "reason like a fuzzer" with no step that actually runs a tool. Coverage and the load test are not tied to commands.
- Token cost: the codebook and the stack standards are large code blocks with little reusable method. Most of the value fits in about 30 lines.
- Design variety: none. This range is engineering only, and its one visual note is product-specific.

## PLACEMENT
- Safe-area insets on every edge; bottom navigation on the bottom inset; input bar clears keyboard and home indicator (S2-P23-4327, S2-P23-4179).
- Keyboard-tracking input keeps the last item visible; avoid the simple keyboard-avoiding wrapper on heavy chat screens (S2-P23-4179, S2-P23-4379).
- Scroll position stays stable when new items arrive; new items appear at the bottom of an inverted list (S2-P23-4091).
- Monospace digits for live counters prevent layout shift; no layout shift on dynamic numbers (S2-P23-4142, S2-P20-3521 tier 5).
- All states required: loading, empty, error, offline, throttled; skeleton matches the content (S2-P22-3979, S2-P22-3790, S2-P20-3521 tier 2).
- Visible pending marker on optimistic items, visible offline and busy states, no silent drop (S2-P23-4283, S2-P22-3864, S2-P20-3521 tier 7).
- Touch targets at least 44x44; visible focus ring; icon-only buttons named; meaning never carried by color alone (S2-P22-3735).
- Content text selectable, chrome not; no pull-to-refresh on live lists; status bar follows theme (S2-P23-4179, S2-P23-4327).
- Gesture conflicts on one element resolved by exclusive composition with distance and time thresholds (S2-P23-4179).
- Server-first rendering with client boundaries pushed to leaf components; per-route loading, error and not-found screens (S2-P22-3790).
- Release vetoes: listener-driven live list, unbounded list, JS-thread animation, full-res list images, phone-clock ordering (S2-P23-4379).
