# software-development-plugins

A Claude Code plugin marketplace that guides agents through the full software product lifecycle — plan, design, build, verify, ship, measure.

## About

This repository is a [Claude Code](https://claude.com/claude-code) **plugin marketplace**: a bundle of nine plugins that each cover one phase of the software product loop. Every plugin ships skills (auto-invoked playbooks) and agents (task-scoped subagents) so a Claude Code session can move from "what should we build?" to "what did shipping teach us?" without leaving the tool.

### The Plugins

| Plugin | Phase | What it covers |
|--------|-------|----------------|
| [`plan`](plugins/plan) | Discover & prioritize | Convert user needs, research, and stakeholder input into prioritized product direction (PRDs, backlog intake, user research, prioritization). |
| [`design`](plugins/design) | Technical design | Resolve product intent into a concrete technical approach grounded in the existing codebase (design specs, spec review, code exploration). |
| [`build`](plugins/build) | Execution | Turn decisions into working software with version-control hygiene (scaffold, commit, simplify, guard tests/boundaries, create PRs, clean up branches). |
| [`verify`](plugins/verify) | Quality gate | Check what was built against what should have been built (code review, test strategy, doc review). |
| [`ship`](plugins/ship) | Release | Package and publish finished changes (tag release, GitHub release, changelog, release notes, README, CI/CD pipelines). |
| [`measure`](plugins/measure) | Feedback loop | Turn shipped reality into signals that shape the next cycle. |
| [`docs`](plugins/docs) | Documentation | Generate developer- and stakeholder-facing docs (API docs, architecture docs). |
| [`harness`](plugins/harness) | Agent tuning | Tune the project itself to host AI agents well (skills, subagents, hooks, rules, design system docs). |
| [`misc`](plugins/misc) | Utilities | Miscellaneous helpers that don't belong to a single phase (e.g. git activity summaries). |

## Quick Start

### Installation

Install the marketplace in Claude Code, then install the plugins you want.

```shell
# install in user scope
claude plugin marketplace add huangboming/software-development-plugins
# install in project scope
claude plugin marketplace add huangboming/software-development-plugins --scope project

# install plugins
claude plugin install build@software-development-plugins
claude plugin install design@software-development-plugins
claude plugin install docs@software-development-plugins
claude plugin install harness@software-development-plugins
claude plugin install measure@software-development-plugins
claude plugin install misc@software-development-plugins
claude plugin install plan@software-development-plugins
claude plugin install ship@software-development-plugins
claude plugin install verify@software-development-plugins
```

Or install within a Claude Code session:

```text
/plugin marketplace add huangboming/software-development-plugins
/plugin install plan@software-development-plugins
/plugin install build@software-development-plugins
# …or any subset you need
```

See the [Claude Code plugin docs](https://docs.claude.com/en/docs/claude-code) for the full plugin workflow.

### Usage

Once a plugin is installed, Claude Code auto-invokes its skills from the natural-language triggers declared in each `SKILL.md` — you rarely need to call a skill by name. Agents are invoked via the `Task` tool (or by skills that delegate to them), e.g. `ship:write-readme` delegates to the `readme-writer` agent.

The two common entry points:

#### Start a brand-new project

Run this end-to-end when you're greenfield — no code, no backlog, maybe just an idea.

| Step | Phase | Say something like… | Skill |
|------|-------|---------------------|-------|
| 1 | Plan | "research the users and jobs for this idea" | `plan:research-users` |
| 2 | Plan | "write a product vision" | `plan:write-vision` |
| 3 | Plan | "write a PRD for the first release" | `plan:write-prd` |
| 4 | Build | "scaffold a new \<stack\> project" | `build:scaffold-project` |
| 5 | Harness | "set up project CLAUDE.md rules" / "add a skill for \<X\>" | `harness:create-rules`, `harness:create-skill` |
| 6 | Design | "design the technical spec for \<feature\>" | `design:design-spec` |
| 7 | — | **Implement the spec** — write the code yourself (or with Claude Code's editing loop); no dedicated skill. | _(no skill)_ |
| 8 | Build | During implementation, at each phase: "simplify this code" / "guard the tests" / "check for boundary leaks" | `build:simplify-code`, `build:guard-test`, `build:guard-boundary` |
| 9 | Build | "commit these changes" → "create a PR" | `build:commit-changes`, `build:create-pr` |
| 10 | Verify | "review the code on this branch" | `verify:review-code` |
| 11 | Docs | "write architecture docs" / "write API docs" | `docs:write-architecture`, `docs:write-api` |
| 12 | Ship | "set up the CI pipeline" → "write a README" → "tag v0.1.0" → "create a GitHub release" | `ship:generate-pipeline`, `ship:write-readme`, `ship:tag-release`, `ship:create-github-release` |

#### Work with an existing project

Use this loop for each feature, fix, or chore on an already-live codebase.

| Step | Phase | Say something like… | Skill |
|------|-------|---------------------|-------|
| 1 | Plan | "intake this new requirement into the backlog" → "prioritize" | `plan:intake-backlog`, `plan:prioritize-backlog` |
| 2 | Plan | "write a PRD for \<feature\>" | `plan:write-prd` |
| 3 | Design | "design the technical approach for \<feature\>" | `design:design-spec` |
| 4 | — | **Implement the spec** — write the code yourself (or with Claude Code's editing loop); no dedicated skill. | _(no skill)_ |
| 5 | Build | During implementation, at each phase: "simplify this code" / "guard the tests" / "check for boundary leaks" | `build:simplify-code`, `build:guard-test`, `build:guard-boundary` |
| 6 | Build | "commit changes" → "clean up the branch" → "create a PR" | `build:commit-changes`, `build:cleanup-branch`, `build:create-pr` |
| 7 | Verify | "review the code" | `verify:review-code` |
| 8 | Docs | "update the API / architecture docs" | `docs:write-api`, `docs:write-architecture` |
| 9 | Ship | "tag release" → "write changelog" → "write release notes" → "publish GitHub release" | `ship:tag-release`, `ship:write-changelog`, `ship:write-release-note`, `ship:create-github-release` |

You don't have to run every step. Skip what doesn't apply, and invoke skills out of order whenever the work demands it — this is a menu, not a pipeline.

## Settings

The [`settings/`](settings) directory holds **standalone reference material**, not part of the marketplace runtime. Copy what you want into your own Claude Code config:

- [`settings/settings.json`](settings/settings.json) — an example Claude Code `settings.json` with a baseline permission allow/ask/deny list, status line, and env vars. Drop into `~/.claude/settings.json` (user scope) or `.claude/settings.json` (project scope) as a starting point.
- [`settings/user-CLAUDE.md`](settings/user-CLAUDE.md) — example personal-preferences `CLAUDE.md` covering communication, problem-solving, and coding style. Drop into `~/.claude/CLAUDE.md` to apply it globally across projects.

## Contributing

### Add a new plugin

1. Create `plugins/<name>/.claude-plugin/plugin.json` with `name`, `version`, `description`, `author`.
2. Add at least one skill (`skills/<skill-name>/SKILL.md`) or agent (`agents/<agent>.md`).
3. Register the plugin in `.claude-plugin/marketplace.json`.
4. Validate:

   ```bash
   claude plugin validate plugins/<name>
   ```

### Add a skill or agent to an existing plugin

- **Skill**: create `plugins/<plugin>/skills/<skill-name>/SKILL.md`. The `description` frontmatter is the auto-invocation signal — include concrete trigger phrases users would say.
- **Agent**: create `plugins/<plugin>/agents/<agent>.md` with `name`, `description`, `tools`, `model`, and (if wrapping a skill) `skills: <plugin>:<skill-name>`. Keep the system prompt focused on role and constraints; defer the procedure to the referenced skill.

**Naming conventions**: `write-*` for generators (`write-prd`, `write-readme`), `guard-*` / `review-*` for quality checks, concrete verbs (`create-*`, `tag-*`, `cleanup-*`) for operations. Matching these keeps discovery-by-trigger predictable.

Full authoring conventions live in [CLAUDE.md](CLAUDE.md). The canonical reference for writing skills is [`plugins/harness/skills/create-skill/SKILL.md`](plugins/harness/skills/create-skill/SKILL.md).

## License

Licensed under the MIT License. See [LICENSE](LICENSE).
