# Workflow Patterns

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. It is often helpful to give Claude an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

## Decision Loop Pattern

For agentic skills that explore, act, and iterate, define an explicit decision loop. Without one, agents tend to either stop too early or over-plan.

```markdown
## Process

1. **Gather context** — Read relevant files, run discovery scripts, understand current state
2. **Plan** — Outline the steps required; identify any ambiguities
3. **Execute** — Carry out one step at a time, verifying each step before proceeding
4. **Verify** — Confirm the outcome matches the goal (run tests, validate output)
5. **Report** — Summarize what was done, what changed, and any open issues
```

This pattern works well for code review skills, refactoring skills, and any skill where the work involves multiple rounds of investigation and action.

## Self-Correction Pattern

For skills that produce output requiring quality standards, build in a review-and-revise cycle:

```markdown
## Process

1. Generate a first draft of the output
2. Review the draft against these criteria:
   - Does it address every requirement from the user's request?
   - Does it follow the output format specified below?
   - Are there any factual errors or unsupported claims?
3. Revise the draft to fix any issues found in the review
4. Deliver the final version
```

This is especially useful for report-generation skills, document-creation skills, and skills where output quality depends on catching errors before delivery.