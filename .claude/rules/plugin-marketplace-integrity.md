# Claude Code Plugin Marketplace Integrity

Rules for the marketplace root (`.claude-plugin/marketplace.json`) and per-plugin manifests (`plugins/<plugin>/.claude-plugin/plugin.json`). These files govern what Claude Code can actually load — drift between them and the filesystem silently breaks discovery.

## Manifest contract

Every plugin directory must contain `.claude-plugin/plugin.json` with:

- `name` — matches the directory name exactly.
- `version` — SemVer string. Bump on any change that alters external behavior: new skill, renamed skill or agent, changed `description` trigger phrases, removed artifact.
- `description` — one sentence stating the plugin's scope.
- `author` — object with at least `name`.

The root `.claude-plugin/marketplace.json` must list every plugin directory under `plugins/` in its `plugins` array, with `name` matching the directory name and `source` set to `./plugins/<name>`.

## Always

- Always update `marketplace.json` in the same change that adds, removes, or renames a plugin. A plugin directory present on disk but missing from the manifest is invisible to Claude Code.
- Always run `claude plugin validate plugins/<plugin>` after any structural change (new skill/agent, renamed directory, edited manifest). Read the output — do not assume success.
- Always bump `version` when user-visible behavior changes, especially trigger phrases in skill or agent `description` fields. Downstream users pin to versions.

## Ordering when adding a plugin

1. Create `plugins/<name>/.claude-plugin/plugin.json`.
2. Add at least one artifact under `skills/` or `agents/`.
3. Register the plugin in `.claude-plugin/marketplace.json`.
4. Run `claude plugin validate plugins/<name>` and confirm no errors.

Skipping step 4 is the most common cause of shipped-broken plugins.

## Ordering when removing or renaming

- Renaming a plugin directory: rename on disk, update `plugin.json` `name`, update `marketplace.json` entry (both `name` and `source`), bump `version`, validate.
- Removing a plugin: delete the directory and remove its entry from `marketplace.json` in the same commit. Orphaned manifest entries break loading for every plugin listed after them in some loader implementations.

## Never

- Never leave the filesystem and `marketplace.json` out of sync across a commit — they must move together.
- Never share or reuse version numbers across plugins. Each plugin tracks its own release history.
- Never add unknown top-level keys to `marketplace.json` or `plugin.json` without checking the loader contract — unrecognized fields are ignored at best and rejected at worst.
- Never skip validation after a rename. Renames are the most common source of silent marketplace breakage.
