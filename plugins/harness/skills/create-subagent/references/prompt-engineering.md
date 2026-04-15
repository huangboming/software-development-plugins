# Prompt Engineering for Subagent System Prompts

## The Contract Pattern

Structure every system prompt as a short contract with four sections:

```
You are [role]. [One sentence on expertise/context.]

## Goal
[What success looks like — the outcome, not the process.]

## Constraints
- [Boundary 1]
- [Boundary 2]

## When uncertain
[What to do when the agent doesn't know — ask, flag, or stop.]
```

This pattern works because Claude 4.x takes instructions literally. Omit a section and the agent has no guidance for that dimension.

## Techniques

### 1. Specific Role Definition

The single highest-impact technique. A specific role activates relevant domain knowledge.

| Quality | Example |
|---------|---------|
| Bad | "You are a helpful assistant." |
| OK | "You are a code reviewer." |
| Good | "You are a senior security engineer specializing in Python web applications." |

**Rule**: Include domain, seniority/expertise level, and relevant context.

### 2. Be Direct and Explicit

Claude does exactly what you ask — nothing more, nothing less.

- **Say what to do**, not what to "try" or "consider"
- **Specify format**: "Return a markdown checklist" not "summarize your findings"
- **State constraints explicitly**: "Do not modify test files" not "be careful with tests"
- **Use imperatives**: "List", "Analyze", "Return" — not "You should" or "Please consider"

### 3. Use XML Tags for Structure

When the prompt has distinct sections (context, instructions, output format), XML tags reduce ambiguity.

```markdown
You are a database migration specialist.

<task>
Analyze the schema change and generate a safe migration.
</task>

<constraints>
- Never drop columns without explicit user approval
- Always create reversible migrations
- Check for index implications on tables over 1M rows
</constraints>

<output_format>
Return the migration SQL in a fenced code block, preceded by a
one-paragraph risk assessment.
</output_format>
```

**When to use XML tags**: Multiple distinct sections, nested data, or when you need Claude to parse/reference specific parts. Skip them for short, simple prompts.

### 4. Numbered Steps for Procedures

When the agent must follow a specific sequence, use numbered steps. This is more reliable than prose.

```markdown
1. Read the failing test file
2. Identify the assertion that fails
3. Read the source code under test
4. Determine root cause
5. Apply the minimal fix to the source (not the test)
6. Re-run the test to confirm
```

**Rule**: Each step should be a single, verifiable action.

### 5. Negative Instructions (Guardrails)

Explicitly state what the agent must NOT do. Prevents common failure modes.

```markdown
- Do not modify files outside the `src/` directory
- Do not install new dependencies without asking
- Do not guess at API behavior — read the source
- If unsure, say so explicitly. Do not fabricate answers.
```

**Hallucination prevention**: Always include "If unsure, say so explicitly" for research/analysis agents.

### 6. Few-Shot Examples for Output Format

When you need a specific output structure, 2-3 examples are more effective than describing the format.

```markdown
When reporting findings, use this format:

<example>
**Finding**: SQL injection vulnerability
**Location**: `src/api/users.py:42`
**Severity**: High
**Fix**: Use parameterized query instead of f-string interpolation
</example>

<example>
**Finding**: Unused import
**Location**: `src/utils/helpers.py:3`
**Severity**: Low
**Fix**: Remove `import os`
</example>
```

### 7. Chain of Thought for Complex Agents

For agents doing analysis or multi-factor decisions, instruct them to reason explicitly.

```markdown
Before providing your answer:
1. List what you observe in the code
2. Identify potential issues and their severity
3. Consider trade-offs of each fix approach
4. Recommend the approach with the best trade-off

Show your reasoning, then provide your recommendation.
```

**Trade-off**: Increases output length and latency. Use only for agents that make complex judgment calls (architecture, debugging), not for agents that follow a fixed procedure.

### 8. Scope Boundaries

Clearly define what's in and out of scope to prevent scope creep.

```markdown
## In scope
- Bug fixes in the authentication module
- Related test updates

## Out of scope
- Refactoring unrelated code
- Adding new features
- Changing the API contract
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| "Be helpful and thorough" | Vague, no actionable guidance | State specific goal and success criteria |
| Restating Claude's defaults | Wastes tokens, no effect | Only include non-obvious instructions |
| Wall of text | Attention dilution | Use structure (headers, bullets, numbered steps) |
| Too many responsibilities | Agent tries everything, does nothing well | One goal per agent |
| No uncertainty handling | Agent guesses or hallucinates | Add "if unsure" clause |
| Overly rigid scripts | Breaks on edge cases | Balance structure with judgment allowance |

## Checklist

Before finalizing a system prompt, verify:

- [ ] Role is specific (domain + expertise level)
- [ ] Goal states the outcome, not just the process
- [ ] Constraints are explicit (what NOT to do)
- [ ] Output format is specified or exemplified
- [ ] Uncertainty handling is defined
- [ ] Each instruction is an imperative, not a suggestion
- [ ] No redundant instructions (things Claude does by default)
- [ ] Prompt is under 500 words (conciseness = better adherence)
