# Existing project workflow

Use this loop for each feature, fix, or chore on an already-live codebase.

## Skill sequence

| Step | Phase | Say something like… | Skill |
|------|-------|---------------------|-------|
| 1 | Discover | "capture this user signal" (features) / "capture this bug" (defects) → "frame the problem" | `discover:capture-signal`, `build:capture-issue`, `discover:frame-problem` |
| 2 | Define | "prioritize" → "slice the MVP" → "set success metrics" → "write a PRD for \<feature\>" → "write user stories" | `define:prioritize`, `define:slice-mvp`, `define:set-success-metrics`, `define:write-prd`, `define:write-user-story` |
| 3 | Design | "design the technical approach for \<feature\>" | `design:design-spec` |
| 4 | — | **Implement the spec** — write the code yourself (or with Claude Code's editing loop); no dedicated skill. | _(no skill)_ |
| 5 | Build | During implementation, at each phase: "simplify this code" / "guard the tests" / "check for boundary leaks" | `build:simplify-code`, `build:guard-test`, `build:guard-boundary` |
| 6 | Build | "commit changes" → "clean up the branch" → "create a PR" | `build:commit-changes`, `build:cleanup-branch`, `build:create-pr` |
| 7 | Verify | "review the code" | `verify:review-code` |
| 8 | Docs | "update the API / architecture docs" | `docs:write-api`, `docs:write-architecture` |
| 9 | Ship | "tag release" → "write changelog" → "write release notes" → "publish GitHub release" | `ship:tag-release`, `ship:write-changelog`, `ship:write-release-note`, `ship:create-github-release` |

## Decision points

- **Skip Discover (step 1)** when the work is already specified — assigned ticket, agreed scope, no fresh signal to capture or frame.
- **Skip Define (step 2)** for small bug fixes and chores. The fix itself is the spec.
- **Skip Design (step 3)** for trivial changes — typo fixes, copy edits, dependency bumps, refactors that don't cross a boundary.
- **Start at step 5 (quality)** for pure refactors with no behavior change.
- **Skip steps 4, 7, 8 (implement/verify/docs)** for docs-only changes — go Discover → Build → Ship.
- **Loop back to Design (step 3)** when step 5 quality checks reveal the spec missed something — don't patch around it.
- **Bundle releases** — step 9 doesn't have to fire after every PR. Tag and publish in cadenced batches once enough merged work has accumulated.

## Artifacts produced

| Step | Artifacts left behind |
|------|----------------------|
| 1 | Captured signal or issue, framed problem statement |
| 2 | Prioritization rationale, MVP slice, success metrics, PRD, user stories |
| 3 | Design spec doc |
| 4 | Code changes |
| 5 | Cleaner code, passing tests, no boundary leaks |
| 6 | Commits, cleaned-up feature branch, open PR |
| 7 | Code review report |
| 8 | Updated API / architecture docs |
| 9 | Version tag, changelog entry, release notes, published GitHub release |
