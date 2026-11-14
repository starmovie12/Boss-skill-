# Craft log (D-5, D-8)

Rendered with `boss_verify.py` at 360 and 1280 px (screenshots in `_boss/shots/`), axe-core 4.10.2 in a CSP-bypass page.

| # | Weak point (DS-9 criterion) | Before | Fix | After |
|---|---|---|---|---|
| 1 | Hierarchy, correctness | Limit-price field visible while Market was selected: the `hidden` attribute lost to `.row { display: grid }` | global `[hidden] { display: none !important }` | field appears only for Limit (1280 shot) |
| 2 | Density, rhythm | watchlist rows about 90 px tall: name wrapped beside the symbol, arrow and percent split over two lines | name stacked under the symbol with ellipsis; numbers `nowrap`; row button 48 px | 12 rows fit the first 1280 view; rows about 57 px |
| 3 | Rhythm | large empty bands in the center column at 1280 (grid rows stretched by the tall watchlist) | `grid-template-rows: min-content min-content 1fr` | summary, chart and holdings stack without gaps |
| 4 | Accessibility (found by axe) | scrollable table regions not keyboard reachable (scrollable-region-focusable, serious) | `tabindex="0"`, `role="region"`, labelled by the section heading | axe: 0 serious or critical at 2 widths |
| 5 | Verification tool defect (found while dogfooding) | axe injection was blocked by the page's own CSP and the result read as a clean pass | axe now runs in a separate CSP-bypass page; an injection error reports NOT-RUN | real violations surfaced (row 4) |

Left (P3, disclosed): at 360 px the holdings table scrolls inside its own focusable container to show P&L (PL-7 allows it); a card reflow would avoid the scroll.
First-glance test (360): portfolio value, then day change, then the watchlist; the primary action is reached after the chart, by design (PL-8 exception in the layout plan). First-glance test (1280): portfolio value, watchlist, Review order.
