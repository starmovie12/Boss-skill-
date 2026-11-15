# Stacks and phone-first delivery

Facts about hosts and services change; every limit below is UNVERIFIED unless the user's current docs confirm it. Re-check before promising a limit.

## ST-1 Web stack decision
| Situation | Choose | Why |
|---|---|---|
| Up to about 5 content pages, a form, little state | Static HTML, CSS and a small script | Nothing to build, smallest JS, deploys anywhere |
| An interactive app on one page (dashboards, tools, calculators) | Vite with a light framework (or none) | Fast build, small bundles, static output |
| Many pages where search ranking matters, or content from markdown | A static-site framework with islands (for example Astro) | Pages ship as HTML, JS only where needed |
| Server logic, auth, per-user data, server rendering | A full-stack framework (for example Next.js) with a hosted backend | Only when the brief needs a server |
Existing project: keep its stack and versions (read the manifest). Pick the smallest option that meets the brief and write the reason.

## ST-2 Free web hosting a phone user can drive from a browser
- GitHub Pages: static output from a repository, built by a GitHub Actions workflow; good for static and Vite sites.
- Cloudflare Pages, Netlify, Vercel: connect the GitHub repository in the browser; every push builds and gets a preview URL; frameworks detected automatically.
- Phone workflow: edit in GitHub's web editor or a cloud coding agent, commit, let the host build, open the preview URL on the phone, test, then promote. Check speed and accessibility with a web-based page audit (for example PageSpeed Insights) on the preview URL.
- Forms without a backend: a hosted form endpoint the user signs up for, or the host's own form handling; never post to an unknown service.

## ST-3 App stack decision
| Situation | Choose |
|---|---|
| Native look, device APIs (camera, location, notifications, files), store install | Expo (managed) with TypeScript |
| No device API beyond what the browser offers; install from a link is enough | Progressive web app (manifest, service worker, offline page) |
| A native module that cannot run through Expo config plugins | Bare React Native or native code, stated as forced |
Keep the Expo SDK and libraries aligned: install with `npx expo install`, check with `npx expo-doctor`.

## ST-4 Building and testing an app from a phone
- Run during development: Expo Go on an Android phone opening the project from the dev server or a published update (Expo Go only runs the SDK versions it supports; check the project's SDK matches).
- Try code without any setup: Expo Snack in the phone browser for small screens and components.
- Installable builds without a computer: EAS Build in the cloud (an Android APK or AAB from the browser dashboard or a CI workflow); preview builds install from a link; free plans have a monthly build quota and slower queues.
- Ship JavaScript-only fixes: EAS Update to a channel the installed build follows.
- iOS store builds need an Apple developer account; Android is the practical phone-only path.
- CI from a phone: a GitHub Actions workflow that runs typecheck, lint and tests on every push, and starts a cloud build on tags.

## ST-5 Environment and secrets
- One config per environment (development, preview, production) through app config or the host's environment settings; never commit `.env` files with real values; commit an `.env.example` with fake values.
- Anything shipped to a browser or bundled into an app is public. Server secrets stay on a server or in the host's secret store; client code calls a server endpoint.
- Rotate any key that was ever committed; deleting the line does not remove it from history.

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

# India layer: audiences in India, Indic scripts, Hinglish, payments, phones

Load when the brief's audience is in India or the content uses an Indic language. Regulatory and payment facts change:
everything marked "verify" must be checked against current official docs before it is promised; nothing here is legal advice.

## IN-1 Language and copy
- Ask or infer the content language from the brief; never translate the user's brand or product names. Common real mixes: English UI with Hindi content, Hindi UI with English numbers and brand names, Hinglish (Hindi in Latin script) for casual consumer apps.
- Hinglish copy: short, spoken word order, common English loanwords kept in English ("order", "payment", "OTP"), no forced Sanskritized Hindi; one spelling per word across the product ("kijiye" or "kariye", not both). Test with a native reader when stakes are high; label machine translation as such.
- Each language gets its own `lang` (`hi`, `en-IN`, `mr`, `ta`, `bn`...); Hinglish in Latin script is `lang="hi-Latn"`. Labels survive about 30 percent expansion and wrap without clipping.

## IN-2 Scripts and fonts
Devanagari, Bengali, Tamil, Telugu, Gujarati, Gurmukhi, Kannada and Malayalam all need DS-7 verify-first handling: confirm the family covers the script's Unicode block for the exact version used, declare a script fallback stack, render conjuncts and vowel signs, and give fixed-height controls extra height. Tamil and Malayalam words run long: allow wrapping in buttons and tabs. Never set letter-spacing or all-caps on Indic text.

## IN-3 Numbers, money, dates
`Intl.NumberFormat('en-IN')` for lakh and crore grouping (1,00,000); rupee sign before the amount; money stored as integer paise; dates as day-month-year in the UI; times in IST when the business is Indian; phone numbers with +91 and a 10-digit check.

## IN-4 Phones and networks
Design for low-end Android: 2 to 3 GB RAM, small screens around 360 px, 4G that drops to 3G, data cost. Budgets: first view usable on a slow 4G profile, images sized and compressed, no autoplay video, offline or retry states on every network action, text-first layouts that still work with images off. Test at 360 px and with the system font at its largest.

## IN-5 Payments and identity (verify current docs)
- UPI: intent or QR for mobile web and apps through a licensed payment gateway's official SDK; show the payee name and exact amount before the user leaves for the UPI app; on return, poll the gateway (never trust the client redirect) and show pending, success or failed with a retry; never store UPI PINs or card data.
- OTP login: auto-read only through the platform's SMS retriever or one-time-code autofill, a visible resend timer, a manual entry path, and rate limits on the server.
- KYC and identity numbers (PAN, Aadhaar): collect only when the regulated flow requires it, mask on screen (last 4), never in URLs or logs; flag every such flow "verify current regulator rules".

## IN-6 Privacy basics (not legal advice; verify current law)
Collect the minimum personal data each feature needs; a plain-language notice in the user's language before collection; consent that is specific and can be withdrawn as easily as given; a way to see, correct and delete one's data; no pre-ticked consent; extra care and parental consent for children's data. Record these in the acceptance list for any flow that collects personal data.
