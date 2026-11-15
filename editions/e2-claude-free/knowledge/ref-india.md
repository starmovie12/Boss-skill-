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
