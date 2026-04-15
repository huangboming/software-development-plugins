---
name: tag-release
description: "Tag a release, bump version, create a git tag. Triggers: 'tag release', 'git tag', 'bump version', 'tag v2.1', '/tag-release'."
---

# Tag Release

## Steps

1. Determine version and target commit
2. Bump version files
3. Compose the tag message
4. Create the tag
5. Verify and present

## Step 1: Determine Version and Target Commit

**Version:**
- Use the version the user specifies (e.g., "tag v2.1.0").
- If no version given but a changelog or release notes were generated earlier in this conversation, use that version.
- If neither, check for version indicators:
  1. Most recent git tag: `git tag --sort=-creatordate | head -1`
  2. `CHANGELOG.md` — latest entry version
  3. Package manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, etc.) — current version field
- Propose the next version based on semver signals (breaking → major, features → minor, fixes → patch).
- Confirm with the user before proceeding.

**Target commit:**
- Default to `HEAD` (or the bump commit if Step 2 creates one).
- If the user specifies a commit, branch, or SHA, use that — skip Step 2 since you're tagging a historical commit.
- Confirm: "Tagging commit `<short-sha>` (`<subject>`) as `v<version>`. Correct?"

**Tag format:** `v<version>` (e.g., `v2.1.0`). Match existing convention if different (check `git tag --sort=-creatordate | head -5`).

## Step 2: Bump Version Files

Scan the project root for version files (`package.json`, `pyproject.toml`, `Cargo.toml`, `*.gemspec`, `build.gradle`/`kts`, `pom.xml`, `mix.exs`, `version.txt`/`VERSION`). Also check for secondary version locations (`__version__` in Python source, version constants in source files).

Present what will be updated (file, current version, new version) and confirm.

1. Update each confirmed file.
2. Stage and commit: `git commit -m "chore: bump version to <version>"`
3. The tag in Step 4 will point to this bump commit.

**Skip when:** No version files found, version already matches, tagging a historical commit, or user says version is already bumped. Inform the user when skipping.

## Step 3: Compose the Tag Message

**If a changelog or release notes exist from this conversation:** Derive the message from them — pull highlights and breaking changes.

**If generating independently:** Gather changes via `git log` from the previous tag to the target commit.

**Tag message structure:**

```
<version>

<1-sentence release summary>

Highlights:
- <highlight 1>
- <highlight 2>
- <highlight 3>

Breaking Changes:
- <breaking change with migration pointer>

See CHANGELOG.md or docs/release-notes/v<version>.md for full details.
```

Omit Breaking Changes if none. Omit the footer reference if the files don't exist.

## Step 4: Create the Tag

**Annotated tag (default):** `git tag -a v<version> <target-commit> -F <tmpfile>`

**Signed tag (when requested or when existing tags are signed):** `git tag -s v<version> <target-commit> -F <tmpfile>`

If signing fails (no GPG key), explain and offer to create an unsigned annotated tag instead.

## Step 5: Verify and Present

1. Verify: `git show v<version> --no-patch`
2. Present: tag name, target commit (SHA + subject), version files bumped, signed/unsigned, tag message preview.
3. Inform the tag is local only. To share: `git push origin v<version>`. Do NOT push automatically.

## Edge Cases

If a tag with this version already exists:
  → Tell the user. Options: choose a different version, delete and recreate (warn about history rewrite if pushed), or abort.

If the working tree has uncommitted changes:
  → Warn and ask to commit first. Proceed only with confirmation.

If tagging a past commit (not HEAD):
  → Verify ref exists with `git rev-parse --verify <ref>`. Skip version bump (Step 2).

If no previous tags exist:
  → First release. Skip version inference from tags, ask the user for the version.

If the user wants a lightweight tag:
  → `git tag v<version> <target-commit>` (no `-a` or `-m`). Skip tag message step.

If version files show inconsistent versions:
  → Surface the inconsistency, ask which is correct, update all to the target.

If monorepo with multiple packages:
  → Ask which package is being released. Only bump relevant version files.
