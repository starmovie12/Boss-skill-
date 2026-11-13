# s3b review (65 units: design-system references, 39 data files, 8 scripts)
Ids abbreviated: DS:x = S3-F:references/design-system/x.md, R:x = S3-F:references/x.md, D:x = S3-F:data/x, ST:x = S3-F:data/stacks/x.csv, SC:x = S3-F:scripts/x.py.

## STRENGTHS
- Three-tier token method with dark mode as a semantic-only delta, paired on-colour roles, may-use/may-not-use per token, hex written once in a measured palette table [DS:token-architecture, DS:semantic-tokens, R:visual-tokens-recipes] WEB,APP.
- Full state model: six states, precedence order, two-layer focus ring, loading/error/disabled treatments wired to assistive-tech attributes [DS:states-and-variants, DS:component-specs] WEB,APP,AUDIT.
- Verify-first script coverage: never trust a font name; catalog or file check, explicit fallback, five render checks, honest label; plus a lookup tool [R:typography-rules, SC:check_devanagari] WEB,APP.
- Visual heuristics scoped by screen archetype with a one-line exception format, restraint budget, autopilot-sign list and a four-layer change-depth test [R:visual-craft] WEB,APP,AUDIT.
- Context-scaled motion and a chart picker with numeric fallbacks and accessibility fallbacks per chart [R:motion-and-charts, D:charts.csv, D:motion.csv] WEB,APP.
- Large checkable do/don't corpus with severity and version stamps (119 UX, 32 mobile, 44 performance, 1271 stack rows) [D:ux-guidelines.csv, D:app-interface.csv, D:react-performance.csv, ST:*] AUDIT.
- Honest tooling: closed non-executable rule grammar, search that abstains under thresholds, data and skill linters, provenance freshness windows [SC:reasoning_contract, SC:core, SC:validate_data, SC:validate_brain] CORE.
- Evidence wording discipline: tool-verified only with command shown, "spec-approved, render-unverified" otherwise [R:examples] CORE,AUDIT.

## FLAWS
- Token files disagree with each other: default radius 0.5rem vs 0.25rem, card padding space-4 vs space-6, dark page background gray-900 vs gray-950, ring said to be "primary" but uses a different step [DS:token-architecture, DS:primitive-tokens, DS:component-tokens, DS:states-and-variants].
- Component tier breaks its own rule: spacing, radius and literal white point at primitives, not semantic roles [DS:token-architecture, DS:component-tokens].
- Utility-CSS mapping uses an old major-version config and a primitive commented as HSL that holds RGB channels; contradicts the stack table that bans legacy channel snippets [DS:tailwind-integration vs ST:shadcn].
- Category tables prescribe soft low-contrast styles for health, mental-health and telemedicine that the style matrix vetoes for critical accessibility; many rows ban purple AI gradients while the AI row prescribes indigo-violet [R:industry-playbook-192, D:ui-reasoning.csv, D:colors.csv vs R:style-matrix].
- Most numbers are self-labelled unverified (hero 1.5x, 60-30-10, 3s window, dial presets, motion ranges); reasoning confidence scores 0.88-0.94 are self-assigned and exist on only 31 of 192 rows [R:visual-craft, R:direction-recipes, D:ui-reasoning.csv].
- Disabled controls told to meet 3:1 as a rule (standards exempt them); palette contract admits not every colour pair was measured [DS:states-and-variants, D:data-provenance.json].
- Contrast tool always exits 0 and ignores background alpha, so it cannot act as a gate [SC:contrast_check].
- Heavy duplication: pairings markdown = typography CSV, industry playbook = reasoning CSV, style matrix = subset of styles CSV, motion tiers in both markdown and CSV [R:typography-pairings-74, R:industry-playbook-192, R:style-matrix, R:motion-and-charts].
- Stale-prone pinned facts: framework versions, icon package version, font snapshot, old config syntax; a fully deprecated platform table still ships [ST:*, D:google-fonts.csv, D:phosphor-icons-upstream.json, ST:uwp].
- Examples embed one product's canon and a self-scored 42/50; the changelog shows a "verified" example number that was wrong [R:examples, R:CHANGELOG].

