# Acceptance (written before design)

| requirement | how it is checked | pass condition |
|---|---|---|
| Watchlist, chart, order ticket, portfolio on one screen | open at 360 and 1280 px | all four present; at 1280 visible without scrolling past the fold for watchlist, summary and ticket |
| Prices update with a visible live or stale state | watch the status line, press Pause | status says live with time; paused says stale with last update time |
| Gains and losses not by color alone | read the watchlist | every change shows sign, arrow and percent; screen reader label says up or down |
| Indian number format and rupee sign | read values | grouping like 1,23,456.78 with the rupee sign |
| Order ticket safety (K5, FT-2) | place a buy and an oversized buy | confirmation states the full order and estimates; oversized buy is rejected with the reason and a quantity that fits; success shows only after the mock server accepts |
| Double submit places one order | click Place order twice quickly | one order in the list (button locks; idempotency key) |
| Validation with cause and fix | quantity 0, sell more than held, limit 100.03 | message under the field with the fix; focus moves to the field |
| Empty states | before any order | orders section shows the empty message |
| Accessibility floor | boss_verify axe at 360 and 1280 | 0 serious or critical |
| Placement floor | placement_check at 360 and 1280 | no overlap, off-screen, small target, covered element; primary action found |
| No stubs, no secrets | boss_verify substance and secrets | 0 hits |
| Initial JS under 170 KB gzip | boss_verify js_budget | pass |
