# Audit checklists (hunting lists per class)

Each item is something to look for and how; a hit becomes a finding only with evidence (AUDIT U4).

## AC-SEC Security
- Authorization on every read and write route, checked on the server against the object's owner (look for handlers that trust an id from the request); unknown records answer not-found, not forbidden.
- Injection: queries, shell commands, file paths, template rendering or HTML built by string concatenation with request data; `eval`, dynamic `require`/`import`, unsafe deserialization (pickle, YAML load).
- XSS: raw HTML sinks (`innerHTML`, `dangerouslySetInnerHTML`, `v-html`, unescaped template output) fed by user data; missing Content-Security-Policy.
- CSRF on cookie-authenticated state changes; CORS allowing any origin with credentials; cookies without Secure, HttpOnly, SameSite.
- SSRF and open redirects: server fetches or redirects to a URL taken from the request.
- Secrets in code, config, history, client bundles or logs (`secrets_scan.py`); public-prefixed environment variables holding private values.
- Abuse paths: no rate limit on login, signup, password reset, OTP, payments or messages; mutation handlers that are not idempotent where retries happen; read-then-write races on balances, stock or counters (needs a transaction or atomic update).
- Webhooks accepted without signature verification; file uploads without type and size limits; path traversal in downloads.

## AC-PRIV Privacy
Personal data collected beyond what features need; analytics or third-party scripts loaded before consent where consent is required; personal data in logs, URLs or error messages; no way to delete an account or export data; retention never defined. Legal statements in findings say "verify current rules, not legal advice".

## AC-A11Y Accessibility (WCAG 2.2 AA)
Contrast of every text pair and control border; keyboard reachability and visible focus; focus hidden under sticky UI; target size; form labels and error association; names on icon-only controls; heading order and landmarks; alternative text; `lang`; reduced motion; content not depending on color, hover or a gesture alone; status messages announced; dialogs trap and return focus correctly; accessible authentication (paste allowed, no puzzle-only login).

## AC-PERF Performance
Initial JS size (gzip) against budget; render-blocking resources; images without dimensions, oversized, not lazy below the fold; web fonts without swap or subsetting; layout shift from late content; request waterfalls (sequential awaits that could run in parallel); unvirtualized long lists; work on the UI thread during gestures (apps); missing caching headers for static assets; N+1 queries and missing indexes on the server.

## AC-SEO SEO and sharing
Unique title and description per page; one `h1`; canonical URL; crawlable links (real anchors, not click handlers); sitemap and robots; structured data that matches visible content; social preview tags; `lang` and `hreflang` for multilingual pages; content hidden behind client-only rendering on pages meant to rank.

## AC-COR Correctness
Logic against the stated requirement; boundary values (zero, one, maximum, negative, empty string, very long input); time zones, locale formats and daylight saving; money in floating point; integer overflow; error paths swallowed (empty catch, ignored promise rejection, ignored error return); retries that duplicate effects; state not cleaned up on unmount or cancel; tests that never fail (no assertions, mocked to always pass).

## AC-DEP Dependencies
Known-vulnerable versions (ecosystem audit tool); unmaintained or typo-squatted packages; packages far larger than their use; lockfile missing or out of sync; version ranges that pull breaking majors.

## AC-UX UX and placement
The 8-item checklist in `ref-placement.md`; dead ends; missing empty, loading, error and offline states; dark patterns (K4); copy that blames the user or says "something went wrong" with no fix; inconsistent navigation position across pages.

## AC-CODE Code health
Duplicated logic that has already drifted; functions doing several unrelated jobs; dead code and unused exports; type escapes (`any`, casts, non-null assertions) hiding real errors; magic numbers for business rules; missing tests on the paths that move money or data.

## Language gotchas (quick grep list)
JavaScript/TypeScript: `==`, floating-point money, unhandled promises, prototype pollution via object merge. Python: mutable default arguments, bare `except`, blocking calls inside async code, `pickle`/`yaml.load` on input. Go: ignored `err`, goroutine leaks, writes to nil maps. Shell: unquoted variables, no `set -euo pipefail`. SQL: string-built queries, unbounded result sets. Mobile: UI work off the main thread, secrets in plain storage.

## Spec and PRD audits
Defect kinds: missing section; vague word without a number; untestable requirement; metric without a measurement; missing state, edge case or failure mode; missing non-functional target; contradiction (say which source wins); unstated assumption or dependency; goals written as activities; no definition of done; abuse or security gap; privacy or legal gap; open question without owner or date; traceability gap (requirement with no test, metric with no event); numeric hygiene (units, currency, time zone, baseline). Each finding carries the corrected text.
