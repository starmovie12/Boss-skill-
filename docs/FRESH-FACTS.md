# Fresh facts (retrieved 2026-11-12)

Each row: fact, source URL, retrieval date, label. VERIFIED = read on the vendor's own page in this session.
UNVERIFIED = third-party or search snippet only. BLOCKED-BY-ENV = the host is outside the session's network allowlist.

| # | Fact | Source | Label |
|---|---|---|---|
| F1 | Claude Code project skills live at `.claude/skills/<name>/SKILL.md`; personal at `~/.claude/skills/<name>/SKILL.md`; plugin skills at `<plugin>/skills/<name>/SKILL.md` invoked as `/plugin-name:skill-name`. | https://code.claude.com/docs/en/skills | VERIFIED |
| F2 | Cloud sessions do not read the user's local `~/.claude/skills/`. They load skills enabled for the claude.ai account, plus (outside project threads) skills committed to the repository's `.claude/skills/`. | https://code.claude.com/docs/en/skills | VERIFIED |
| F3 | Skill descriptions are always in context; the SKILL.md body loads only on invocation. `description` + `when_to_use` are truncated at 1,536 characters in the listing. Keep SKILL.md under 500 lines. After compaction the first 5,000 tokens of each invoked skill are re-attached (25,000 combined). | https://code.claude.com/docs/en/skills | VERIFIED |
| F4 | A plugin is a directory with a manifest at `.claude-plugin/plugin.json` (name required; version, description optional) and components such as `skills/<name>/SKILL.md`. A marketplace is a repo with `.claude-plugin/marketplace.json`. | https://code.claude.com/docs/en/plugins | VERIFIED |
| F5 | `/plugin` is a terminal-only command; a cloud session (claude.ai/code) does not load plugins from local settings. The same plugin format installs on claude.ai through its own plugin pages. | https://code.claude.com/docs/en/plugins ; https://code.claude.com/docs/en/claude-code-on-the-web | VERIFIED |
| F6 | Cloud environment network levels are named None, Limited (default allowlist + listed domains) and Full. "Trusted" and "Custom" are legacy saved names. Edit from the environment selector under the message box at claude.ai/code, or the caret after a running session's title -> Edit cloud environment. | https://code.claude.com/docs/en/cloud-environments | VERIFIED |
| F7 | Cloud sessions are available on Pro and share the account's usage limits; a PR is created from claude.ai/code after Claude pushes a branch. | https://code.claude.com/docs/en/claude-code-on-the-web | VERIFIED |
| F8 | Claude.ai free plan: Projects (reported cap: 5), project instructions, file creation, connectors and Skills reported available since Feb 2026; usage limits remain. | search snippets (macrumors.com 2026-02-11, techradar.com) | UNVERIFIED |
| F9 | Gemini Gems: about 4,000 characters of instructions (one blog; Google recommends shorter), up to 10 knowledge files per Gem. | search snippets (fast.io, geotoolbox.ai) | UNVERIFIED; the work order's 4,000-character assumption is used and labeled |
| F10 | Google is moving Gems to "skills" in the Gemini app; a Google support page lists removal dates for personal accounts in Nov-Dec 2026 and later dates for work and school accounts. Dates in snippets conflict. | https://support.google.com/gemini/answer/18560919 | BLOCKED-BY-ENV (host not in allowlist); snippet only |
| F11 | Expo EAS free plan: a limited monthly quantity of low-priority builds (third-party figure: 15 Android + 15 iOS), no overage charges; Expo Go store builds track recent SDKs (SDK 57 as of Sept 2026). Snack: nothing retrieved. | search snippets (docs.expo.dev/billing/plans, expo.dev/changelog) | UNVERIFIED (docs.expo.dev BLOCKED-BY-ENV) |
| F12 | WCAG 2.2 is the current W3C accessibility recommendation; AA includes target size minimum 24 by 24 CSS px (SC 2.5.8), focus not obscured (2.4.11), dragging alternatives (2.5.7), accessible authentication (3.3.8). | https://www.w3.org/TR/WCAG22/ | BLOCKED-BY-ENV for re-reading; stated from model knowledge, UNVERIFIED |

Consequences: E3 must say that Gems may already be replaced by Gemini skills on the operator's account and give a
fallback (paste the same instruction text wherever the Gemini app accepts custom instructions). The final report tells
the operator that the network level names are Limited and Full, not "Trusted".
