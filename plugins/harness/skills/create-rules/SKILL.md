---
name: create-rules
description: "Create Claude Code rules files (`.claude/rules/*.md`). Triggers: 'create rules for...', 'write rules for...', 'add a rule about...', 'set up coding standards', 'generate claude rules', 'draft a rule about...', '/create-rules'."
---

# Claude Code Rules Writer

Write excellent Claude Code rules as markdown files saved to `.claude/rules/` in the current project. Rules are project-scoped — they live in the repository, not in `~/.claude/`.

## What Are Rules

Rules are markdown files in `.claude/rules/` that provide focused instructions to Claude Code. They load automatically at session start with the same priority as CLAUDE.md. Each file covers one topic.

## Workflow

1. **Gather context**: Ask what area the rules should cover (e.g., "TypeScript style", "testing", "API design"). Ask about existing conventions, tech stack preferences, and strong opinions.

   Edge cases:
   - If the user is unsure what to create, read [references/recommended-rules.md](references/recommended-rules.md) and surface the default trio plus any entries that match their recent pain points.
   - If the topic is vague or unspecified, propose 3–5 candidates from the Rule Categories table and let the user pick.
   - If a rule file on that topic already exists in `.claude/rules/`, read it first and ask whether to extend it, replace it, or create a sibling file.
   - If the target directory `.claude/rules/` does not exist, create it.

2. **Research**: Research current best practices before writing language- or framework-specific rules. If a researcher subagent is available via the Task tool, invoke it — launch one call per independent topic so research runs in parallel. Skip research for universal principles you are confident in (generic git hygiene, naming). See [references/research-guidelines.md](references/research-guidelines.md) for what to look for and how to apply findings.

3. **Plan**: Outline which rule files to create, what each covers, and the filename. Present this plan to the user before writing. One topic per file — split any file that spans unrelated areas.

4. **Write**: Create the rule files following the format and quality guidelines below. Read [references/examples.md](references/examples.md) first to calibrate tone, specificity, and structure for the target category — adapt, do not copy. Save each file to `.claude/rules/<topic>.md` in the current project.

5. **Validate**: Before presenting, check each file against this list. Fix any failures.
   - Every bullet is specific enough that two readers would implement it the same way.
   - No bullet restates what the linter, formatter, or type checker already enforces.
   - All `paths:` glob values are quoted strings, even single entries.
   - Each instruction lives in exactly one file — no cross-file duplication.
   - Inline examples number 1–2 per instruction at most.
   - The file reflects real standards the team already follows, not aspirations.

## Rule File Format

**Filename:** lowercase-kebab-case describing the topic (`error-handling.md`, `api-design.md`). Name by topic, not audience (`testing.md`, not `for-developers.md`). No `rule-` or `claude-` prefix — the directory provides context.

**Structure:**

```markdown
---
paths:
  - "pattern/here/**/*.ts"
---

# Title

Brief one-line context sentence if the topic needs framing (optional).

## Section Heading (if needed)
- Specific, actionable instruction
- Another specific instruction
- Include the *why* when it's non-obvious
```

**Frontmatter `paths:`** is optional. Include it only when the rule genuinely applies to specific file types; omit entirely for rules that apply globally (security, naming, git). Always quote glob strings — `"**/*.ts"`, `"src/api/**/*"` — even a single entry. Unquoted globs break YAML parsing.

## Quality Principles

### Be Specific and Actionable
- **Bad**: "Write clean code" / "Handle errors properly" / "Use good naming"
- **Good**: "Catch specific exceptions, not bare `except:` — include the operation that failed and the input that caused it"
- Every instruction should be unambiguous enough that two developers would implement it the same way.
- Refer to patterns and principles, not hardcoded file paths or internal service names — rules must stay valid when files move.

### Be Opinionated
- Rules are decisions, not discussions. Pick a stance and state it directly.
- **Bad**: "Consider using either interfaces or type aliases for object shapes"
- **Good**: "Use `interface` for object shapes, `type` for unions and intersections"