## GAPS
- Design variety: these tables make outputs alike. D:products.csv puts one minimal style as primary in 75 of 192 rows; D:colors.csv has about half its primaries in blue hues, one blue and one violet across 33 rows and one destructive red in 172 rows; D:typography.csv leans on one neutral sans (12 pairings) and sans-plus-sans; D:landing.csv joins every category to a few hero-plus-features templates; SC:design_system derives every dark palette from the same fixed slate surfaces; keyword search returns the same top row for the same wording; font popularity rank pushes the same families.
- No algorithm to build a palette or type scale from a brand seed (perceptual lightness ramps, modular scale); only fixed tables and seed ranges [R:direction-recipes, D:colors.csv].
- Verification needs a render (first-glance, squint, logo-cover, script rendering) but no render or visual-diff harness exists [R:visual-craft, R:typography-rules].
- APP: native navigation conventions, dynamic type scaling and platform motion are single table rows, not method [D:app-interface.csv].
- PROMPT: nothing turns direction fields, dials and tokens into a work-order template, though they map cleanly to prompt slots [R:direction-recipes].
- Token cost: about 2.8 MB, mostly dumps with no method (font licences, icon dump, font catalog); reference markdown repeats the CSVs [D:google-font-licenses.json, D:phosphor-icons-upstream.json, D:google-fonts.csv].
- Other scripts: pairings cover Arabic, Hebrew, CJK, Thai, but only Devanagari has a check; no RTL mirroring or CJK line-break rules [R:typography-pairings-74].
- AUDIT: severities inconsistent across tables (Low-Medium, Medium-High) and no cross-table scoring rule [D:react-performance.csv, ST:*].

## PLACEMENT
- Action rank decides variant and position; one primary per screen; destructive starts as outline, sits 16px+ from the primary, gets undo or confirm [DS:component-specs, R:visual-tokens-recipes].
- Primary action in thumb reach, full width, 48-56px; empty-state action in thumb zone; bottom nav at most 5 items; chip rows at most 5 plus "more" [R:examples, R:visual-tokens-recipes].
- Archetype decides the anchor (hero, single KPI, no hero for forms, outcome plus safe exit for dialogs) and the 3s/5s first-glance check [R:visual-craft].
- Composition: no habitual cards, balance top/middle/bottom weight, prominence equals importance, single column improved by type not widgets [R:visual-craft].
- Labels above fields, errors directly below with icon, spinner position per component, skeleton over 1s [DS:states-and-variants, R:visual-tokens-recipes].
- Tables: text left, numbers and actions right, status centred; dialog footer cancel before confirm; card header/body/footer anatomy [DS:component-specs].
- Landing: ordered sections and where the primary action repeats [D:landing.csv].
- Stacking: named z-index ladder dropdown < sticky < modal < popover < tooltip; documented tokens, not DOM order [DS:primitive-tokens, ST:html-tailwind, D:ux-guidelines.csv].
- Responsive: breakpoints chosen where content measure breaks; composition changes (single column, list-detail, grid plus sidebar) at about 375/768/1024; no horizontal scroll, reserved image space, safe areas, focus not hidden by sticky bars [R:visual-tokens-recipes, D:ux-guidelines.csv, D:app-interface.csv].
- State precedence and interruptible transitions keep elements stable during rapid input [DS:states-and-variants, R:motion-and-charts].
- Icon discipline: role decides labelling (decorative hidden, meaningful named, control named with state); one family per surface [D:icons.csv].
- Signature element lists where it appears and where it never appears; do-not-use lists veto directions and styles [R:visual-craft, R:direction-recipes, R:style-matrix].
