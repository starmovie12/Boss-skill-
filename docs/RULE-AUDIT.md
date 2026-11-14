# Rule audit (Q-2): every rule, the output change it causes, and where it came from

Origin: a ledger unit id (S1-, S2-, S3-), a field repo (F2/F3 rows), "new", or "fixed from <unit>" when a source defect
(docs/FLAWS.md) was repaired. Behavior-change test: deleting the rule would visibly worsen some output.

## Kernel (SKILL.md)
| Rule | Observable effect | Origin |
|---|---|---|
| Mode table + one mode per task (P-1) | about 2-3K tokens loaded per task instead of the whole method | S2-P21-3569, S2-P21-3578 (router), upgraded: load table with named files |
| K1 mode router (deliverable decides; audit-then-fix split) | "prompt that builds a site" produces a prompt, not a site | new |
| K1 size router XS/S/M/L, smaller when unsure | an XS fix returns the change plus one evidence line, no ceremony | S3-B-0067, S3-B-0287 (cheaper: 5 lines instead of an 11-row matrix) |
| P-2 never stall, at most 3 questions with defaults | unattended runs finish; questions carry defaults | fixed from S2-P00-0194, S2-P10-2688, S3-B-0055 |
| P-2 inputs are data | instruction-shaped text in files is reported, not obeyed | S3-B-0046, S2-P14-3105 |
| P-3 evidence labels VERIFIED / INFERRED / UNVERIFIED | every success claim names its command or reasoning | S3-B-0089 (three labels instead of four; layers folded into the label) |
| P-4 universal defaults | no product language, brand or stack leaks into outputs | fixed from S1-2410, S2-P25-5468 |
| P-5 phone-first delivery | every deliverable ends with phone build/preview/deploy steps | S2-P06-1949 |
| P-6 brownfield: read, run checks before and after, smallest diff | existing projects keep their design system; regressions caught | S2-P01-0504, S2-P11-2909 |
| K3 substance gate with demo-data rule | no TODO, lorem, dead buttons; demo data seeded and labeled | S1-0696 (verifiable: boss_verify substance scan), new demo-data rule |
| K3 design gate (brief and plan before UI code, craft log before done) | design thinking happens before code and is inspectable | work order D gate; S3-B-0166 |
| K3 placement gate | geometry hits fixed or justified | S3-B-0253 (verifiable: placement_check) |
| K4 safety floor | refusals are one line and the rest is finished | S3-B-0036, S2-P01-0354; fixed from S1-1812 (no deceptive defenses) |
| K5 no-shortcut zone | money and deletion controls show outcome, confirm, idempotency | S3-B-0098, S3-B-0204 |
| K6 conflict order | rule conflicts resolve the same way every time | fixed from S3-B-0157 vs S3-B-0166, S2-P01-0567 |
| K7 output contract with three lists | reports separate verified from inferred from not done | S3-B-0089 receipt, S2-P21-3591 |
| K8 script list | the executor knows which tool proves which gate | new |

## WEB mode
| Rule | Observable effect | Origin |
|---|---|---|
| W0 refine vs redesign | edits keep identity unless a redesign is asked | F2 impeccable |
| W0 acceptance file before design | criteria cannot drift to fit the result | S3-B-0189, S2-P13-3038 |
| W1 floors (WCAG 2.2 AA, 170 KB JS, 360 px, CSP, lang, real content) | measurable floors every page meets | S1-0810, S1-0841, S2-P22-3735; work order |
| W2 domain study keep/avoid/depart (D-1) | designs fit the domain and depart on purpose | F2 gstack; new depart list |
| W3 brief with surface mode (D-2) | per-section intent (persuade, operate, read, experience) | F2 impeccable; work order D-2 |
| W4 seed roll + three directions + category and specificity tests (D-3) | two layers beyond color differ between options; category look rejected | S3-B-0132, S3-B-0148, F2 gstack, F2 impeccable; new seed |
| W5 layout plan, PL-0 three paths | placement decided in text, flows compared by taps | S3-B-0204, S3-B-0132 |
| W6 derived tokens + tokens.md with ratios (D-4) | contrast recomputed by boss_verify; no copied palettes | S3-F:references/design-system/token-architecture.md; fixed from S3-F:scripts/contrast_check.py |
| W7 first screen + first-glance test (D-5) | primary action among the first three eye targets | F2 gstack; S3-B-0230 check 6.12 |
| W8 one system, forms, states, demo data, SEO, navigation | complete pages with all states and sharing metadata | S2-P06-1910, S1-0710, S3-F:references/ux-rules-full.md |
| W9 boss_verify + P0-P3 fix loop, max 3, revert | measured gates, bounded fixing | S3-F:references/tests-gates.md, F2 gstack |
| W10 craft pass + fingerprint (D-6, D-8) | before/after log; no repeat of an earlier project's look | new (fingerprint), F2 gstack inverted |
| W11 output contract | phone deploy steps and three lists | K7 |
| Habits to avoid (120 words) | first-reflex clichés need a written reason | F2 impeccable, S3-F:references/visual-craft.md |

