# Rule Examples by Category

Curated examples of excellent, project-agnostic Claude Code rules. Use these as models for style, specificity, and structure. Adapt to the user's stack and conventions.

## Table of Contents

- [Code Quality](#code-quality)
- [Error Handling & Safety](#error-handling--safety)
- [Testing](#testing)
- [Git & Workflow](#git--workflow)
- [Architecture & Design](#architecture--design)
- [Security](#security)
- [Performance](#performance)
- [Documentation & Naming](#documentation--naming)

---

## Code Quality

### TypeScript Strict Standards

```markdown
---
paths:
  - "**/*.ts"
  - "**/*.tsx"
---

# TypeScript Standards

- Enable and respect `strict: true` — never use `any` without a comment justifying why
- Prefer `unknown` over `any` for values with uncertain types
- Use discriminated unions over optional fields when modeling variants
- Explicit return types on exported functions; inferred is fine for internal/private
- Prefer `interface` for object shapes, `type` for unions and intersections
- Use `readonly` for properties that should not be mutated after construction
- Avoid enums — use `as const` objects or string literal unions instead
```

### Python Style

```markdown
---
paths: "**/*.py"
---

# Python Standards

- Target Python 3.11+ — use modern syntax (match/case, type unions with `|`, etc.)
- Type-annotate all function signatures; use `typing` imports only when necessary
- Prefer dataclasses or Pydantic models over raw dicts for structured data
- Use pathlib over os.path for file operations
- Use f-strings over .format() or % formatting
- Imports: stdlib → third-party → local, separated by blank lines (isort convention)
- Prefer explicit over implicit — no star imports, no mutable default arguments
```

---

## Error Handling & Safety

### Robust Error Handling

```markdown
# Error Handling

- Never swallow exceptions silently — at minimum, log them
- Catch specific exceptions, not bare `except:` or `catch (error)`
- Include context in error messages: what operation failed, what input caused it
- Distinguish between recoverable errors (retry, fallback) and fatal errors (fail fast)
- At system boundaries (API handlers, CLI entry points), catch broadly and return structured errors
- Internal code should let unexpected exceptions propagate — don't hide bugs
- Use Result/Either types or explicit error returns over exceptions for expected failure cases when the language supports it
```

### Defensive Input Validation

```markdown
# Input Validation

- Validate all external input at system boundaries: API endpoints, CLI args, file reads, environment variables
- Do not re-validate inside internal functions — trust the boundary
- Fail fast with clear messages: include the field name, expected format, and actual value
- Use schema validation libraries (Zod, Pydantic, JSON Schema) over hand-written checks
- Sanitize user-provided strings before interpolation into SQL, HTML, shell commands, or URLs
```

---

## Testing

### Test Standards

```markdown
---
paths:
  - "**/*.test.*"
  - "**/*.spec.*"
  - "**/test_*.py"
  - "**/*_test.go"
---

# Testing Standards

## Test Structure
- One concept per test — if the name has "and" in it, split it
- Name tests descriptively: "should [expected behavior] when [condition]"
- Arrange-Act-Assert pattern: setup, execute, verify — separated by blank lines
- Use factory functions (e.g., `buildUser(overrides)`) over raw object literals for test data

## Test Quality
- Test behavior, not implementation — tests should survive refactors
- Cover the happy path, edge cases, and at least one error case per function
- Mock external dependencies (network, DB, filesystem) — never in-process logic
- Avoid snapshot tests except for serialization formats — they create false confidence
- No test interdependence — each test must pass in isolation and in any order

## What to Test
- Public API surface and exported functions: always
- Complex business logic and state machines: always
- Simple getters, formatters, trivial wrappers: skip unless bug-prone
- Generated code and third-party library behavior: never
```

---

## Git & Workflow

### Commit Conventions

```markdown
# Git Commit Standards

## Message Format
- Use conventional commits: `type(scope): description`
- Types: feat, fix, refactor, test, docs, chore, perf, ci
- Scope is optional but encouraged for multi-module projects
- Subject line: imperative mood, lowercase, no period, under 72 chars
- Body: explain *why*, not *what* — the diff shows what changed

## Commit Hygiene
- One logical change per commit — split unrelated changes
- Never commit generated files, build artifacts, or secrets
- Fixup commits are fine during development; squash before merge
- Write the commit message as if the reader has no context beyond the diff

## Examples
- `feat(auth): add OAuth2 login with Google provider`
- `fix(api): handle null response from payment gateway`
- `refactor: extract validation logic into shared module`
- `test(cart): add edge cases for discount calculation`
```

### Branch Strategy

```markdown
# Branch Conventions

- Branch from main/master for all work
- Naming: `{type}/{short-description}` — e.g., `feat/user-auth`, `fix/null-cart`
- Keep branches short-lived — merge within days, not weeks
- Rebase onto main before opening PR to keep history linear
- Delete branches after merge
```

### Pull Request Standards

```markdown
# Pull Request Standards

- PR title follows conventional commit format: `type(scope): description`
- Description includes: what changed, why, how to test
- Keep PRs focused — one feature or fix per PR
- If a PR exceeds ~400 lines of non-test code, consider splitting it
- Include before/after screenshots for UI changes
- Link to the issue or ticket being addressed
- All CI checks must pass before merge
- Self-review the diff before requesting review
```

---

## Architecture & Design

### Code Organization

```markdown
# Code Organization

- Group by feature/domain, not by technical layer (prefer `users/` over `controllers/`)
- Keep modules cohesive — a module should have one reason to change
- Dependencies flow inward: handlers → services → repositories → models
- No circular dependencies between modules
- Shared utilities go in a `shared/` or `common/` directory — keep it small
- Co-locate tests with source files (`foo.ts` + `foo.test.ts` in same directory)
- Index/barrel files only at module boundaries — not inside modules
```

### API Design

```markdown
---
paths:
  - "src/api/**/*"
  - "src/routes/**/*"
  - "src/handlers/**/*"
---

# API Design

## Request/Response
- Use consistent response envelope: `{ data, error, meta }`
- HTTP status codes must be semantically correct (don't return 200 for errors)
- Accept and return JSON with camelCase field names
- Paginate list endpoints — use cursor-based pagination for large datasets
- Version APIs in the URL path (`/v1/`) not headers

## Endpoint Design
- RESTful resource naming: plural nouns (`/users`, not `/user` or `/getUsers`)
- Use appropriate HTTP methods: GET reads, POST creates, PUT replaces, PATCH updates, DELETE removes
- Validate request body with a schema at the handler level
- Return 201 for successful creation, 204 for successful deletion
- Include correlation/request IDs in responses for debugging
```

### Dependency Management

```markdown
# Dependencies

- Pin exact versions in lockfiles — never commit without an updated lockfile
- Evaluate before adding: does this dependency justify its weight? (bundle size, maintenance, security surface)
- Prefer well-maintained, widely-used packages over obscure alternatives
- Wrap third-party dependencies behind your own interfaces when they touch core logic
- Audit for known vulnerabilities regularly
- One package manager per project — do not mix npm/yarn/pnpm
```

---

## Security

### Security Baseline

```markdown
# Security Rules

## Never
- Log or expose secrets, tokens, passwords, or PII in error messages or responses
- Use string concatenation/interpolation for SQL queries — always parameterize
- Store secrets in source code, config files, or environment variable defaults
- Disable TLS/SSL verification, even in development
- Use `eval()`, `exec()`, or dynamic code execution with user input

## Always
- Use parameterized queries or an ORM for database access
- Escape or sanitize user input before rendering in HTML (prevent XSS)
- Validate and sanitize file paths to prevent directory traversal
- Use constant-time comparison for secrets and tokens
- Set appropriate CORS headers — never use `*` in production
- Apply rate limiting to authentication endpoints
- Use HTTPS for all external communication
```

### Authentication & Authorization

```markdown
---
paths:
  - "src/auth/**/*"
  - "src/middleware/**/*"
---

# Auth Standards

- Authenticate at the middleware/gateway level, not in individual handlers
- Authorize at the handler level — check permissions before business logic
- Use short-lived tokens (JWTs < 15 min) with refresh token rotation
- Hash passwords with bcrypt/argon2 — never MD5, SHA-1, or plain SHA-256
- Invalidate all sessions on password change
- Log authentication events (login, logout, failed attempts) for audit
- Implement account lockout or exponential backoff after repeated failures
```

---

## Performance

### Performance Guidelines

```markdown
# Performance

- Profile before optimizing — measure, don't guess
- Database queries are the #1 bottleneck: avoid N+1 queries, add indexes for frequent lookups
- Cache expensive computations and external API responses — with explicit TTLs and invalidation
- Use pagination for list endpoints — never return unbounded result sets
- Prefer streaming over buffering for large data transfers
- Lazy-load heavy modules and components when possible
- Set timeouts on all external calls (HTTP, DB, cache) — never wait indefinitely
- Log slow operations (>1s) for investigation
```

---

## Documentation & Naming

### Naming Conventions

```markdown
# Naming

- Names should reveal intent — `getUsersByRole` over `getData`
- Use consistent casing: camelCase (JS/TS), snake_case (Python/Ruby/Rust), PascalCase (types/classes)
- Boolean variables: use `is`, `has`, `should`, `can` prefixes — `isActive`, not `active`
- Functions: use verb phrases — `validateInput`, `calculateTotal`, `fetchUserProfile`
- Avoid abbreviations unless universally understood (id, url, http are fine; usr, mgr, ctx are not)
- Collection variables should be plural: `users`, `orderItems` — never `userList` or `orderItemArray`
- Constants: SCREAMING_SNAKE_CASE for true constants, camelCase for "const but not conceptually constant"
```

### Code Comments

```markdown
# Comments

- Don't comment *what* the code does — make the code self-evident
- Comment *why* — non-obvious business rules, workarounds, performance decisions
- Use TODO with a ticket reference: `// TODO(JIRA-123): migrate to new API`
- Delete commented-out code — version control remembers it
- Docstrings on public APIs: describe behavior, parameters, return values, and exceptions
- Keep comments up to date — stale comments are worse than no comments
```
