# FORGE_STATE

- phase: PH1 ledger (extraction running)
- working branch: `claude/hopeful-fermat-35aqea` (mirror: `boss-skill-forge`)
- last commit: see `git log -1` on the working branch
- freeze hash: not set
- pull request: https://github.com/starmovie12/Boss-skill-/pull/1 (opened by the operator from the Claude Code UI; every push to the working branch updates it)
- next step: finish shards s2a s2b s2c (a shard is done when `ledger/units/<shard>.jsonl` and `ledger/digests/<shard>-digest.md` are committed), then launch s2d and s3b, then `python3 tools/ledger_check.py --skip-field` (`/tmp/forge-src/units/<shard>.tsv` -> `ledger/units/<shard>.jsonl`), then run `python3 tools/ledger_check.py --skip-field`.

## Done
- PH0 preflight: sources located and hashed (ledger/SOURCES.json), environment probed (docs/ENV.md), fresh facts (docs/FRESH-FACTS.md), unit rules + manifest (521 units), push probe.

## Resume notes
- Raw sources are NOT in the repo. A new session needs the three attachments again (or `_inbox/`), unpacked to `/tmp/forge-src/{prose/S1.md,prose/S2.xml,skill/}`; `tools/ledger_check.py --gen /tmp/forge-src/units` rebuilds shard listings.
- Shards: s1a s1b s2a s2b s2c s2d s3a s3b. Done so far: s1a s1b s3a s2a s2b s2c s2d. Extraction brief: recreate from `evals/authoring`-style notes in docs/DESIGN-DECISIONS.md if /tmp is gone (brief text is in the session transcript; per-shard prompts name the line ranges: s2a 1-1556, s2b 1557-2856, s2c 2857-4418, s2d 4419-5959 of S2; s3b = all archive files not covered by s3a).
- Second usage-limit stop on 2026-11-13 (resets were needed twice during PH1).

## Subagent counters (used / cap)
| Kind | Used | Cap |
|---|---|---|
| source extraction | 8 launched (s1a s1b s3a s2a s2b s2c s2d done; s3b running) | 8 |
| field study | 0 | 4 |
| fixture and key authoring | 0 | 2 |
| dev contestants | 0 | 8 |
| sealed contestants | 0 | 24 (12 in MVB) |
| design-diversity contestants | 0 | 4 (3 in MVB) |
| graders | 0 | 10 |
| proxy tests | 0 | 6 |
| fresh-context review | 0 | 2 |
| total | 8 | 68 |

Field-study fetches: 0 / 60.

## Open decisions
- none

## Events
- 2026-11-13: the account's 5-hour usage limit hit during PH1 (three extraction agents stopped with HTTP 429). Agents were resumed from their transcripts after the reset. Budget now looks short: PH6 is planned as MVB and drop_order items 1-3 are expected to be WAIVED-BY-BUDGET unless usage allows.

## Labeled blockers
- FRESH-FACTS F9-F12: UNVERIFIED / BLOCKED-BY-ENV (hosts outside the Limited allowlist).
