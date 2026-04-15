# Hooks API Reference

## Table of Contents

- [Configuration Structure](#configuration-structure)
- [Hook Types](#hook-types)
- [Exit Codes & Output](#exit-codes--output)
- [Universal Output Fields](#universal-output-fields)
- [Decision Control Patterns](#decision-control-patterns)
- [Environment Variables](#environment-variables)
- [Common Input Fields](#common-input-fields)
- [Event Reference](#event-reference)
  - [SessionStart](#sessionstart)
  - [UserPromptSubmit](#userpromptsubmit)
  - [PreToolUse](#pretooluse)
  - [PermissionRequest](#permissionrequest)
  - [PostToolUse](#posttooluse)
  - [PostToolUseFailure](#posttoolusefailure)
  - [Notification](#notification)
  - [SubagentStart](#subagentstart)
  - [SubagentStop](#subagentstop)
  - [Stop](#stop)
  - [TeammateIdle](#teammateidle)
  - [TaskCompleted](#taskcompleted)
  - [PreCompact](#precompact)
  - [SessionEnd](#sessionend)
- [Tool Input Schemas](#tool-input-schemas)
- [Matcher Patterns](#matcher-patterns)

---

## Configuration Structure

```json
{
  "hooks": {
    "<EVENT_NAME>": [
      {
        "matcher": "<REGEX_PATTERN>",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script",
            "timeout": 600,
            "async": false,
            "statusMessage": "Running hook..."
          }
        ]
      }
    ]
  }
}
```

Three nesting levels: event → matcher group (optional) → hook handlers.

### Configuration Locations

| Location | Scope |
|----------|-------|
| `~/.claude/settings.json` | All projects (user-wide) |
| `.claude/settings.json` | Single project (committable) |
| `.claude/settings.local.json` | Single project (gitignored) |
| Plugin `hooks/hooks.json` | When plugin enabled |
| Skill/agent YAML frontmatter | When component active |

---

## Hook Types

### Command (`type: "command"`)

Shell command receiving JSON via stdin.

```json
{
  "type": "command",
  "command": "uv run --script \"$CLAUDE_PROJECT_DIR/hooks/my-hook.py\"",
  "timeout": 600,
  "async": false
}
```

### Prompt (`type: "prompt"`)

Single-turn LLM evaluation. Must return `{ "ok": true/false, "reason": "..." }`.

```json
{
  "type": "prompt",
  "prompt": "Evaluate if this command is safe: $ARGUMENTS",
  "model": "haiku",
  "timeout": 30
}
```

### Agent (`type: "agent"`)

Multi-turn subagent with tool access. Same response schema as prompt hooks.

```json
{
  "type": "agent",
  "prompt": "Verify all tests pass: $ARGUMENTS",
  "model": "sonnet",
  "timeout": 60
}
```

**Prompt/Agent events**: PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, UserPromptSubmit, Stop, SubagentStop, TaskCompleted.

---

## Exit Codes & Output

| Exit Code | Behavior | JSON Processed? |
|-----------|----------|----------------|
| **0** | Success | Yes — stdout parsed for JSON |
| **2** | Block action | No — stderr fed to Claude as error |
| **Other** | Non-blocking error | No — stderr shown in verbose mode |

---

## Universal Output Fields

These work across **all events** when exiting with code 0:

```json
{
  "continue": false,
  "stopReason": "Build failed",
  "suppressOutput": false,
  "systemMessage": "Warning: check test results"
}
```

- `continue: false` — stops Claude entirely (overrides all other decisions)
- `stopReason` — shown to user when `continue: false`
- `suppressOutput` — hides stdout from verbose mode
- `systemMessage` — warning shown to user

---

## Decision Control Patterns

### Pattern A: Top-level `decision` (block/allow)

**Events**: UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop, SubagentStop

```json
{
  "decision": "block",
  "reason": "Tests must pass before stopping"
}
```

### Pattern B: `hookSpecificOutput` for PreToolUse

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Explanation",
    "updatedInput": {},
    "additionalContext": "Extra info for Claude"
  }
}
```

### Pattern C: `hookSpecificOutput` for PermissionRequest

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": {},
      "updatedPermissions": {},
      "message": "Denial reason",
      "interrupt": true
    }
  }
}
```

### Pattern D: Exit code only

**Events**: TeammateIdle, TaskCompleted — exit code 2 blocks, stderr provides feedback.

---

## Environment Variables

| Variable | Available In | Description |
|----------|-------------|-------------|
| `$CLAUDE_PROJECT_DIR` | All hooks | Project root directory |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin hooks | Plugin cache directory |
| `$CLAUDE_ENV_FILE` | SessionStart only | File path for persisting env vars |
| `$CLAUDE_CODE_REMOTE` | All hooks | `"true"` in remote environments |

---

## Common Input Fields

Every hook receives via stdin:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/dir",
  "permission_mode": "default|plan|acceptEdits|dontAsk|bypassPermissions",
  "hook_event_name": "PreToolUse"
}
```

---

## Event Reference

### SessionStart

Fires when a session begins or resumes.

**Matcher values**: `startup`, `resume`, `clear`, `compact`
**Can block**: No

**Additional input**:

```json
{
  "source": "startup|resume|clear|compact",
  "model": "claude-sonnet-4-5-20250929",
  "agent_type": "custom-agent-name"
}
```

**Output**: Plain text stdout added as context automatically. Or use:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Branch: main\nModified: 3 files"
  }
}
```

**Special**: Write to `$CLAUDE_ENV_FILE` to persist env vars for the session.

---

### UserPromptSubmit

Fires when the user submits a prompt.

**Matcher**: None (always fires)
**Can block**: Yes (Pattern A)

**Additional input**:

```json
{
  "prompt": "the user's submitted prompt text"
}
```

---

### PreToolUse

Fires before a tool executes.

**Matcher values**: Tool names — `Bash`, `Write`, `Edit`, `Read`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Task`, `mcp__<server>__<tool>`
**Can block**: Yes (Pattern B — `permissionDecision: "deny"`)

**Additional input**:

```json
{
  "tool_name": "Bash",
  "tool_input": { "command": "npm test", "description": "Run tests" },
  "tool_use_id": "toolu_01ABC..."
}
```

**Output** (Pattern B): Can allow, deny, modify input, or add context.

---

### PermissionRequest

Fires when a permission dialog appears.

**Matcher values**: Tool names (same as PreToolUse)
**Can block**: Yes (Pattern C)

**Additional input**:

```json
{
  "tool_name": "Bash",
  "tool_input": {},
  "permission_suggestions": [
    { "type": "toolAlwaysAllow", "tool": "Bash" }
  ]
}
```

---

### PostToolUse

Fires after a tool succeeds.

**Matcher values**: Tool names
**Can block**: No (but `decision: "block"` provides feedback to Claude)

**Additional input**:

```json
{
  "tool_name": "Write",
  "tool_input": {},
  "tool_response": { "filePath": "/path/to/file.txt", "success": true },
  "tool_use_id": "toolu_01ABC..."
}
```

**Output**:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Formatted with prettier",
    "updatedMCPToolOutput": "new value"
  }
}
```

---

### PostToolUseFailure

Fires after a tool fails.

**Matcher values**: Tool names
**Can block**: No

**Additional input**:

```json
{
  "tool_name": "Bash",
  "tool_input": {},
  "tool_use_id": "toolu_01ABC...",
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false
}
```

---

### Notification

Fires when Claude sends a notification.

**Matcher values**: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`
**Can block**: No

**Additional input**:

```json
{
  "message": "Claude needs your permission",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

---

### SubagentStart

Fires when a subagent spawns.

**Matcher values**: Agent types — `Bash`, `Explore`, `Plan`, or custom agent names
**Can block**: No

**Additional input**:

```json
{
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

**Output**: Can inject context via `additionalContext`.

---

### SubagentStop

Fires when a subagent finishes.

**Matcher values**: Agent types
**Can block**: Yes (Pattern A)

**Additional input**:

```json
{
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/.../subagents/agent-def456.jsonl"
}
```

---

### Stop

Fires when the main agent finishes a response.

**Matcher**: None (always fires)
**Can block**: Yes (Pattern A)

**Additional input**:

```json
{
  "stop_hook_active": true
}
```

**Critical**: Always check `stop_hook_active` to prevent infinite continuation loops. If `true`, the hook was already triggered once — exit 0 without blocking.

---

### TeammateIdle

Fires when a team member goes idle.

**Matcher**: None (always fires)
**Can block**: Yes (exit code 2 only)

**Additional input**:

```json
{
  "teammate_name": "researcher",
  "team_name": "my-project"
}
```

---

### TaskCompleted

Fires when a task is marked complete.

**Matcher**: None (always fires)
**Can block**: Yes (exit code 2 only)

**Additional input**:

```json
{
  "task_id": "task-001",
  "task_subject": "Implement authentication",
  "task_description": "Add login/signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

---

### PreCompact

Fires before context compaction.

**Matcher values**: `manual`, `auto`
**Can block**: No

**Additional input**:

```json
{
  "trigger": "manual|auto",
  "custom_instructions": ""
}
```

---

### SessionEnd

Fires when a session terminates.

**Matcher values**: `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`
**Can block**: No

**Additional input**:

```json
{
  "reason": "clear|logout|prompt_input_exit|bypass_permissions_disabled|other"
}
```

---

## Tool Input Schemas

These are the `tool_input` shapes for PreToolUse/PostToolUse/PermissionRequest:

### Bash

```json
{ "command": "npm test", "description": "Run tests", "timeout": 120000, "run_in_background": false }
```

### Write

```json
{ "file_path": "/absolute/path/to/file.txt", "content": "file content" }
```

### Edit

```json
{ "file_path": "/path/to/file.txt", "old_string": "original", "new_string": "replacement", "replace_all": false }
```

### Read

```json
{ "file_path": "/path/to/file.txt", "offset": 10, "limit": 50 }
```

### Glob

```json
{ "pattern": "**/*.ts", "path": "/optional/dir" }
```

### Grep

```json
{ "pattern": "TODO.*fix", "path": "/path", "glob": "*.ts", "output_mode": "content", "-i": true, "multiline": false }
```

### WebFetch

```json
{ "url": "https://example.com", "prompt": "Extract endpoints" }
```

### WebSearch

```json
{ "query": "search terms", "allowed_domains": [], "blocked_domains": [] }
```

### Task (subagent)

```json
{ "prompt": "Find all endpoints", "description": "API discovery", "subagent_type": "Explore", "model": "sonnet" }
```

### MCP Tools

Tool name pattern: `mcp__<server>__<tool>`. Input schema depends on the MCP server.

---

## Matcher Patterns

Matchers are regex strings. Match target depends on event type.

| Event | Matches Against | Examples |
|-------|----------------|----------|
| PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest | `tool_name` | `Bash`, `Edit\|Write`, `mcp__.*` |
| SessionStart | `source` | `startup`, `resume` |
| SessionEnd | `reason` | `clear`, `logout` |
| Notification | `notification_type` | `permission_prompt`, `idle_prompt` |
| SubagentStart, SubagentStop | `agent_type` | `Bash`, `Explore`, `Plan` |
| PreCompact | `trigger` | `manual`, `auto` |
| UserPromptSubmit, Stop, TeammateIdle, TaskCompleted | N/A | Always fires |

Omitting `matcher` or using `"*"` matches everything.