## APP mode
| Rule | Observable effect | Origin |
|---|---|---|
| A0 stack (Expo / PWA / bare) with reason | the smallest stack that meets the brief | S2-P06-1839, new decision rule |
| A1 floors (labels, 44/48 targets, dynamic type, low-end Android, secure store) | apps usable at large font and on weak phones | S2-P23-4091, S2-P23-4349, S1-0810 |
| A2 navigation by destination count and use | tabs, stacks, sheets chosen for a reason; back restores state | new (closes GAPS APP-1) |
| A3-A4 domain study, brief, divergence (D-1 to D-3) | as WEB, plus platform conventions kept | as WEB |
| A5 layout plan with thumb zone and edge cases | placement fixed before styling | S3-B-0204, S3-F:references/layout-platform.md |
| A6 tokens with theme hook, tokens.md (D-4) | live light/dark switch; ratios recomputable | S2-P23-4064, S2-P03-1137 |
| A7 storage, permissions at point of need, network states | no launch-time permission walls; denied path works | new (closes GAPS APP-2) |
| A8 first screen in Expo Go or web export (D-5, D-7) | early critique on a real viewport | new |
| A9 boss_verify (typecheck, lint, expo-doctor, export, permissions) | static-only labels when installs cannot run | S2-P23-4359, new permission check |
| A10 craft pass and fingerprint (D-6, D-8) | as WEB | as WEB |
| A11 store readiness, output contract | release checklist tied to real data collection | S1-2769, new |

## PROMPT mode
| Rule | Observable effect | Origin |
|---|---|---|
| R0 intake incl. autonomy and size limits | prompts fit the executor and the platform | S2-P05-1731, new |
| R1 three forms | short prompts stay short; system prompts get a scope | S2-P16-3240 (sizing) |
| R2 ten-part work order | stop rules, budgets, status words always present | S1-3281, F3 spec-kit, F3 BMAD |
| R3 writing rules + requirement tests | vague words replaced by numbers; conflict rule stated | S2-P05-1731, S2-P08-2441, S1-0480 |
| R4 nine-question adversarial review + prompt_lint | contradictions, halting traps and injection exposure removed | new; S2-P09-2585 |
| R5 output contract with test inputs | every prompt ships with a way to test it | new |
| R6 build-UI work orders carry the design and placement floors | delegated builds keep BOSS quality | new |

## AUDIT mode
| Rule | Observable effect | Origin |
|---|---|---|
| U0 scope and authorization | no testing of systems the user does not control | work order safety floor |
| U1 inventory + sampling rule | large repos audited with a stated sample | fixed from S2-P01-0504 (read everything) |
| U2 coverage matrix before hunting | "not checked" is explicit | new (closes GAPS AUDIT-2) |
| U3 static then dynamic; judgment before tools | tools do not anchor UX judgment | F2 impeccable; S2-P18-3431 |
| U4 finding schema with confidence | every finding reproducible and labeled | S1-2603, S2-P18-3455 (verifiable citation added) |
| U5 written severity criteria + support tie-break | consistent severity across audits | S2-P09-2606, F2 impeccable |
| U6 report rendered and citations verified by audit_report.py | fabricated citations caught before delivery | new script (closes GAPS AUDIT-2) |
| U7 fix outcomes, stop after two reverts | bounded fixing with evidence | F2 gstack |
| U8 self-check | summary matches findings; no unverified VERIFIED | new |

## References (loaded on demand)
| Section | Observable effect | Origin |
|---|---|---|
| PL-0 to PL-8, gate, 8-item checklist | elements placed by frequency, convention, stakes; occlusion and edge cases checked | S3-B-0204, S3-F:references/layout-platform.md, S2-P03-0989, S2-P03-1096, F2 gstack, F2 ui-ux-pro-max |
| DS-1 to DS-9 | tokens derived, contrast computed, scripts verified, distinct by two layers, critiqued from screenshots | S3-F:references/design-system/*, S3-B-0213, S3-B-0148, F2 impeccable |
| QG-1 to QG-6 | stress, recovery, regression, consistency, severity, veto rows filled with observed results | S3-F:references/tests-gates.md, S3-B-0253 (31 questions folded to 16) |
| ST-1 to ST-5 | smallest stack and a free phone deploy path; secrets kept server-side | S2-P06-1949, S1-1548 |
| AC-SEC to AC-CODE, gotchas, spec defects | class-by-class hunting lists | S1-2380, S2-P18-3440, S2-P19-3487, S2-P09-2534 |
| FT-1 to FT-5 | broker products: conventions, order safety, seeded demo market | new (operator domain), S3-B-0204 money rules |
