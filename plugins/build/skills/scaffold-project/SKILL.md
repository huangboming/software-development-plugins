---
name: scaffold-project
description: Scaffold a new project with standard tooling. Triggers on requests to create, initialize, set up, or bootstrap a new project, app, or service.
---

# Scaffold Project

Scaffold a new project with modern tooling, testing, CI, and best practices.

## Arguments

Parse the following from the user's request:

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| mode | yes | — | `frontend` or `backend` |
| name | yes | — | Project directory name (kebab-case) |

**Parsing examples:**

- "Create a React app called my-dashboard" → mode: frontend, name: my-dashboard
- "Set up a new Go service" → mode: backend, name: (ask)
- "Build me a todo app" → mode: (ask), name: todo-app
- "Scaffold a backend in Python" → mode: backend, name: (ask)
- "Set up a Next.js project with shadcn" → mode: frontend, name: (ask)

Extract what you can from the request. Ask only for missing required values. If mode is unclear, ask.

## Workflow

1. Parse arguments from the user's request. Determine the mode first.
2. Read the mode-specific workflow reference for detailed steps and mode-specific arguments:
   - **Frontend mode**: See [references/frontend/workflow.md](references/frontend/workflow.md). Read when mode is `frontend`.
   - **Backend mode**: See [references/backend/workflow.md](references/backend/workflow.md). Read when mode is `backend`.
3. Follow the workflow steps — each workflow reference links to framework/language-specific references for the exact files to create.
4. Create all files in a new directory relative to the user's current working directory.
5. Install dependencies and verify:

```bash
cd <project-name>
make install
make check
```

The scaffold is only complete when `make check` passes. If it fails, diagnose and fix before finishing.

## What Every Scaffold Includes

| Component | Purpose |
|-----------|---------|
| Makefile | Standard targets: `install`, `dev`, `format`, `lint`, `test`, `check` |
| .gitignore | Language/framework-appropriate ignores |
| Pre-commit hooks | Lint and format checks on staged files |
| .github/workflows/ci.yml | CI running lint + test |
| CLAUDE.md | Project instructions for Claude Code |
| Example tests | At least one passing test |

## Edge Cases

- **Directory already exists**: Check before creating. If non-empty, ask the user whether to overwrite, choose a different name, or abort.
- **`make check` fails**: Read the error output. Run `make format` first (many lint failures are auto-fixable), then retry. If still failing, fix the specific issue before finishing.
- **User wants features beyond the scaffold**: This skill scaffolds the starting point only. Scaffold first, then help add features separately.

