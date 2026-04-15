# Component Architecture — Template & Guide

## Document Template

Use this structure for `docs/development/system/components/<component-name>/architecture.md`. Each component doc is self-contained — a reader should understand the component without reading other component docs.

```markdown
# <Component Name> Architecture

> Last updated: <date>

## Responsibility

What this component does, what it owns, and where its boundaries are.
One paragraph. State what is NOT this component's responsibility if the
boundary is non-obvious.

## Internal Structure

How code is organized within this component. Map directories and key files
to their roles. Include a table for components with 5+ significant files
or directories.

## Key Abstractions

Core types, interfaces, patterns, and domain concepts used internally.
For each: name, purpose, and where it's defined. Focus on abstractions
a developer must understand before modifying this component.

## Data Flow

How data moves through this component for its primary operations.
Include a Mermaid diagram for non-trivial flows. Show entry points,
transformations, and where data exits the component.

## Dependencies

What this component depends on (internal modules, external services,
libraries) and what depends on it. Distinguish between runtime
dependencies and build/test dependencies.

Include a Mermaid diagram if dependency relationships are non-trivial.

## Public Interface

What this component exposes to the rest of the system — exported
functions, classes, events, API endpoints, or message contracts.
This is the contract other code depends on; changes here have the
widest blast radius.
```

## Exploration Guide

When documenting a component from scratch:

1. **Identify boundaries** — Find the component's root directory. Read its entry point(s) and public exports to understand what it exposes. Check package boundaries, module exports, or API route registrations.
2. **Map internal structure** — Scan subdirectories and key files. Identify the organizational pattern (by layer, by feature, flat).
3. **Trace key abstractions** — Read core types and interfaces. Identify the domain model and patterns (repository, service, handler, etc.).
4. **Follow primary data flows** — Pick 1-2 primary operations and trace data from entry to exit. Note transformations, validations, and side effects.
5. **Map dependencies** — Check imports from outside the component boundary. Note external service calls, database access, and inter-component communication.
6. **Catalog public interface** — List everything exported or exposed. This is what other code depends on.

### Identifying Bounded Contexts

If the user isn't sure what constitutes a component, look for these signals:

- Directories with their own package manifest or module boundary
- Services behind an API or message interface
- Modules with a clear public API and internal implementation
- Feature directories with self-contained logic
- Anything with its own data store or schema

## Quality Checklist

- [ ] Document is self-contained — understandable without reading other component docs
- [ ] Responsibility section clearly states boundaries (what the component does AND does not do)
- [ ] Internal structure maps directories/files to roles with concrete paths
- [ ] Key abstractions are named, located, and explained — not just listed
- [ ] Data flow covers at least one primary operation end-to-end
- [ ] Dependencies distinguish what the component uses from what uses it
- [ ] Public interface lists concrete exports, not vague descriptions
- [ ] Mermaid diagrams included for non-trivial data flows or dependency graphs
- [ ] Mermaid node labels use actual line breaks, never `\n` escape sequences
- [ ] Written for a developer with zero prior context on this component

## Edge Cases

- **Very small component** (< 5 files): Keep proportionally brief. Responsibility + Internal Structure + Public Interface may suffice.
- **Component with no clear public interface** (tightly coupled): Document what it exposes in practice and note the coupling as an observation.
- **Component spanning multiple directories**: Document the logical boundary, not just the directory structure. Note where files live and why.
- **Shared/utility component** (used by many others): Emphasize Public Interface and list major consumers in Dependencies.
