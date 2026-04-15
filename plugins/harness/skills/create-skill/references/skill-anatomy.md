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
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation loaded on demand
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

### References (`references/`)

Documentation loaded on demand to inform Claude's thinking.

- **Include when** detailed content is only needed for specific request types.
- **Examples**: `references/finance.md` for schemas, `references/api_docs.md` for specs, `references/policies.md` for org rules.
- **Benefits**: Keeps SKILL.md lean, loaded only when Claude determines it's needed.
- **Best practices**:
  - For files >10k words, include grep search patterns in SKILL.md so Claude searches without loading in full.
  - Each reference file gets exactly one index entry in SKILL.md with *what* it contains and *when* to read it.

### Assets (`assets/`)

Files not intended to be loaded into context, but used within the output Claude produces.

- **Include when** the skill needs files for the final output.
- **Examples**: `assets/logo.png`, `assets/slides.pptx`, `assets/frontend-template/`, `assets/font.ttf`.
- **Benefits**: Separates output resources from documentation. Claude uses these files without loading them into the context window.

## Optional: Split `references/` by Content Type

For larger skills, a flat `references/` directory becomes a catch-all. When content volume justifies it, split references by the *kind* of content so Claude opens the right file on the first try:

- **`rules/`** — Long-term constraints that must always be followed ("use constructor injection", "API dates are ISO 8601"). Imperative-shaped.
- **`workflows/`** — Ordered step-by-step procedures for specific tasks ("adding a new Controller", "shipping a release"). Sequence-shaped.
- **`references/`** — Explanatory material, architecture notes, gotcha catalogues. Descriptive-shaped.

When a piece of content sits on a boundary, classify by shape:

| Content looks like | Target directory |
|--------------------|------------------|
| "You must do X" (imperative) | `rules/` |
| "Do step 1, then step 2, then step 3" (ordered) | `workflows/` |
| "Be careful of X" / "X happens because Y" (descriptive) | `references/` |

For small skills, `references/` alone is fine — splitting prematurely adds navigation overhead without benefit. Split when the flat directory mixes unrelated content types or Claude starts loading the wrong file.
