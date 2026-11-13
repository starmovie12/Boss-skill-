# s2a review (S2 lines 1-1556)

## STRENGTHS
- Nine-step project ingestion: full intake, written source-of-truth order, project model, conflict map with OPEN items, closing report of live vs stubbed vs assumed (S2-P01-0504) [CORE]
- Safety floor ranked above user instruction, paired with a concrete behavior: state the conflict and offer the safe path (S2-P01-0354) [CORE]
- Shelf-life law: every hard external number is a dated claim to re-verify or caveat, with headroom when unconfirmable (S2-P02-0883) [CORE]
- Layout law plus stakes-based container choice and per-list scroll map give real placement rules, not taste (S2-P03-0989, S2-P03-1096) [WEB,APP]
- Thirteen-item design preflight folds tokens, motion, placement, states, copy and icons into one gate (S2-P03-1148) [WEB,APP]
- Nine audit lenses, each with a core question, probe list and fixed finding record, plus a cross-lens compound scan (S2-P04-1239 to S2-P04-1397) [AUDIT]
- Four stress passes with timeline checkpoints and an A to D friction rubric tied to ship or no-ship (S2-P04-1413, S2-P04-1483) [WEB,APP,AUDIT]
- Epistemic discipline: confidence per claim, self-disproof before delivery, contradictions surfaced, three-way triage (S2-P04-1498) [CORE]

## FLAWS
- Reader-directed activation and "permanent brain" claims repeat at four places (S2-P00-0001, S2-P00-0014, S2-P00-0194, S2-P01-0344); part counts disagree: 25, sixteen, nine, seven, and 21 called authoritative (S2-P00-0015, S2-P00-0194, S2-P00-0222).
- Contradiction: activation orders presenting three paths and halting before any build, while the working behaviors order continuing to full completion without stopping at a plan (S2-P00-0194 vs S2-P01-0369).
- Contradiction: prohibitions ban reconnect replay and reconciliation for network blips, while the realtime law requires gap-fill from history and lens six asks for next-session reconciliation (S2-P04-1523 vs S2-P02-0796, S2-P04-1313).
- Hidden gates: the pre-work routine, lens gauntlet and final checklist are to run silently, so none can be verified; any single veto demands restart from step one (S2-P01-0567, S2-P01-0391, S2-P04-1510, S2-P03-1165).
- Imagined measurement: a load-and-attack simulation run mentally with latency and error pass criteria, bills computed with no data, a fixed fifty-times multiplier (S2-P02-0796, S2-P04-1239, S2-P04-1204).
- Unsourced or stale-prone figures stated as fact: user-per-engineer counts, per-tap drop-off, retention loss on creator exit, bot-suspicion threshold, a 14-day trust window, one country's intermediary threshold, breach-notice window, edge runtime budgets (S2-P04-1230, S2-P04-1371, S2-P04-1351, S2-P02-0842); the shelf-life law (S2-P02-0883) is never applied to them.
- Blanket legal claim that machine moderation of private messages is prohibited and servers must be unable to read them, applied to every product regardless of jurisdiction or type (S2-P04-1204, S2-P04-1523).
- Rigid universals: no truncation whatever the length; nothing may appear instantly; linear easing banned; common button words banned; nineteen states per component; seven fields with haptic and abuse score per gesture (S2-P01-0450, S2-P02-0627, S2-P03-0975, S2-P03-1067, S2-P03-1021, S2-P03-1037).
- Active-defense kit (instant permanent bans, decoy endpoints, graduated delays) pushed as default on every value-mutating surface with no false-positive handling beyond an appeal flag (S2-P02-0659).
- Repetition: state matrix, interaction record, exact-value and no-truncation rules duplicate S1; five principles restate the palette-to-type rules; the floor is stated three times; the final checklist restates earlier gates; heading says 18 states, list has 19 (S2-P03-1001, S2-P03-1021, S2-P04-1510, S2-P01-0450).

