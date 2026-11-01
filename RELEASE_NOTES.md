# Release preparation — public browser demos

This repository contains two independent static demos.

## TaskFlow Lite
- Add, complete, reopen and delete tasks.
- Filter active/completed tasks.
- Save tasks to browser storage.
- Export a local JSON backup.
- Limitations: no import, no cross-device synchronization; local data may be deleted when browser data is cleared.

## RepoScope Explorer
- Explore a GitHub account's public repositories using the REST API.
- Filter and sort results.
- Show errors for missing users and API limits.
- Limitations: currently fetches at most 100 repositories; no private repo access.

## Quality checks
Automated checks run in `.github/workflows/static-app-checks.yml` using `node --test tests/static-apps.test.cjs`. A successful workflow verifies basic structure and JavaScript parsing, **not complete browser behavior**.

## Before publishing a GitHub Release
1. Run both applications in Chrome and Firefox.
2. Validate mobile layout, keyboard navigation and the TaskFlow JSON backup.
3. Validate RepoScope against real GitHub API results and errors.
4. Verify the Pages URL publicly if a live demo is advertised.
5. Review changes, assign an appropriate version and publish release notes.

**Status:** release candidate documentation; not an official published GitHub Release.
