# Frontend Architecture — Template & Guide

## Document Template

Use this structure for `docs/development/system/architecture.md` in frontend projects. Adapt based on what the codebase contains — omit inapplicable sections (e.g., skip "Data Fetching" for a static site), add sections for significant concerns not listed.

```markdown
# Architecture

> Last updated: <date>

## Application Overview

What the app does, who uses it, and the rendering strategy (SPA, SSR, SSG,
or hybrid). Whether it's standalone, part of a larger system, or a
micro-frontend.

## Tech Stack & Build Pipeline

Framework and version, language (TypeScript/JavaScript), build tool, package
manager. Key libraries and their roles (state, routing, UI kit, forms).
Deployment target (static hosting, Node server, edge).

## Routing & Page Structure

How routes are defined (file-based, config-based). Page/layout hierarchy —
which layouts wrap which pages. Code splitting and lazy loading strategy.
Route guards or auth-protected routes.

Include a table mapping URL patterns to page components and source locations.

## Component Architecture

How components are organized:
- Directory structure and naming conventions
- Component categories (pages, feature modules, shared/UI primitives)
- Composition patterns (container/presentational, compound components,
  render props, slots)
- Where major feature areas live (e.g., `Dashboard → src/features/dashboard/`)

Include a Mermaid diagram if component hierarchy or feature module boundaries
are non-trivial.

## State Management & Data Flow

Global vs local state strategy. State library and why it was chosen. Where
state definitions live. How data flows from API to rendered UI. Server state
vs client state distinction if applicable.

Include a Mermaid diagram for a primary use case's data flow.

## Data Fetching & API Integration

How the app communicates with backends:
- API client setup (Axios, fetch wrapper, GraphQL client)
- Fetching patterns (hooks, server components, loaders)
- Caching and revalidation strategy
- Loading/error state conventions
- Type safety (generated types, Zod, tRPC)

## Styling Architecture

CSS strategy (modules, Tailwind, CSS-in-JS, vanilla extract). Design tokens
or theming — where values are defined, how components consume them.
Responsive breakpoints. How styles are co-located or organized.

## Configuration & Environment

Environment variables and access pattern (import.meta.env, process.env).
Build-time vs runtime config. Feature flags.
```

## Exploration Guide

When creating from scratch, prioritize these areas during deep exploration:

| Area | What to look for | Why it matters |
|------|-----------------|----------------|
| Routing | Route definitions, page directory, layout hierarchy, route guards | The route-to-component mapping is the first thing developers look for when navigating unfamiliar code |
| Components | Directory structure, naming patterns, categories (pages, features, shared/UI) | Reveals the actual organizational philosophy — where new code should go |
| State | Store setup, state library config, context providers, where state lives | State architecture has the most impact on how features are built and how bugs manifest |
| Data fetching | API client setup, fetching hooks/patterns, caching config | The bridge between frontend and backend; often the most complex part to understand |
| Styling | CSS strategy, theme/token definitions, design system conventions | Developers need to know this before writing any UI code |
| Build & config | Build tool config, environment variables, feature flags | Often scattered and poorly documented; surfacing it saves repeated archaeology |

## Quality Checklist

- [ ] Architectural claims are grounded in concrete code (specific files or directories)
- [ ] Component/feature descriptions are one sentence each, not paragraphs
- [ ] Mermaid diagrams included for non-trivial component hierarchies and data flows
- [ ] Mermaid node labels use actual line breaks, never `\n` escape sequences
- [ ] Concrete path examples (e.g., "`src/features/auth/LoginForm.tsx` → `src/hooks/useAuth.ts` → `src/api/auth.ts`") instead of abstract layer names
- [ ] Written for a developer with zero project context
- [ ] Intentional design decisions distinguished from emergent patterns
- [ ] Route-to-component mapping is clear — a developer can find which file renders a given URL

## Edge Cases

- **Monorepo with multiple apps**: One architecture.md per app, or top-level with cross-references. Ask the user.
- **Very small project** (< 10 components): Keep proportionally brief. Skip sections like "State Management" if not warranted.
- **No clear architectural pattern**: Document actual structure honestly. Note as observation.
- **Full-stack framework** (Next.js, Nuxt, SvelteKit with API routes): Document frontend architecture here. If API routes are substantial, recommend a separate backend architecture.md or note briefly under a "Server-Side" section.
