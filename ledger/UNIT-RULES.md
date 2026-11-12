# Unit rules

A unit is the smallest block of a source that gets exactly one fate. Units are regenerated from the raw
sources by `tools/ledger_check.py` (regex and file list), never typed by hand. The ledger holds ids, line
spans, a 12-hex sha256 prefix of the unit text, a neutral one-line summary, up to three mechanism notes and
a fate. It never holds source text.

| Source | Marker discovered | Unit rule | Id form | Count |
|---|---|---|---|---|
| S1 (markdown) | `###` headings (laws, schemas, templates, sub-sections) and `##` banner groups, outside code fences | one unit per `###` heading; one per `##` banner group (consecutive `##` lines count once); front matter plus title banner is one unit | `S1-<line>` | 70 |
| S2 (25-part XML) | one `<..._master_prompt part=…>` element per part; rule-carrying child tags at 2-space indent | one unit per 2-space child tag of each part (CDATA skipped); a unit longer than 120 lines is split at its 4-space child tags; text before the first tag of a part is a preamble unit | `S2-P<part>-<line>` | 347 |
| S3 (archive) | 77 files; one file is a decision-rule XML (the Brain) whose top-level child tags each carry a distinct rule | one unit per file (76), except the Brain, which is one unit per top-level child tag (28) | `S3-F:<path>` / `S3-B-<line>` | 104 |

Total 521 units. `ledger/EXPECTED-UNITS.json` is the committed manifest (ids, spans, hashes) used when the
raw sources are absent; the check then reports `manifest-only`.

## Fates

KEEP-CORE, KEEP-MODE(WEB|APP|PROMPT|AUDIT[,…]), KEEP-REFERENCE, QUARANTINE (product-specific, never ships),
QUARANTINE-DESIGN (fixed color, font, layout or component-skin prescription; the reasoning may survive as
method; placement, platform, state, icon and gate rules never get this fate), DROP(reason), CONFLICT(id)
(resolved in docs/CONTRADICTIONS.md).

A KEEP fate means the mechanism is a candidate. Whether it ships, and upgraded on which Q-7 axis, is decided
in docs/OVERMATCH.md and docs/RULE-AUDIT.md.
