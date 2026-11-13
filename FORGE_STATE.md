# FORGE_STATE

- phase: PH1 ledger (extraction running)
- working branch: `claude/hopeful-fermat-35aqea` (mirror: `boss-skill-forge`)
- last commit: see `git log -1` on the working branch
- freeze hash: not set
- pull request: https://github.com/starmovie12/Boss-skill-/pull/1 (opened by the operator from the Claude Code UI; every push to the working branch updates it)
- next step: finish shards s1a s1b s3a (running), then launch s2a s2b s2c s2d s3b (`/tmp/forge-src/units/<shard>.tsv` -> `ledger/units/<shard>.jsonl`), then run `python3 tools/ledger_check.py --skip-field`.

## Done
- PH0 preflight: sources located and hashed (ledger/SOURCES.json), environment probed (docs/ENV.md), fresh facts (docs/FRESH-FACTS.md), unit rules + manifest (521 units), push probe.

## Resume notes
- Raw sources are NOT in the repo. A new session needs the three attachments again (or `_inbox/`), unpacked to `/tmp/forge-src/{prose/S1.md,prose/S2.xml,skill/}`; `tools/ledger_check.py --gen /tmp/forge-src/units` rebuilds shard listings.
- Shards: s1a s1b s2a s2b s2c s2d s3a s3b. A shard is done when `ledger/units/<shard>.jsonl` is committed.

## Subagent counters (used / cap)
| Kind | Used | Cap |
|---|---|---|
| source extraction | 3 (s1a, s1b, s3a; resumed once after a usage-limit stop) | 8 |
| field study | 0 | 4 |
| fixture and key authoring | 0 | 2 |
| dev contestants | 0 | 8 |
| sealed contestants | 0 | 24 (12 in MVB) |
| design-diversity contestants | 0 | 4 (3 in MVB) |
| graders | 0 | 10 |
| proxy tests | 0 | 6 |
| fresh-context review | 0 | 2 |
| total | 3 | 68 |

Field-study fetches: 0 / 60.

## Open decisions
- none

## Events
- 2026-11-13: the account's 5-hour usage limit hit during PH1 (three extraction agents stopped with HTTP 429). Agents were resumed from their transcripts after the reset. Budget now looks short: PH6 is planned as MVB and drop_order items 1-3 are expected to be WAIVED-BY-BUDGET unless usage allows.

## Labeled blockers
- FRESH-FACTS F9-F12: UNVERIFIED / BLOCKED-BY-ENV (hosts outside the Limited allowlist).
