# Greenfield project workflow

Use this end-to-end when you're greenfield — no code, no backlog, maybe just an idea.

## Skill sequence

| Step | Phase | Say something like… | Skill |
|------|-------|---------------------|-------|
| 1 | Discover | "prepare user research for this idea" → "synthesize the findings" → "frame the problem" | `discover:prepare-user-research`, `discover:synthesize-research`, `discover:frame-problem` |
| 2 | Discover | "map the opportunity tree" → "test the riskiest assumption" | `discover:map-opportunities`, `discover:test-assumption` |
| 3 | Define | "define the product" → "write a product vision" → "slice the MVP" → "set success metrics" → "write a PRD for the first release" → "write user stories" | `define:define-product`, `define:define-vision`, `define:slice-mvp`, `define:set-success-metrics`, `define:write-prd`, `define:write-user-story` |
| 4 | Build | "scaffold a new \<stack\> project" | `build:scaffold-project` |
| 5 | Harness | "set up project CLAUDE.md rules" / "add a skill for \<X\>" | `harness:create-rules`, `harness:create-skill` |
| 6 | Design | "design the technical spec for \<feature\>" | `design:design-spec` |
| 7 | — | **Implement the spec** — write the code yourself (or with Claude Code's editing loop); no dedicated skill. | _(no skill)_ |
| 8 | Build | During implementation, at each phase: "simplify this code" / "guard the tests" / "check for boundary leaks" | `build:simplify-code`, `build:guard-test`, `build:guard-boundary` |
| 9 | Build | "commit these changes" → "create a PR" | `build:commit-changes`, `build:create-pr` |
| 10 | Verify | "review the code on this branch" | `verify:review-code` |
| 11 | Docs | "write architecture docs" / "write API docs" | `docs:write-architecture`, `docs:write-api` |
| 12 | Ship | "set up the CI pipeline" → "write a README" → "tag v0.1.0" → "create a GitHub release" | `ship:generate-pipeline`, `ship:write-readme`, `ship:tag-release`, `ship:create-github-release` |

## Decision points

- **Skip Discover (steps 1-2)** if the problem is already validated — research was done elsewhere and you have a framed problem ready to commit to.
- **Skip step 4 (scaffold)** when starting from a template or extending an existing scaffold.
- **Skip Harness (step 5)** unless you're actively tuning the project to host AI agents (custom skills, project rules, hooks). Standard greenfield apps rarely need it on the first iteration.
- **Loop back to Design (step 6)** whenever step 8 quality checks (`guard-test`, `guard-boundary`) reveal architectural mismatch — fix the spec, then re-implement, rather than patching around it.
- **Skip step 11 (Docs)** for a throwaway prototype — but write them before inviting a second contributor.
- **After step 12, switch workflows** — the next cycle isn't greenfield. Move to the [existing-project workflow](existing-project.md) once measure-phase signals come back.

## Artifacts produced

| Step | Artifacts left behind |
|------|----------------------|
| 1 | Research plan, raw findings, synthesis notes, framed problem statement |
| 2 | Opportunity tree, assumption test results |
| 3 | Product definition, vision doc, MVP slice, success-metrics doc, first-release PRD, user stories |
| 4 | Project skeleton (folder layout, dependency manifest, CI/test scaffolding) |
| 5 | Project `CLAUDE.md`, custom skills/rules under `.claude/` |
| 6 | Design spec doc |
| 7 | Working code |
| 8 | Cleaner code, passing tests, no boundary leaks |
| 9 | Commits on a feature branch, open PR |
| 10 | Code review report |
| 11 | Architecture docs, API docs |
| 12 | CI pipeline config, project README, version tag, published GitHub release |
