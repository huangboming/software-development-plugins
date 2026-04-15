---
name: write-release-note
description: "Write user-facing release notes or summarize what shipped. Triggers: 'write release notes', 'what shipped', 'summarize changes for users', 'release summary', '/write-release-note'."
---

# Write Release Note

## References

- [references/release-notes-template.md](references/release-notes-template.md) — Template for user-facing release notes. Read when drafting.
- [references/writing-guide.md](references/writing-guide.md) — Audience-specific writing rules, commit translation examples, anti-patterns, and quality checklists. Read when drafting or reviewing.

## Steps

1. Gather changes
2. Categorize and identify highlights
3. Draft the release note
4. Review and present

## Step 1: Gather Changes

**If `CHANGELOG.md` was updated earlier in this conversation:** Derive the change list from the latest entry. Skip to Step 2.

**Otherwise:**

| User Context | Data Source |
|---|---|
| References a tag range, branch, SHA, or "since last release" | **Git Analysis** |
| Provides a list of changes or feature descriptions | **Manual** |
| Both | **Hybrid** |

**Git Analysis:**
1. Identify the range (`git tag --sort=-creatordate -n1` if unclear).
2. Extract commits: `git log <from>..<to> --format="%H|%s|%b" --no-merges`
3. Filter — be stricter than changelogs: exclude refactors, test-only, doc-only changes unless they affect user-visible behavior.
4. Deduplicate, extract metadata, present for confirmation.

**Manual/Hybrid:** Same approach as write-changelog.

Use the version the user specifies, derive from tags, or ask.

## Step 2: Categorize and Identify Highlights

Assign each change to a category. Read [writing-guide.md](references/writing-guide.md) for categorization rules.

Order: breaking changes first, then by user impact. Identify the top 3-5 changes as highlights — the changes most likely to matter to end users. Omit empty categories.

## Step 3: Draft

Read [release-notes-template.md](references/release-notes-template.md) and [writing-guide.md](references/writing-guide.md).

1. Create `docs/product/release-notes/v<version>.md` using the template.
2. Write a 1-2 sentence overview framing the release theme.
3. Write the highlights section — 3-5 most impactful changes with benefit descriptions.
4. Translate every entry to user-benefit language (see translation examples in writing-guide.md).
5. Group by product area when 5+ changes; by category when fewer.
6. For breaking changes, include a migration note.
7. Set the release date.

**Executive summary** — include when requested or for major releases. Add as `## Executive Summary` after the overview. 3-5 bullets mapping changes to business outcomes, no technical terminology.

## Step 4: Review and Present

Review against the user-facing quality checklist in [writing-guide.md](references/writing-guide.md). Revise to fix any issues, then present.

## Edge Cases

If no user-facing changes between the refs:
  → Tell the user. Ask if internal changes should be documented as a maintenance release.

If a single feature spans many commits:
  → Deduplicate into one entry.

If the release is large (20+ changes):
  → Group by product area. Limit highlights to 5.

If the user asks for audience-specific notes (API consumers, mobile users):
  → Scope entries to that audience. Adjust tone accordingly.

If no git tags exist and the user says "since last release":
  → Check for other version markers. If none, ask.

If commit messages are poor quality:
  → Flag, ask for context, mark uncertain entries.

If the user wants to downplay breaking changes:
  → Recommend including them. Defer to user's final decision.
