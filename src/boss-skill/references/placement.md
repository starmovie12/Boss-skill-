# Placement: where every element goes, and why

Placement is a correctness problem, not taste. This file says where things go; it never says how they look.

## PL-1 Layout plan, in text, before any styling
Write `_boss/layout-plan.md`. Platform first (phone if unstated, labeled ASSUMED). Per screen:
```
Screen: <name> | platform | job: <one line> | primary: "<visible verb label>" zone=<bottom|middle|top>
| element | where (top/middle/bottom; left/right/full) | size (S/M/L) | next to / after | why here | label | rank (hero/second/quiet) |
```
- Grade every action by frequency: A frequent, B sometimes, C rare. Large is reserved for the screen's real job.
- Exactly one primary action per screen; never two equal-weight primaries.
- Floating elements (FAB, toasts, banners, chat bubbles) are listed separately with what they may never cover.
- Color-stripped test: read the plan with no styling; the order and grouping must already make sense.
- The `primary:` line is machine-read by `placement_check`; keep its label identical to the built button text.

## PL-2 Zones, conventions, proximity
- Phone: A actions in the bottom and middle thumb zone; B one tap away (sheet, menu, secondary row); C in a menu or settings, never removed. Top corners are the hardest reach.
- Conventional positions (a deviation needs a written reason): back top-left plus the system back; close in the same top corner of every overlay; search in the top bar or as a tab; account or profile in exactly one place; logo top-left linking home (web); primary navigation as bottom tabs (2 to 5, icon plus text) on phones, a rail on tablets, a sidebar or top bar on desktop, identical on every page; legal and contact in the footer.
- Proximity: related controls close together, unrelated groups clearly apart; labels touch what they label; on-screen order equals task order.
- Destructive actions: away from the primary action and outside the easy zone, visually distinct, the label states the outcome ("Delete 3 photos"), confirm for large or irreversible, undo for small reversible. Money, identity, consent and security steps follow K5 and are never merged away to save taps.
- Container by stakes: inline first; a sheet for quick picks and filters; a full screen for focused high-stakes input; a takeover that returns on reopen for a decision that must not be lost. A new page only when the task cannot happen here.
- Occlusion rule: nothing fixed, sticky, floating, keyboard-raised, cookie banner, chat bubble or system inset may cover the primary action, a required control, the focused element or the last content row. Fixed bars reserve their height; safe-area insets are added, never ignored.
- Forms: one column on phones; the active field and the primary action stay visible above the keyboard; long forms keep a sticky summary and action at the bottom.
- Data screens: the single most important number is the largest, with its context and tabular numerals; no equal-weight 2x2 statistic grid by habit; tables put text left and numbers right; filters stay compact so the first result sits high.
- Landing pages: section order follows the visitor's questions (what is it, is it for me, why believe it, what does it cost, how do I start); the main action sits next to the content that convinces and repeats at the end; a sticky action only on long pages.
- Scrolling: chrome (top bar, tabs) may hide on scroll down and return on scroll up; inputs and primary actions stay pinned.

## PL-3 Traceability
Table `requirement | screen | element | states`. A requirement with no element is a defect fixed before code. Low-frequency features move to a menu; they never disappear.

## PL-4 Platform edge cases (one line per screen: what changes, or why nothing does)
Android back gesture and navigation bar; iOS safe areas and swipe-back; tablet two-column composition and line length 45 to 75 characters; desktop keyboard (tab order, Enter, Escape, shortcuts) and hover (never hover-only); weak network and offline; text at 200 percent or the largest system font (no clipping, targets hold, buttons grow); app or page reopened mid-task (screen, scroll position and draft restored).

## PL-5 States and transitions
Every screen has empty (one line plus the next action), loading (content-shaped skeleton for waits over about 300 ms), error (cause plus a one-tap fix), offline (queued or read-only, said plainly) and success. Map rows: `state -> trigger -> state | feedback | exit or undo`. No dead end: every screen has a next action and a way out; every overlay closes by its button, by Escape or back, and by tapping outside where nothing is lost.

## PL-6 Icons
Vector only; one family and one stroke weight per product; one style (filled or outline) per hierarchy level; never an emoji as a structural icon; meaning comes from use (a decorative icon beside text is hidden from assistive tech); icon-only controls carry accessible names and expose state; primary navigation pairs icon with text; brand logos are official assets, never redrawn; small glyphs get an enlarged hit area, not a bigger glyph.

## PL-7 Responsive by content
Breakpoints sit where the content breaks, never at device names. Each width gets its own composition, not a scaled copy. At about 360, 768 and 1280 px check: no sideways scroll; navigation form fits the width; sticky bars and the open keyboard leave the primary action reachable; safe areas respected; text scaling holds; wide tables scroll inside their own container or reflow; long words, URLs and ids wrap.

## PL-8 Heuristics are defaults
Every number in this file (zones, line lengths, widths, timings) is a heuristic. Override with a one-line note in the layout plan: `rule | why for this screen | what instead`. Never force landing-page heuristics (hero size, sticky action) onto dashboards, forms, settings or dialogs.

## Gate
`python3 scripts/placement_check.py --url <page> --plan _boss/layout-plan.md --json` (or via `boss_verify.py`) reports, at 360 and 1280 px: overlapping interactive elements, elements outside the viewport, clipped text, targets under 44 px (48 px for the primary action on mobile), fixed or sticky layers covering content or the primary action, horizontal scroll, and whether the primary action sits in the planned zone. It is a heuristic lint: fix or justify each hit in `_boss/craft-log.md`, and still look at the screenshots.

## 8-item manual checklist (when scripts cannot run)
1. The plan existed before styling, with five answers per element and one primary action per screen.
2. Every brief requirement maps to a named element (trace table complete).
3. Frequent actions are in easy reach, rare ones in menus; destructive actions are apart, labeled with their outcome, and confirmed or undoable.
4. Back, close, search, account and navigation sit in their conventional places, or the deviation is explained.
5. Nothing covers the primary action, the focused field or a required control at 360 px, with the keyboard open, or at the largest font.
6. At 360 and 1280 px: no sideways scroll, no clipped text, no overlapping controls; targets at least 44 px (primary 48 on mobile).
7. Every screen has empty, loading, error and offline states, and every overlay has an exit.
8. Icons: one family, no emoji icons, named icon-only buttons, navigation pairs icon with text.
