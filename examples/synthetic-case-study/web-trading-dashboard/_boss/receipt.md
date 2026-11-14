# Receipt

Size: M (one new screen with a money flow). Mode: WEB.

## Done and VERIFIED
`python3 src/boss-skill/scripts/boss_verify.py --root examples/synthetic-case-study/web-trading-dashboard --final --json` (exit 0, axe-core resolvable through NODE_PATH):

| check | status | key output |
|---|---|---|
| design_gate | PASS | all present |
| substance | PASS | no stubs found |
| secrets | PASS | none found |
| palette | PASS | 12 pairs recomputed |
| token_match | PASS | 13 of 13 code token colors are in tokens.md |
| js_budget | PASS | 5.4 KB gzip initial JS (budget 170 KB); app.js |
| screenshots | PASS | _boss/shots/shot-360.png; /home/user/Boss-skill-/examples/synthet |
| placement | PASS | no geometry hits at 360 and 1280 px |
| console | PASS | no console errors |
| axe | PASS | 0 serious or critical at 2 widths |

## Done but INFERRED or UNVERIFIED
- Order flow behavior (confirmation sentence, oversized-order rejection, double-click idempotency, validation messages): written to the acceptance list, exercised by reading the code paths; not driven by an automated browser test here. UNVERIFIED.
- Devanagari stack declared as a token but not used on this page (English-only example). Not applicable.

## Not done or not tested
- Light theme (out of scope; one-line reason in the brief).
- Real-device check on an Android phone; landscape; 200 percent text zoom (not run).
- Holdings table reflow at 360 px (P3, disclosed in the craft log).
