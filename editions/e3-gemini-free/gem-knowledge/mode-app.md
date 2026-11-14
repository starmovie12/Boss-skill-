# APP mode

Mobile apps. Steps run in order; size S skips A3 to A5 and follows the existing design file. Artifacts go to `_boss/`.

## A0 Intake and stack
- Brownfield (P-6): read `package.json`, the app config, navigation setup and theme file; run typecheck, lint and tests before and after; keep the existing design system unless a redesign is asked.
- Stack (details in `ref-stacks-and-fintech.md`): Expo with TypeScript by default; a PWA when no native API is needed and install-from-browser is enough; bare native only when a required native module cannot work through Expo config plugins. Write the choice and reason in one line.
- Write `_boss/acceptance.md` before design: `requirement | how it is checked | pass condition`, one row per brief requirement plus the floors in A1. Never edit a criterion after seeing the design.

## A1 Floors (always on)
- Accessibility: every touchable has an accessible label and role; targets at least 44 pt (iOS) / 48 dp (Android), primary action 48 or more; contrast 4.5:1 text, 3:1 large text and controls; layouts survive the largest system font without clipping; screen-reader order matches visual order; reduced motion honored; nothing by color alone.
- Low-end Android on a slow network: lists virtualized with stable keys and memoized rows; images sized for their box and cached; no heavy work on the UI thread during gestures (animate transform and opacity on the native driver or UI thread); cold start shows a meaningful first screen quickly; no unbounded timers or listeners (clean up on unmount).
- Security: tokens and secrets in the platform secure store, never in plain async storage and never in the bundle (any `EXPO_PUBLIC_` value is public); per-environment config through app config and build profiles; server decides money, roles and scores.
- Content: real copy; demo data from a seeded generator, labeled demo; every screen has loading, empty, error and success states.

## A2 Navigation and structure
Choose by counting top-level destinations and how they are used: 2 to 5 equal destinations used often = bottom tabs (icon plus text label); a linear task = a stack; rare destinations = a menu or settings screen, never a sixth tab; a short focused task or a picker = a bottom sheet or modal with a clear close; a decision that must not be lost = a full screen that comes back on reopen. Android back and iOS swipe-back always go one step back and restore scroll, filters and input. Key screens get deep links. Write the choice and the reason in `_boss/layout-plan.md`.

## A3 Domain study (D-1)
Look at 4 to 6 real apps in the domain (or write "from knowledge"). In `_boss/design-brief.md` list keep (expected conventions), avoid (category clichés), depart (one or two product-fact differences). Never clone trade dress, icons or copy. Platform conventions (system back, sheets, tab bars, system fonts and dynamic type) are kept unless a reason is written.

## A4 Design brief (D-2) and divergence (D-3)
- `_boss/design-brief.md`, at most 400 words: who, where and how they hold the phone (one hand, hurry, outdoors light, data cost), the key task, 3 adjectives plus 1 anti-adjective, the domain lists, the memorable thing every choice serves, light or dark from the use scene.
- treat the roll as a provocation that domain fit, platform convention and accessibility may override with a written reason. How to roll: on each axis (density, shape language, type voice, color strategy, imagery, layout archetype, motion character) pick the option you would least reflexively choose.
- Write three directions that differ in at least two layers beyond color and shadow (type, composition, component relationships and signature); choose one with a reason. Category test (does the category alone predict the look? then rebuild one choice from a product fact) and specificity test (at least two elements only this product could have).

## A5 Layout plan (PL-1 to PL-8)
Read `ref-placement.md` now. Write `_boss/layout-plan.md` before any styling: per screen, every element with its five answers, the thumb-zone placement of frequent actions, the primary action, the requirement trace table, platform edge cases (Android back gesture and navigation bar, iOS safe areas and swipe-back, tablet, very large font, weak network, app reopened mid-task), and the state and transition map.

## A6 Tokens (D-4)
Read `ref-design-system.md` now. Derive type scale (respect dynamic type), spacing, color roles with computed contrast in both themes if both ship, radius and elevation, motion durations and haptic intents from the chosen direction, into one theme file read through a theme hook so light and dark switch live; the palette table with every pair's ratio goes to `_boss/tokens.md` (`role | foreground | background | ratio as N:1 | floor`). Never copied from earlier work.

## A7 Data, storage and permissions
- Persistence: small key-value data in async storage; relational or large data in SQLite; secrets in the secure store. Writes are optimistic only when reversible, with a visible pending mark and rollback on failure; offline actions queue and say so.
- Permissions: request only what a brief feature needs, at the moment of need, after an in-app sentence saying why; declare each in the app config with a human-readable rationale string; the denied case keeps the app usable (a manual alternative plus a link to settings); never request at launch.
- Network: every request has a timeout, a retry for idempotent calls, and a visible state; stale data shows "updated N minutes ago" with a refresh.

## A8 First screen and critique (D-5), then the rest (D-7)
Build the first screen alone and run it on a small and a large phone viewport. Without scripts: run it in Expo Go on a phone and in the browser's responsive mode at 360 and 430 px wide, and look at both. Critique against the DS-9 rubric and the first-glance test (first three things the eye lands on; the primary action is among them). Revise, then build the remaining screens on the same system: same tokens, components, navigation and gestures everywhere.

## A9 Verify and fix
For sizes M and L read `ref-quality-gates.md` now and fill its stress, recovery and veto rows.
Manual verification (no scripts): 1 run in Expo Go on the phone and walk every screen and state; 2 turn on the largest font and confirm nothing clips; 3 try every action with the network off; 4 deny each permission and confirm the app still works; 5 rotate and open the keyboard on every form; 6 search the files for TODO, lorem, coming soon and empty onPress; 7 confirm no key or token sits in the code or in EXPO_PUBLIC values; 8 walk the 8-item placement checklist in ref-placement.md.
Fix loop P0 to P3 as in WEB W9: fix every P0 and P1, re-run the same check, at most 3 loops, revert a fix that breaks something else, list leftovers.

## A10 Craft pass and distinctiveness (D-6, D-8)
Screenshot every screen and state (default, loading, empty, error, offline, permission denied) on a small and a large phone viewport; write the three weakest points against DS-9, fix, re-shoot, record before and after in `_boss/craft-log.md`.  Without scripts: record palette hue families, font pair and screen skeleton in _boss/design-history.md; at least two of the three must differ from every earlier project.

## A11 Store readiness and delivery (output contract, K7)
Before calling an app release-ready: app name, unique bundle id and package name, version and build number, adaptive icon and splash, a privacy policy URL, data-safety and privacy-label answers that match the code's real data collection, permission rationale strings, no debug flags or test keys, crash-free cold start on a low-end device profile. Deliver per K7: how to run it on the phone (Expo Go or an installable preview build), how to build in the cloud and ship updates from a phone (`ref-stacks-and-fintech.md`), and the three-list report.

## Domain seeds
Broker, trading or investing apps: read `ref-stacks-and-fintech.md` at A3.
