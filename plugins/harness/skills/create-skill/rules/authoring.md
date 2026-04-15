# Authoring Rules

Hard constraints for writing SKILL.md and reference content.

## Frontmatter

YAML frontmatter has exactly two required fields:

- `name` — The skill name (hyphen-case identifier).
- `description` — The primary triggering mechanism. Include both what the skill does *and* specific triggers/contexts for when to use it.

Include all "when to use" information in the `description` — not in the body. The body is only loaded after the skill triggers, so a "When to Use This Skill" section inside the body is invisible to the routing decision.

**Example description for a `docx` skill:**

> Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks.

Do not include any other fields in the frontmatter beyond `name` and `description` (and the optional `license` reference).

## Imperative Form

Write instructions in imperative or infinitive form. Imperative instructions are followed more reliably than descriptive prose.

| Weak (descriptive) | Strong (imperative) |
|---------------------|---------------------|
| "The skill analyzes code for issues" | "Analyze the code for issues" |
| "This skill helps users create reports" | "Create a report based on the user's input" |
| "It should check for errors" | "Check for errors before proceeding" |

See `references/writing-effective-instructions.md` for the full prompt engineering playbook (positive framing, constraint design, example patterns, anti-patterns checklist).

## What Not to Include

A skill contains only files that directly support its functionality. Do not create auxiliary documentation such as:

- `README.md`
- `INSTALLATION_GUIDE.md`
- `QUICK_REFERENCE.md`
- `CHANGELOG.md`

The skill is for another AI agent to use, not a human reader. Setup procedures, meta-context about creation history, and user-facing documentation add clutter. If human-facing onboarding material is needed, it belongs in the plugin's top-level docs, not inside a skill.

## Avoid Duplication

Each piece of information lives in exactly one place — either in SKILL.md or in a reference file, not both. Duplicated content drifts over time and produces conflicting signals.

Default: put detailed material in references, keep SKILL.md lean. Promote content into SKILL.md only when it's truly needed on every invocation.

## Reference Every File

Every file under `rules/`, `workflows/`, `references/`, `scripts/`, or `assets/` must be named and described somewhere in the routing path — SKILL.md, or a workflow that loads it. An unreferenced file is invisible: Claude will never load it, so it contributes zero signal and pure clutter.
