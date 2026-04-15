#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Scaffold a Claude Code hook script for a given event."""

import argparse
import sys
from pathlib import Path


HEADER = '''#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""{description}"""

import json
import sys


def main():
    input_data = json.load(sys.stdin)

{body}

if __name__ == "__main__":
    main()
'''


BODIES = {
    "PreToolUse": '''    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # To block:   print("reason", file=sys.stderr); sys.exit(2)
    # To allow with context: print(json.dumps({"hookSpecificOutput": {...}})); sys.exit(0)

    sys.exit(0)
''',
    "PostToolUse": '''    tool_name = input_data.get("tool_name", "")
    tool_response = input_data.get("tool_response", {})

    # Post-process output, run formatters, log results, etc.

    sys.exit(0)
''',
    "PostToolUseFailure": '''    tool_name = input_data.get("tool_name", "")
    error = input_data.get("error", "")

    # Analyze, alert, or log the failure.

    sys.exit(0)
''',
    "UserPromptSubmit": '''    prompt = input_data.get("prompt", "")

    # To block: print(json.dumps({"decision": "block", "reason": "..."})); sys.exit(0)

    sys.exit(0)
''',
    "SessionStart": '''    source = input_data.get("source", "startup")

    # Inject context:
    # print(json.dumps({"hookSpecificOutput": {
    #     "hookEventName": "SessionStart",
    #     "additionalContext": "..."
    # }}))

    sys.exit(0)
''',
    "Stop": '''    # Infinite-loop guard — always first.
    if input_data.get("stop_hook_active"):
        sys.exit(0)

    # To block stopping: print(json.dumps({"decision": "block", "reason": "..."}))

    sys.exit(0)
''',
    "SubagentStop": '''    if input_data.get("stop_hook_active"):
        sys.exit(0)

    agent_type = input_data.get("agent_type", "")

    sys.exit(0)
''',
    "Notification": '''    message = input_data.get("message", "")
    notification_type = input_data.get("notification_type", "")

    # Send desktop / Slack / etc. notification.

    sys.exit(0)
''',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "event",
        help="Hook event (PreToolUse, PostToolUse, Stop, SessionStart, UserPromptSubmit, SubagentStop, Notification, PostToolUseFailure)",
    )
    parser.add_argument("name", help="Hook script name (kebab-case, no extension)")
    parser.add_argument("--path", default=".", help="Directory to write the script into (default: .)")
    parser.add_argument("--description", default="", help="One-line docstring for the script")
    args = parser.parse_args()

    body = BODIES.get(
        args.event,
        f'    # TODO: implement logic for event "{args.event}"\n    sys.exit(0)\n',
    )
    description = args.description or f"{args.event} hook: {args.name}"
    content = HEADER.format(description=description, body=body)

    out_dir = Path(args.path)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{args.name}.py"
    if out_file.exists():
        print(f"Error: {out_file} already exists", file=sys.stderr)
        sys.exit(1)
    out_file.write_text(content)
    out_file.chmod(0o755)
    print(f"Created {out_file}")


if __name__ == "__main__":
    main()
