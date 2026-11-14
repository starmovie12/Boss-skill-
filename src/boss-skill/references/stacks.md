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
