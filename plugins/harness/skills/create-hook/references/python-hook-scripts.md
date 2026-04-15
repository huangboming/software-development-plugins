# Python Hook Scripts

Conventions for writing Claude Code hook scripts in Python.

## Table of Contents

- [uv Script Format](#uv-script-format)
- [Script Structure](#script-structure)
- [Exit Codes](#exit-codes)
- [stdout / stderr Rules](#stdout--stderr-rules)
- [JSON Output Patterns](#json-output-patterns)
- [Stop Hook Loop Safety](#stop-hook-loop-safety)

## uv Script Format

Write hooks as standalone `uv run --script` files (PEP 723). The frontmatter declares the Python version and dependencies — no virtualenv or `pip install` step is needed.

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
```

Either `chmod +x` the file or invoke it via `uv run --script path/to/script.py` in the hook config.

## Script Structure

Every hook script follows this pattern:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import json
import sys


def main():
    input_data = json.load(sys.stdin)

    # ... hook logic ...

    sys.exit(0)


if __name__ == "__main__":
    main()
```

Read stdin once at the top. The input schema for each event is in `hooks-api.md`.

## Exit Codes

| Exit | Meaning | stdout | stderr |
|------|---------|--------|--------|
| 0 | Success | Parsed as JSON if non-empty | Shown in verbose mode |
| 2 | Block the action | Ignored | Fed to Claude as error context |
| Other | Non-blocking error | Ignored | Shown in verbose mode |

## stdout / stderr Rules

- **stdout** must be valid JSON or empty. A stray `print()` corrupts decision parsing.
- **stderr** is shown to Claude on exit 2 and in verbose mode on other non-zero exits. Safe for debugging output.
- Use `json.dumps(result)` — never hand-assemble JSON.

## JSON Output Patterns

### PreToolUse — allow / deny / modify input

```python
result = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",  # or "allow" / "ask"
        "permissionDecisionReason": "Blocked: destructive command",
    }
}
print(json.dumps(result))
sys.exit(0)
```

### Stop / UserPromptSubmit / PostToolUse — block with feedback

```python
result = {"decision": "block", "reason": "Tests must pass before stopping"}
print(json.dumps(result))
sys.exit(0)
```

### SessionStart / SubagentStart — inject context

```python
result = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "Branch: main\nModified: 3 files",
    }
}
print(json.dumps(result))
sys.exit(0)
```

### Simple block via stderr

```python
print("Blocked: reason here", file=sys.stderr)
sys.exit(2)
```

Exit 2 with stderr is the simplest way to block — no JSON required. Claude receives the stderr text as the rejection reason.

## Stop Hook Loop Safety

Stop and SubagentStop hooks can re-trigger themselves indefinitely if they keep blocking. Always guard:

```python
def main():
    input_data = json.load(sys.stdin)

    if input_data.get("stop_hook_active"):
        sys.exit(0)  # Already fired once — don't block again

    # ... normal logic ...
```
