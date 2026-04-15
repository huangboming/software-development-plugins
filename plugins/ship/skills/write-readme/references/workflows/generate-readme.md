# Generate README Workflow

Create a README from scratch by exploring the codebase and existing documentation.

## Step 1: Gather Context

Explore these sources in priority order. Stop once enough context is gathered to write a confident README.

### 1a. Package Manifests and Config Files

Read first — these are the densest source of project metadata:

- `package.json` — name, description, dependencies, scripts, engines, repository
- `pyproject.toml` / `setup.py` / `setup.cfg` — name, description, dependencies, Python version
- `go.mod` — module path, Go version, dependencies
- `Cargo.toml` — name, description, edition, dependencies, features
- `Makefile` / `Justfile` — available commands, build targets
- `docker-compose.yml` / `Dockerfile` — deployment model, services
- `.env.example` — required environment variables

Extract: project name, description, language/runtime, dependencies, available commands, deployment model.

### 1b. Existing Documentation

Check for and read:

- `docs/` directory — architecture docs, specs, PRDs
- `CLAUDE.md` or similar project guide — project overview, conventions
- `CONTRIBUTING.md` — dev setup, test commands
- `LICENSE` — license type
- Existing `README.md` — even placeholder content gives intent signals

Extract: project purpose, architecture overview, intended audience, contribution workflow.

### 1c. Codebase Structure

Explore the project layout:

- Entry points (`main.*`, `index.*`, `app.*`, `cmd/`)
- Directory structure (breadth-first scan, note major directories)
- Test files (what's tested reveals what's important)
- CI config (`.github/workflows/`, `.gitlab-ci.yml`) — build/test/deploy commands

Extract: project structure, key features, how to build/test/run, deployment targets.

### 1d. Git History (If Sparse)

If the above sources don't give enough context:

- Recent commit messages — what's being worked on
- Tags — version history
- Contributors — team size signal

## Step 2: Determine README Type

Based on gathered context, classify the project:

| Signal | Type |
|--------|------|
| Has a UI, runs as a service, CLI, or deployed application | **Project-level** |
| Published to a registry, installed as a dependency, exposes an API for code consumption | **Library/package** |
| Both (monorepo) | Root = project-level, packages = library-level |

Read the appropriate template from references.

## Step 3: Ask Clarifying Questions (If Needed)

If critical sections can't be filled from the codebase alone, ask 2-4 targeted questions. Common gaps:

- **Purpose:** "The code shows X, Y, Z — is the primary purpose [inferred description]?"
- **Audience:** "Who is the intended user — developers, end users, ops teams?"
- **Status:** "Is this production-ready, beta, or experimental?"
- **Quick start:** "What's the minimal command to get this running from a fresh clone?"

Skip this step if the codebase is self-explanatory.

## Step 4: Draft the README

Read [writing-guide.md](../writing-guide.md) for quality standards.

1. Start with the tagline. Apply the formula: [what it is] + [primary capability] + [differentiator].
2. Fill each section from the template, using gathered context.
3. Write the quick-start section from the user's perspective — test it mentally step by step:
   - Does it assume any knowledge not stated in prerequisites?
   - Does it work on a fresh clone/install?
   - Does it produce visible output?
4. For installation: derive from package manifests and build config. Include exact commands.
5. For features: extract from codebase capabilities. Lead with user benefits.
6. For configuration: extract from `.env.example`, config files, or CLI flags.
7. Add badges if the project has CI, a published version, or a license file.
8. Omit template sections that don't apply. Don't add empty sections.

## Step 5: Review and Present

1. Run through the appropriate quality checklist in [writing-guide.md](../writing-guide.md).
2. Verify all commands and paths reference actual files in the project.
3. Check that no section contains stale or fabricated information — every claim should trace to something discovered in Step 1.
4. Write the README to `README.md` at the project root (or the path the user specified).
5. Present a summary of what was included and note any sections marked with TODOs or assumptions.
