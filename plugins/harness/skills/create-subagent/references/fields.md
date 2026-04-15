# Subagent Field Reference

## Frontmatter Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Unique identifier. Lowercase letters, numbers, hyphens only. |
| `description` | Yes | string | When Claude should delegate to this subagent. This is the primary trigger mechanism. |
| `tools` | No | string | Comma-separated tool allowlist. Inherits all tools if omitted. |
| `disallowedTools` | No | string | Tools to deny, removed from inherited/specified list. |
| `model` | No | string | `sonnet`, `opus`, `haiku`, or `inherit` (default: `inherit`). |
| `permissionMode` | No | string | `default`, `acceptEdits`, `delegate`, `dontAsk`, `bypassPermissions`, or `plan`. |
| `maxTurns` | No | integer | Maximum agentic turns before subagent stops. |
| `skills` | No | string | Skills to inject into subagent context at startup. |
| `mcpServers` | No | string | MCP servers available to this subagent. |
| `hooks` | No | object | Lifecycle hooks scoped to this subagent (e.g., PreToolUse). |
| `memory` | No | string | Persistent memory scope: `user`, `project`, or `local`. |

## Available Tools

Common tools to include in the `tools` field:

| Tool | Purpose |
|------|---------|
| `Read` | Read file contents |
| `Edit` | Edit existing files |
| `Write` | Create/overwrite files |
| `Bash` | Execute shell commands |
| `Glob` | Find files by pattern |
| `Grep` | Search file contents |
| `WebFetch` | Fetch and process web content |
| `WebSearch` | Search the web |
| `Task` | Spawn sub-subagents. Use `Task(agent1, agent2)` to restrict which. |
| `NotebookEdit` | Edit Jupyter notebooks |

## Task Tool Restriction Syntax

Control which subagents can be spawned:

- `Task` — allow spawning any subagent
- `Task(worker, researcher)` — only allow spawning `worker` and `researcher`
- Omit `Task` entirely — agent cannot spawn subagents

## Model Selection Guide

| Model | Best For |
|-------|----------|
| `haiku` | Fast, cheap tasks: search, grep, simple analysis |
| `sonnet` | Balanced: code review, moderate complexity |
| `opus` | Complex reasoning, architecture, nuanced decisions |
| `inherit` | Use whatever the parent agent uses (default) |

## Memory Scopes

| Scope | Persists Across | Shareable via Git |
|-------|-----------------|-------------------|
| `user` | All projects | No |
| `project` | Current project | Yes |
| `local` | Current project | No |

## Hooks Example

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
```