## GAPS
- WEB: no responsive breakpoint method, no desktop or keyboard-first layout, no content hierarchy, information architecture or search visibility; the layout law is thumb-first mobile only.
- APP: no permissions, deep links, store review, tablet or landscape, system back gesture or OS-version edge cases; the native-feel list is shaped by a chat product.
- PROMPT: nothing on writing prompts or work orders in this range beyond exact values and one-owner hygiene; the wrapper itself (shouting, repetition, threats) is a counter-example.
- AUDIT: lenses are tuned to social, economy and realtime products; none covers accessibility, measured performance, content quality or plain correctness; no severity scale, evidence standard or report layout here; "skip none" gives no way to drop lenses that do not fit a site or utility app.
- Design variety: the design part claims brand neutrality yet presumes a warm premium look, one accent, three type families and a calm-plus-celebration mood; no method for choosing among directions.
- Verification: gates are self-attested; no step runs a tool (contrast check, literal search, screenshots at several sizes, test run) and shows output; contrast ratios are "known", never measured.
- Token cost: about 1,550 always-loaded lines, roughly 340 of them wrapper, index and handoff recaps; lenses alone about 160 lines; no triage, so small tasks get the council, nine lenses and four passes.
- No clarifying-question step beyond missing files; ingestion says read everything but gives no sampling rule for a repo too large to read whole.

## PLACEMENT
- Layout law: 8-point token grid; 44pt / 48dp targets with extended hit area; one primary decision per screen; full-width primary action where thumb or focus rests; core action within 2 taps (S2-P03-0989; echoed in S2-P01-0391, S2-P01-0567).
- Fixed corners and single homes: back top-left only; contextual actions top-right, 2 at most; identity surface in exactly one place; one navigation anatomy reused (S2-P03-0989, S2-P03-1148).
- Planning order before any UI is written: choose container (screen, sheet, takeover), then zones, sightlines, thumb path, and which state survives navigation (S2-P01-0567); every element has a zone, sightline, reason and path (S2-P01-0450).
- Container by stakes: full screen for focused high-stakes input, bottom sheet for quick picks, persistent takeover for must-resolve decisions; live surfaces keep context (S2-P03-1096); a pending critical decision follows the user across surfaces (S2-P01-0391).
- Transition map: each navigation event typed (push/pop, sheet, crossfade, shared element) so motion encodes deeper, sideways or new context (S2-P03-1096).
- Scroll map per list: direction, refresh on or off, sticky headers, item-height strategy, keyboard behavior, new-item behavior (auto-scroll at bottom, badge when scrolled up), pagination, empty state (S2-P03-1096, S2-P03-1057).
- Platform edges: bottom navigation above the home indicator; input bar clears keyboard and home indicator; status bar matches canvas; input rises to keyboard top with last message visible; no pull-to-refresh on live lists; selection only on content (S2-P03-1057).
- States keep elements in place: per-component state table including empty, skeleton, offline; disabled via its own token; skeleton shaped like content with fade to real content; inline banner instead of full-screen wipe for blips (S2-P03-1021, S2-P03-1110).
- Interaction record ties each gesture to its final UI state and navigation side effect (S2-P03-1037).
- Icons and labels: one family, fixed action-to-icon dictionary, size and color map per context (navigation, header, inline, button-leading, list, status) (S2-P03-1087); labels only from one dictionary (S2-P03-1067).
- Layout-shift guards: fixed-width digits for live numbers; fixed item heights in lists; placeholders instead of blank areas (S2-P03-0964, S2-P03-1057, S2-P04-1230).
- Gates and vetoes: design preflight (S2-P03-1148); reviewer vetoes for over 2 taps, over 1 decision, primary action outside thumb zone, target below minimum (S2-P01-0391); conflict order ranking accessibility and platform conventions above token definitions (S2-P01-0567); build gate (S2-P04-1510). Missing: responsive breakpoints, desktop and landscape checks.
