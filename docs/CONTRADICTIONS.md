# Contradictions

## Operator-reported facts versus what was found (never fatal)

| Reported | Found | Note |
|---|---|---|
| Work order "v2_7" (chat message) | attached file says version 2.9 | executed 2.9 |
| .md about 172 KB | 172,230 bytes | match |
| .xml about 534 KB | 533,896 bytes | match |
| .skill about 692 KB zipped, about 3.6 MB unpacked | 691,912 bytes; 3,638,382 bytes | match |
| 77 files, 8 python scripts, 22 stack CSVs | 77 files, 8 .py, 22 stack CSVs (35 CSV in all, 4 JSON, 28 md, 1 xml, 1 txt) | match |
| One prose source is multi-part ("PART n OF 25") with laws L1 to L30, schemas A to N, 14 templates, version near v18 rev 3 | These facts are spread over three sources: S2 is the 25-part file; S1 carries 30 numbered laws, schemas A to N and 14 templates; the v18 marker belongs to the Brain inside S3 | recorded, units follow the real structure |
| Network level "Trusted or Full" | Current names are None, Limited, Full (FRESH-FACTS F6) | final report uses current names |
| Gemini Gem instructions | Gems are reported to be migrating to Gemini skills (FRESH-FACTS F10, unverified) | E3 carries a fallback |

## Conflicts between source units (rule: universal beats specific, verifiable beats asserted, shorter wins ties)

| Conflict | Resolution in BOSS | Rule applied |
|---|---|---|
| S2-P10-2688 (always halt after offering three paths) vs S2-P10-2770 (follow an explicit instruction) | Offer options only for large new screens and only when a human is present; otherwise choose, record the rejected options in `_boss/decisions.md`, continue (P-2) | universal beats specific; protects the unattended operator |
| S2-P25-5393 (seven-mind sign-off) vs S2-P24-4532 (thirteen-chair sign-off) | Both dropped: persona sign-offs change no output; the review is a concrete checklist with recorded results | verifiable beats asserted |
| S2-P25-5468 (no web code at all) vs S2-P22-3790 (web standards) | BOSS is universal: WEB and APP are both first-class modes; the ban is product canon (QUARANTINE) | universal beats specific |
| S3-F:references/design-system/tailwind-integration.md (legacy space-separated color channels) vs S3-F:data/stacks/shadcn.csv (bans them) | BOSS ships no framework config snippets; token method says "map semantic tokens through the project's current theme layer, verify against current framework docs" | verifiable beats asserted; stale-prone detail not shipped |
| S2-P00-0194 (present paths and halt) vs S2-P01-0369 (continue to completion) | Continue to completion (P-2) | universal beats specific |
| S2-P04-1523 (no reconnect replay) vs S2-P02-0796 and S2-P04-1313 (gap-fill and reconciliation required) | Reconnect = resubscribe, buffer, gap-fill from server time, dedupe by id; never silently drop | verifiable beats asserted |
| S1-0710 announces 18 states, lists 19; S1-3083 likewise | State list sized to the component; no fixed count | shorter wins and is checkable |
| S3-B-0148 (dark mode only if needed) vs S3-F:references/pro-rules-and-predelivery.md (always test both themes) | Dark mode only when the brief or platform needs it; when shipped, contrast is measured separately per theme | universal beats specific |
| S3-B-0148 (uniform durations banned) vs S3-F:references/ux-rules-full.md (unify duration tokens) | A small named set of duration tokens chosen by distance and importance; not one value for everything | both kept as one checkable rule |
| Touch floor stated as 48 everywhere (S3-F:references/tests-gates.md) vs 44 pt iOS / 48 dp Android / 24 CSS px web (S3-F:references/icons-tokens-states.md) | 44 px minimum for web and iOS-style targets, 48 px for the primary mobile action (work order placement gate); WCAG 2.2 minimum 24 CSS px cited as the legal floor | the work order is more specific |
