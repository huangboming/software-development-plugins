# Recommended Starter Hooks

Catalog of high-value hooks to suggest when the user isn't sure what to build. Each entry lists the problem it solves, the event wiring, and a sketch of the check. Three (★) have complete runnable recipes in `hook-examples.md`; the rest are sketches — use `scripts/init_hook.py` to scaffold and adapt.

## Table of Contents

- [Safety guardrails](#safety-guardrails)
- [Code quality automation](#code-quality-automation)
- [Context enrichment](#context-enrichment)
- [Observability & audit](#observability--audit)
- [UX & notifications](#ux--notifications)
- [Workflow enforcement](#workflow-enforcement)
- [Picking a starter](#picking-a-starter)

---

## Safety guardrails

### ★ Destructive-command guard — `PreToolUse`, `^Bash$`

**Problem:** Claude can issue `rm -rf`, `dd`, or fork-bomb commands when debugging or cleaning up. These are catastrophically irreversible.

**Sketch:** Regex-match `tool_input.command` against a small denylist (`rm -rf /`, `:() { :|:& };:`, `dd if=.* of=/dev/[sh]d`). On match, print the reason to stderr and exit 2.

**Gotcha:** Keep the denylist narrow — over-broad patterns block legitimate cleanup (`rm -rf node_modules` is fine).

Full recipe in `hook-examples.md`.

### Secret-file guard — `PreToolUse`, `^(Write|Edit|MultiEdit)$`

**Problem:** Claude may edit files containing secrets (`.env`, `*.pem`, `credentials.json`, `id_rsa`). Writes can leak keys into commits, caches, or terminal scrollback.

**Sketch:** Match `tool_input.file_path` basename/suffix against a denylist. Deny with a clear reason pointing to the project's secret-management workflow (1Password, Vault, `.env.example`, etc.).

**Gotcha:** Also match common variants (`.env.local`, `.env.production`) — not just `.env`.

### Protected-path guard — `PreToolUse`, `^(Write|Edit|Bash)$`

**Problem:** Accidental edits to `.git/`, `node_modules/`, `/etc/`, or paths outside the project root can corrupt state in ways that are hard to notice.

**Sketch:** Resolve `tool_input.file_path` (or parse the Bash command target); reject anything outside `$CLAUDE_PROJECT_DIR` or inside a `.git/` subtree. For Bash, look for `>`, `>>`, `tee`, `mv`, `cp` targets.

**Gotcha:** Parsing Bash for write targets is error-prone. Start by blocking only the obvious cases (`>`, `>>`, `rm`) and accept that some edits slip through.

---

## Code quality automation

### ★ Auto-format on save — `PostToolUse`, `^(Write|Edit|MultiEdit)$`

**Problem:** Formatters (prettier, ruff, gofmt, rustfmt) drift when Claude doesn't run them after every edit, producing noisy diffs that mask real changes.

**Sketch:** Inspect `tool_input.file_path` extension; shell out to the matching formatter; emit `additionalContext` summarizing what ran so Claude knows the file was modified post-edit.

Full recipe in `hook-examples.md`.

### Type-check or test gate on Stop — `Stop`

**Problem:** Claude happily ends turns with broken types or failing tests, forcing a re-prompt loop.

**Sketch:**

```python
if input_data.get("stop_hook_active"):
    sys.exit(0)

result = subprocess.run(["pytest", "-q", "--no-header"], capture_output=True, text=True)
if result.returncode != 0:
    print(json.dumps({
        "decision": "block",
        "reason": f"Tests failed:\n{result.stdout[-2000:]}"
    }))
    sys.exit(0)
```

**Gotcha:** Full test suites can be slow. Scope to changed packages (`pytest path/to/changed`), use `--changed-since main`, or cache successful runs by commit SHA. A Stop hook that takes 30s every turn is worse than flaky tests.

### Lint surfacer — `PostToolUse`, `^(Write|Edit|MultiEdit)$`

**Problem:** Lint warnings don't surface unless a human runs the linter; Claude misses signal it could act on.

**Sketch:** Run the linter on the edited file. If warnings exist, emit them as `additionalContext` so Claude sees them in the next turn — don't block, just inform.

---

## Context enrichment

### ★ Git-context injector — `SessionStart`, `startup|resume`

**Problem:** Claude starts every session blind to repo state — branch, modified files, ongoing rebase, unpushed commits.

**Sketch:** Shell out to `git rev-parse --abbrev-ref HEAD`, `git status --porcelain`, `git log origin..HEAD`. Emit a short summary via `additionalContext`.

Full recipe in `hook-examples.md`.

### Project-env loader — `SessionStart`

**Problem:** Project-specific env vars (`DATABASE_URL`, `AWS_PROFILE`, `NODE_ENV`) aren't available to Claude's shell unless you source them every session.

**Sketch:** Parse `.env.local` (or similar); write `export KEY=value` lines to `$CLAUDE_ENV_FILE` so they persist for the session. Skip secrets that shouldn't enter context.

**Gotcha:** `$CLAUDE_ENV_FILE` is only available on `SessionStart`. Don't read secrets into `additionalContext` — they'd land in transcripts.

### Recent-activity summary — `SessionStart`, `resume|compact`

**Problem:** After a compact or resume, Claude loses short-term memory of what it just worked on.

**Sketch:** Read `$CLAUDE_PLUGIN_DATA/recent-files.log` (populated by a companion PostToolUse hook that logs file edits) and inject the last N files touched into `additionalContext`.

---

## Observability & audit

### Command audit log — `PostToolUse`, `^Bash$`

**Problem:** You want a post-hoc record of every shell command Claude ran — for debugging, compliance, or reviewing a suspicious session.

**Sketch:** Append `{timestamp, session_id, command, exit_code}` as JSON lines to `$CLAUDE_PLUGIN_DATA/commands.log`. Cheap, always-on, never blocks.

### File-change log — `PostToolUse`, `^(Write|Edit|MultiEdit)$`

**Problem:** Hard to answer "what did Claude touch this session?" without diffing every file.

**Sketch:** Append `{timestamp, tool, file_path}` to `$CLAUDE_PLUGIN_DATA/changes.log`. Rotate daily or by session_id.

### TODO tracker — `PostToolUse`, `^(Write|Edit|MultiEdit)$`

**Problem:** New `TODO` / `FIXME` comments accumulate without anyone noticing.

**Sketch:** Read the edited file, grep for new TODO/FIXME vs. the previous version, append to a tracker file. Optionally surface the count as `systemMessage`.

---

## UX & notifications

### Desktop notification — `Notification`, `permission_prompt|idle_prompt`

**Problem:** You alt-tab while Claude runs; permission prompts and idle states go unnoticed.

**Sketch:** Shell out to `osascript -e 'display notification "..." with title "Claude"'` (macOS) or `notify-send "Claude" "..."` (Linux). Skip on remote (`$CLAUDE_CODE_REMOTE == "true"`).

### Terminal bell — `Notification`

**Problem:** Minimal version of the above — works over SSH, no dependencies.

**Sketch:** `sys.stderr.write("\a")`; exit 0. That's the whole hook.

### Slack / webhook ping on long tasks — `Stop` or `SessionEnd`

**Problem:** You kick off a multi-minute task and want a ping when it finishes.

**Sketch:** POST to a webhook URL stored in `$CLAUDE_PLUGIN_DATA/config.json`. Gate by elapsed session time (e.g., only ping if the session lasted > 2 minutes) so short tasks don't spam.

---

## Workflow enforcement

### Commit-message enforcer — `PreToolUse`, `^Bash$`

**Problem:** Ad-hoc commit messages break conventional-commits tooling (changelogs, semver bumps, PR titles).

**Sketch:** Parse `git commit -m "..."` (or `-F <file>`) from the Bash command; regex-match against `(feat|fix|chore|docs|refactor|test|perf|build|ci)(\(.+\))?: .+`. Deny non-matches with a format reminder.

**Gotcha:** Don't match on `git commit --amend` without `-m` — it opens an editor and you can't inspect the message.

### Branch protection — `PreToolUse`, `^Bash$`

**Problem:** `git push origin main` or direct commits to `main` slip through when Claude is operating autonomously.

**Sketch:** Read current branch with `git rev-parse --abbrev-ref HEAD`. If on `main`/`master`/`trunk` and the command matches `git (commit|push)`, deny with a "create a feature branch first" reason.

### Test-coverage guard — `Stop`

**Problem:** Claude adds new code without tests and stops cleanly.

**Sketch:** Use `git diff --name-only <base>` to find changed source files; for each, check if a corresponding test file (`*.test.ts`, `test_*.py`) was also touched. Warn or block when source-only changes are detected.

**Gotcha:** This will false-positive on refactors and config changes. Limit to specific directories (`src/`, `lib/`) and exempt certain file patterns.

---

## Picking a starter

When the user is vague about what they want, ask two questions:

1. **What has bitten you recently?** — accidental `rm`, broken types shipped, secrets committed, missing git context. Pick the matching guardrail.
2. **What do you re-run by hand every session?** — formatters, env sourcing, test runs. Automate it.

**Default trio for a fresh Claude Code install on a real project:**

1. **Destructive-command guard** (PreToolUse + Bash) — the irreversible-damage floor
2. **Auto-format on save** (PostToolUse + Write/Edit) — removes noise from every review
3. **Git-context injector** (SessionStart) — Claude stops asking "what branch am I on?"

These three cover ~80% of the daily pain with near-zero failure modes. Add a **test/type gate on Stop** next if the project has a fast-enough test suite; hold off if CI takes more than ~30s.
