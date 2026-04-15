# Progressive Disclosure Patterns

Progressive disclosure is the technique of keeping SKILL.md lean by moving detail into references that load only when needed. Three patterns show up repeatedly; pick whichever matches the skill's shape.

## Pattern 1: High-level Guide with References

SKILL.md provides the core workflow; specialized topics live in separate files linked by topic name.

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](FORMS.md) for the complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

Claude loads FORMS.md, REFERENCE.md, or EXAMPLES.md only when the task calls for that topic.

**Use when:** The skill has a single core workflow plus several optional deep-dive topics that only some tasks need.

## Pattern 2: Domain-specific Organization

When a skill spans multiple domains (or multiple frameworks/variants), organize references by domain so Claude loads only the relevant slice:

```
bigquery-skill/
├── SKILL.md                 (overview and navigation)
└── references/
    ├── finance.md           (revenue, billing metrics)
    ├── sales.md             (opportunities, pipeline)
    ├── product.md           (API usage, features)
    └── marketing.md         (campaigns, attribution)
```

When a user asks about sales metrics, Claude only reads `sales.md`.

The same pattern works for multi-variant skills:

```
cloud-deploy/
├── SKILL.md                 (workflow + provider selection)
└── references/
    ├── aws.md               (AWS deployment patterns)
    ├── gcp.md               (GCP deployment patterns)
    └── azure.md             (Azure deployment patterns)
```

When the user chooses AWS, Claude only reads `aws.md`.

**Use when:** Content splits cleanly along a dimension (domain, framework, provider, language) and a given task only needs one slice.

## Pattern 3: Conditional Details

Show the common-case content inline; link to advanced content for specialized needs:

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

Claude reads REDLINING.md or OOXML.md only when the user needs those features.

**Use when:** Most tasks are handled by a simple default path, but a minority of tasks need deeper, specialized guidance.

## Choosing Between Patterns

| If the skill has... | Use... |
|---------------------|--------|
| One workflow + optional deep-dives | Pattern 1 |
| Clean partition by domain/variant | Pattern 2 |
| Common simple path + rare deep path | Pattern 3 |
| Mix of the above | Combine patterns — they compose cleanly |

## Guidelines That Apply to All Three

- **One topic per file.** Don't bundle unrelated content; Claude must load the whole file to reach any part of it.
- **Descriptive file names.** `python-scaffold-guide.md` beats `guide-3.md`. The name is the first signal Claude uses to decide whether to open a file.
- **Index each reference in SKILL.md.** For every reference, write one line that answers *what's in it* and *when to read it*. Unreferenced files are invisible.
- **One level deep.** Keep references directly under SKILL.md, not nested inside sub-folders Claude has to traverse.
- **Table of contents for long files.** Files over 100 lines should start with a TOC so Claude can scope the content without reading in full.
