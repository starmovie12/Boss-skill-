# Overmatch: every source strength, its BOSS counterpart, and the Q-7 upgrade axis

Axes: sharper (trigger, action, check explicit), cheaper (fewer tokens, same effect), verifiable (a script, screenshot
or checklist catches a miss), adaptive (works across projects). Status here is design intent; whether BOSS output
actually beats the sources is NOT MEASURED (benchmark deferred, docs/NEXT-SESSION.xml).

## S1
| Strength | BOSS counterpart | Axis | How it exceeds |
|---|---|---|---|
| ST-S1-1 state table | PL-5, DS-6, QG-1 | adaptive, cheaper | states sized to the component instead of 18 fixed rows |
| ST-S1-2 interaction record | DS-5, DS-6, PL-5 map rows | cheaper | one map row per transition instead of seven fields per gesture |
| ST-S1-3 accessibility checklist | W1, A1, AC-A11Y; axe in boss_verify | verifiable | axe at two widths replaces a self-ticked list |
| ST-S1-4 handler order, atomic writes | AC-SEC, K5 | verifiable | audit hunts it with evidence; no code snippets to go stale |
| ST-S1-5 exact-value table | PROMPT R3 | cheaper | one rule ("replace vague words with numbers") plus prompt_lint |
| ST-S1-6 audit finding record | U4, audit_report.py | verifiable | citations checked against files |
| ST-S1-7 attacker questions | AC-SEC | cheaper | grouped hunting list across classes |
| ST-S1-8 stress-plan shape | QG-1, PROMPT R2.5 | adaptive | stress rows for UI; load tests sized to expected load |
| ST-S1-9 native app spec | A0, A7, A11, ST-3/4 | sharper | permission timing and denied path, store data-safety match |
| ST-S1-10 work-order skeleton, skipped-with-reason | PROMPT R2, K7 | sharper | stop rules, budgets and status words required |

## S2
| Strength | BOSS counterpart | Axis | How it exceeds |
|---|---|---|---|
| ST-S2-1 project ingestion | P-6, U1 | cheaper, adaptive | sampling rule for large repos |
| ST-S2-2 shelf-life and confidence | P-3, ST header (UNVERIFIED limits) | verifiable | labels on every claim |
| ST-S2-3 nine lenses + stress passes | U2 coverage matrix, AC lists | adaptive | lenses no longer tuned to one product type |
| ST-S2-4 prompt craft | R3 | cheaper | same rules in a third of the text |
| ST-S2-5 requirement tests, completeness gate | R3, AUDIT spec defects | sharper | four tests applied to every requirement |
| ST-S2-6 spec audit taxonomy and severity | AC spec defects, U5 | cheaper | one severity scale for code, UI and specs |
| ST-S2-7 diverge then converge | W4, PL-0 | verifiable | two-layer difference rule + fingerprint across projects |
| ST-S2-8 execution loop with stop rule | W9, U7, PROMPT R2.6 | sharper | revert and two-revert stop |
| ST-S2-9 delegation brief, handoff | PROMPT R2.9 (state file) | cheaper | state file instead of a council |
| ST-S2-10 eval ladder, gauntlet schema | W0 acceptance, U4 | verifiable | deterministic checks first via scripts |

## S3
| Strength | BOSS counterpart | Axis | How it exceeds |
|---|---|---|---|
| ST-S3-1 size router | K1 | cheaper | five lines, same behavior |
| ST-S3-2 evidence labels, layers, receipt | P-3, K7 | cheaper, verifiable | three labels, three lists, scripts produce VERIFIED lines |
| ST-S3-3 acceptance before design | W0, A0 | verifiable | a file whose timestamp precedes design files |
| ST-S3-4 text-only placement plan | W5, A5, PL-1 | verifiable | `primary:` line compared by placement_check |
| ST-S3-5 no-shortcut zone, safety floor, priority order | K4, K5, K6 | sharper | one order, applied in kernel |
| ST-S3-6 platform edge cases, responsive checks, states | PL-4, PL-5, PL-7 | verifiable | geometry measured at two widths |
| ST-S3-7 gate stack and veto list | QG-1 to QG-6 | cheaper | 31 veto questions folded to 16 |
| ST-S3-8 three paths, anti-generic two-layer rule | PL-0, W4, DS-8 | verifiable | design_fingerprint across projects |
| ST-S3-9 verify-first scripts, archetype heuristics | DS-7, PL-8 | sharper | five render checks plus exception note format |
| ST-S3-10 token tiers, state model | DS-1, DS-6 | adaptive | no fixed values; derived per project |

## Placement block (docs/STRENGTHS.md PL-S-1 to PL-S-20)
| Source mechanism | BOSS | Axis |
|---|---|---|
| PL-S-1 text plan before styling | PL-1, K3 design gate | verifiable (gate files) |
| PL-S-2 platform first | PL-1 | sharper |
| PL-S-3 five questions per element | PL-1 table | cheaper (one table row per element) |
| PL-S-4 frequency grading | PL-1, PL-2 | sharper |
| PL-S-5 one primary action | PL-1, QG-5 | verifiable (placement_check primary) |
| PL-S-6 thumb zone, proximity, order | PL-2 | verifiable (zone check) |
| PL-S-7 corner conventions, one home | PL-2 conventional positions | adaptive (web and app) |
| PL-S-8 destructive and money placement | PL-2, K5, FT-2 | sharper |
| PL-S-9 container by stakes | PL-2 | cheaper |
| PL-S-10 hiding vs pinned bars, keyboard | PL-2 | sharper |
| PL-S-11 platform edge cases | PL-4 | cheaper |
| PL-S-12 responsive checks | PL-7, placement_check | verifiable |
| PL-S-13 states and transition map | PL-5 | sharper |
| PL-S-14 icon discipline | PL-6 | cheaper |
| PL-S-15 touch floor, focus order | W1, A1, placement_check small targets | verifiable |
| PL-S-16 layer scale, dimension block | DS-1 tokens, PL-2 occlusion | verifiable (covered-element check) |
| PL-S-17 stress matrix for placement | QG-1 | sharper |
| PL-S-18 lost feature and veto | PL-3 trace table, QG-6 | verifiable |
| PL-S-19 regression and consistency | QG-3, QG-4 | sharper |
| PL-S-20 landing action placement, heuristic limits | PL-2, PL-8 | adaptive |

## Brain mechanisms required by the work order (sources/brain_priority)
| Mechanism | BOSS rule | Axis |
|---|---|---|
| Per-element placement planning | PL-1 | verifiable |
| Zone and proximity rules | PL-2 | verifiable |
| Per-platform edge cases | PL-4 | cheaper |
| State transition map | PL-5 | sharper |
| Responsive checks | PL-7 + placement_check | verifiable |
| Veto list blocking delivery | QG-6 | cheaper |
| Task-size routing | K1 | cheaper |
| Acceptance test before designing | W0, A0 | verifiable |
| No-shortcut zone | K5 | sharper |
| Three different paths for large new screens | PL-0 | sharper |
| Anti-generic audit (two layers beyond color) | W4, DS-8, design_fingerprint | verifiable |
| Verify-first Devanagari fonts | DS-7 | sharper |
| Evidence labels and three-list receipt | P-3, K7 | cheaper |

Rejected strengths: none. Product-specific canon (navigation skin, economy, council personas) was quarantined in the
ledger and never counted as a strength.
