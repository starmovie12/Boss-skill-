# Environment probe (PH0, 2026-11-12)

| Probe | Result | Evidence |
|---|---|---|
| Session branch | `claude/hopeful-fermat-35aqea` accepts pushes | `git push -u origin claude/hopeful-fermat-35aqea` -> `[new branch]` |
| Alternate branch | `boss-skill-forge` also accepted a push (kept as a mirror at phase ends) | `git push origin HEAD:refs/heads/boss-skill-forge` -> `[new branch]` |
| Remote before this session | `main` only, one commit (README stub) | `git ls-remote origin` |
| Resume | No FORGE_STATE.md on any remote branch: fresh start | `git ls-tree -r --name-only origin/<branch>` |
| Repo visibility | public | `curl https://api.github.com/repos/starmovie12/Boss-skill-` -> `"visibility": "public"` |
| gh CLI | present; GraphQL blocked, token not usable for `gh repo view`; REST via proxy only for this repo | `gh repo view` -> HTTP 403 |
| GitHub MCP tools | present (deferred), scoped to this repo | tool list |
| node / npm | v22.23.4 / 10.9.9 | `node -v; npm -v` |
| python3 | 3.13.18 (no `playwright` python module) | `python3 --version` |
| Playwright + Chromium | preinstalled for node: `/opt/pw-browsers/chromium-1243/chrome-linux64/chrome` | `node -e "require('playwright')..."` |
| Subagent tool | available (Agent tool) | tool list |
| Web search | available (WebSearch tool) | used in PH0 |
| Web fetch | works for `code.claude.com`, `raw.githubusercontent.com`; blocked for `support.google.com`, `docs.expo.dev`, `www.w3.org`, GitHub API of other repos | `curl` -> 200 / 200 / `CONNECT tunnel failed, response 403`; WebFetch -> `getaddrinfo ENOTFOUND support.google.com` |
| Network level | Limited (default allowlist plus package managers) | docs + blocked hosts above |
| Disk / memory / CPU | 31 GB free / 15.6 GB free / 4 cores | `df -h; free -m; nproc` |
| Transcripts | session transcript at `~/.claude/projects/-home-user-Boss-skill-/<session>.jsonl`; subagent transcript path recorded after the first launch | `find ~/.claude/projects` |
| Auto-discovered skills | `~/.claude/skills/synced/` (account skills) and a session plugin exist in this container and are visible to every subagent, all arms alike; recorded as a benchmark limitation | `ls ~/.claude/skills` |
| `.claude/skills` in repo | absent (must stay absent until PH7) | `ls -a` |
