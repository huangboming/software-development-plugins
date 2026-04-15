# Writing Effective Instructions

This guide covers prompt engineering best practices for writing SKILL.md body instructions — the content Claude reads after a skill triggers.

## The Mental Model

Write instructions as if onboarding a brilliant but context-free new employee on their first day. They are highly intelligent but have zero implicit knowledge of your norms, terminology, or expectations.

**The pass/fail test:** Every instruction should be specific enough that a human could objectively pass or fail a response against it. If an instruction is too vague to evaluate, rewrite it.

## Write in Imperative Form

Use imperative ("Identify the three most critical issues") or infinitive ("To begin, read the input file") form. Imperative instructions are followed more reliably than descriptive prose.

| Weak (descriptive) | Strong (imperative) |
|---------------------|---------------------|
| "The skill analyzes code for issues" | "Analyze the code for issues" |
| "This skill helps users create reports" | "Create a report based on the user's input" |
| "The assistant identifies patterns" | "Identify patterns in the data" |
| "It should check for errors" | "Check for errors before proceeding" |

## Be Concrete and Specific

Vague instructions produce inconsistent results. Replace abstract language with concrete expectations.

| Vague | Concrete |
|-------|----------|
| "Be helpful and respond appropriately" | "Respond with: (1) a one-sentence verdict, (2) a bulleted list of up to 5 issues sorted by severity" |
| "Provide a thorough analysis" | "Analyze each function for: cyclomatic complexity, parameter count, and coupling to external modules" |
| "Handle errors gracefully" | "If the script fails, report the exit code, stderr output, and the command that failed" |
| "Use good judgment" | "If more than 3 files are affected, ask the user before proceeding" |

Every token in a skill competes for attention in a shared context window. Challenge each piece of content: "Does this instruction justify its token cost? Would Claude handle this correctly without it?"

## Structure for Clarity

Use formatting to create visual hierarchy that helps Claude parse instructions efficiently:

- **Markdown headers** (`##`, `###`) for major sections and subsections
- **Numbered steps** for sequential processes where order matters
- **Bullet points** for parallel items where order doesn't matter
- **Tables** for reference data (argument definitions, type mappings, severity levels)
- **Code blocks** for exact command syntax, output templates, or file formats
- **Bold** for key terms or decision points within prose

For skills with 3+ sections, start with a brief overview of the process before diving into details:

```markdown
## Process

Report generation involves these steps:

1. Gather metrics (run metrics.py)
2. Analyze trends
3. Write the report
4. Validate output (run validate.py)

### Step 1: Gather Metrics
...
```

This gives Claude the full picture before it encounters each step's details.

## Prefer Positive Instructions

Negative instructions ("don't do X") are less reliable than positive alternatives. When told *not* to think about something, models still activate that concept first — the "Pink Elephant Problem."

| Avoid | Prefer |
|-------|--------|
| "Don't use technical jargon" | "Write in plain language accessible to a non-technical reader" |
| "Don't go off-topic" | "Limit your response strictly to the question asked" |
| "Don't make things up" | "If uncertain, say so explicitly and suggest how the user can verify" |
| "Don't be verbose" | "Respond in 3 sentences or fewer" |
| "Don't use markdown" | "Write in flowing prose paragraphs" |

**Exception:** Negative constraints remain valuable for hard safety/scope limits where a positive rewrite would be weaker or ambiguous. Limit hard negatives to 3–5 critical items and make them specific:

```markdown
## Hard Constraints
- Never execute commands that modify production data without explicit user confirmation.
- Never commit files containing secrets (.env, credentials.json).
```

## Distinguish Hard Constraints from Soft Preferences

Explicitly label constraint severity so the model prioritizes correctly when constraints conflict:

```markdown
## Constraints

**Hard limits — never violate:**
- Never access files outside the /workspace directory
- Never delete files without explicit user confirmation

**Soft preferences — apply when practical:**
- Prefer idiomatic patterns over verbose alternatives
- Prefer short variable names in tight loops
```

## Use Examples to Teach Behavior

Providing worked examples is one of the highest-leverage prompt engineering techniques. Examples communicate format, tone, reasoning style, and quality expectations more reliably than descriptions alone.

