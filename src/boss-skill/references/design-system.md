# Design system: deriving tokens from a direction

Method only. No value here is a default look; every value is derived per project from the brief and the chosen direction, and written once in the project's token file with its reason.

## DS-1 Tokens in three tiers
- Primitive: raw values without meaning (color ramps, spacing steps, type sizes, radii, durations, z-layers).
- Semantic: purpose roles that reference primitives only: background, surface, elevated, foreground, muted-foreground, border, primary and on-primary, accent and on-accent, danger, warning, success, info (each with an on-color), focus ring. Every fill role has a paired text role.
- Component: references semantic roles only, per variant and state (bg, fg, border, hover, pressed, focus, disabled). Size variants change padding, height and font, never color.
- Dark mode is a delta: one block overriding semantic roles only; surfaces get lighter as they rise; contrast is measured again for every pair.
- Every role carries a may-use and may-not-use line (for example: accent marks the primary action and active state, under about a tenth of the screen; never body text or large backgrounds). A raw color or pixel value appears once, in the primitive tier or palette table; components cite names.

## DS-2 Type
- Body size from reading context: at least 16 px on phones (also stops input zoom), larger for long reading or older audiences.
- Scale ratio from density: dense data 1.125 to 1.2, balanced 1.25, expressive editorial 1.333 to 1.5. Name the steps (display, title, heading, body, label, caption); at most 4 sizes and 3 weights on one screen; display at most once per screen and never in dialogs or dense dashboards.
- Line height 1.4 to 1.65 for body, tighter for large display; measure 45 to 75 characters (35 to 60 on phones). Tabular numerals for prices, tables, timers and changing numbers.
- Families: at most two (a voice for headings and a calm reading face, or one family with weight steps) plus a monospace only where code or aligned data needs it. Choose from the type voice in the brief; load only the weights used, subset, swap.

## DS-3 Color
- Strategy from the direction: monochrome plus one signal hue; analogous; neutral-forward with one high-chroma accent; complementary pair; or full-chroma expressive. The domain-study "avoid" list rules out the category's default hue when it is a cliché.
- Derive ramps in a perceptual space (OKLCH or HSL lightness steps), tint neutrals 2 to 6 percent toward the brand hue, and keep one accent unless the direction needs more.
- Contrast is computed, never assumed: linearize sRGB channels, luminance L = 0.2126 R + 0.7152 G + 0.0722 B, ratio = (lighter + 0.05) / (darker + 0.05); composite any transparent foreground over its real background first. Floors: 4.5 for text, 3 for large text (24 px, or 18.66 px bold), icons, borders of controls and focus rings. Write each pair and ratio in the palette table.
- Status colors never stand alone: pair with an icon, text or shape, and check red and green are distinguishable for common color-vision deficiencies (vary lightness, not only hue).
- Proportion heuristic for showcase screens: mostly neutral, some surface, a small accent share. Not for data visualization, strict brand rules or expressive directions (PL-8 exception note).

## DS-4 Space, shape, depth
- Spacing base 4 or 8 px; density sets the range (spacious, balanced, compact). Related items closer than unrelated groups, always.
- Radius ladder from the shape language (sharp, soft, round); nested radius = outer radius minus padding; no stray one-off radii.
- One light direction; elevation by shadow in light themes and by lighter surfaces in dark themes. Use cards only where spacing and type cannot separate groups.

## DS-5 Motion and feedback
- Duration by distance and size: small state changes about 100 to 150 ms, moving components 200 to 300 ms, sheets and page transitions 300 to 450 ms; exits shorter than entrances. One easing family product-wide.
- Animate transform and opacity only; at most one or two animated elements per view; every animation interruptible and never blocking input; reduced motion replaces movement with an instant change or a short fade.
- Press feedback within about 100 ms. Apps: haptics by named intent (selection, success, warning), strength matched to importance, off when the user disables them.

## DS-6 Component states
Default, hover (pointer only), focus-visible (two-layer ring at 3:1), pressed, disabled (still legible, says why when it matters), loading (locks the width, blocks double submit), error (message under the field, cause plus fix, tied to the field for assistive tech), success, selected where relevant. Precedence when several apply: disabled, loading, pressed, focus, hover, default. Button ranks: one filled primary per screen; secondary tonal; tertiary outline or text; destructive filled only inside its confirmation.

## DS-7 Non-Latin scripts (Devanagari and others): verify first
1. Never trust a font name. Check the family's published subsets or the font file's character coverage (Devanagari U+0900 to U+097F) for the exact version used.
2. Missing or unknown coverage: declare a fallback stack (Latin face, script face, system fallback) and set `lang` on the passage.
3. Render real and mixed text and check five things: conjuncts join, vowel signs attach without collision, line height about 1.5 to 1.6 for body, no clipped marks inside fixed-height buttons and inputs, mixed-script baselines align.
4. No letter-spacing, no all-caps transforms, no faux italics on the script. Labels survive about 30 percent text expansion.
5. Label it: rendered and checked = VERIFIED; coverage data only = INFERRED, rendering not tested.

## DS-8 Distinctiveness
- Change depth: L1 color and shadow; L2 typography; L3 layout and composition; L4 component relationships and signature. A design counts as different from another only when at least two of L2 to L4 differ.
- One signature element per product, derived from the gap between category habits and the brief's adjectives; written with the 3 or 4 places it appears and where it never appears (forms, dialogs, utility screens). Logo-cover test: hide the logo; the product is still recognizable.
- The habits list in the mode file names the category defaults to avoid as a first reflex.

## DS-9 Critique rubric (first screen, then the craft pass)
For each criterion write what you see in the screenshot, not what the spec says:
- Hierarchy: three visible ranks; the primary action is among the first three eye targets; weak = everything the same weight, or two competing primaries.
- Rhythm: spacing from the scale, consistent alignment edges, groups readable at a squint; weak = arbitrary gaps, ragged edges.
- Contrast: every text pair at its floor, focus visible, status not by color alone; weak = gray-on-tint text, invisible focus.
- Density: matches the archetype (dense dashboards, calm reading); weak = cramped forms or empty dashboards.
- Domain fit: a user of this domain finds expected conventions where they look; weak = an unusual pattern with no reason.
- Distinctiveness: passes DS-8 and the specificity test; weak = could be any product's page with the logo swapped.
