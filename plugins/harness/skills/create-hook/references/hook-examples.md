# Hook Examples

Three complete end-to-end hook examples. Each shows both the configuration JSON and the Python script.

## Table of Contents

- [PreToolUse: Bash Command Guard](#pretooluse-bash-command-guard)
- [PostToolUse: Auto-Format Python on Write](#posttooluse-auto-format-python-on-write)
- [SessionStart: Inject Git Branch Context](#sessionstart-inject-git-branch-context)

---

## PreToolUse: Bash Command Guard

Block destructive shell commands before they run.

### Configuration (`.claude/settings.json`)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^Bash$",
        "hooks": [
          {
            "type": "command",
            "command": "uv run --script \"$CLAUDE_PROJECT_DIR/.claude/hooks/bash-guard.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### Script (`.claude/hooks/bash-guard.py`)

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Block destructive shell commands."""

import json
import re
import sys

DANGEROUS = [
    r"\brm\s+-rf?\s+/",
    r":\(\)\s*\{",          # fork bomb
    r"\bdd\s+if=.*of=/dev/[sh]d",
]


def main():
    data = json.load(sys.stdin)
    command = data.get("tool_input", {}).get("command", "")

    for pattern in DANGEROUS:
        if re.search(pattern, command):
            print(f"Blocked: command matches {pattern!r}", file=sys.stderr)
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
```

---

## PostToolUse: Auto-Format Python on Write

Run `ruff format` after Claude writes or edits a Python file.

### Configuration (`.claude/settings.json`)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "^(Write|Edit|MultiEdit)$",
        "hooks": [
          {
            "type": "command",
            "command": "uv run --script \"$CLAUDE_PROJECT_DIR/.claude/hooks/format-python.py\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Script (`.claude/hooks/format-python.py`)

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Format Python files with ruff after Write/Edit/MultiEdit."""

import json
import subprocess
import sys


def main():
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    if not file_path.endswith(".py"):
        sys.exit(0)

    result = subprocess.run(
        ["ruff", "format", file_path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"ruff format failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)  # non-blocking; surfaces in verbose mode

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": f"Formatted {file_path} with ruff",
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
```

---

## SessionStart: Inject Git Branch Context

At session start, tell Claude what branch is checked out and how many files are modified.

### Configuration (`.claude/settings.json`)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "uv run --script \"$CLAUDE_PROJECT_DIR/.claude/hooks/git-context.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Script (`.claude/hooks/git-context.py`)

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Inject git branch and modified-files count at session start."""

import json
import subprocess
import sys


def git(*args):
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()


def main():
    json.load(sys.stdin)  # drain stdin; no fields needed

    branch = git("rev-parse", "--abbrev-ref", "HEAD") or "(detached)"
    modified = git("status", "--porcelain").splitlines()
    summary = f"Branch: {branch}\nModified files: {len(modified)}"

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": summary,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
```
