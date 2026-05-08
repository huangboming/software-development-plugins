# Workflow: Create a New Skill

End-to-end procedure for building a skill from scratch.

## 1. Ground in concrete examples

Skip if the usage pattern is already obvious.

Ask the user (or propose and validate) for 2–3 concrete examples of how the skill will fire:

- "What functionality should this skill support?"
- "Give me an example user request that should trigger it."
- "Anything it should *not* fire on?"

Stop when the trigger surface is clear. One question at a time.

## 2. Plan reusable resources

For each example from step 1:

1. Imagine executing it from scratch.
2. Identify what would help on every repeat invocation: scripts, schemas, templates.

Output: a short list of resources to bundle.

| Bundled resource | Use when |
|---|---|
| `scripts/*.py` | The same code is rewritten across sessions, or determinism matters. |
| `references/*.md` | Schemas, conventions, gotchas only some invocations need. |
| `assets/*` | Templates, fonts, images copied into output. |
| `rules/*.md` | Hard constraints honored on every invocation. |
| `workflows/*.md` | Multi-step procedures where order matters. |

Skip a directory entirely if nothing fits. Don't invent content to fill it.

## 3. Initialize

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script writes a SKILL.md template with frontmatter and example directories. Delete what doesn't apply.

## 4. Build

Build order:

1. **Bundled resources first** — scripts, references, assets. Run scripts to confirm they work.
2. **SKILL.md last** — by then the resource inventory is concrete and can be indexed precisely.

While writing SKILL.md, apply the four signal-to-noise tests from `rules/core-principles.md` (justification, duplication, example, knowledge) to every line. Procedural skill SKILL.md ≤ 30–40 lines.

For each bundled file: write its index entry — `path/to/file.md — what it contains. Read when X.`

## 5. Self-review

Before declaring done, walk SKILL.md and each bundled file once through these checks:

- Does the `description` open with one imperative sentence and list 3+ concrete trigger phrases?
- Is every line in SKILL.md justified by the four tests?
- Does every file under `rules/`, `workflows/`, `references/` have an index entry naming *what* and *when*?
- Are there any "you should consider…" or "try to…" weasel phrases? Replace with imperatives.
- Does every conditional (`if X then Y`) have its `otherwise Z` or explicit "otherwise proceed"?

Fix what fails. Don't ship known violations.

## 6. Package

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Validates frontmatter, naming, structure, and writes a `.skill` archive. Fix validation errors and re-run.
