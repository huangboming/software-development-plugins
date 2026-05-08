# Greenfield project workflow

Use this end-to-end when you're greenfield — no code, no backlog, maybe just an idea.

## Skill sequence

| Step | Phase | Say something like… | Skill |
|------|-------|---------------------|-------|
| 1 | Define | "grill me on the product" → "write product.md" → "grill me on the first feature" → "write a PRD for the first release" | `define:grill-me`, `define:write-product-md`, `define:grill-me`, `define:write-prd` |
| 2 | Build | "scaffold a new \<stack\> project" | `build:scaffold-project` |
| 3 | Harness | "set up project CLAUDE.md rules" / "add a skill for \<X\>" | `harness:create-rules`, `harness:create-skill` |
| 4 | Design | "write a tech spec for \<feature\>" | `design:write-spec` |
| 5 | — | **Implement the spec** — write the code yourself (or with Claude Code's editing loop); no dedicated skill. | _(no skill)_ |
| 6 | Build | During implementation, at each phase: "simplify this code" / "guard the tests" / "check for boundary leaks" | `build:simplify-code`, `build:guard-test`, `build:guard-boundary` |
| 7 | Build | "commit these changes" → "create a PR" | `build:commit-changes`, `build:create-pr` |
| 8 | Verify | "review the code on this branch" | `verify:review-code` |
| 9 | Docs | "write architecture docs" / "write API docs" | `docs:write-architecture`, `docs:write-api` |
| 10 | Ship | "set up the CI pipeline" → "write a README" → "tag v0.1.0" → "create a GitHub release" | `ship:generate-pipeline`, `ship:write-readme`, `ship:tag-release`, `ship:create-github-release` |

Discovery work (problem framing, user research, competitive analysis) happens in conversation and memory before this loop — there is no dedicated discover-phase skill in this marketplace. For source-finding subtasks, delegate to the `research:researcher` agent.

## Decision points

- **Skip `grill-me`** within step 1 when scope is already aligned — when the inputs feeding the writer are unambiguous, the writer alone is enough.
- **Skip step 2 (scaffold)** when starting from a template or extending an existing scaffold.
- **Skip Harness (step 3)** unless you're actively tuning the project to host AI agents (custom skills, project rules, hooks). Standard greenfield apps rarely need it on the first iteration.
- **Loop back to Design (step 4)** whenever step 6 quality checks (`guard-test`, `guard-boundary`) reveal architectural mismatch — fix the spec, then re-implement, rather than patching around it.
- **Skip step 9 (Docs)** for a throwaway prototype — but write them before inviting a second contributor.
- **After step 10, switch workflows** — the next cycle isn't greenfield. Move to the [existing-project workflow](existing-project.md) once measure-phase signals come back.

## Artifacts produced

| Step | Artifacts left behind |
|------|----------------------|
| 1 | Shared understanding (transient), product definition, first-release PRD |
| 2 | Project skeleton (folder layout, dependency manifest, CI/test scaffolding) |
| 3 | Project `CLAUDE.md`, custom skills/rules under `.claude/` |
| 4 | Design spec doc |
| 5 | Working code |
| 6 | Cleaner code, passing tests, no boundary leaks |
| 7 | Commits on a feature branch, open PR |
| 8 | Code review report |
| 9 | Architecture docs, API docs |
| 10 | CI pipeline config, project README, version tag, published GitHub release |
