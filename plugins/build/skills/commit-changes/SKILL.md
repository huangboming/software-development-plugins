---
name: commit-changes
description: Commit working tree changes as atomic conventional commits. Triggers on requests to commit, save progress, or after finishing implementation work.
model: sonnet
---

# Commit

Commit all outstanding changes in the working tree as a series of atomic conventional commits.

## Workflow

1. Run the project's format, lint, and test commands (if configured) to catch issues before committing. Fix any failures before proceeding. If no such commands are configured, skip this step.
2. Run these in parallel to understand all changes:
   - `git status` (never `-uall`)
   - `git diff` (unstaged changes)
   - `git diff --cached` (staged changes)
   - `git diff --name-status` (file-level A/M/D/R summary)
3. Analyze every change — staged, unstaged, and untracked — and group them into logical changesets. Each group = one coherent change. Prefer fewer meaningful commits over many trivial ones.
4. Commit each group in dependency order (see Commit Ordering below):
   a. Stage files explicitly: `git add <file1> <file2> ...` (never `git add .` or `git add -A`)
   b. Commit via HEREDOC:
      ```
      git commit -m "$(cat <<'EOF'
      type(scope): concise summary
      EOF
      )"
      ```
5. Run `git status` to confirm the tree is clean.

## Commit Message Format

Use [Conventional Commits v1.0.0](https://conventionalcommits.org) format. Add `(scope)` when it clarifies the affected area. Include a body only when the "why" isn't obvious from the header.

## Grouping Heuristics

- Files in the same feature/module serving a single purpose = one commit
- New code and its corresponding tests = one commit
- Renames/moves without content changes = separate commit (preserves `git log --follow` history)
- Config, dependency, or lockfile changes = separate commit
- Formatting or linting-only fixes = separate commit
- Migration files = commit with the code changes they support
- .gitignore changes + removal of newly-ignored tracked files = one commit
- Binary assets = group with related code, but separate large additions

## Commit Ordering

Commit in dependency order so each commit leaves the codebase functional:

1. Config / infrastructure / build changes
2. Dependency additions or updates (including lockfiles)
3. Refactoring or cleanup (no behavior change)
4. Feature implementation + tests
5. Bug fixes + tests
6. Documentation

## Edge Cases

- **Renamed files**: If a file is both renamed and heavily modified, split into a pure rename commit then a modification commit. This keeps git rename detection working (50% similarity threshold).
- **Generated / lockfiles**: Commit lockfiles (`poetry.lock`, `package-lock.json`) — they ensure reproducible builds. Use `chore:` type. Never commit build artifacts.
- **Sensitive files**: Skip `.env`, credentials, secrets. Warn the user if they appear in the diff.

