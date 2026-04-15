# Cleanup Strategies

## Restructure

Use when commits need to be regrouped or squashed. Resets all commits while preserving file changes, then recommits cleanly.

```bash
# Reset to base — all changes preserved in working tree (unstaged)
git reset $BASE
```

Then recommit following the `commit-changes` skill conventions:

1. `git diff --name-status` to see all changes
2. Group into logical changesets
3. For each group: `git add <specific-files>` and commit
4. Use conventional commit format, dependency ordering
5. Stage files explicitly — never `git add .`

When the branch contains `fixup!` or `squash!` prefixed commits, identify their target commits from the prefix (e.g., `fixup! add auth` targets the commit with message `add auth`). Combine their changes with the target's changes when regrouping.

## Replay

Use when the commit structure is mostly good but specific commits need rewording, reordering, or dropping. Replays commits via cherry-pick with targeted modifications.

```bash
# Record commits to replay (oldest first)
git log --reverse --format='%H %s' $BASE..HEAD

# Reset to base — working tree wiped clean for cherry-pick (backup exists)
git reset --hard $BASE
```

Then cherry-pick selectively:

- **Keep as-is:** `git cherry-pick <sha>`
- **Reword:** `git cherry-pick <sha>` then `git commit --amend -m "type(scope): new message"`
- **Drop:** skip the sha entirely
- **Reorder:** cherry-pick shas in the desired order

If a cherry-pick conflicts: resolve the conflicting files, `git add` them, and `git cherry-pick --continue`. If conflicts are too complex, abort with `git cherry-pick --abort`, restore from backup, and suggest switching to the **Restructure** strategy instead.

## Amend

Use when only the latest commit's message needs fixing:

```bash
git commit --amend -m "type(scope): corrected message"
```

No backup needed for single amend (reflog provides recovery).
