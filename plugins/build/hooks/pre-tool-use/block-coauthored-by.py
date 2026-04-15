#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import json
import sys


def main():
    input_data = json.load(sys.stdin)

    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    # Only inspect git commit commands
    if "git commit" not in command:
        sys.exit(0)

    # Check for Co-Authored-By (case-insensitive)
    if "co-authored-by" in command.lower():
        result = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Commit message contains 'Co-Authored-By' trailer. Remove it and retry.",
            }
        }
        print(json.dumps(result))

    sys.exit(0)


if __name__ == "__main__":
    main()
