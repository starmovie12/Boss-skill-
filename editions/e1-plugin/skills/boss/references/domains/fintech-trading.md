# Domain seed: broker, trading and investing products

Conventions and safety, not looks. Mock data only; never real credentials or live order routing. Broker and exchange APIs are official ones only, flagged "verify current docs". Regulatory text is flagged "verify current regulator rules, not legal advice".

## FT-1 Conventions users expect (keep unless the brief says otherwise)
- Dense numeric tables: instrument, last price, absolute change, percent change, volume; numbers right-aligned in tabular numerals; prices rounded to the instrument's tick size.
- Indian formats when the market is Indian: the rupee sign, Indian digit grouping (1,00,000 and 1,00,00,000 via `Intl.NumberFormat('en-IN')`), lakh and crore in summaries, IST times with the exchange calendar.
- Gain and loss never by color alone: sign (+/-), an arrow or triangle, and text for screen readers; colors chosen for color-vision safety (vary lightness too).
- Live versus stale: every price shows its time or "delayed by N minutes"; a stale or disconnected feed is said plainly with the last update time; market open, pre-open, closed and holiday states are visible.
- Watchlist rows tap through to an instrument screen with a chart, key stats and buy and sell actions in the thumb zone (phone).

## FT-2 Order-ticket safety (no-shortcut zone, K5)
- Buy and sell are visually distinct and never adjacent to destructive actions; side, quantity, order type (market, limit, stop), price, validity and product type are explicit, with sensible defaults shown, never hidden.
- Before confirmation show: estimated value, charges and taxes (labeled estimate), margin required versus available, and what happens if the price moves (market order slippage note).
- Confirmation states the full order in one sentence; the request carries an idempotency key; success shows only after the (mock) server accepts; a failure says whether an order was placed.
- Modify and cancel are reachable from the order list; cancel has a short undo window only where the backend allows it. Rejections give the exchange-style reason and the fix.
- Never auto-place orders from detection, notifications or chat; never pre-fill quantity from a previous large order without showing it.

## FT-3 Auth, session and trust
Login with a second factor; session timeout with a warning; re-authentication before high-risk actions (adding a bank account, changing contact details, large withdrawals); device and session list with sign-out; no account numbers or PAN-like ids in full on screen (mask all but the last 4). Disclaimers ("investments are subject to market risk; read all related documents", demo-data notice) are visible but never block the task; their text is flagged "verify current regulator rules".

## FT-4 Demo-data method (procedure, never stored datasets)
1. Seeded generator: one seed per session so screenshots are reproducible; label the app "demo data".
2. Instruments: a small universe (for example 20 to 60 fictional or clearly labeled symbols) with sector, lot size and tick size (0.05 for typical Indian equities, labeled as a heuristic).
3. Prices: geometric random walk per instrument with volatility clustering (each step's volatility = previous volatility nudged toward a long-run level plus a shock term, so calm and stormy stretches alternate); daily drift near zero; occasional gaps at open; every price rounded to the tick size.
4. Calendar: generate ticks only inside market hours on trading days; pre-open and closed states produce no new ticks; the "last updated" time comes from the generator's clock.
5. Consistency: holdings quantity times last price equals current value; profit and loss equals current value minus invested amount; day's change uses the previous close; positions, orders and holdings agree after every simulated fill; balances never go negative without a margin state.
6. Candles for charts aggregate the same tick stream (open, high, low, close, volume per interval), so chart and table never disagree.

## FT-5 Charts and dashboards
Pick the chart by question: price over time = line or candlestick (with a line fallback for small screens); allocation = horizontal bar (pie only for 5 or fewer slices); comparison = bar. Every chart has an accessible summary sentence, a visible data table option, crosshair values on hover, tap and keyboard focus, and empty, loading and error states. The portfolio screen leads with one number (current value) and day and total change with sign, arrow and percent.
