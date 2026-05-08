# Existing project workflow

Use this loop for each feature, fix, or chore on an already-live codebase.

## Skill sequence

| Step | Phase | Say something like… | Skill |
|------|-------|---------------------|-------|
| 1 | Define | "grill me on \<feature\>" → "write a PRD for \<feature\>" | `define:grill-me`, `define:write-prd` |
| 2 | Design | "write a tech spec for \<feature\>" | `design:write-spec` |
| 3 | — | **Implement the spec** — write the code yourself (or with Claude Code's editing loop); no dedicated skill. | _(no skill)_ |
| 4 | Build | During implementation, at each phase: "simplify this code" / "guard the tests" / "check for boundary leaks" | `build:simplify-code`, `build:guard-test`, `build:guard-boundary` |
| 5 | Build | "commit changes" → "clean up the branch" → "create a PR" | `build:commit-changes`, `build:cleanup-branch`, `build:create-pr` |
| 6 | Verify | "review the code" | `verify:review-code` |
| 7 | Docs | "update the API / architecture docs" | `docs:write-api`, `docs:write-architecture` |
| 8 | Ship | "tag release" → "write changelog" → "write release notes" → "publish GitHub release" | `ship:tag-release`, `ship:write-changelog`, `ship:write-release-note`, `ship:create-github-release` |

To log a bug, refactor, or tech-debt item ad-hoc — anytime, in or out of this loop — use `build:capture-issue`. For source-finding subtasks during any step, delegate to the `research:researcher` agent.

## Decision points

- **Skip Define (step 1)** for small bug fixes and chores. The fix itself is the spec.
- **Skip `grill-me`** within step 1 when scope is already aligned — assigned ticket with clear acceptance, or a conversation you've already had. The writer alone is enough.
- **Skip Design (step 2)** for trivial changes — typo fixes, copy edits, dependency bumps, refactors that don't cross a boundary.
- **Start at step 4 (quality)** for pure refactors with no behavior change.
- **Skip steps 3, 6, 7 (implement/verify/docs)** for docs-only changes — go Define → Build → Ship.
- **Loop back to Design (step 2)** when step 4 quality checks reveal the spec missed something — don't patch around it.
- **Bundle releases** — step 8 doesn't have to fire after every PR. Tag and publish in cadenced batches once enough merged work has accumulated.

## Artifacts produced

| Step | Artifacts left behind |
|------|----------------------|
| 1 | Shared understanding (transient), PRD |
| 2 | Design spec doc |
| 3 | Code changes |
| 4 | Cleaner code, passing tests, no boundary leaks |
| 5 | Commits, cleaned-up feature branch, open PR |
| 6 | Code review report |
| 7 | Updated API / architecture docs |
| 8 | Version tag, changelog entry, release notes, published GitHub release |
