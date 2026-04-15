---
name: write-readme
description: "Write, generate, or update a README for a project or library. Triggers: 'write a README', 'create a README', 'generate a README', 'update the README', 'document this project', '/write-readme'."
---

# README Writer

## References

### Workflows

- [references/workflows/generate-readme.md](references/workflows/generate-readme.md) — Step-by-step process for creating a README from scratch. Read when the project has no README or the user wants to create one.
- [references/workflows/update-readme.md](references/workflows/update-readme.md) — Process for refreshing an existing README against the codebase. Read when the user wants to update or improve an existing README.

### Templates and Guides

- [references/project-readme-template.md](references/project-readme-template.md) — Template for project-level READMEs (applications, services, tools). Read when drafting a project README.
- [references/library-readme-template.md](references/library-readme-template.md) — Template for library/package READMEs (npm, PyPI, Go modules). Read when drafting a library README.
- [references/writing-guide.md](references/writing-guide.md) — Writing rules, tagline formulas, badge guidance, quality checklists, anti-patterns. Read when drafting or reviewing any README.

## Process

1. Determine **README type** and **workflow**
2. Read the corresponding workflow reference
3. Follow the workflow steps
4. Present the result

### Determine README Type

| Signal | Type |
|--------|------|
| Has a UI, runs as a service, or is deployed | **Project-level** → read [project-readme-template.md](references/project-readme-template.md) |
| Installed as a dependency or published to a registry | **Library/package** → read [library-readme-template.md](references/library-readme-template.md) |
| Monorepo with both | Project-level at root, library-level in each package |

If ambiguous, ask.

### Determine Workflow

| Situation | Workflow |
|-----------|----------|
| No README.md or user asks to "write" / "create" / "generate" | **Generate** → read [generate-readme.md](references/workflows/generate-readme.md) |
| README.md exists and user asks to "update" / "improve" / "fix" | **Update** → read [update-readme.md](references/workflows/update-readme.md) |
| README.md exists but nearly empty (< 20 lines) | **Generate** |

## Edge Cases

If the project has no code yet:
  → Minimal README with name, description, goals, "Coming Soon." Pull from `docs/product/prd/` if available.

If the user wants implementation details:
  → READMEs are for users. Suggest linking to `docs/development/architecture/`. Defer if they insist.

If monorepo:
  → Offer root README + individual package READMEs.

If the README would exceed ~400 lines:
  → Move detailed content to linked docs.

If minimal codebase (no tests, no docs):
  → Rely on code structure and manifests. Flag low-confidence sections.
