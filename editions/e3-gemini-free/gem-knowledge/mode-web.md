# WEB mode

Websites, landing pages, web apps, dashboards. Steps run in order; size S skips W2 to W5 and follows the existing design file. Every artifact named here is written to `_boss/` in the project.

## W0 Intake
- Brownfield (P-6): read the manifest, routes, the existing tokens or design file, and run the existing build and tests before touching anything. Decide refine (keep identity, change only what is asked) or redesign (keep content and function, move away from the old look); write the choice in one line.
- Greenfield: pick the stack from `ref-stacks-and-fintech.md` (static, Vite SPA, or a framework for many SEO pages) and the free host the user can deploy to from a phone.
- Write `_boss/acceptance.md` before any design: one row per requirement in the brief plus the floors below: `requirement | how it is checked | pass condition`. Never edit a criterion after seeing the design.

## W1 Floors (always on)
- Accessibility WCAG 2.2 AA: text contrast 4.5:1 (3:1 for large text and UI parts), visible focus never hidden by sticky UI, targets at least 24 CSS px (44 px for touch-first controls, 48 px for the primary mobile action), labels on every field, names on icon-only buttons, a skip link, headings in order, nothing conveyed by color alone, reduced motion honored, no keyboard trap, paste allowed in login fields.
- Performance: initial JavaScript at most 170 KB gzip; fonts subset with `font-display: swap` and only the weights used; every image has width and height (or aspect ratio), modern format, lazy loading below the fold, priority on the main above-fold image; no layout shift from late content.
- Mobile-first from 360 px: zero horizontal scroll at 360 px; every width gets its own composition (`ref-placement.md` PL-7).
- Security: a Content-Security-Policy (header or meta), no secret in client code (anything bundled is public), `rel="noopener noreferrer"` on external links that open new tabs, forms never post to unknown third parties.
- Internationalization: `lang` on the root and on every passage in another language; no hard-coded language assumptions; Indic and RTL scripts get a verified font stack (`ref-design-system.md` DS-7) and `dir` where needed.
- Content: real, specific copy written for this audience; no lorem ipsum, no fake testimonials, ratings or user counts, no placeholder phone, address or email presented as real (use clearly fictional values and label them when the business is fictional).

## W2 Domain study (D-1)
With web access, look at 4 to 6 real products in the same domain. Without it, reason from the brief and write "from knowledge". Write in `_boss/design-brief.md`:
- keep: conventions users of this domain expect (one reason each);
- avoid: the clichés that crowd the category (one reason each);
- depart: one or two places where this product should differ, tied to a product fact.
Study, never clone: no trade dress, logos or copy.

## W3 Design brief (D-2)
`_boss/design-brief.md`, at most 400 words: audience and their context of use (device, light, hurry, literacy, language); the key task; surface mode per page or section (Persuade = decide and act, Operate = finish a task, Read = understand, Experience = enjoy); emotional target as 3 adjectives plus 1 anti-adjective; the domain-study lists; one sentence naming the memorable thing every choice must serve; light or dark from the use scene, not habit.

## W4 Divergence (D-3)
1.  Roll it yourself: on each axis (density, shape language, type voice, color strategy, imagery strategy, layout archetype, motion character) pick the option you would least reflexively choose.
2. The roll is a provocation. Domain fit, usability and accessibility override it; write each override with its reason.
3. Write three directions, one line each, that differ in at least two layers beyond color and shadow (typography, layout and composition, component relationships and signature element), plus why each fits or not. Choose one; write the reason.
4. Tests on the chosen direction, each answered in the brief: Category test: does the product category alone predict this look? If yes, rebuild one key choice from a product fact. Specificity test: list the elements only this product could have; fewer than two means revise the direction, not polish it.

## W5 Layout plan (PL-1 to PL-8)
Read `ref-placement.md` now. For a new M or L screen or flow, first write the three paths (PL-0). Then write `_boss/layout-plan.md` before any styling: platform (phone if unstated, labeled ASSUMED), every screen and section, every element with its five answers (where, how big, next to and after what, why here, label and rank), the primary action per screen, the requirement-to-element trace table, platform edge cases, and the state and transition map. A requirement with no element is fixed here, before code.

