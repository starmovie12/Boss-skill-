# s2b review (S2 lines 1557-2856)

## STRENGTHS
- The audit engine is complete and portable: a 20-category defect taxonomy, written severity criteria, a 7-field fix protocol and a report shape with an explicit pass bar. Units S2-P09-2534, 2606, 2615, 2627 (AUDIT).
- Spec construction gives concrete acceptance-criteria tooling: requirement tests, 23 canonical sections each with a "must contain" list and a common failure, and a 14-item gate. Units S2-P08-2284, 2441, 2453, 2300..2432 (PROMPT, AUDIT).
- The prompt-writing craft is specific and checkable: section order, the agent reminders (persist, verify with tools, plan and reflect), conflict handling, long-context sandwiching, edit format and strict JSON. Unit S2-P05-1731 (PROMPT).
- The output contract and self-check form a usable pre-delivery gate (no truncation, manifest with named skips, examples agree with the rules). Units S2-P05-1560, 1791 (CORE).
- Option generation has real guards: options must differ in their core mechanism, there is no padding to hit a count, the user's explicit choice is binding, and outputs are treated as hypotheses. Units S2-P10-2757, 2770, 2810 (CORE, WEB, APP, PROMPT).
- The testing strategy works by risk and layer, always covers unhappy paths and treats coverage as a diagnostic only. The localization rules are complete. Units S2-P06-1997, 2006.
- The work starts from the repo (read the manifest and sibling files, live code wins) and keeps a conflict ledger with resolved and open entries. Units S2-P06-1829, S2-P07-2226, 2134 (CORE).
- Phone-only operations are covered: a tool map, no desktop steps, package checks, and a reduced version with stubbed-versus-live disclosure for a solo operator. Units S2-P06-1949, S2-P07-2173 (WEB, APP).

## FLAWS
- Unit S2-P10-2688 forces a halt with exactly three paths and a fixed Hinglish question on every task. This contradicts S2-P10-2770 (an explicit instruction is followed), S2-P10-2757 (no fixed count) and S2-P05-1560 (no preamble).
- Unit S2-P05-1585 demands an ARIA label, role, tabindex and key handler on every interactive element. That is over-ARIA: native elements should come first.
- Unit S2-P05-1675 sets universal pass numbers (100% of malicious traffic banned within 5 minutes, zero false positives, zero memory growth). These are unrealistic as universal gates, and the unit says to "regenerate" on failure with no method for doing so.
- Units S2-P05-1634 and 1658 make honeypots, tarpits and instant permanent bans a standard part of every security deliverable. That is heavy-handed and not universal.
- Self-graded or unsourced claims:
  - "measurably raises quality" for personas (S2-P05-1777);
  - "sandwich outperforms" (S2-P05-1731);
  - "would anyone remember it" as a finish test (S2-P10-2788);
  - "10x every single time" (S2-P10-2702).
- Stale or vendor-locked facts:
  - exact framework versions (S2-P07-2052);
  - a fixed animation-library version, a no-Lottie absolute and a 60 fps on 3 GB target (S2-P06-1839);
  - a vendor subscriber cap (S2-P07-2173, though the unit itself says to verify it).
- The rules are rigid: every spec carries all 23 sections (S2-P08-2300), "survive 50x load" applies universally (S2-P08-2348, S2-P09-2593), and the weight calibration is deferred to a later part (S2-P08-2507, S2-P09-2643).
- Unit S2-P10-2728 says to "leave hooks now" for 10-step futures. That invites over-building and works against scope discipline.
- Repetition and ceremony: S2-P06-2015 repeats 1829, 1923 and 1949; S2-P10-2797 repeats 2673; S2-P07-2239 is self-praise; S2-P10-2661 and 2819 are motivational.
- Product leakage into the universal parts: a product-specific ceremony sequence and the reference screen in S2-P06-1839, a batch size of 400 in S2-P06-1923, and the house direction in S2-P05-1698.

## GAPS
- Phone-only operations covers building and shipping but not on-device testing: no steps for installing a development build, scanning a preview, reading logs or debugging from the phone (S2-P06-1949). The WEB mode also has no phone-only preview or deploy flow.
- APP: the unit has no store-submission, signing, privacy-declaration or review-rejection procedure, and it is tied to one framework family (S2-P06-1839, S2-P05-1667).
- WEB: the playbook is tied to one framework (S2-P06-1910). Responsive checks stop at "mobile-first". There is no viewport list and no overflow or tap-target sweep.
- PROMPT: the prompt craft lacks scope boundaries, stop conditions, explicit "done means" checks and anti-overbuilding rules for work orders. Borrow the requirement tests from Part 8 to fill this.
- AUDIT: findings carry no evidence or confidence label, there is no step to re-verify fixes, there is no dedupe or cap on findings, and the engine is spec-focused, with no code or UI audit variant except the security report.
- Verification: every gate in this shard is self-assessed. Nothing requires running a tool, measuring a number or citing output as proof.
- Design variety: the aesthetic method lists fixed named presets. There is no procedure for choosing a direction from the audience, brand or content, and diverge-converge never touches visual design concretely.
- Token cost: the 23 sections, 20 defect categories and 14 schemas would be costly to load always. They need on-demand loading and scaling by task weight.

## PLACEMENT
- S2-P05-1573: blueprint per section. Exact height, width, min and max, padding, margin, layer order by name, safe-area edges, per-breakpoint changes, and layout mode, direction, alignment and gap.
- S2-P05-1585: style layering with every component state and mobile-first responsive rules; semantic landmarks for the page regions.
- S2-P05-1667: native spec. Safe-area insets for the notch and gesture bar.
- S2-P06-1839, navigation and input: navigation above the home indicator; the input accounts for keyboard plus indicator; a keyboard controller keeps the last message visible.
- S2-P06-1839, lists and sheets: new items appear at the bottom; reading position holds when items arrive. The sheet's inner scroll does not fight its drag, and its z-order composes with the router's gesture layer.
- S2-P06-1839, motion: fixed-width digits for counters and timers, so there is no layout shift; reduced-motion fallbacks.
- S2-P06-1910: loading, error and not-found siblings per route; skeletons shaped like the content; explicit image dimensions to stop layout shift; the main above-fold image gets priority.
- S2-P06-2006: layouts sized for text expansion and mirrored for right-to-left.
- S2-P07-2087 (quarantined values, keep the method): fixed chrome heights with a stated sum; large titles that collapse on scroll; touch targets of at least 44 pt or 48 dp; a flush bottom bar plus the safe area.
- S2-P07-2197: visible staged degradation under load, with a "new items" chip on scroll-up instead of jumping the reader.
- S2-P08-2354, S2-P09-2558, S2-P09-2534 (D05, D18): every screen state is enumerated (default, loading, empty, error, offline, success, throttled, disabled, partial), and any missing state, copy, keyboard or screen-reader behavior is an audit finding.
- S2-P05-1791: the design pre-check must pass for exactly what ships before delivery.
