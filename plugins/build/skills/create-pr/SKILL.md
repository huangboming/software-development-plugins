---
name: create-pr
description: Create a pull request end-to-end via gh CLI. Triggers on requests to create, open, submit, or draft a PR or PR message.
---

# Create Pull Request

Create a pull request end-to-end: analyze commits, draft a structured PR message, get user approval, and open the PR via `gh`.

## Workflow

### 1. Determine commit range and target branch

Parse the user's request to identify the commit range (e.g., "last N commits", "since main", "from branch A to B"). If no range is specified, infer from the current branch vs its upstream or default branch. If ambiguous, ask.

Determine the **target branch**: use what the user specifies, or detect via `gh repo view --json defaultBranchRef`. If on the default branch with no remote tracking branch, ask.

### 2. Gather context

Read commit messages, diff stats, and the full diff for the commit range.

### 3. Draft PR message

Analyze the commits and diff, then draft the PR message:

```markdown
## Summary

<1-3 sentence high-level summary of what this PR does and why>

## Problem

<Describe the issue, bug, or missing feature that motivated this change.
Focus on the "why" — what was broken, limited, or needed.>

## Proposed Solution

<Describe the approach taken. Use bullet points for multiple changes.
Each bullet should explain what was changed and why.>

## Key Changes

<Bulleted list of the most important file-level or component-level changes.
Group related changes together. Keep it scannable.>
```

Draft a concise **PR title** (under 72 characters, conventional commit style if the repo follows it).

### 4. Present for review

Present the draft PR title and message to the user. Ask them to review and request any changes.

If the user requests changes, revise and present again. Repeat until the user approves.

### 5. Pre-flight checks

Before creating the PR, verify:

1. **Branch is pushed** — if not, push with `git push -u origin <branch>` (ask user first)
2. **No uncommitted changes** — warn and ask whether to proceed or commit first
3. **Branch is up to date with remote**

### 6. Create the PR

After user approval, create the PR using `gh`:

```bash
gh pr create --title "<title>" --base "<target-branch>" --body "$(cat <<'EOF'
<approved PR message body>
EOF
)"
```

If the repository uses draft PRs by convention, or the user requests it, add `--draft`.

After creation, display the PR URL to the user.

## Edge Cases

If the user asks to "just write the PR message" without creating:
  → Run steps 1-4 only. Output the approved message in the response and stop. Do not proceed to steps 5-6.

If `gh` is not installed or not authenticated:
  → Output the PR message in the response and inform the user. Provide instructions: `gh auth login`.

If a PR already exists for this branch:
  → `gh pr view` will show it. Inform the user and ask if they want to update the existing PR's description instead (`gh pr edit`).

If the user wants to target a non-default branch:
  → Use the specified branch as `--base`. Verify it exists on the remote.
