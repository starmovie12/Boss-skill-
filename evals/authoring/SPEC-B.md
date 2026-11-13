# Check-authoring spec B: audit and prompt tasks (run name: B)

Read `SPEC-COMMON.md` (same directory) first. Then author everything below.

## Task one-liners (fixed; expand each into a full statement)
- SU1 (sealed, AUDIT): audit a small web-app fixture holding planted and unplanted defects.
- DU1 (dev, AUDIT): the same kind of task on a fixture written in a different stack from SU1.
- SP1 (sealed, PROMPT): write a work order for an unattended coding agent to build and deploy a small tool
  from a one-paragraph idea. Rubric-only task with neutral structural checks.

## Audit fixtures
Build two small but real applications (each roughly 8 to 20 source files, 400 to 1,200 lines in total, no
dependencies that must be installed to read the code): `evals/fixtures/SU1/` and `evals/fixtures/DU1/`,
in clearly different stacks (for example a Node server with a vanilla front end, and a Python web app with
templates). Each fixture:
- works in principle and reads like a real small product, with a short README;
- holds 8 to 12 PLANTED defects spread over several classes, each anchored to a specific file and line
  range, each a genuine defect (not a style preference), none marked by a comment;
- at least 3 of the planted defects per fixture must be of kinds that are NOT in this list of common
  kinds: hard-coded secrets, missing content-security policy, unsafe external links, missing form labels,
  low color contrast, small tap targets, missing `lang` attribute, missing meta or SEO tags, oversized
  script bundle, images without dimensions or lazy loading, TODO or placeholder stubs, dead buttons or
  empty handlers, horizontal scroll, overlapping elements. (Think of logic, concurrency, authorization,
  data-integrity, injection, resource and privacy defects.) The remaining planted defects may be of any
  kind, including kinds from that list;
- also contains a few real UNPLANTED imperfections, as any real code base does. These are not in the key.
The key (`/tmp/forge-sealed/keys/SU1.json`, `/tmp/forge-sealed/keys/DU1.json`) lists every planted defect:
id, class (from the fixed taxonomy below), file, line_start, line_end, one-line description.
Fixed class taxonomy (print it in the task statement so every contestant uses the same labels):
security, authorization, injection, data-integrity, concurrency, correctness, privacy, accessibility,
performance, dependency, configuration, ux.

## Audit task statement and deliverables
The contestant receives a copy of the fixture inside WORKDIR (state the path, `fixture/`). Deliverables:
`out/findings.json` (an array of findings, each with: `id`, `title`, `class` (from the taxonomy),
`severity` (critical, high, medium or low), `file` (fixture-relative path), `line` (1-based),
`snippet` (the offending code copied exactly, 1 to 10 lines), `impact`, `fix`) and `out/report.md`
(a human-readable report). State that findings must be backed by the quoted snippet, that the audit is
static (do not attack any live system), and that real defects beyond any expected list are welcome.

## Audit scorer: `evals/scorers/score_audit.py`
- Recall: a planted defect counts as found when some finding has the same class (allow a small documented
  set of near-equivalent class pairs, for example authorization and security) and the same file, and its
  line lies within the planted range widened by 3 lines either side. One check per planted defect.
- Fabrication: a finding is fabricated when its quoted snippet (whitespace-normalized) does not occur in
  the cited file within 5 lines of the cited line, or the file does not exist. Report
  `extra.fabrication_count` and add one check "zero fabricated citations". Real but unplanted defects are
  NOT penalized: a finding is false only if its citation fails to verify.
- Structure: `findings.json` parses and every finding carries all required fields with valid values;
  `report.md` exists and is not a stub. A few atomic checks.
`contract_score` = passed / total over all of these checks; also report `extra.recall`.

## Prompt task (SP1)
Write the one-paragraph idea yourself (a small, concrete, deployable tool; include 5 to 8 hard facts such as
its name, input, output, one constraint, the deploy target, one thing it must never do). Deliverable:
`out/work-order.md`. Scorer `evals/scorers/score_prompt.py` runs NEUTRAL structural checks only and labels
its output `structural-only`: file exists and is non-trivial; every hard fact from the key is carried into
the work order; it states measurable acceptance criteria (define an objective heuristic); it says what the
agent must do when blocked or when to stop; it names the deliverables and where they go; it has no
unresolved placeholders (TBD, bracketed blanks); length is within a sane range. Do not encode any
particular prompt-writing style. Key: `/tmp/forge-sealed/keys/SP1.json`. The rubric
`evals/rubrics/SP1.md` carries the real judgment: would an unattended agent, given only this work order,
build and deploy the right tool without asking anything? (clarity, completeness, measurable acceptance,
handling of ambiguity and failure, feasibility in a sandbox, absence of contradictions.)

## Self-test packets required in this run
SU1 good and degraded; DU1 good and degraded; SP1 good and degraded. A good audit packet finds most planted
defects with exact snippets; a degraded one finds few and contains at least two fabricated citations.
