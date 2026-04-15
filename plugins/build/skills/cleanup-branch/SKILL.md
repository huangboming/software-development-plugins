---
name: cleanup-branch
description: Clean up branch commit history before PR review. Triggers on requests to squash, reword, reorder, tidy, or clean up commits.
---

# Cleanup Branch

Clean up a branch's commit history into a clear, logical series of commits suitable for PR review.

## Workflow

### 1. Pre-flight

- If uncommitted changes exist → ask the user to commit or stash first.
- If on `main`, `master`, or the default branch → refuse. Never rewrite shared branch history.

### 2. Analyze the branch

```bash
DEFAULT=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@') || DEFAULT=main
BASE=$(git merge-base $DEFAULT HEAD)
git log --oneline --reverse $BASE..HEAD
```

Present the numbered commit list to the user.

### 3. Choose strategy and present plan

| Situation | Strategy |
|-----------|----------|
| Many WIP/fix commits that should be fewer logical commits | **Restructure** |
| History has fixup!/squash! commits to fold into targets | **Restructure** |
| Mostly clean, but some messages need fixing | **Replay** (or **Amend** if only HEAD) |
| Need to drop or reorder specific commits | **Replay** |
| Already clean | No action — inform the user |

Present to the user:
- What the resulting history will look like (commit count, proposed messages)
- Which strategy
- Whether force push will be needed (check: `git rev-parse @{u} 2>/dev/null`)

**Wait for explicit approval before proceeding.**

### 4. Create backup

```bash
BRANCH=$(git branch --show-current)
git branch backup/pre-cleanup-$BRANCH
```

Tell the user: "Backup created at `backup/pre-cleanup-<branch>`. Restore with `git reset --hard backup/pre-cleanup-<branch>`."

### 5. Execute

Read [references/strategies.md](references/strategies.md) for the chosen strategy's detailed steps (Restructure, Replay, or Amend).

### 6. Verify

```bash
git log --oneline --reverse $BASE..HEAD
git diff HEAD backup/pre-cleanup-$BRANCH  # must be empty — no content lost
```

If the diff is non-empty, content was lost. Warn the user and offer to restore from backup.

Present a before/after comparison of the commit history.

### 7. Offer cleanup

After user confirms the result:
- Offer to delete backup: `git branch -D backup/pre-cleanup-<branch>`
- If branch was pushed, remind: `git push --force-with-lease` is required. Do not force push without explicit approval.

## Edge Cases

If the branch has only 1 commit:
  → Only amend (reword) is useful. Offer `git commit --amend`.

If the branch contains merge commits:
  → Warn that replay will linearize history. Suggest restructure instead.

If the user wants to also rebase onto an updated base:
  → Do that first (`git rebase <base>`), then clean up history as a separate step.
