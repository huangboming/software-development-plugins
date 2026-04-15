# Release Notes Template

```markdown
# <Product Name> — <Version>

> Released: <date>

<1-2 sentence overview framing the theme of this release.>

## Highlights

- **<Highlight 1>** — <one-sentence benefit description>
- **<Highlight 2>** — <one-sentence benefit description>
- **<Highlight 3>** — <one-sentence benefit description>

## Breaking Changes

> These changes require action. Review before upgrading.

- **<Change>** — <what changed, who is affected, what to do>

  **Migration:** <specific steps to adapt>

## What's New

### <Product Area 1>

- <Change description focused on user benefit>
- <Change description focused on user benefit>

### <Product Area 2>

- <Change description focused on user benefit>

## Improvements

- <Change description>

## Bug Fixes

- <Fix description — name the symptom that was resolved>

## Performance

- <Improvement with quantified impact when available>

## Security

- <Patch description — name the risk that was addressed>

## Deprecations

- **<Feature>** — <what is deprecated, when it will be removed, what to use instead>
```

### Usage Notes

- Omit any section that has no entries.
- When there are fewer than 5 changes total, skip product-area grouping and list by category only.
- Highlights are the 3-5 most impactful changes, pulled from any category. Every highlight also appears in its category section.
- Breaking Changes always appears first when present, before Highlights.
- When generating an executive summary alongside user-facing notes, add it as an `## Executive Summary` section at the top of the document (after the release overview, before Highlights).
