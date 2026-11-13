# Check-authoring spec A: web, app and design-diversity tasks (run name: A)

Read `SPEC-COMMON.md` (same directory) first. Then author everything below.

## Task one-liners (fixed; expand each into a full statement)
- SW1 (sealed, WEB): a bilingual landing page (English plus Hindi in Devanagari) for a fictional small
  business, five sections, contact form, mobile-first, no backend.
- DW1 (dev, WEB): a landing page in a different domain from SW1 and in a single language, otherwise
  comparable in size (sections, a form, mobile-first, no backend).
- SA1 (sealed, APP): an Expo two-screen app (list and detail, local persistence, one device permission),
  no backend.
- DIV1, DIV2, DIV3 (design-diversity, WEB, one screen each): DIV1 a broker-style trading dashboard
  (watchlist, chart, order ticket, portfolio, mock data only); DIV2 a children's story-learning site;
  DIV3 a heritage restaurant. Each brief states content and functional requirements only. It must NOT
  prescribe colors, fonts, layout or visual style: the visual design is the contestant's decision.

## Deliverable convention for web tasks (state it in every web task statement)
The finished site must be directly servable as static files from `out/site/` with `index.html` at its
root (a contestant who uses a build tool copies the built output there). No network access may be
required to render the page (fonts and scripts are local or fall back gracefully; the scorer blocks
external requests). Source files, if any, may sit elsewhere under `out/`.

## Web scorer: `evals/scorers/score_web.mjs` (used for SW1 and DW1, parameterized by the key)
Serve `out/site/` on a local port, drive Chromium through Playwright, block non-local requests. The
check families that MUST be covered (split each into as many atomic checks as is natural; aim for 20 to 30
checks per task):
1. Opens: index returns 200, renders real visible text, no uncaught page error on load.
2. Substance scan (see common spec), over delivered HTML, CSS and JS and over the rendered DOM.
3. Accessibility: axe-core serious plus critical violation count is zero, at 360 px and at 1280 px width.
4. No horizontal scroll at 360 px width.
5. Placement, measured in the browser: no two interactive elements overlap; no interactive element or
   text block lies outside the viewport horizontally at 360 px; the primary action named in the key is
   reachable (visible, enabled, not covered by another element at its center, reasonably large tap target
   at 360 px).
6. Document basics: `lang` on the root element, title, meta description, viewport meta.
7. Required content from the key: the required sections, the required strings. For SW1 the required Hindi
   strings must be present, must sit inside an element whose effective `lang` is `hi`, and the computed
   font stack on that element must include a Devanagari-capable family or a generic fallback strategy you
   define and document (be fair: do not require one specific font).
8. The form: every field has a programmatic label; submitting it empty shows a validation message and
   does not navigate away; submitting valid data shows a success state without any network call.
9. JavaScript weight: total gzip size of script loaded on first view is within the budget in the key
   (use 170 KB unless you have a reason to choose another number; say so in the statement).
Write keys `/tmp/forge-sealed/keys/SW1.json` and `/tmp/forge-sealed/keys/DW1.json` holding the parameters
(required strings, section identifiers, primary-action locator hints, budgets). The task statement must
give the exact required strings (for example the business name and tagline in both languages) so that the
checks are fair.

## Screenshot tool: `evals/scorers/shoot.mjs`
`node shoot.mjs --site <dir with index.html> --dest <dir>` writes full-page PNG screenshots at 360 px and
1280 px width (`360.png`, `1280.png`) with external requests blocked. Used later to build grader packets.

## App scorer: `evals/scorers/score_app.py` (SA1)
The deliverable is an Expo project under `out/` (state the exact root, for example `out/app/`). Static
contract checks, always run and labeled `static-only`: project manifest and app config are valid and
name an Expo SDK; two screens (list and detail) exist and are connected by navigation with a parameter;
the list reads from and writes to local persistent storage and data survives a restart by construction
(real read and write calls on a real storage API); exactly the device permission the statement asks for is
declared in the app config with a human-readable rationale string, requested at runtime at the point of
need, and the denied case is handled in the UI; touch targets carry accessibility labels; loading, empty
and error states exist; substance scan (no stubs, no empty `onPress`). Add an optional `--dynamic` flag
that runs `npm install` and `npx tsc --noEmit` in a temporary copy with a time limit and adds two checks
(install succeeds, typecheck passes); a probe on this machine showed a blank Expo SDK 58 TypeScript app
installs in about 30 seconds and 385 MB, typecheck 1 second. Key: `/tmp/forge-sealed/keys/SA1.json`.
Choose the permission and the app domain yourself and state them in the task statement.

## Fingerprint scorer: `evals/scorers/fingerprint.mjs` (DIV1 to DIV3)
`node fingerprint.mjs --site <dir> --json` extracts three axes from a rendered one-screen site at 1280 px:
- palette: dominant hue clusters of what is actually painted (weight by area), plus a background
  luminance class (light, mid or dark);
- type: the display family and the body family actually used (first available family of the largest
  heading and of body text);
- layout skeleton: the ordered sequence of landmark and section types (define a small vocabulary and the
  heuristics that map DOM regions to it).
`node fingerprint.mjs --compare <a.json> <b.json> --json` reports, per axis, a distance and whether the
axis counts as DIFFERENT under fixed thresholds. Choose the thresholds now, write them into
`evals/scorers/fingerprint-thresholds.json`, and self-test them: build a near-identical pair of pages
(same design, different copy) that must come out with 0 axes different, and a clearly different pair that
must come out with 3 axes different. Put the pairs under `/tmp/forge-sealed/selftest/FP/` and the outcome
in the RESULTS file. There is no key for DIV tasks.
Also write one grader rubric `evals/rubrics/DIV.md`: for each anonymous packet score domain fit from 1 to 5
(does the design suit this domain and audience, with reasons) and answer yes or no to "is this
indistinguishable from a generic template?".

## Self-test packets required in this run
SW1 good and degraded; DW1 good and degraded; SA1 good and degraded (static checks; run `--dynamic` once on
the good packet if time allows and report the result); the fingerprint pairs.
