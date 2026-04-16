# Skill Anatomy

Folder structure, file types, and when to use each.

## Basic Layout

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── rules/            - Imperative constraints ("you must do X")
    ├── workflows/        - Ordered step-by-step procedures
    ├── references/       - Explanatory material loaded on demand
    ├── scripts/          - Executable code (Python/Bash/etc.)
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

## SKILL.md (required)

Two parts:

- **Frontmatter (YAML)** — `name` and `description`. Read by Claude to decide when the skill triggers, so write it clearly and comprehensively.
- **Body (Markdown)** — Instructions and guidance. Loaded *only* after the skill triggers.

## Bundled Resources

### Scripts (`scripts/`)

Executable code for tasks that require deterministic reliability or are repeatedly rewritten.

- **Include when** the same code is being rewritten repeatedly or deterministic reliability is needed.
- **Example**: `scripts/rotate_pdf.py` for PDF rotation.
- **Benefits**: Token efficient, deterministic, executed without loading into context.
- **Note**: Scripts may still need to be read by Claude for patching or environment-specific adjustments.

### Rules (`rules/`)

Long-term constraints that must always be followed. Imperative-shaped.

- **Include when** the skill has invariants Claude must honor on every invocation.
- **Examples**: `rules/coding-standards.md`, `rules/api-conventions.md`.
- **Shape test**: content reads as "You must do X" or "Never do Y".

### Workflows (`workflows/`)

Ordered step-by-step procedures for specific tasks. Sequence-shaped.

- **Include when** the skill has multi-step processes where order and completeness matter.
- **Examples**: `workflows/create-new-widget.md`, `workflows/deploy-release.md`.
- **Shape test**: content reads as "Do step 1, then step 2, then step 3".

### References (`references/`)

Explanatory material, architecture notes, gotcha catalogues. Descriptive-shaped.

- **Include when** detailed content is only needed for specific request types.
- **Examples**: `references/finance.md` for schemas, `references/api_docs.md` for specs, `references/policies.md` for org rules.
- **Shape test**: content reads as "Be careful of X" or "X happens because Y".
- **Benefits**: Keeps SKILL.md lean, loaded only when Claude determines it's needed.
- **Best practices**:
  - For files >10k words, include grep search patterns in SKILL.md so Claude searches without loading in full.
  - Each reference file gets exactly one index entry in SKILL.md with *what* it contains and *when* to read it.

### Assets (`assets/`)

Files not intended to be loaded into context, but used within the output Claude produces.

- **Include when** the skill needs files for the final output.
- **Examples**: `assets/logo.png`, `assets/slides.pptx`, `assets/frontend-template/`, `assets/font.ttf`.
- **Benefits**: Separates output resources from documentation. Claude uses these files without loading them into the context window.

## Classifying Content by Shape

Always separate bundled content by shape into `rules/`, `workflows/`, and `references/`. When a piece of content sits on a boundary, classify by shape:

| Content looks like | Target directory |
|--------------------|------------------|
| "You must do X" (imperative) | `rules/` |
| "Do step 1, then step 2, then step 3" (ordered) | `workflows/` |
| "Be careful of X" / "X happens because Y" (descriptive) | `references/` |

Not every skill needs all three directories — a skill with no imperative constraints has no `rules/`, a skill with no procedures has no `workflows/`. But when a content type is present, it goes in the matching directory. Never mix content shapes in a single directory.
