# TaskFlow Lite

A minimal, no-dependency task board demo by Joel Stephen.

## Run

Open `index.html` in a modern desktop or mobile browser, or serve this folder from any static host.

## Features

- Create, complete, reopen and delete tasks.
- Filter all, active and completed tasks.
- Track completed/total counts.
- Responsive layout with keyboard-visible focus.
- Data stays in this browser's `localStorage`. No remote database or analytics.
- Text is rendered with DOM `textContent`, not injected as HTML.

## Privacy and limits

This is a local demo, **not** an account-backed task manager. Clearing site data deletes stored tasks; browser private mode or blocked storage may prevent persistence. There is no multi-device sync or cloud backup.

## Manual checks

1. Add two tasks and confirm the count.
2. Complete one and check the Done/Active filters.
3. Reopen it, delete the other, and refresh to verify persistence when storage is enabled.
4. Use only a keyboard to navigate fields and buttons.
5. Add task text containing HTML tags; it must appear as text, not execute.

## Follow-up

See the project issue and pull request for development discussion.
