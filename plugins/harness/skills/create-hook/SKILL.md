---
name: create-hook
description: Create Claude Code hooks — lifecycle event handlers that run shell commands, LLM prompts, or agents at specific points during a session. Use when the user wants to create, add, or set up a hook for Claude Code, including hooks for tool validation, auto-formatting, notifications, security gates, context injection, logging, or any custom automation triggered by session events (PreToolUse, PostToolUse, Stop, Notification, SessionStart, etc.).
---

# Hook Creator

Create hooks by producing two things:

1. **Hook configuration** — JSON entries in a `hooks.json` or `settings.json` file
2. **Hook script** — the command that runs when the event fires

## Process

1. Clarify the user's goal: what should trigger the hook, what it should do, and where it should live. If the user is unsure what to build, read `references/recommended-hooks.md` and surface one or two starters that match their pain.
2. Select the event using the Event Selection table below; read `references/hooks-api.md` for that event's input/output schema.
3. Write the hook script. Default to Python in uv-script format — see `references/python-hook-scripts.md`. Use `scripts/init_hook.py` to scaffold.
4. Write the hook configuration JSON at the chosen location.
5. Test by piping sample JSON to stdin (see Testing below).

## Event Selection

Once the hook's purpose is settled, match it to an event. See `references/hooks-api.md` for full schemas and `references/hook-examples.md` for complete worked examples of the three most common patterns.

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
| Gate task completion (teams) | TaskCompleted | — | Exit 2 only |
| Nudge idle teammates | TeammateIdle | — | Exit 2 only |

## Placement

Ask the user where the hook should live:

| Location | Config file | Script location | Path macro |
|----------|------------|-----------------|------------|
| **Plugin** | `hooks/hooks.json` | `hooks/scripts/` | `${CLAUDE_PLUGIN_ROOT}` |
| **Project** | `.claude/settings.json` | `.claude/hooks/` | `$CLAUDE_PROJECT_DIR` |
| **User-global** | `~/.claude/settings.json` | `~/.claude/hooks/` | absolute path |

## Configuration Format

Minimal project-level example:

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

Swap `$CLAUDE_PROJECT_DIR` for `${CLAUDE_PLUGIN_ROOT}` when placing the hook in a plugin. See `references/hooks-api.md` for advanced fields (`async`, `statusMessage`) and for `type: "prompt"` / `type: "agent"` hooks.

- `matcher` is optional; omit it (or use `"*"`) to match every occurrence of the event.
- Multiple hooks in the same `hooks` array run in parallel — any blocking result wins.

## Testing

Pipe a realistic stdin payload to the script and check the exit code:

```bash
echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rm -rf /"},"session_id":"test","cwd":"/tmp","permission_mode":"default"}' | uv run --script hooks/my-hook.py
echo "Exit code: $?"
```

Verify the exit code matches the expected decision, stdout is valid JSON or empty, and no stray `print()` output lands on stdout.

## Gotchas

- **`stdout` must be JSON or empty** — a stray `print("debug")` silently corrupts decision parsing. Route all debugging output to `stderr`.
- **Stop hooks loop forever without a guard** — always check `input_data.get("stop_hook_active")` and exit 0 immediately if true. Same applies to SubagentStop.
- **Plugin hooks must use `${CLAUDE_PLUGIN_ROOT}`** — relative paths break because plugin directories are cached and may be relocated.
- **Matcher is a regex, not a literal** — `"Edit"` also matches `"MultiEdit"`. Anchor with `^Edit$` when the match must be exact.
- **Parallel hooks: any blocking result wins** — if two PreToolUse hooks match and one denies, the tool is denied regardless of the other's decision.
- **`type: "command"` hooks run non-interactively** — they inherit `$PATH` but do not source `~/.zshrc` or similar. Use absolute paths, or set `$PATH` explicitly for non-standard tooling.
- **Exit-code-2 stderr is Claude's rejection reason** — write stderr so Claude (not just a human tailing logs) can act on it.

## References

- `references/hooks-api.md` — Full event input/output schemas, matcher targets, tool input shapes, and hook types (`command` / `prompt` / `agent`). Read when you need event-specific details or are using a non-command hook type.
- `references/python-hook-scripts.md` — uv-script structure, exit codes, JSON output patterns, loop safety. Read when writing a Python hook script.
- `references/hook-examples.md` — Three complete worked examples: PreToolUse command guard, PostToolUse formatter, SessionStart context injector. Read when unsure how a full hook looks end-to-end.
- `references/recommended-hooks.md` — Catalog of 16 high-value starter hooks organized by purpose (safety, quality, context, observability, UX, workflow), with problem statements and implementation sketches. Read when the user is vague about what hook to build, or when looking for ideas beyond the SKILL.md table.

## Scripts

- `scripts/init_hook.py <event> <name> --path <dir>` — Scaffold a uv-script hook with event-appropriate stdin handling and exit-code stubs. Supported events: PreToolUse, PostToolUse, PostToolUseFailure, UserPromptSubmit, SessionStart, Stop, SubagentStop, Notification (any other event falls back to a TODO stub).
