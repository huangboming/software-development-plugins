---
name: create-subagent
description: Create and configure custom Claude Code subagents (Task tool subagent types). Use when the user wants to create a new subagent, add a new agent type, build a custom agent, define a specialized agent, or set up agent orchestration. Triggers on requests like "create a subagent for...", "add a new agent type", "help me build an agent", "define an agent that...", "make a code review agent".
---

# Subagent Creator

Create custom Claude Code subagents — specialized agents invoked via the Task tool. Subagents are Markdown files with YAML frontmatter stored in `.claude/agents/`.

## Workflow

### 1. Gather Requirements

Ask the user:
- **What should the agent do?** (e.g., "review code for security issues", "run and fix failing tests")
- **Scope**: Project-level (`.claude/agents/`) or user-level (`~/.claude/agents/`)?
- **Read-only or read-write?** Determines tool access.

### 2. Research the Domain

Before writing the agent, research the domain to ground the prompt in real expertise. If a researcher subagent is available via the Task tool, invoke it to gather:

- **Best practices**: What do experts in this domain prioritize?
- **Common pitfalls**: What mistakes are easy to make? What are the known failure modes?
- **Key terminology**: What domain-specific concepts should the agent understand?
- **Established workflows**: Are there standard procedures or checklists (e.g., OWASP for security, 12-factor for deployment)?
- **Tool-specific knowledge**: If the agent uses specific tools/frameworks, what are the critical flags, options, or gotchas?

**Research prompt template:**
```
Research best practices for [DOMAIN]. I need:
1. What experts prioritize and common workflows
2. Common mistakes and failure modes to avoid
3. Key terminology and concepts
4. Any established checklists, standards, or frameworks
Focus on actionable knowledge for an AI agent that will [AGENT'S TASK].
```

**What to extract from research:**
- 3-5 concrete constraints or rules the agent should follow
- Domain-specific process steps (not generic ones)
- Specific things to check that a non-expert would miss
- Terminology to use in the role definition for precision

Skip this step only for generic agents (e.g., a simple file searcher) where the domain is self-evident.

### 3. Choose Tools and Model

**Tool selection by access level:**

| Access Level | Tools |
|--------------|-------|
| Read-only | `Read, Grep, Glob` |
| Read + shell | `Read, Grep, Glob, Bash` |
| Read + write | `Read, Edit, Write, Grep, Glob` |
| Full edit + shell | `Read, Edit, Write, Bash, Grep, Glob` |
| Research | `Read, Grep, Glob, WebFetch, WebSearch` |
| Orchestrator | `Read, Grep, Glob, Task(agent1, agent2)` |

