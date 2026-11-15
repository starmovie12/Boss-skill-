# Synthetic case study: one fictional broker, all four BOSS modes

Everything here is fictional and uses demo data. It shows the process artifacts and real script output.

| Folder | Mode | What it shows | Evidence |
|---|---|---|---|
| `web-trading-dashboard/` | WEB | a one-screen demo trading desk built by following W0-W11: acceptance first, domain study, seed roll with overrides, three directions, layout plan with PL-0 paths, derived tokens with computed ratios, first-screen critique and a craft pass | `_boss/receipt.md`: boss_verify exit 0 (design gate, substance, secrets, palette recompute, token match, JS 5.4 KB gzip, placement at 360 and 1280 px, console, axe 0 serious or critical); `_boss/craft-log.md` lists the five fixes the checks forced |
| `app/` | APP | navigation choice, three paths, a per-element layout plan and the permissions decision for the phone version | planning artifacts only (no build) |
| `prompt/` | PROMPT | a ready work order for an unattended agent to build the Expo app with BOSS | `prompt-lint.json`: 1 advisory flag, a false positive (the word TODO inside the stub-scan rule) |
| `audit/` | AUDIT | a small fixture, `findings.json` in the U4 schema, and the rendered `report.md` | `audit_report-output.json`: 5 of 5 citations verified at their file and line |

Open `web-trading-dashboard/index.html` in any browser to try it; no network is used.