## W6 Tokens (D-4)
Read `ref-design-system.md` now. Derive tokens from the chosen direction: type scale from base size and ratio, spacing scale, color roles in three tiers with every text/background pair's contrast computed and written in the palette table, radius and elevation from the shape language, motion durations by distance and importance. Write them once (CSS custom properties or the stack's theme file) and write the palette table to `_boss/tokens.md`: one row per pair, `role | foreground | background | ratio as N:1 | floor`, so the ratios can be recomputed. Never copy tokens from a previous project, a source file, a template or your own earlier output.

## W7 First screen and critique (D-5)
Build the first screen alone, with real content.  Without scripts: open the page in a phone browser and a desktop browser (or the browser's responsive mode at 360 and 1280 px) and look at both. Then critique against the rubric in `ref-design-system.md` DS-9 (hierarchy, rhythm, contrast, density, domain fit, distinctiveness) and the first-glance test: write what a visitor sees first, second and third; the primary action must be among them and the order must match intent. Revise, then build the rest.

## W8 Build the rest
- One system across all pages (D-7): every page uses the same tokens, components and navigation position; pages differ by content and archetype, never by design language.
- Forms: visible label per field; input types and `autocomplete` set; validation on blur and on submit with the cause and the fix next to the field, focus moved to the first error or an error summary; a success state; spam resistance without tracking (a hidden honeypot field plus a minimum fill time, no third-party captcha unless the user asks). With no backend, submit to a clearly labeled demo handler that shows the success state, or to a free form endpoint the user configures (name it as a setup step).
- States: every data view has loading (content-shaped skeleton after about 300 ms), empty (one line plus the next action), error (cause plus a one-tap retry) and offline where it can occur.
- Demo data: generated by a small seeded function with realistic ranges and consistent relations, never one hard-coded row; labeled demo where a user could take it for real.
- SEO and sharing: unique `title` and meta description per page, canonical URL, Open Graph and Twitter card tags with an image, structured data (JSON-LD) matching the business or content type, a sitemap and robots file for multi-page sites, semantic landmarks (header, nav, main, footer), one `h1` per page.
- Navigation keeps the same position on every page; the current page is marked; key pages are reachable by URL.

## W9 Verify and fix
For sizes M and L read `ref-quality-gates.md` now and fill its stress, recovery and veto rows.
Manual verification (no scripts): 1 open every page at 360 px and confirm no sideways scroll and nothing clipped or overlapping; 2 tab through each page and confirm visible focus and logical order; 3 check every text color pair with a contrast checker (4.5:1, large 3:1); 4 search the files for TODO, lorem, coming soon, href="#" and empty onclick; 5 submit each form empty and valid; 6 confirm title, description, social tags and lang; 7 confirm no key or token appears in client files; 8 walk the 8-item placement checklist in ref-placement.md.
Fix loop: tag each problem P0 (task, safety or critical accessibility broken), P1 (clarity, hierarchy, primary action), P2 (inconsistency), P3 (polish). Fix all P0 and P1, re-run the same check, record before and after. At most 3 loops; then stop and list what is left in the receipt. A fix that breaks something else is reverted.

## W10 Craft pass and distinctiveness (D-6, D-8)
1. Screenshot every distinct page and state (default, loading, empty, error) at 360 and 1280 px.
2. Write the three weakest points against the DS-9 rubric, fix them, re-shoot. Record before and after in `_boss/craft-log.md`.
3.  Without scripts: write the palette hue families, the font pair and the section skeleton of this design in _boss/design-history.md and compare them with earlier entries; at least two of the three must differ from every earlier project.

## W11 Deliver (output contract, K7)
Files on disk; how to preview on a phone and deploy free from a phone (`ref-stacks-and-fintech.md`); the three-list report. A design history entry exists. The receipt names every gate and its result.

## Habits to avoid as a first reflex (each allowed only when the brief justifies it in one line)
A purple-to-blue gradient on white; a centered hero over a blurred blob, then three equal feature cards, then a testimonial carousel; every block in a card with the same radius and shadow; glass effects on content surfaces; gradient text; emoji as icons; one default sans (Inter, Roboto, Arial) at one weight for everything; dark mode chosen because it looks "premium"; stock-photo people smiling at laptops; "Get started" and "Learn more" as the only calls to action; a 2x2 grid of equal statistic cards on a dashboard.

## Domain seeds
Broker, trading or investing products: read `ref-stacks-and-fintech.md` at W2.
