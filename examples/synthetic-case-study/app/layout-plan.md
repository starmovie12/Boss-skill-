# APP worked example: Tarang demo app (Expo), planning artifacts only

Shows the A2, A5 and A7 artifacts for the phone version of the web example. Process and structure, not a look.

## A2 navigation decision
Destinations: Watchlist (many times a day), Portfolio (daily), Orders (after each trade), Account (rare). Four equal,
frequent-enough destinations = bottom tabs with icon and text. Instrument detail = stack screen pushed from Watchlist.
Order entry = full screen (high stakes, focused input) with a confirmation sheet; never a small popover. Settings,
statements and help live inside Account, never as a fifth tab. Android back: closes the confirmation sheet, then the
order screen, then returns to the previous tab's scroll position.

## PL-0 paths for placing an order
Literal: tab Orders -> New order -> search -> fill -> confirm (5 taps). Least friction: watchlist row -> instrument ->
Buy (prefilled instrument and last price) -> confirm (3 taps). Different structure: long-press a watchlist row -> quick
ticket sheet (2 taps, hidden gesture). Chosen: least friction, plus a visible "Trade" button on each instrument screen.

## A5 layout plan (instrument screen, phone)
Screen: Instrument | platform: phone (ASSUMED Android) | job: decide and act | primary: "Buy" zone=bottom

| element | where | size | next to / after | why here | label | rank |
|---|---|---|---|---|---|---|
| back + symbol | top, left | S | before price | orientation, system back also works | "ARVO · Arvo Textiles" | second |
| last price + change | top, full width | L | under the title | the number the user came for | "431.90 ▲ +5.15%" | hero |
| feed state | under price | S | after price | live or stale must be visible with the price | "Live (demo) · 10:42:20" | quiet |
| chart with range chips | middle | M | after price | confirms the trend before acting | "1D 1W 1M 1Y" chips | second |
| key stats | middle, two columns | M | after chart | context for the order | "Prev close, high, low" | quiet |
| Buy / Sell bar | bottom, pinned above the gesture bar | L | last | most frequent action, thumb zone | "Buy", "Sell" | hero |

Edge cases: gesture navigation bar inset added under the pinned bar; largest font wraps stats to one column and the bar
grows taller; offline shows the last price with "stale since" and disables Buy and Sell with the reason; reopened
mid-order restores the order screen draft.

## A7 permissions
None needed for the core flow. Price alerts (optional feature) need notifications: requested only when the user taps
"Create alert", after one sentence explaining why; declared in app config with that rationale; when denied, alerts
appear in an in-app inbox instead, with a link to system settings.
