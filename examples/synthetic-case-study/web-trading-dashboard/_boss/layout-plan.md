# Layout plan

Paths (PL-0) for placing an order: literal (separate order page, 4 taps); least friction (ticket beside the chart, row tap preloads it, 2 taps plus confirm); different structure (long-press a watchlist row opens a sheet, 2 taps but hidden gesture). Chosen: least friction; the hidden gesture fails discoverability.

Screen: Desk | platform: web, phone first (360 px) and desktop (1280 px) | job: see moves, place a correct order
primary: "Review order"
(no zone line: on a scrolling phone page the ticket follows the chart; a sticky bar would cover table rows. PL-8 exception: thumb-zone rule | the ticket sits mid-page after the chart, reached by the skip link or a row tap, which moves focus into it | focus jump instead of a pinned bar.)

| element | where | size | next to / after | why here | label | rank |
|---|---|---|---|---|---|---|
| status line | top, full width | S | after brand | live or stale must be seen before any number | "Market open (demo) · last update" | second |
| pause control | top right | S | after status | rare action, top corner | "Pause demo feed" | quiet |
| portfolio value | top of workspace | L | above day change | the one number users check first | "Portfolio value" | hero |
| watchlist | 360: after summary; 1280: left column | M | before chart | scanning precedes choosing | "Watchlist" | second |
| chart | after watchlist (center at 1280) | M | above stats | confirms the choice | "Price, last 90 ticks" | second |
| order ticket | after chart (right column, sticky at 1280) | M | after chart | decide then act, in reading order | "Order ticket" | second |
| Review order | bottom of ticket, full width | L | after estimates | estimates are read before the action | "Review order" | hero |
| holdings, orders | last | M | after ticket | results of actions | "Holdings", "Orders today" | quiet |
| confirmation dialog | overlay, centered | M | n/a | money action needs a full sentence and figures | "Confirm order" | hero |

Trace: watchlist -> watch section; chart -> chart section; ticket -> ticket form + dialog; portfolio -> summary + holdings; demo label -> demo note + footer.
Edge cases: Android back closes the dialog (native dialog cancel); desktop Escape closes the dialog and focus returns to Review order; 200 percent text wraps (labels wrap, grid collapses); weak network: no network used (all local); reopened mid-task: demo resets (stated in the demo note scope).
States: watchlist loading row until first render; orders empty message; validation errors per field; rejection inside the dialog with no order placed; stale feed in the status line.
Transitions: Review order -> dialog (focus Edit order) -> Place order (button locks, "Placing order") -> filled or open -> list updated, focus back to Review order | rejected -> reason + quantity that fits, dialog stays open.
