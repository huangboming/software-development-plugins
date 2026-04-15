# Update README Workflow

Refresh an existing README against the current state of the codebase.

## Step 1: Analyze the Existing README

1. Read the current `README.md` (or the file the user specified).
2. Identify what sections exist and their quality:
   - Present and current
   - Present but outdated (stale versions, old screenshots, dead links)
   - Present but weak (vague description, placeholder content, missing examples)
   - Missing (expected sections not present)
3. Note the existing tone, structure, and conventions — preserve what works.

## Step 2: Assess What Changed

Determine what in the codebase has drifted from the README:

### If the user specifies what to update

Focus on the requested sections. Still scan for critical staleness (broken install commands, wrong version numbers) and flag if found.

### If the user says "update" or "improve" without specifics

Compare the README against the codebase:

- **Package manifests** — has the name, description, version, or dependency list changed?
- **Installation** — do the install commands still work? Have prerequisites changed?
- **Features** — are there new capabilities not mentioned, or removed features still listed?
- **Configuration** — have environment variables, config options, or CLI flags changed?
- **Project structure** — has the directory layout changed significantly?
- **CI/CD** — have badges broken or new badges become available?
- **License** — has it changed?

Also check:
- Links (internal and external) — do they still resolve?
- Code examples — do they use current API syntax?
- Version numbers — do they match the latest release/tag?

## Step 3: Determine README Type

If the README doesn't follow a clear type pattern, classify the project (see [generate-readme.md](generate-readme.md) Step 2) and read the appropriate template to understand what sections are expected.

## Step 4: Draft Updates

Read [writing-guide.md](../writing-guide.md) for quality standards.

**Guiding principle:** Preserve the existing structure and voice. Update content, don't rewrite the whole file unless the user explicitly asks for a rewrite.

1. **Fix stale content first** — wrong versions, broken commands, dead links. These erode trust fastest.
2. **Strengthen weak sections** — apply the quality benchmarks from the writing guide. Common improvements:
   - Vague description → concrete tagline following the formula
   - Missing quick start → add a working example
   - "PRs welcome" → actual contributing instructions
   - No license line → add one
3. **Add missing sections** — check the template for expected sections. Add high-value ones:
   - Installation (if missing — highest priority)
   - Quick start (if missing — second priority)
   - Features list (if missing and project has multiple capabilities)
4. **Remove outdated content** — features that no longer exist, deprecated options, stale screenshots.
5. **Update badges** — fix broken ones, remove defunct ones, add meaningful new ones.

**Targeted updates:** If the user asked to update a specific section (e.g., "add installation instructions"), focus there. Don't reorganize the whole README.

## Step 5: Review and Present

1. Run through the appropriate quality checklist in [writing-guide.md](../writing-guide.md).
2. Verify all updated commands and paths reference actual files in the project.
3. Diff the changes mentally — ensure nothing was accidentally removed.
4. Write the updated README.
5. Present a summary of what changed:
   - Sections updated (with brief rationale)
   - Sections added
   - Content removed (with reason)
   - Remaining issues or TODOs the user should verify
