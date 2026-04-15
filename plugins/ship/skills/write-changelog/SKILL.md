---
name: write-changelog
description: "Write, update, or generate a changelog. Triggers: 'write changelog', 'update changelog', 'generate changelog', 'what changed', '/write-changelog'."
---

# Write Changelog

## References

- [references/changelog-template.md](references/changelog-template.md) — Keep a Changelog format template. Read when drafting a new changelog or adding an entry.
- [references/writing-guide.md](references/writing-guide.md) — Categorization rules, commit-to-entry translation, anti-patterns, and quality checklist. Read when categorizing changes or reviewing the draft.

## Steps

1. Determine the data source
2. Gather changes
3. Categorize and order
4. Draft the changelog entry
5. Review and present

## Step 1: Determine Data Source

| User Context | Data Source |
|---|---|
| References a tag range, branch, SHA, or "since last release" | **Git Analysis** (Step 2a) |
| Provides a list of changes or feature descriptions | **Manual** (Step 2b) |
| Both | **Hybrid** (Step 2c) |
| "Update the changelog" with no further context | Check for git tags. If tags exist, propose the most recent range. If none, ask. |
| First release (no tags AND no CHANGELOG.md) | **First Release** (Step 2d) |

**Detecting first release:** If no git tags exist (`git tag` returns empty) AND no `CHANGELOG.md` exists, treat as a first release — do not ask the user to confirm this.

Use the version the user specifies. If working from tags, derive from the target tag. For first releases, check version files (`package.json`, `pyproject.toml`, `Cargo.toml`, `version.txt`). If neither tags nor version files exist, ask.

## Step 2a: Git Analysis

1. **Identify the range.** If unclear, list recent tags with `git tag --sort=-creatordate -n1` and propose a range.
2. **Extract commits:** `git log <from>..<to> --format="%H|%s|%b" --no-merges`
3. **Filter noise.** Exclude bot/automated commits and trivial changes. Include notable refactors, test changes, and doc changes.
4. **Deduplicate.** Group commits touching the same feature into a single entry (same files, same PR, sequential related commits).
5. **Extract metadata:** what changed, category, breaking status, PR/issue reference.
6. **Present** the extracted changes to the user for confirmation.

## Step 2b: Manual Input

1. Read the user's list, infer categories (ask if ambiguous).
2. Ask about breaking changes.
3. If fewer than 3 items, ask if the list is complete.

## Step 2c: Hybrid

Run git analysis, merge in user's changes (user wording takes precedence), present merged list for confirmation.

## Step 2d: First Release

For first releases, gather the entire project history:

1. **Get root commit:** `git rev-list --max-parents=0 HEAD` to find the initial commit.
2. **Extract all commits:** `git log $(git rev-list --max-parents=0 HEAD)..HEAD --format="%H|%s|%b" --no-merges`. If the root commit itself should be included, also capture it separately.
3. **Summarize aggressively.** First releases often span many commits. Group heavily by feature area rather than listing individual commits. Aim for 5-15 changelog entries even if there are hundreds of commits.
4. **Filter noise.** Exclude scaffolding commits (initial project setup, boilerplate, dependency installs, CI config iterations) unless they represent a notable capability. Early "fix typo" and "wip" commits are noise.
5. **Frame as features, not commits.** A first release changelog answers "what can this project do?" not "what happened during development." Each entry describes a capability the project ships with, written as a feature statement. Do not mechanically translate commit messages into entries.
6. **Only use the Added category.** A first release has no prior version — nothing was changed, removed, or deprecated. All entries go under Added. The only exception is if the release includes a security fix for a vulnerability discovered during development (use Security).
7. **Present** the summarized list for confirmation. Note that you grouped heavily and ask if anything important is missing.

## Step 3: Categorize and Order

Assign each change to one category (Breaking Changes, Added, Changed, Fixed, Deprecated, Removed, Security, Performance). Read [writing-guide.md](references/writing-guide.md) for category definitions and inference heuristics.

**First release exception:** Use only the Added category (and Security if applicable). Changed, Removed, Fixed, and Deprecated are meaningless without a prior version — bugs fixed during development are not "Fixed", they were never released broken.

Order: breaking changes first, then by significance within each category. Omit empty categories.

## Step 4: Draft

Read [changelog-template.md](references/changelog-template.md) and [writing-guide.md](references/writing-guide.md).

1. If `CHANGELOG.md` exists, prepend the new entry below `[Unreleased]`. If none, create using the template.
2. Start each entry with an imperative verb. Include PR/issue references.
3. Document breaking changes with before/after behavior and migration path.
4. Keep `[Unreleased]` section present above the new entry.

## Step 5: Review and Present

Review against the technical changelog quality checklist in [writing-guide.md](references/writing-guide.md). Revise to fix any issues, then present.

## Edge Cases

If `CHANGELOG.md` exists but uses a different format:
  → Follow the existing format. Note the deviation.

If the user wants unreleased changes:
  → Place under `[Unreleased]`.

If the release is large (20+ changes):
  → Keep flat by category. Do not group by product area.

If no git tags exist and the user says "since last release":
  → Check for other version markers (CHANGELOG.md entries, package.json). If none, ask for a starting commit or date.

If this is the first release and the commit count is very large (50+):
  → Do not list every commit. Summarize by feature area. Target 5-15 entries that describe what the project ships with. Present to user for review.

If this is the first release and there is only one or a few commits:
  → Each commit likely represents a significant chunk of work. Expand each into a meaningful entry rather than using the commit message verbatim.

If commit messages are poor quality ("fix", "wip", "asdf"):
  → Flag to user. Ask for context. Mark uncertain entries.

If breaking changes exist but the user wants to downplay them:
  → Recommend including them (reduces support load, builds trust). Defer to user's final decision.
