---
name: generate-pipeline
description: "Generate or update CI/CD pipeline configs (GitHub Actions, GitLab CI). Triggers: 'set up CI', 'create CI/CD pipeline', 'add GitHub Actions', 'generate workflow', 'update CI', 'add deploy stage', '/generate-pipeline'."
---

# CI Pipeline

## References

- [references/github-actions.md](references/github-actions.md) — GitHub Actions workflow structure, job patterns, caching, language-specific setup. Read when generating or updating GitHub Actions workflows.
- [references/gitlab-ci.md](references/gitlab-ci.md) — GitLab CI pipeline structure, stage patterns, caching, language-specific setup. Read when generating or updating GitLab CI pipelines.

## Process

1. Determine workflow (Generate or Update)
2. Explore the codebase to detect tooling
3. Confirm provider and stages with the user
4. Read the provider-specific reference
5. Generate or update the pipeline config
6. Verify the output

### Determine Workflow

| User Intent | Workflow |
|---|---|
| "set up CI", "create CI/CD pipeline", "add GitHub Actions" | **Generate** |
| "update CI", "add deploy stage", "fix the CI", "CI is outdated" | **Update** |
| Ambiguous | Ask |

### Step 1: Explore the Codebase

Detect the following by reading project files:

| Signal | Where to look |
|---|---|
| **Language** | File extensions, config files (tsconfig.json, pyproject.toml, go.mod, Cargo.toml) |
| **Framework** | Dependencies (next, react, fastapi, hono, axum, gin) |
| **Package manager** | Lock files (pnpm-lock.yaml, uv.lock, go.sum, Cargo.lock) |
| **Test runner** | Config or dependencies (vitest, jest, pytest, go test, cargo test) |
| **Linter/Formatter** | Config files (eslint.config.*, .ruff.toml, .golangci.yml) |
| **Build tool** | Scripts in package.json, Makefile, Dockerfile |
| **Deploy target** | Dockerfile, serverless.yml, vercel.json, fly.toml, render.yaml |

For **Update**, also read existing pipeline files (`.github/workflows/*.yml`, `.gitlab-ci.yml`).

### Step 2: Confirm with the User

Present detected tooling and proposed pipeline stages. Include which stages are recommended and which are optional (e.g., E2E, deploy). Confirm the CI provider. If no deploy target is detected, propose lint + test + build only.

### Step 3: Generate or Update

Read the appropriate provider reference:
- GitHub Actions → [references/github-actions.md](references/github-actions.md)
- GitLab CI → [references/gitlab-ci.md](references/gitlab-ci.md)

**Generate:** Create the config at the provider's expected location.

**Update:** Read existing config, apply targeted edits. Preserve user customizations (custom jobs, comments, environment variables).

### Step 4: Verify

1. Confirm YAML is syntactically valid (check indentation, no tab characters for GitHub Actions).
2. Verify referenced actions/images use known-good versions.
3. Confirm secret references match what the user described.
4. Present the generated file(s) and summarize what each job/stage does.

## Edge Cases

If monorepo with multiple languages:
  → Ask which services need CI. Generate separate workflows per service or one with path filters.

If existing CI uses a different provider than requested:
  → Flag. Ask whether to migrate or add a second provider.

If no tests, linter, or build step:
  → Suggest a minimal pipeline with at least a syntax/type check. Flag missing quality gates.

If deploy requested but no target configured:
  → Ask where they deploy. If unknown, generate without deploy and add a placeholder.

If unsupported provider (CircleCI, Azure Pipelines):
  → Offer best-effort config with a disclaimer.
