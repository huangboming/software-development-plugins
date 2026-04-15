#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Block git push --force, require --force-with-lease instead.

Enforces the cleanup-branch skill convention: never force push without lease.
"""

import json
import re
import sys


def main():
    input_data = json.load(sys.stdin)

    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    # Only inspect git push commands
    if not re.search(r"\bgit\s+push\b", command):
        sys.exit(0)

    # Allow --force-with-lease (check first, before checking bare --force)
    if re.search(r"--force-with-lease", command):
        sys.exit(0)

    # Block --force or -f
    if re.search(r"(--force|\s-f)(\s|$)", command):
        result = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    "git push --force is not allowed. "
                    "Use --force-with-lease instead to avoid overwriting others' work."
                ),
            }
        }
        print(json.dumps(result))

    sys.exit(0)


if __name__ == "__main__":
    main()
