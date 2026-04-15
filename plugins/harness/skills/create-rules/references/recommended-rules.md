# Recommended Starter Rules

Catalog of high-value rules to suggest when the user isn't sure what to create. Each entry lists the problem it prevents, the key instructions to include, and a common gotcha. Full rule-file examples for most categories are in `examples.md` — use these sketches as the *shape* and `examples.md` as the *wording*.

## Table of Contents

- [Code quality (stack-specific)](#code-quality-stack-specific)
- [Safety & security](#safety--security)
- [Testing discipline](#testing-discipline)
- [Git & workflow](#git--workflow)
- [Architecture & organization](#architecture--organization)
- [API & data contracts](#api--data-contracts)
- [Documentation & naming](#documentation--naming)
- [Domain-specific invariants](#domain-specific-invariants)
- [Picking a starter](#picking-a-starter)

---

## Code quality (stack-specific)

### Language conventions — `typescript.md`, `python.md`, `go.md`, `rust.md`

**Problem:** Without explicit style rules, Claude picks idioms from whatever training data is in context — sometimes modern, sometimes circa-2018. Inconsistent code drifts across sessions and reviews fill with style nits.

**Sketch:** Pin the target language version. State the project's stance on type annotations, error handling idiom, import ordering, and the 3–5 patterns the team strongly prefers or forbids (e.g., "no enums, use `as const` objects"). Scope with `paths: "**/*.{ext}"`.

**Gotcha:** Don't restate what the linter/formatter already enforces. Rules compete with tool config for attention — cover the *judgment calls* a linter can't check.

### Framework conventions — `react.md`, `nextjs.md`, `django.md`

**Problem:** Framework idioms change quickly (hooks vs. classes, app-router vs. pages-router, class-based vs. function-based views). Claude can't tell which era the codebase uses without a hint.

**Sketch:** Name the framework version in use. Declare which patterns the project has committed to (server components vs. client, class vs. function views, etc.). Include 2–3 concrete anti-patterns seen in past PRs.

**Gotcha:** These rules go stale fastest — pin the framework version in the rule body and review when the project upgrades. A React-18 rule applied to a React-19 project is worse than no rule.

---

## Safety & security

### Security baseline — `security.md`

**Problem:** Claude will happily log request bodies, interpolate into SQL, or include credentials in error messages when debugging. Once in logs or commits, secrets are effectively published.

**Sketch:** Forbid logging secrets, tokens, PII. Forbid committing `.env*`, keys, dumps. Require parameterized queries. Require constant-time comparison for tokens. Apply globally (no `paths:`).

**Gotcha:** Keep this file separate from general error-handling rules. Security rules are hard constraints; error-handling rules are preferences. Mixing them dilutes both.

### Input validation — fold into `api-design.md` or stand-alone `validation.md`

**Problem:** Validation either gets duplicated in every function (noise, drift) or forgotten at the boundary (exploit surface).

**Sketch:** Validate at system boundaries (API handlers, CLI entry, file reads, env vars); trust internal callers; fail fast with field name + expected format + actual value. Name the boundary concept, not the library.

---

## Testing discipline

### Testing standards — `testing.md`

**Problem:** Without rules, Claude writes tests that pass but teach nothing — snapshot tests of implementation, mocks of the code under test, 20-step setup for a single assertion. This is Claude's weakest-default area and usually the biggest quality jump from a single rule file.

**Sketch:** One concept per test. Test behavior, not implementation. Mock external deps only. No test interdependence. Cover happy path + one edge case + one error case. Include a short list of *what not to test* (trivial getters, third-party libs, generated code). Scope to `**/*.test.*`, `**/test_*.py`, etc.

**Gotcha:** State which test kind this governs (unit vs. integration). Rules for one often break the other — "mock the DB" is right for unit, wrong for integration.

### Test data factories — fold into `testing.md`

**Problem:** Hand-built fixtures drift. Each test has a slightly different "valid user" shape, so a model change breaks hundreds of tests instead of one factory.

**Sketch:** Require factory functions (`buildUser(overrides)`) over raw literals. Name the canonical factory file. Forbid reusing production seed data in tests.

---

## Git & workflow

### Commit conventions — `git-conventions.md`

**Problem:** Inconsistent commit messages break changelog tooling, semver bumps, release notes, and PR review speed.

**Sketch:** Conventional commits format. Imperative mood, lowercase subject, under 72 chars. Body explains *why*, not *what*. One logical change per commit. Include 3–4 concrete example commit messages — Claude copies the shape.

**Gotcha:** If the project uses a non-standard format (JIRA-prefix, ticket-first, etc.), say so explicitly and show an example. Claude defaults to conventional-commits otherwise.

### Pull request standards — fold into `git-conventions.md`

**Problem:** PRs arrive oversized, unscoped, or missing the "why." Review stalls; reviewers guess intent from the diff.

**Sketch:** Target size ceiling (e.g., <400 lines non-test). Required description sections (what / why / how tested). Screenshot for UI changes. Linked issue. Self-review before requesting review.

---

## Architecture & organization

### Code organization — `code-organization.md`

**Problem:** Claude places new code by copying the nearest file it found — which may be the wrong layer. Over time, layering erodes into a flat soup.

**Sketch:** State the dependency direction (e.g., handlers → services → repositories → models). Declare group-by-feature vs. group-by-layer. Where shared code lives. Co-location rules for tests. Forbid circular dependencies explicitly.

**Gotcha:** Rules here rot fastest when architecture changes. Review when the project restructures, or the rule will start lying.

### Dependency hygiene — `dependencies.md`

**Problem:** Easy to `npm install` something speculatively; hard to remove later. Supply-chain surface grows silently.

**Sketch:** Evaluate before adding (bundle size, maintenance, security). Pin exact versions. One package manager per project. Wrap third-party libs when they touch core logic so they can be swapped.

---

## API & data contracts

### API design — `api-design.md`

**Problem:** Endpoint shapes drift — some return `{data}`, some bare arrays, some `{result, errors: []}`. Clients special-case each, and the surface grows inconsistent.

**Sketch:** Response envelope shape. HTTP status semantics (no 200-with-error). Pagination style (cursor for large sets). URL versioning. Resource naming (plural nouns, REST verbs). Scope to `src/api/**` or `src/routes/**`.

**Gotcha:** If the project has both REST and GraphQL (or REST and gRPC), split into two rule files. Their conventions conflict and one file trying to cover both produces either vagueness or contradictions.

### Data model conventions — `data-model.md`

**Problem:** Dates as strings here, Unix timestamps there, ISO 8601 in one place, locale-formatted in another. Money as floats. IDs as integers or UUIDs depending on the table. Timezone and rounding bugs in perpetuity.

**Sketch:** Canonical types for dates, money, IDs, enums. Nullable vs. optional stance. Serialization format at boundaries (ISO 8601, camelCase JSON, etc.).

---

## Documentation & naming

### Naming conventions — `naming.md`

**Problem:** `getData`, `handleClick`, `utils.ts` everywhere. Names that don't reveal intent force readers (and Claude) to read the body to understand the contract.

**Sketch:** Verb phrases for functions. `is`/`has`/`should` prefixes for booleans. Plural for collections (`users`, not `userList`). Avoid non-universal abbreviations (`id`/`url` fine; `mgr`/`ctx` not). Case style per language.

**Gotcha:** Don't conflict with framework conventions — React's `on*` handlers and `use*` hooks are their own naming system.

### Comment policy — fold into `naming.md` or stand-alone `comments.md`

**Problem:** Claude defaults to over-commenting — JSDoc on one-line functions, narration of obvious code, stale comments that contradict the code. Noise drowns the rare comments that matter.

**Sketch:** Comment *why* not *what*. Delete stale comments rather than leave them. Docstrings on public API only. `TODO` requires a ticket reference.

---

## Domain-specific invariants

### Business rules & invariants — `domain.md` or `{domain}.md`

**Problem:** Every project has non-obvious invariants Claude can't infer from code alone — "orders are immutable after payment", "user IDs are UUIDs never integers", "times are always stored UTC." Violating one creates silent data corruption that surfaces weeks later.

**Sketch:** List the 5–10 hard invariants in the domain. For each: one line stating the rule + one line on why it matters. Update when an invariant is added or retired.

**Gotcha:** Don't list things the type system already enforces. Focus on what a newcomer would break in their first week — the tribal knowledge that lives in senior engineers' heads.

---

## Picking a starter

When the user is vague about what they want, ask two questions:

1. **What has bitten you recently?** — shipped-secret, broken-type, flaky-test, merge-conflict pain. Pick the matching rule category.
2. **What conventions do you repeat in every review?** — those are the rules that should live in `.claude/rules/` instead of in a reviewer's head.

**Default trio for a fresh project:**

1. **Language conventions** (`typescript.md` / `python.md` / etc.) — fires on every file edit; highest leverage per token spent.
2. **Testing standards** (`testing.md`) — Claude's weakest-default area; biggest single quality jump.
3. **Commit conventions** (`git-conventions.md`) — keeps history usable for changelogs, review, and blame.

Add **security** next if the project has any external surface (API, user uploads, auth). Add **domain invariants** once the team has caught Claude violating the same unwritten rule more than twice.
