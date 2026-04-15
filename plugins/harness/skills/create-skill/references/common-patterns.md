# Common Patterns to Consider

Three patterns show up in most production skills. Consider whether each applies before writing SKILL.md.

## Gotchas Section

A `## Gotchas` section is the highest-signal part of most skills. It captures specific failure modes — wrong defaults, quiet footguns, surprising edge cases — so the next invocation avoids them.

Every skill should have one. Start it empty or with known issues, then grow it every time iteration uncovers a new failure. Each entry should be terse: the symptom, the fix, and why the default is wrong.

```markdown
## Gotchas

- **Empty `items` array deserializes as `null`** — coerce with `items ?? []` before iterating.
- **`migrate up` blocks on open connections** — run `db drain` first or the command hangs without output.
- **Do not use `time.Now()` in tests** — use the injected clock; otherwise snapshot tests drift across timezones.
```

## First-Run Configuration

Some skills need user-specific context before they can run — a Slack channel, a project ID, a data source UID. Store this in a `config.json` file so subsequent invocations pick it up without re-prompting.

On invocation, check whether the config exists. If not, ask the user for the values and write the file. For multiple-choice setup questions, instruct Claude to use the `AskUserQuestion` tool rather than free-form prompting.

**Location**: write user-specific config to `${CLAUDE_PLUGIN_DATA}` (see below) so it survives plugin upgrades. Only use a `config.json` inside the skill directory for defaults that are part of the skill itself.

## Persistent Data Across Sessions

Skills can keep state between runs — logs of prior invocations, cached lookups, append-only history. Do not write this to the skill directory: upgrading the skill (or reinstalling the plugin) may wipe it.

Use `${CLAUDE_PLUGIN_DATA}`, a stable per-plugin directory provided by Claude Code. Reference it directly in SKILL.md so Claude reads/writes to the right place. Example: a `standup-post` skill appends each generated post to `${CLAUDE_PLUGIN_DATA}/standups.log` so the next run can diff against yesterday.
