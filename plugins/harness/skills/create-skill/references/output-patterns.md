# Output Patterns

Use these patterns when skills need to produce consistent, high-quality output.

## Template Pattern

Provide templates for output format. Match the level of strictness to your needs.

**For strict requirements (like API responses or data formats):**

```markdown
## Report structure

ALWAYS use this exact template structure:

# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

**For flexible guidance (when adaptation is useful):**

```markdown
## Report structure

Here is a sensible default format, but use your best judgment:

# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]

Adjust sections as needed for the specific analysis type.
```

## Examples Pattern

For skills where output quality depends on seeing examples, provide input/output pairs:

```markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Follow this style: type(scope): brief description, then detailed explanation.
```

Examples help Claude understand the desired style and level of detail more clearly than descriptions alone.

## Structured Data Pattern

When the skill must produce structured output (JSON, YAML, etc.), specify the exact schema with field types, optionality, and a sample value — not just a description.

**Concrete schema (preferred):**

```markdown
## Output Format

Return a JSON object with this structure:

{
  "verdict": "pass" | "fail" | "needs_review",
  "issues": [
    {
      "severity": "critical" | "major" | "minor",
      "location": "filename:line_number",
      "description": "One-sentence description of the issue"
    }
  ],
  "summary": "One paragraph overall assessment"
}

Return only valid JSON. Do not wrap in markdown code fences.
```

**Vague description (avoid):**

```markdown
Return a JSON object with the results of the review.
```

The schema approach eliminates ambiguity about field names, types, optionality, and nesting.

## Arguments Pattern

For skills that accept user arguments (explicit or parsed from natural language), use a parameters table to define each argument clearly:

```markdown
## Arguments

Parse the following arguments from the user's request:

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| name | yes | — | Name of the output file (kebab-case) |
| format | no | "markdown" | Output format: "markdown", "json", or "html" |
| depth | no | "standard" | Analysis depth: "quick", "standard", or "deep" |
| output | no | "./" | Directory to write the output file |

**Parsing examples:**

- "Generate a quick review called api-audit" → name: api-audit, depth: quick
- "Create a deep analysis in JSON format" → format: json, depth: deep
```

Including parsing examples helps Claude reliably extract arguments from natural language requests.
