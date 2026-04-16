# Workflow: Create a New Skill

End-to-end procedure for building a new skill from scratch. Steps are sequential; skip one only when there's a clear reason it doesn't apply.

## Prerequisite Reading

Before starting, confirm the agent has loaded all six "Always Read" files from SKILL.md:

- `rules/core-principles.md` — the four principles every skill must honor
- `rules/authoring.md` — frontmatter, imperative form, exclusions, no-duplication
- `rules/context-engineering.md` — context allocation strategies, signal-to-noise tests, anti-patterns
- `references/skill-anatomy.md` — folder structure and file types
- `references/progressive-disclosure.md` — three-level loading system
- `references/writing-effective-instructions.md` — how to write SKILL.md instructions

## Step 1: Understand the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood.

Clearly understand concrete examples of how the skill will be used. Ask the user for examples directly, or generate candidate examples and validate them with user feedback.

Relevant questions (for an image-editor skill, as an example):

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

Avoid overwhelming the user with too many questions in one message. Start with the most important and follow up as needed.

Conclude this step when there is a clear sense of the functionality the skill should support.

## Step 2: Plan the Reusable Skill Contents

For each concrete example from Step 1:

1. Consider how to execute the example from scratch.
2. Identify which scripts, references, or assets would help when executing this workflow repeatedly.

**Examples:**

- `pdf-editor` skill for "Rotate this PDF" → rotating a PDF requires the same code each time → `scripts/rotate_pdf.py`.
- `frontend-webapp-builder` skill for "Build me a todo app" → same boilerplate HTML/React each time → `assets/hello-world/` template.
- `big-query` skill for "How many users logged in today?" → re-discovering table schemas each time → `references/schema.md`.

Output of this step: a list of the reusable resources to include.

## Step 3: Initialize the Skill

Skip this step only if the skill already exists and the task is iteration or packaging.

Run the init script — it generates a template with proper structure and frontmatter:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script creates the skill directory, a SKILL.md template with TODO placeholders, and example `scripts/`, `references/`, and `assets/` directories. After initialization, customize or remove the generated files.

## Step 4: Edit the Skill

The skill is being created for another Claude instance. Include information that would be beneficial and non-obvious to Claude — procedural knowledge, domain-specific details, reusable assets.

### Load Additional References

The prerequisite files (`skill-anatomy.md`, `progressive-disclosure.md`, `writing-effective-instructions.md`, `context-engineering.md`) are already loaded.

Load any additional references that match the skill being built:

- **Skill produces structured output** (templates, schemas, examples) → read `references/output-patterns.md` before writing output sections.
- **Skill has multi-step procedures** (sequential, conditional, loops) → read `references/workflow-patterns.md` before designing the workflow.
- **Skill is large enough to split across files** → read `references/progressive-disclosure-patterns.md` before deciding file layout.
- **Skill needs gotchas, first-run config, or persistent data** → read `references/common-patterns.md` before writing those sections.

### Build Order

1. Start with the reusable resources identified in Step 2 — `scripts/`, `references/`, `assets/`. Fetch user input where needed (brand assets, templates, documentation).
2. Run any scripts added to `scripts/` to confirm they work. For many similar scripts, test a representative sample.
3. Delete any example files from `init_skill.py` that the skill doesn't need.
4. Write SKILL.md last — by that point the reference inventory and scripts exist and can be referenced precisely.

### Classify Content Into the Right Location

Always separate bundled content by shape (see `references/skill-anatomy.md` for the full taxonomy). Not every skill needs all three directories, but when a content type is present, it goes in the matching directory:

- Imperative constraints → `rules/`
- Ordered procedures → `workflows/`
- Descriptive/explanatory material → `references/`

## Step 5: Review (Multi-Axis)

Before packaging, review the skill for quality issues across multiple axes. Present the user with review options:

> Which review axes should I run? (select one or more, or skip)
>
> - **A) context-engineering** — content placement, progressive disclosure, signal-to-noise, no orphans
> - **B) instructional-clarity** — ambiguity, implicit assumptions, over/under-specification, conflicting directives
> - **C) trigger-quality** — description coverage, trigger phrase diversity, false-positive/negative risk
> - **D) all three** — run A + B + C in parallel
> - **E) skip** — fast self-review against signal-to-noise tests only

For each selected axis, launch the `skill-reviewer` agent via the Task tool, passing:
1. The absolute path to the skill directory
2. The axis name (`context-engineering`, `instructional-clarity`, or `trigger-quality`)

Launch all selected axes in parallel — one Task call per axis. Wait for all reviewers to complete before proceeding.

**If the user selects "skip":** Perform a fast self-review by checking only the five signal-to-noise tests from `rules/context-engineering.md` (justification, duplication, example, knowledge, front-loading). Report any issues found and proceed directly to packaging.

## Step 6: Reconcile and Fix

After all reviewers return:

1. **Merge findings** — deduplicate findings that appear across multiple axes (same file, same issue)
2. **Group by severity** — present all findings in a single list: Critical first, then Major, then Minor
3. **Show per-axis verdicts** — include each axis's verdict line so the user sees the overall picture
4. **Apply accepted fixes** — for each finding, ask the user whether to fix or skip. Apply accepted fixes to the skill files
5. **Skip declined fixes** — do not re-raise declined findings

If all axes approve with no findings, report that and proceed directly to packaging.

## Step 7: Package the Skill

Once development and review are complete, package into a distributable `.skill` file. Packaging auto-validates first:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory:

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

The script validates (YAML frontmatter, naming, directory structure, description completeness, file organization) and, if validation passes, writes a `.skill` file (a zip archive). Fix any validation errors and re-run.

## Next: Iterate

After the first real use, follow `workflows/iterate-on-skill.md` to capture lessons. Skills improve through iteration, not upfront design.
