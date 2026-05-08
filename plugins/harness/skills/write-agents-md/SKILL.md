---
name: write-agents-md
description: "Write or update AGENTS.md at project root. Triggers: '/write-agents-md', 'write AGENTS.md', 'create AGENTS.md', 'init AGENTS.md', 'update AGENTS.md', 'bootstrap agents config'."
---

## Process

1. **Locate.** `AGENTS.md` at project root. Read if it exists.
2. **Discover.** Explore the codebase to fill template values. Ask the user only for what isn't discoverable — especially Gotchas. Do not invent.
3. **Draft against the template, review against the quality bar, present.**

## Template

```markdown
# Developer Guidelines

## Overview

<1–3 sentences. Present-tense. What this project is for and who uses it.>

## Related Projects *(omit if N/A)*

- `<repo>` — <relationship in one line>

## Commands

| Task | Command |
|---|---|
| <Task> | <command> |

## Code Quality *(omit if none)*

<Style or design rules not enforced by tooling.>

## Testing *(omit if Commands cover it)*

<Where tests live. Coverage expectations.>

## Commit

- Conventional Commits.
- One coherent change per commit.

## Pull Requests

Title: ≤72 chars, conventional-commit style.

Body sections: **Summary** · **Problem** · **Proposed Solution** · **Key Changes**.

## Release *(omit if no release process)*

1. Update `CHANGELOG.md` (Keep a Changelog format).
2. Bump version in manifest files.
3. Annotated tag: `git tag -a v<version> -m "<summary>"`.
4. Push tag: `git push origin v<version>`.
5. `gh release create v<version>` — confirm before publishing.

## Gotchas / Don'ts

- <Project-specific trap. Highest read-rate section over time.>
```

## Quality bar

- ≤ 80 lines total. Over-detailed → cut.
- Commands match manifests/scripts. No invented commands.
- No content restating training (Conventional Commits, semver, agents.md spec, etc.) — link, don't explain.
- No README duplication. Overview ≤ 3 sentences, not a sales pitch.
- Flat sections only. No h3/h4 nesting.
- If a section's placeholder is the only thing in it after drafting, omit the section.
