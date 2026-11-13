# FORGE_STATE

- phase: PH1b field study (PH1 ledger PASS: 521/521 units, all fated)
- working branch: `claude/hopeful-fermat-35aqea` (mirror: `boss-skill-forge`)
- last commit: see `git log -1` on the working branch
- freeze hash: not set
- pull request: https://github.com/starmovie12/Boss-skill-/pull/1 (opened by the operator from the Claude Code UI; every push to the working branch updates it)
- next step: run field-study runs F1-F4 (prompts in session; brief at /tmp/forge-field/FIELD-BRIEF.md, rebuild from docs/GAPS.md if lost), then docs/FIELD-SYNTHESIS.md, then PH2 authoring runs A and B (specs in evals/authoring/).

## Done
- PH1 ledger: 521 units fated (`python3 tools/ledger_check.py --skip-field` PASS), digests in ledger/digests/, docs GAPS, FLAWS, STRENGTHS, CONTRADICTIONS, hashed ISOLATION-TOKENS.
- PH0 preflight: sources located and hashed (ledger/SOURCES.json), environment probed (docs/ENV.md), fresh facts (docs/FRESH-FACTS.md), unit rules + manifest (521 units), push probe.

## Resume notes
- Raw sources are NOT in the repo. A new session needs the three attachments again (or `_inbox/`), unpacked to `/tmp/forge-src/{prose/S1.md,prose/S2.xml,skill/}`; `tools/ledger_check.py --gen /tmp/forge-src/units` rebuilds shard listings.
- Shards: s1a s1b s2a s2b s2c s2d s3a s3b. Done so far: s1a s1b s3a s2a s2b s2c s2d. Extraction brief: recreate from `evals/authoring`-style notes in docs/DESIGN-DECISIONS.md if /tmp is gone (brief text is in the session transcript; per-shard prompts name the line ranges: s2a 1-1556, s2b 1557-2856, s2c 2857-4418, s2d 4419-5959 of S2; s3b = all archive files not covered by s3a).
- Second usage-limit stop on 2026-11-13 (resets were needed twice during PH1).

## Subagent counters (used / cap)
| Kind | Used | Cap |
|---|---|---|
| source extraction | 8 (all shards done) | 8 |
| field study | 4 launched (F2 done; F1, F3, F4 running) | 4 |
| fixture and key authoring | 0 | 2 |
| dev contestants | 0 | 8 |
| sealed contestants | 0 | 24 (12 in MVB) |
| design-diversity contestants | 0 | 4 (3 in MVB) |
| graders | 0 | 10 |
| proxy tests | 0 | 6 |
| fresh-context review | 0 | 2 |
| total | 12 | 68 |

Field-study fetches: 18 / 60 counted at PH0 (field/FETCHLOG-PH0.txt); run budgets F1 10, F2 12, F3 12, F4 8.

## Open decisions
- none

## Events
- 2026-11-13: the account's 5-hour usage limit hit during PH1 (three extraction agents stopped with HTTP 429). Agents were resumed from their transcripts after the reset. Budget now looks short: PH6 is planned as MVB and drop_order items 1-3 are expected to be WAIVED-BY-BUDGET unless usage allows.

## Labeled blockers
- FRESH-FACTS F9-F12: UNVERIFIED / BLOCKED-BY-ENV (hosts outside the Limited allowlist).
