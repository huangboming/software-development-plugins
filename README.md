# software-development-plugins

A Claude Code plugin marketplace that guides agents through the full software product lifecycle — discover, define, design, build, verify, ship, measure.

## About

This repository is a [Claude Code](https://claude.com/claude-code) **plugin marketplace**: a bundle of ten plugins that each cover one phase of the software product loop. Every plugin ships skills (auto-invoked playbooks) and agents (task-scoped subagents) so a Claude Code session can move from "what should we build?" to "what did shipping teach us?" without leaving the tool.

### The Plugins

| Plugin | Phase | What it covers |
|--------|-------|----------------|
| [`discover`](plugins/discover) | Discovery | Turn raw signals into framed opportunities (capture-signal, user-research prep, synthesis, problem framing, opportunity mapping, assumption tests, competitor teardowns). |
| [`define`](plugins/define) | Definition | Turn framed opportunities into committable specs (vision, prioritization, MVP slicing, success metrics, PRDs, user stories). |
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
claude plugin install define@software-development-plugins
claude plugin install design@software-development-plugins
claude plugin install discover@software-development-plugins
claude plugin install docs@software-development-plugins
claude plugin install harness@software-development-plugins
claude plugin install measure@software-development-plugins
claude plugin install misc@software-development-plugins
claude plugin install ship@software-development-plugins
claude plugin install verify@software-development-plugins
```

Or install within a Claude Code session:

```text
/plugin marketplace add huangboming/software-development-plugins
/plugin install discover@software-development-plugins
/plugin install define@software-development-plugins
/plugin install build@software-development-plugins
# …or any subset you need
```

See the [Claude Code plugin docs](https://docs.claude.com/en/docs/claude-code) for the full plugin workflow.

### Usage

Once a plugin is installed, Claude Code auto-invokes its skills from the natural-language triggers declared in each `SKILL.md` — you rarely need to call a skill by name. Agents are invoked via the `Task` tool (or by skills that delegate to them), e.g. `ship:write-readme` delegates to the `readme-writer` agent.

End-to-end workflows live in [`workflows/`](workflows/):

- [Greenfield project](workflows/greenfield-project.md) — idea to first GitHub release.
- [Existing project](workflows/existing-project.md) — feature, fix, or chore on a live codebase.

Each workflow lists the skill sequence, decision points (when to skip a step or loop back), and artifacts produced. These are menus, not pipelines — skip what doesn't apply, and invoke skills out of order whenever the work demands it.

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
