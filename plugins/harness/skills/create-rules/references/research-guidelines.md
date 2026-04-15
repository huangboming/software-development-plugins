# Research Guidelines for Rules

Rules must reflect current, real-world best practices — not stale or generic advice. Use this guide during workflow step 2 (Research) of the `create-rules` skill.

## When to Research

- **Always research**: Language/framework-specific rules (React, Rust, Go, Next.js, etc.), library-specific patterns, API design for specific ecosystems, security practices for specific stacks.
- **Skip research**: Universal principles you are highly confident about (basic git hygiene, generic naming conventions, fundamental error handling patterns).
- **When in doubt, research.** Outdated advice in a rule is worse than no rule at all.

## What to Research

For each rule topic, look for:

- **Official style guides and documentation** — e.g., Go's Effective Go, Rust API Guidelines, React docs
- **Widely-adopted community standards** — e.g., Airbnb JS style guide, Google style guides
- **Current idioms and patterns** — what the ecosystem actually does today, not 3 years ago
- **Common pitfalls** — frequent mistakes and anti-patterns specific to the domain
- **Recent ecosystem changes** — deprecated APIs, new recommended approaches, breaking changes

## How to Research

If a researcher subagent is available via the Task tool, invoke it — one call per independent topic so research runs in parallel. Use whichever researcher the current environment exposes; do not hard-code a plugin-prefixed name. Example briefs:

```
Task(
  subagent_type="<researcher>",
  prompt="Research current React best practices: component patterns, state management, performance optimization, common anti-patterns. Focus on official React docs, widely-adopted community conventions, and recent ecosystem changes."
)

Task(
  subagent_type="<researcher>",
  prompt="Research current TypeScript best practices: strict mode patterns, type-level programming idioms, common mistakes, utility type usage. Focus on the official handbook and widely-adopted style guides."
)
```

If no researcher subagent is installed, fall back to WebSearch/WebFetch directly.

## Applying Research to Rules

- Distill findings into **specific, actionable instructions** — do not dump raw research into the rule.
- Prefer conventions with broad community consensus over niche opinions.
- When the ecosystem is split (e.g., two popular state management approaches), note both briefly and pick a default with rationale.
- Discard anything you cannot verify from multiple credible sources.
