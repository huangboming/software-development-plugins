# Core Principles for Skill Authoring

These principles apply to every skill. Internalize them before writing SKILL.md or reference files.

## Concise is Key

The context window is a shared, finite resource. Skills compete for attention with the system prompt, conversation history, other skills' metadata, and the user's actual request. Every unnecessary token dilutes the signal of necessary ones.

**The justification test:** For each piece of content, ask: "Would Claude handle this incorrectly without this information?" If the answer is no, cut it. Prefer concise examples over verbose explanations — examples communicate more per token.

See `references/context-engineering.md` for a complete framework on allocating content across SKILL.md, references, scripts, and assets.

## Push Claude Off Its Defaults

Claude already knows a lot about general coding, common libraries, and popular frameworks. A skill earns its tokens by telling Claude what it does *not* already know or would get wrong by default.

Before writing an instruction, ask: "would Claude already do this without being told?" If yes, cut it. Focus on:

- Non-obvious gotchas and failure modes specific to this domain or codebase
- Internal conventions that differ from community defaults
- Opinions that override Claude's usual taste (e.g., "do not use the Inter font or purple gradients" in a design skill)

Generic coding advice dilutes signal. Surprising, specific, organization-flavored content is what makes a skill worth loading.

## Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

- **High freedom (text-based instructions)** — Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.
- **Medium freedom (pseudocode or scripts with parameters)** — Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.
- **Low freedom (specific scripts, few parameters)** — Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of Claude as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

## Avoid Railroading

Skills are reused across many situations. Over-specifying a procedure makes the skill brittle — Claude follows the script even when the situation calls for adaptation.

Give Claude the information it needs, then leave room for judgment. Prefer "when X, do Y because Z" over rigid numbered steps, unless the sequence is genuinely fragile. Reserve low-freedom scripts for the places where consistency truly matters; everywhere else, trust Claude to compose.