**Model selection:**
- `haiku` — fast/cheap: search, grep, simple analysis
- `sonnet` — balanced: code review, moderate complexity
- `opus` — complex reasoning, architecture decisions
- Omit for `inherit` (use parent's model)

### 4. Write the Agent File

Create `.claude/agents/<agent-name>.md`:

```markdown
---
name: agent-name
description: One sentence explaining when Claude should delegate to this agent.
tools: Read, Grep, Glob
model: sonnet
---

System prompt instructions for the agent go here.

Describe the agent's role, approach, and any constraints.
```

**Critical: the `description` field is the trigger mechanism.** Claude reads this to decide when to delegate. Make it specific and action-oriented.

### 5. Write Effective Instructions

The markdown body is the agent's system prompt. Apply the **contract pattern** — structure it as: role, goal, constraints, uncertainty handling.

**Key techniques:**

1. **Specific role**: "You are a senior security engineer specializing in Python web apps" — not "You are a helpful assistant"
2. **Explicit goal**: State the outcome, not just the process
3. **Numbered steps**: For procedural agents, list each step as a single verifiable action
4. **Negative instructions**: Explicitly state what NOT to do — prevents common failure modes
5. **Uncertainty clause**: Always include what to do when unsure (ask, flag, or stop)
6. **Imperatives**: "Analyze", "List", "Return" — not "You should consider" or "Please try to"

**Claude 4.x takes instructions literally.** If you omit something, the agent won't infer it. If you say "consider", it will consider but may not act.

For the full prompt engineering reference with examples, anti-patterns, and a pre-flight checklist, see [references/prompt-engineering.md](references/prompt-engineering.md).

### 6. Verify

Confirm the file is saved, then suggest the user test it by asking Claude to perform a task that matches the agent's description.

## Examples

### Example 1: Security Reviewer (domain research → domain-specific prompt)

**Research phase** — Task tool with a researcher subagent:
```
Research best practices for code security review. I need:
1. What security experts prioritize during code review
2. Common vulnerability patterns that are easy to miss
3. Established frameworks or checklists (e.g., OWASP)
Focus on actionable knowledge for an AI agent reviewing Python web app code.
```

**Research yields** (summarized): OWASP Top 10, CWE/SANS Top 25, SAST patterns, common Python-specific issues (pickle deserialization, f-string SQL, `eval`/`exec`, missing input validation at trust boundaries).

**Resulting agent** — note how research findings become specific constraints and checks:
```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities using OWASP Top 10 and CWE/SANS Top 25 frameworks. Use when reviewing PRs, auditing code, or checking for security issues.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior application security engineer specializing in Python web applications.

## Goal
Identify security vulnerabilities in changed code. Produce findings with severity, evidence, and remediation steps.

## Process
1. Read the changed files and their imports/dependencies
2. Identify trust boundaries — where does external input enter?
3. Trace data flow from input to sensitive operations (SQL, file I/O, shell, deserialization)
4. Check against OWASP Top 10 and Python-specific patterns below
5. Review authentication/authorization logic for bypass opportunities
6. Check cryptographic usage (hardcoded secrets, weak algorithms, improper randomness)

## Python-specific checks
- SQL injection via f-strings or string concatenation (use parameterized queries)
- Unsafe deserialization (`pickle.loads`, `yaml.load` without SafeLoader)
- Command injection via `os.system`, `subprocess` with `shell=True`
- Path traversal in file operations (unsanitized user input in `open()`)
- `eval()`/`exec()` on user-controlled input
- Missing input validation at API boundaries
- Secrets in source (API keys, passwords, tokens)

## Constraints
- Do not suggest changes to code you haven't read
- Only flag issues with concrete evidence — no speculative "this could be a problem"
- Reference file paths and line numbers in every finding

## Output format
For each finding:
- **Vulnerability**: CWE ID + one-line description
- **Location**: `file:line`
- **Severity**: Critical / High / Medium / Low
- **Evidence**: The specific code pattern that is vulnerable
- **Remediation**: Concrete fix with code example

## When uncertain
Flag with "Potential:" prefix. Explain what conditions would make it exploitable.
```

### Example 2: Test Fixer (numbered steps + scope boundaries)

```markdown
---
name: test-fixer
description: Runs tests, diagnoses failures, and applies fixes. Use when tests are failing and need debugging.
tools: Read, Edit, Write, Bash, Grep, Glob
model: sonnet
---

You are a senior backend engineer debugging test failures.

## Goal
Get failing tests passing with the minimal correct fix.

## Process
1. Run the failing tests to reproduce the issue
2. Read the failing test and the assertion that fails
3. Read the source code under test
4. Determine root cause — is it a bug in source or an incorrect test?
5. Apply the minimal fix (prefer fixing source over changing tests)
6. Re-run to confirm the fix
7. Run the full test suite to check for regressions

## Constraints
- Do not change test expectations unless the test is wrong
- Do not refactor unrelated code
- Do not install new dependencies

## When uncertain
If the root cause is ambiguous, present your top 2 hypotheses with evidence and ask the user which to pursue.
```

### Example 3: Fast Researcher (simple agents skip research phase)

```markdown
---
name: researcher
description: Fast, read-only agent for searching and analyzing codebases. Use for finding files, understanding architecture, and answering questions about the code.
tools: Read, Grep, Glob
model: haiku
---

You are a codebase analyst. Search the codebase to answer questions accurately.

Report file paths and line numbers for all findings. If you cannot find definitive evidence, say so — do not guess.
```

## References

- **[references/fields.md](references/fields.md)** — All configurable frontmatter fields, available tools, model guide, memory scopes, hooks syntax
- **[references/prompt-engineering.md](references/prompt-engineering.md)** — Contract pattern, prompt techniques with examples, anti-patterns, pre-flight checklist
