# RepoScope — GitHub REST API Explorer

A small developer tool by Joel Stephen, powered by the public GitHub REST API.

## Usage
Open `index.html` in a browser with an internet connection, or serve this folder on a static host. Enter a GitHub username, then filter or sort their public repositories.

## Features
- Reads `GET https://api.github.com/users/{username}/repos?per_page=100&type=owner&sort=updated`.
- Search by repository name, sort by update date, stars or name.
- Displays public repository descriptions, languages and star counts.
- Handles missing users, connection errors and rate limiting.
- Uses safe DOM text rendering and validates repository links.
- No access token, login, analytics, server or private repository access.

## Limits
The API result is limited to the first 100 public repositories for a user; it is not complete for larger accounts. Browser network access and GitHub unauthenticated rate limits are required.

## Manual test plan
1. Load Stephen077j and confirm GitHub repositories appear.
2. Filter for `ML`, then sort by stars and name.
3. Enter a nonexistent username and verify the friendly error.
4. Disconnect the network and retry to verify network error handling.
5. Use keyboard navigation and a phone-sized browser window.
6. Inspect DevTools and confirm calls go only to `api.github.com`.

## GitHub Developer Program
This is a real GitHub API integration example. Building this project **does not automatically enroll the author or award a Highlight**; the account owner must review GitHub's Developer Program enrollment requirements separately.