**How many:** Include 3–5 diverse examples for non-trivial tasks.

**Selection criteria:**

| Criterion | Why it matters |
|-----------|----------------|
| Diversity | Cover different sub-cases and input structures. Similar examples produce overgeneralization. |
| Boundary cases | Include at least one edge case to teach where to draw the line. |
| Format fidelity | Every example must use the exact output format expected in practice. |
| Reasoning chains | For judgment tasks, include the reasoning, not just the answer. |

**Pattern for examples with reasoning:**

```markdown
**Example 1:**
Input: "Should I add an index to the `user_id` column in the `events` table?"
Output:
  Reasoning: The `events` table has 50M+ rows and is queried primarily by `user_id`.
  Without an index, each query does a full table scan.
  Recommendation: Yes, add a B-tree index on `user_id`. Monitor for write
  amplification if insert rate exceeds 1000/sec.

**Example 2:**
Input: "Should I add an index to the `created_at` column in the `logs` table?"
Output:
  Reasoning: The `logs` table is append-only with 200M rows, but `created_at`
  queries only happen in nightly batch jobs. Adding an index would slow every
  insert for a marginal improvement in a non-latency-sensitive job.
  Recommendation: No. The batch job's performance is acceptable without an index.
```

## Handle Edge Cases and Uncertainty

Every skill should answer: "What does the agent do when it doesn't know what to do?"

**Define an escalation protocol.** Options, from safest to most autonomous:

1. **Stop and ask** — Pause and request clarification from the user
2. **State assumption and proceed** — Make the assumption explicit, proceed, and surface it in the output
3. **Apply a fallback rule** — Execute a defined default behavior

Choose based on the cost of mistakes. For tasks with hard-to-reverse actions, prefer stopping and asking.

**Enumerate known edge cases** rather than hoping the model will infer the right handling:

```markdown
## Edge Cases
- If the input file is empty, respond: "The provided file is empty."
- If the codebase contains no tests, flag this as a critical risk in the review.
- If the requested operation would affect more than 10 files, stop and request confirmation.
```

**Use if/then structures** for decision rules:

```markdown
If the user's request is ambiguous:
  → Present the two most likely interpretations
  → Ask which is intended before taking action

If the script exits with a non-zero code:
  → Report the exit code and stderr
  → Suggest a fix if the error is recognizable
```

## Claude-Specific Considerations

Claude 4 models (Opus 4.6, Sonnet 4.6) are significantly more responsive to instructions than prior generations. Prompts designed with heavy emphasis for older models may cause overtriggering.

**Dial back aggressive language:**

| Old pattern (overfit to older models) | New pattern (appropriate for Claude 4) |
|---------------------------------------|----------------------------------------|
| "CRITICAL: You MUST ALWAYS use the search tool when..." | "Use the search tool when..." |
| "IMPORTANT: NEVER skip this step" | "Complete this step before proceeding" |
| "You ABSOLUTELY MUST follow this format" | "Follow this format:" |

Reserve ALL-CAPS emphasis for at most 1–2 genuinely non-negotiable constraints. Write everything else in normal prose.

## Anti-Patterns Checklist

Scan your instructions for these common mistakes:

- [ ] **Vagueness** — "Be thorough," "respond appropriately," "use good judgment" without concrete criteria
- [ ] **Descriptive instead of imperative** — "The skill analyzes..." instead of "Analyze..."
- [ ] **Overloaded body** — Cramming every edge case into SKILL.md instead of using references/
- [ ] **Aggressive emphasis** — ALL-CAPS, MUST, NEVER, ALWAYS scattered throughout
- [ ] **Negative-only constraints** — Lists of "don't do X" without positive alternatives
- [ ] **No examples** — Relying entirely on descriptions when examples would be clearer
- [ ] **No edge case handling** — Assuming Claude will infer correct behavior for ambiguous situations
- [ ] **Teaching Claude what it already knows** — Explaining basic programming concepts, general knowledge, or tool syntax that Claude handles natively
- [ ] **No escalation protocol** — No guidance on what to do when uncertain
- [ ] **Inconsistent formatting** — Mixing styles within examples or sections
