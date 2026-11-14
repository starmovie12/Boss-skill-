# Work order: build the Tarang demo trading app (Expo) with the BOSS skill

## Context
You are an unattended coding agent in a cloud sandbox with this repository checked out, Node 22, npm, Python 3 and a
headless Chromium with Playwright. The BOSS skill is at `.claude/skills/boss/` (or `src/boss-skill/`). The owner works
from an Android phone and is away; nobody will answer questions. A web version of the same product exists as a design
reference only: `examples/synthetic-case-study/web-trading-dashboard/` (reuse its demo-market method, never its look).

## Goal and definition of done
An Expo (TypeScript) app in `apps/tarang/` that a phone user can run in Expo Go, with four tabs: Watchlist, Portfolio,
Orders, Account. Done means every acceptance check below passes, and `_boss/receipt.md` lists each check with its
command and result.

## Ordered work
1. Load BOSS APP mode; size L. Write `apps/tarang/_boss/acceptance.md` from the checks below before any design.
2. Run A2 to A6 (navigation choice, domain study from knowledge, brief, seed roll, three directions, layout plan with
   PL-0 paths, tokens with `_boss/tokens.md`). The direction must differ from the web example on at least two of: hue
   families, font pair, screen skeleton (`design_fingerprint.py` against the web example's history).
3. Build the demo market per `references/domains/fintech-trading.md` FT-4 (seed 7001), then the Watchlist screen alone;
   critique it in the web export at 360 and 430 px; revise; then the remaining screens.
4. Run `python3 .claude/skills/boss/scripts/boss_verify.py --root apps/tarang --install --final --json` and fix every
   FAIL (at most 3 loops per finding; revert a fix that breaks something else).

## Constraints
- Mock data only; no network calls, no real credentials, no broker API. Every screen shows a "demo data" label.
- Order flow follows K5 and FT-2: exact order sentence, estimated value and charges, margin needed vs available,
  confirmation, idempotency key, success only after the mock server accepts, rejection reason with a quantity that fits.
- Money in integer paise internally; display with `Intl.NumberFormat('en-IN')` and the rupee sign.
- No new dependency outside `npx expo install` alignment; total added packages at most 6.
- English UI copy; every number uses tabular figures; gains and losses carry sign and arrow, never color alone.

## Acceptance checks (each must end PASS, BLOCKED with proof, or NOT TESTED with the reason)
1. `npx tsc --noEmit` exits 0.
2. `npx expo-doctor` reports no failed checks.
3. `npx expo export --platform web` succeeds and `boss_verify.py` placement, console and axe checks pass at 360 and 1280.
4. Substance scan: 0 hits (no TODO, lorem, coming soon, empty onPress).
5. Secrets scan: 0 findings.
6. Palette check: every pair in `_boss/tokens.md` recomputes at or above its floor.
7. Placing an order twice with the same key creates one order (a unit test proves it).
8. An oversized buy is rejected with a reason and a quantity that fits (a unit test proves it).
9. Holdings value equals quantity times last price for every row after 500 simulated ticks (a unit test proves it).

## Stop rules and blocked handling
Stop only when every check is terminal. If a command cannot run (for example a blocked host), record the command and
its output in the receipt as BLOCKED and continue with everything else. Never wait for approval; never skip a check.

## Output contract
Files under `apps/tarang/`; `_boss/` with acceptance, brief, layout plan, tokens, craft log, receipt; a README section
"Run on your phone" (Expo Go steps) and "Build an APK from the browser" (cloud build steps, limits marked UNVERIFIED).
Commit after each finished screen; push to the current branch.

## Known traps
- Copying the web example's colors or layout: the fingerprint check fails.
- Calling a check PASS without running it: write NOT TESTED with the reason instead.
- Showing "Order placed" before the mock server resolves.
