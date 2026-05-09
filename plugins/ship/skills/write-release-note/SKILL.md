---
name: write-release-note
description: "Write user-facing release notes or summarize what shipped. Triggers: 'write release notes', 'what shipped', 'summarize changes for users', 'release summary', '/write-release-note'."
---

Audience is **end users**, not developers. `git log` is dev-side noise — every entry must be translated into what a user can now do, avoid, or expect.

## Workflow

1. Identify the range (tag, branch, SHA, or "since last release"). If unclear, ask.
2. Pull commits with `git log <from>..<to> --no-merges --format="%H|%s|%b"`.
3. **Drop** refactors, test-only, doc-only, and internal-tooling changes unless user-visible.
4. Translate each surviving change to user-benefit language ("Faster cold starts on first request" not "Cache the bootstrap module").
5. Pick the **top 3-5 highlights** — the changes most likely to matter to end users.
6. Write to `docs/release-notes/v<version>.md`: 1-2 sentence overview, highlights, then remaining changes grouped by product area (or category if <5 entries).
7. For every breaking change, include a migration note. Don't downplay them.

## Hard rules

- One entry per feature, even if it spans many commits.
- Omit empty categories.
- If nothing user-visible shipped, say so and ask whether to publish a maintenance release.
