# Workflow: Create a New Skill

End-to-end procedure for building a new skill from scratch. Steps are sequential; skip one only when there's a clear reason it doesn't apply.

## Prerequisite Reading

Before starting, confirm the agent has loaded:

- `rules/core-principles.md` — the four principles every skill must honor
- `rules/authoring.md` — frontmatter, imperative form, exclusions, no-duplication

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

### Consult Design References

Load references based on the sub-problem at hand:

| Need | Reference |
|------|-----------|
| Folder layout and file types | `references/skill-anatomy.md` |
| Three-level loading system | `references/progressive-disclosure.md` |
| Slicing a large skill across files | `references/progressive-disclosure-patterns.md` |
| Writing clear instructions | `references/writing-effective-instructions.md` |
| Managing what lands in the context window | `references/context-engineering.md` |
| Multi-step process patterns (sequential, conditional, loops) | `references/workflow-patterns.md` |
| Output formats (templates, examples, schemas) | `references/output-patterns.md` |
| Gotchas / first-run config / persistent data patterns | `references/common-patterns.md` |

### Build Order

1. Start with the reusable resources identified in Step 2 — `scripts/`, `references/`, `assets/`. Fetch user input where needed (brand assets, templates, documentation).
2. Run any scripts added to `scripts/` to confirm they work. For many similar scripts, test a representative sample.
3. Delete any example files from `init_skill.py` that the skill doesn't need.
4. Write SKILL.md last — by that point the reference inventory and scripts exist and can be referenced precisely.

### Classify Content Into the Right Location

For small skills, a flat `references/` plus optional `scripts/` and `assets/` is fine — don't split prematurely. For larger skills, split by content shape (see `references/skill-anatomy.md` for the full taxonomy):

- Imperative constraints → `rules/`
- Ordered procedures → `workflows/`
- Descriptive/explanatory material → `references/`

## Step 5: Package the Skill

Once development is complete, package into a distributable `.skill` file. Packaging auto-validates first:

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
