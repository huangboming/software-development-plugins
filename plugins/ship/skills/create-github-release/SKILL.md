---
name: create-github-release
description: "Create or publish a GitHub Release from a tag. Triggers: 'create github release', 'publish release on github', 'github release', '/create-github-release'."
---

# Create GitHub Release

Create a GitHub Release from an existing tag using `gh release create`. The release appears on the repository's Releases page and can trigger downstream CI workflows.

**This creates a publicly visible artifact. Confirm with the user before executing `gh release create`.**

## Steps

1. Determine the tag and release metadata
2. Compose the release body
3. Confirm with the user
4. Create the GitHub Release
5. Verify and present

## Step 1: Determine Tag and Release Metadata

**Tag:**
- Use a tag created earlier in this conversation, or the one the user specifies.
- Otherwise, list recent tags (`git tag --sort=-creatordate | head -5`) and ask.
- Verify the tag exists: `git rev-parse --verify v<version>`

**Release title:** Default to `v<version>`. Add a theme line if release notes have one.

**Release type:**

| User Context | Flags |
|---|---|
| Stable production release (default) | No special flags |
| Pre-release (alpha, beta, RC) | `--prerelease` |
| User wants review before publishing | `--draft` |
| Unclear | Default to `--draft` |

For pre-releases or maintenance releases on older branches, add `--latest=false`.

## Step 2: Compose the Release Body

| Available Artifact | Approach |
|---|---|
| `docs/release-notes/v<version>.md` | Use as body via `--notes-file` (strip top heading) |
| `CHANGELOG.md` entry | Extract version entry as body |
| Neither exists | Offer: (1) auto-generate with `--generate-notes`, or (2) run `write-release-note` first |

If the project produces build artifacts, ask if the user wants to attach them as assets.

## Step 3: Confirm with the User

**Mandatory.** Present: tag, title, type (draft/published/pre-release), body source, assets, latest flag. Proceed only with explicit confirmation.

## Step 4: Create the GitHub Release

```
gh release create v<version> \
  --title "<title>" \
  --notes-file <path> \
  [--draft] \
  [--prerelease] \
  [--latest=false] \
  [<asset paths>...]
```

## Step 5: Verify and Present

1. Verify: `gh release view v<version>`
2. Present: release URL, status (draft/published), assets.
3. If draft, remind how to publish: `gh release edit v<version> --draft=false`

## Edge Cases

If the tag hasn't been pushed to remote:
  → `gh release create` requires the tag on GitHub. Ask to push: `git push origin v<version>`

If a release already exists for this tag:
  → Options: edit existing (`gh release edit`), delete and recreate, or abort.

If `gh` CLI is not installed or not authenticated:
  → Detect with `gh auth status`. Provide install/auth instructions.

If the user wants to add assets after creation:
  → `gh release upload v<version> <asset paths>`

If the user wants to convert draft to published:
  → `gh release edit v<version> --draft=false`

If the release should generate discussion:
  → `gh release create v<version> --discussion-category "Announcements"`
