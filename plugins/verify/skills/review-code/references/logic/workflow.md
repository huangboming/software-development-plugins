# Logic Review Workflow

Review backend code for correctness, API design, database usage, error handling, security, and performance issues.

## Process

1. Determine scope
2. Scan for hot spots
3. Review code
4. Analyze findings
5. Verify findings
6. Write report

### 1. Determine Scope

Ask the user (skip if already clear from context):
- Which files, modules, or directories to review? (or full project)
- Any specific concerns or areas of pain?
- Language/framework context if not obvious from the codebase

### 2. Scan for Hot Spots

Run the endpoint scanner to identify files that warrant the closest attention:

```
uv run --script ${CLAUDE_PLUGIN_ROOT}/skills/review-code/scripts/endpoint_scanner.py --repo <path>
```

This writes to `.hand-offs/endpoint-scan.md`. Use the priority files list, unprotected endpoints, and database pattern counts to prioritize which files to review first.

Always run the script for fresh data, even if `.hand-offs/endpoint-scan.md` already exists.

### 3. Review Code

Launch 2-3 explorer agents in parallel:

**Agent 1 — API Design & Correctness:**
- Endpoint naming conventions (verbs in URLs, inconsistent pluralization, deep nesting)
- HTTP method semantics (unsafe GETs, non-idempotent PUTs)
- Request/response design (inconsistent envelopes, wrong status codes, internal details leaked)
- Pagination on list endpoints (missing pagination, unbounded results)
- Logic bugs: off-by-one errors, null/nil handling, race conditions, incorrect comparisons
- Correctness of business logic: edge cases, boundary conditions, assumptions
- Return a list of 5-15 files with one-line descriptions of the pattern found at each location

**Agent 2 — Database & Performance:**
- N+1 queries (loops over query results without eager loading)
- Missing transaction boundaries on multi-write operations
- Overly broad transactions (external calls inside transactions)
- Raw SQL injection risk (string interpolation in queries)
- Missing pagination / unbounded queries
- Expensive operations in hot paths (synchronous I/O, blocking calls, unnecessary computation)
- Connection management (pooling, leaks, timeouts)
- Return a list of 5-15 files with one-line descriptions of the pattern found at each location

**Agent 3 — Error Handling & Security (OWASP API Top 10):**
- Swallowed errors (bare except, empty catch, ignored errors)
- Error propagation (errors lost, wrapped, or converted appropriately?)
- Error responses to clients (consistent format, no internal details leaked)
- BOLA/IDOR (API1): object access by user-supplied ID without ownership check
- Broken auth (API2): JWT algorithm not pinned, weak password hashing, no token expiry
- Mass assignment (API3): request body spread directly into ORM model without field allowlist
- Function-level auth (API5): admin endpoints without role check
- SSRF (API7): user-supplied URLs fetched server-side without validation
- Input validation: missing schema validation, unbounded inputs
- Secrets management: hardcoded credentials, secrets in logs or error responses
- Return a list of 5-15 files with one-line descriptions of the pattern found at each location

After agents return, read the key files they identified to verify findings.

### 4. Analyze Findings

Load the relevant reference for each dimension:

| Dimension | Reference | Load When |
|-----------|-----------|-----------|
| API design | [api-design.md](api-design.md) — Endpoint design, request/response patterns, pagination, idempotency, versioning, error responses | Full review, or when API design issues found |
| Database | [database-patterns.md](database-patterns.md) — Query patterns (N+1, injection), transactions, schema/migrations, connection management, data integrity | Full review, or when database issues found |
| General security | [security-checklist.md](security-checklist.md) — Injection, auth, authorization, input validation, secrets, data exposure, crypto, CORS, logging. Broad checklist covering all backend security concerns | Full review, or when security concerns found |
| OWASP API Top 10 | [owasp-api-top10.md](owasp-api-top10.md) — BOLA, broken auth, mass assignment, SSRF, security misconfiguration with framework-specific code examples (Python, Node, Go, Rust) | Security-focused review, or when auth/authz patterns found |

For each finding:
1. Name the pattern (use established names from the references)
2. Cite specific files and line numbers
3. Assess severity using the definitions in [shared-quality-standards.md](../shared-quality-standards.md)
4. Explain the concrete risk (not abstract theory)
5. Provide a specific, actionable recommendation

### 5. Verify Findings

Apply the verification checklist from [shared-quality-standards.md](../shared-quality-standards.md). Additionally:
- Respect framework idioms — do not flag framework-idiomatic patterns as issues (e.g., Django's `objects.all()` is fine if paginated downstream)
- For security findings, verify the vulnerability is exploitable given the application's middleware stack and configuration

### 6. Write Report

Write to `.hand-offs/reviews/logic/YYYY-MM-DD-HHMM.md`. Create `.hand-offs/reviews/logic/` if it does not exist.

- **timestamp**: `YYYY-MM-DD-HHMM` (e.g., `2026-03-04-1430`)
- Example: `.hand-offs/reviews/logic/2026-03-04-1430.md`

```markdown
# Logic Review: <Scope>

> Reviewed: <date> | Scope: <files/modules reviewed> | Health: <Solid | Has issues | Needs attention>

## Scan Summary

<Key numbers from endpoint_scanner.py: endpoint count, DB pattern count, security finding count, priority files>

## Findings

### API Design

**[Severity] <Pattern Name>**
Location: `path/to/file.py:42`
Issue: <What the issue is, concretely>
Risk: <What can go wrong>
Fix: <Specific, actionable recommendation>

### Correctness

<Same format per finding>

### Database Usage

<Same format per finding>

### Error Handling

<Same format per finding>

### Security

<Same format per finding>

### Performance

<Same format per finding>

<!-- Order findings by severity within each section: Critical -> High -> Medium -> Low -->
<!-- Omit sections with no findings -->

## Summary

| Severity | Count |
|----------|-------|
| Critical | N |
| High | N |
| Medium | N |
| Low | N |

**Top recommendations:**
1. <Highest impact recommendation>
2. <Second>
3. <Third>

**Overall assessment:** <Solid | Has issues | Needs attention>
```

## Edge Cases

- If the endpoint scanner finds no API endpoints, the project may be a library, CLI tool, or worker service. Adjust the review to focus on applicable dimensions (database, error handling, security) and skip API-specific checks.
- If no database patterns are found, skip database review unless the codebase uses a database through an unconventional pattern the scanner missed — verify by checking for ORM/driver dependencies in the project manifest.
- If the codebase is a library (no endpoints, no database), focus on API design of the public interface, error handling, and correctness.
