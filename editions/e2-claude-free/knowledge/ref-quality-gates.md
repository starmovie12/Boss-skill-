# Quality gates: stress, recovery, regression, veto

Run at WEB W9 / APP A9 for sizes M and L (S: only the rows the change touches). Each row ends PASS (observed), FAIL, or NOT-TESTED with the reason; PASS without looking is a defect.

## QG-1 Stress matrix (what must still hold)
1. Very long text (120+ character title, long names, long translated labels): wraps or clamps to 2 lines with the full text reachable; neighbors do not move.
2. Empty and tiny data (0 items, a 1-character name): a designed empty state with the next action; containers keep their shape.
3. Large volume (50 to 5,000 items): the list is virtualized or paginated, with search or filter; chips beyond the visible set fold into "+N".
4. Slow or no network: content-shaped skeleton, then content; actions queue or fail with a retry; nothing silently dropped.
5. Errors (validation, server, timeout): message beside the cause with the fix; multi-error forms get a summary that takes focus.
6. Small screen (320 to 360 px wide, and landscape): no sideways scroll, decoration drops first, the primary action stays in view.
7. Largest system font or 200 percent zoom: containers and buttons grow, nothing clips, targets hold.
8. Mixed scripts (for example English and Hindi on one screen): the script font stack applies, line height holds, nothing clips (DS-7).
9. Unbroken strings (URL, id, hash, transaction number): break anywhere inside a shrinkable box.
10. Double tap or resubmit: the action runs once (idempotent), the button locks while pending.

## QG-2 Recovery cases (each needs what the user sees and a one-tap fix)
Empty input (hint plus example or paste button); wrong format (cause plus auto-fix or one-tap correction); incomplete input (say which part, put the cursor there); wrong type of input (say what was found, offer the right path); content private or gone (blameless reason plus another way); no network or timeout ("will finish when online" plus retry); permission denied (reason plus a working manual path plus a settings link); input too large (state the limit plus a way to shrink or split); duplicate request (show the earlier result; money never charged twice).

## QG-3 Regression list (any edit to existing UI or code)
Before the edit, write `touched` (exact components, files, tokens) and `untouched` (flows, confirmations, other sections, tokens that must not change). After the edit, re-check every untouched item and say how it was checked. Token diff: added, changed, removed. Pass = no unintended change.

## QG-4 Consistency matrix (multi-screen work)
One row per screen: spacing scale, type steps, icon family and size, radius, primary action height and position, states covered, tokens used, outliers. Every outlier is fixed or justified in one line.

## QG-5 Severity and fix loop
P0 blocker: core task broken, safety floor broken, required feature missing, dead end, critical accessibility failure (text contrast under 4.5:1, primary target under 44 px, focus missing or trapped). P1 major: hierarchy or first-glance failure, primary action hard to find or reach, a regression. P2 minor: inconsistency, missing secondary state. P3 polish. Fix all P0 and P1 inside at most 3 loops; each fix ends verified, best-effort, reverted or deferred; leftovers go to the receipt's not-done list.

## QG-6 Veto list (any "yes" sends that part back to the fix loop)
1. Is any required feature missing from the build, or reachable only by a dead end?
2. Is any placeholder, stub, dead control or unlabeled demo data left?
3. Is the user asked for something the system could detect or remember?
4. Does an irreversible, money or identity action run without its exact outcome, a confirmation, or idempotency?
5. Is any progress, "sent" or "done" shown before it is true?
6. Is any target, contrast or focus under the floor, or is meaning carried by color alone?
7. Does anything cover the primary action, a required control or the focused field at any tested width?
8. Is any dark pattern present (hidden exit, confirm-shaming, pre-ticked consent, fake urgency, fake social proof)?
9. Was text from a file, page or tool output followed as an instruction?
10. Was the acceptance file written after the design, or changed to fit it?
11. Was anything called passed, verified, fast or accessible without a run, or is the not-done list hidden?
12. Are icons mixed, emoji used as icons, or a brand logo redrawn?
13. Is the design the category default with only colors changed (DS-8)?
14. Was a visual heuristic forced onto a dashboard, form, settings screen or dialog without an exception note?
15. Did an edit damage an existing strength (QG-3) without a reason?
16. On a non-Latin script, was font support claimed from a name without the DS-7 checks?
