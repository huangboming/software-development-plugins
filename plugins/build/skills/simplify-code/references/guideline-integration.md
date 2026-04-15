# Guideline Integration

How to read, interpret, and apply project code guidelines from `docs/development/code-guidelines/` during simplification.

## Reading Guidelines

1. Read all `.md` files in `docs/development/code-guidelines/`
2. For each guideline, extract:
   - **Scope** — which languages, frameworks, or file patterns it applies to
   - **Rule** — the specific convention it mandates
   - **Detectability** — can violations be found mechanically, or do they require judgment?
3. Filter to guidelines that apply to files in the current simplification scope
4. Flag only clear violations — skip ambiguous or borderline cases

## Scope Matching

Not all guidelines apply to all files. Match before flagging:

- Language-specific guidelines → only files in that language
- Framework-specific guidelines → only files using that framework
- Directory-specific conventions → only files in those directories

## Confidence Mapping

| Guideline type | Confidence | Rationale |
|----------------|------------|-----------|
| Naming conventions | Clear | Mechanical rename |
| Import ordering | Clear | Mechanical reorder |
| Error handling patterns | Judgment | May change behavior |
| Logging conventions | Judgment | Context-dependent |
| API/database patterns | Judgment | Architecture-dependent |

## Conflict Resolution

When project guidelines and the simplification catalog disagree:

1. **Guidelines endorse a pattern the catalog flags** — project guidelines win. Skip the catalog pattern.
   Example: guidelines say "use wrapper classes for external services" → do not flag as unnecessary wrapping.

2. **Guidelines forbid a pattern the catalog recommends** — project guidelines win. Skip the catalog recommendation.
   Example: guidelines say "no early returns" → do not apply guard clause transforms.

3. **Guidelines are silent on a pattern** — apply the catalog as normal.
