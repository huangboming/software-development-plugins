---
name: create-hook
description: "Create Claude Code hooks (lifecycle event handlers in `.claude/settings.json` or plugin `hooks/hooks.json`). Triggers: 'create a hook', 'add a hook for...', 'set up a PreToolUse/PostToolUse/Stop/SessionStart hook', '/create-hook'."
---

# Hook Creator

Produce two artifacts: a JSON config entry and a script the event invokes.

## Process

1. Clarify the trigger, action, and placement (plugin / project / user-global).
2. Pick the event from the table; read `references/hooks-api.md` for that event's input/output schema.
3. Write the script. Default to Python in uv-script format — see `references/python-hook-scripts.md`. Use `scripts/init_hook.py` to scaffold.
4. Write the JSON config at the chosen location.
5. Test by piping sample stdin to the script (see Testing).

## Event Selection

| Intent | Event | Matcher | Can block? |
|--------|-------|---------|------------|
| Validate / gate a tool call before it runs | PreToolUse | tool name | Yes |
| Auto-format / lint / log after a tool succeeds | PostToolUse | tool name | Feedback only |
| React to a tool failure | PostToolUseFailure | tool name | No |
| Auto-approve permission dialogs | PermissionRequest | tool name | Yes |
| Validate or enrich a user prompt | UserPromptSubmit | — | Yes |
| Inject context or env at session start | SessionStart | source | No |
| Cleanup when session ends | SessionEnd | reason | No |
| Gate stopping until a condition holds | Stop | — | Yes |
| Inject context into subagents | SubagentStart | agent type | No |
| Gate subagent results | SubagentStop | agent type | Yes |
| Desktop / Slack notifications | Notification | notification type | No |
| Backup or log before compaction | PreCompact | trigger | No |

## Placement

| Location | Config file | Script location | Path macro |
|----------|------------|-----------------|------------|
| **Plugin** | `hooks/hooks.json` | `hooks/scripts/` | `${CLAUDE_PLUGIN_ROOT}` |
| **Project** | `.claude/settings.json` | `.claude/hooks/` | `$CLAUDE_PROJECT_DIR` |
| **User-global** | `~/.claude/settings.json` | `~/.claude/hooks/` | absolute path |

## Configuration Format

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<regex>",
        "hooks": [
          {
            "type": "command",
            "command": "uv run --script \"$CLAUDE_PROJECT_DIR/.claude/hooks/my-hook.py\"",
            "timeout": 600
          }
        ]
      }
    ]
  }
}
```

Omit `matcher` (or use `"*"`) to match every occurrence. Multiple hooks in one array run in parallel — any blocking result wins.

## Testing

```bash
echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rm -rf /"},"session_id":"test","cwd":"/tmp","permission_mode":"default"}' | uv run --script hooks/my-hook.py
echo "Exit code: $?"
```

Verify exit code, that stdout is JSON or empty, and that no `print()` debug output landed on stdout.

## Gotchas

- **`stdout` must be JSON or empty** — a stray `print("debug")` corrupts decision parsing. Route debugging to `stderr`.
- **Stop hooks loop forever without a guard** — check `input_data.get("stop_hook_active")` and exit 0 if true. Same for SubagentStop.
- **Plugin hooks must use `${CLAUDE_PLUGIN_ROOT}`** — relative paths break because plugin directories are cached and may be relocated.
- **Matcher is a regex, not a literal** — `"Edit"` also matches `"MultiEdit"`. Anchor with `^Edit$` for exact match.
- **`type: "command"` hooks run non-interactively** — they inherit `$PATH` but don't source `~/.zshrc`. Use absolute paths or set `$PATH` explicitly.
- **Exit-code-2 stderr is Claude's rejection reason** — write stderr so Claude (not just a human tailing logs) can act on it.

## References

- `references/hooks-api.md` — Full event input/output schemas, matcher targets, tool input shapes, hook types (`command` / `prompt` / `agent`).
- `references/python-hook-scripts.md` — uv-script structure, exit codes, JSON output patterns, loop safety.

## Scripts

- `scripts/init_hook.py <event> <name> --path <dir>` — Scaffold a uv-script hook with event-appropriate stdin handling and exit-code stubs.
