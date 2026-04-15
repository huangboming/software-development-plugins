# Backend Workflow

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| language | yes | — | `python`, `go`, `rust`, or `typescript` |
| module_path | go only | — | Go module path (e.g., `github.com/user/project`) |

## Steps

1. Read the language-specific reference for the complete project structure and every file to create:
   - **Python**: See [python.md](python.md) — uv, ruff, pytest, FastAPI. Read when language is `python`.
   - **Go**: See [go.md](go.md) — go modules, golangci-lint, stdlib net/http. Read when language is `go`.
   - **Rust**: See [rust.md](rust.md) — cargo, clippy, rustfmt, axum. Read when language is `rust`.
   - **TypeScript**: See [typescript.md](typescript.md) — pnpm, eslint, prettier, hono, vitest. Read when language is `typescript`.
2. Create all files as specified. Replace `<project-name>` and `<project_name>` (underscore variant) with the project name. For Go, also replace `<module-path>`.
3. Initialize git repo and install pre-commit hooks.

## What Backend Scaffolds Include

| Component | Purpose |
|-----------|---------|
| Health endpoint | `GET /health` returning `{"status": "ok"}` |
| Example test | One passing test for the health endpoint |
| .pre-commit-config.yaml | Standard hooks + language-specific lint/format |

## Edge Cases

- **Missing toolchain**: If `uv`, `go`, `cargo`, or `pnpm` is not available, provide installation instructions before proceeding.
- **Different framework than default** (e.g., Django instead of FastAPI, Echo instead of net/http): Use the reference as a structural template (Makefile targets, CI, pre-commit) but substitute framework-specific code. Maintain the same guarantees (health endpoint, passing tests, working CI).
- **Unsupported language**: Inform the user of supported options. Offer to scaffold with the closest match or create a minimal scaffold.
