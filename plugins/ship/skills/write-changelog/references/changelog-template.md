# Changelog Template

Based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

```markdown
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [<version>] - <YYYY-MM-DD>

### Breaking Changes

- **<Change>** — <before/after behavior, migration path> (#<PR>)

### Added

- <Imperative verb> <what was added> (#<PR>)

### Changed

- <Imperative verb> <what changed> (#<PR>)

### Deprecated

- <Imperative verb> <what is deprecated, removal timeline> (#<PR>)

### Removed

- <Imperative verb> <what was removed> (#<PR>)

### Fixed

- <Imperative verb> <what was fixed> (fixes #<issue>)

### Security

- <Imperative verb> <what was patched> (#<PR>)

### Performance

- <Imperative verb> <what improved, quantified if possible> (#<PR>)
```

### Conventions

- Newest version appears first, directly below `[Unreleased]`.
- Use ISO 8601 dates (YYYY-MM-DD).
- Start each entry with an imperative verb (Add, Fix, Change, Remove, Deprecate, Patch, Improve).
- Include PR or issue references in parentheses at the end of each entry.
- Omit sections with no entries.
- Mark pulled/recalled versions as `[YANKED]` — never silently remove them.
- `[Unreleased]` section is always present at the top for accumulating changes before the next release.
- Breaking Changes section appears first within a version when present, even though it is not a standard Keep a Changelog category.