### Be Concise
- Rules load into context every session — every line costs tokens.
- One bullet per instruction. No filler, no preambles, no "it is recommended that..."
- Inline examples: 1–2 per instruction at most. Move longer catalogues to a project-local reference.
- Don't restate linter or formatter defaults (e.g., "Use semicolons in JavaScript") — the tooling handles those.

### Include the Why (When Non-Obvious)
- "Use cursor-based pagination for large datasets" — the *what* is clear but not the *why*.
- "Use cursor-based pagination for large datasets — offset pagination degrades at scale and skips rows on concurrent writes" — now it teaches.

### Organize for Scanning
- Group related instructions under `##` headings.
- Use bullet points, not paragraphs.
- Put the most important/commonly-violated rules first.
- Use "Never" / "Always" / "Prefer" to signal rule strength.

### Reflect Real Standards, Not Aspirations
- Write down what the team actually does. Aspirational rules get ignored and erode trust in the rest of the file.
- One topic per file. Split anything that spans unrelated areas (style + testing + security + architecture in one file is too broad).
- Each instruction lives in exactly one file. Cross-cutting concerns (like "log errors") belong in the most specific relevant file, not repeated everywhere.
- When two rules conflict, the more specific one wins — say so explicitly in the more specific file.

## Rule Categories

When generating rules, consider these categories. Not every project needs all of them — ask the user what matters most.

| Category | Covers | Example filename |
|----------|--------|-----------------|
| Code quality | Style, patterns, type usage, idioms | `typescript.md`, `python.md` |
| Error handling | Exception strategy, validation, logging | `error-handling.md` |
| Testing | Test structure, coverage, mocking, naming | `testing.md` |
| Git & workflow | Commits, branches, PRs, review | `git-conventions.md` |
| API design | Endpoints, responses, versioning, auth | `api-design.md` |
| Architecture | Module structure, dependencies, layers | `code-organization.md` |
| Security | Input validation, secrets, auth, OWASP | `security.md` |
| Performance | Queries, caching, pagination, profiling | `performance.md` |
| Naming & docs | Naming conventions, comments, docstrings | `naming.md` |

## When Stuck

- **User rejects the plan**: stop. Return to step 1 and re-gather context — a disagreed plan means the intent wasn't clear.
- **Ecosystem is genuinely split** (e.g., two popular state-management libs): document both in one line and pick a default with rationale. Don't punt by listing both as equally valid.
- **New rule contradicts an existing one**: surface the conflict to the user and ask which wins before writing. Never ship two files that disagree.
- **Research returns thin or contradictory results**: tell the user what you found, name the uncertainty, and ask whether to ship a narrower rule or skip the topic.

## Gotchas

- **Rules are project-scoped** — always save into `.claude/rules/` in the current project. Do not write to `~/.claude/rules/`; the user's home directory is a separate concern this skill does not touch.
- **Unquoted `paths:` globs break YAML parsing** — always wrap glob strings in double quotes, even for a single entry.
- **Rules load every session** — a verbose rule file pays its token cost on every invocation. Cut before shipping.
- **Overwriting silently destroys user edits** — if `.claude/rules/<topic>.md` already exists, read it and confirm with the user before replacing.
- **Researcher subagent names vary by install** — invoke whichever researcher subagent the Task tool exposes in the current environment; do not hard-code a plugin-prefixed name.

## References

- **[references/recommended-rules.md](references/recommended-rules.md)** — catalog of high-value starter rules organized by category (code quality, safety, testing, git, architecture, API, naming, domain), with problem statements and sketches. Read during workflow step 1 when the user is vague about what to build, or to suggest rules beyond the Rule Categories table.
- **[references/research-guidelines.md](references/research-guidelines.md)** — what to research for a given rule topic, how to apply findings, when to skip. Read during workflow step 2.
- **[references/examples.md](references/examples.md)** — curated high-quality rule examples across all categories. Read during workflow step 4 to calibrate tone, specificity, and structure for the target category before drafting.
