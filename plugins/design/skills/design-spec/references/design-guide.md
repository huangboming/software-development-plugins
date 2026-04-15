# Design Guide

Decision frameworks for system design choices during spec creation. Use these when analyzing constraints and trade-offs in Step 6.

## Table of Contents

**Backend**
- [Architecture Pattern Selection](#architecture-pattern-selection)
- [Database Selection](#database-selection)
- [Scalability Decision Points](#scalability-decision-points)

**Frontend**
- [Rendering Strategy](#rendering-strategy)
- [Component Architecture](#component-architecture)
- [Client State Management](#client-state-management)
- [Routing & Data Fetching](#routing--data-fetching)
- [Design System & Styling](#design-system--styling)
- [Accessibility & Performance](#accessibility--performance)

**Shared**
- [Code Architecture](#code-architecture)
- [Common Spec Mistakes](#common-spec-mistakes)

---

# Backend

## Architecture Pattern Selection

### Monolith vs Microservices

| Factor | Monolith | Microservices |
|--------|----------|---------------|
| Team size | < 10 developers | Large, independent teams |
| Domain complexity | Single bounded context | Multiple bounded contexts with clear ownership |
| Deployment | Single unit, simpler ops | Independent per service, requires orchestration |
| Data model | Shared database, strong consistency | Database-per-service, eventual consistency |
| Best for | Early-stage, simple domains, small teams | Complex domains with independent scaling needs |

**Decision rule:** Start with a monolith unless you have strong evidence for microservices. A well-structured monolith (modular monolith) can be split later; premature microservices introduce distributed systems complexity without the organizational benefits.

### Event-Driven Architecture

**When to use:**
- Asynchronous processing needed (email, file processing, external API calls)
- Loose coupling between components that evolve independently
- Complex workflows across service boundaries

**Pattern ladder (least to most complex):**
1. **Event notification** — Lightweight signal ("order created"), consumer fetches data separately
2. **Event-carried state transfer** — Full data in event, consumers are self-sufficient
3. **Event sourcing** — Events as source of truth, derive state from event log

**Decision rule:** Start with event notification. Only escalate to event sourcing if you need full audit trails or temporal queries (financial systems, compliance-heavy domains).

### CQRS (Command Query Responsibility Segregation)

**When to use:**
- Read-to-write ratio > 10:1
- Read and write models have fundamentally different shapes
- Combined with event sourcing

**Decision rule:** CQRS adds significant complexity (separate models, eventual consistency, synchronization logic). Only use when the read/write model mismatch is a proven bottleneck, not a hypothetical one.

---

## Database Selection

### SQL vs NoSQL Decision Matrix

| Criterion | Favors SQL | Favors NoSQL |
|-----------|-----------|--------------|
| Data relationships | Complex JOINs across entities | Self-contained documents, few relationships |
| Consistency needs | ACID required (financial, transactional) | Eventual consistency acceptable |
| Schema stability | Well-understood, stable domain model | Evolving/flexible schema, rapid iteration |
| Access patterns | Ad-hoc queries, complex reporting | Known access patterns, key-based lookups |
| Scaling strategy | Vertical first, read replicas | Horizontal scaling priority |

**Decision rule:** Default to SQL (PostgreSQL) unless you have a specific access pattern that NoSQL serves dramatically better. Most applications benefit from relational integrity and flexible querying.

### Normalization vs Denormalization

| Normalize | Denormalize |
|-----------|-------------|
| Write-heavy workloads | Read-heavy (10:1+ ratio) |
| Data integrity critical | Performance-critical queries |
| Frequent updates to shared data | Reporting, analytics, search indexes |

**Decision rule:** Normalize first, denormalize selectively for proven hot paths. Premature denormalization creates update anomalies and data inconsistency.

---

## Scalability Decision Points

### When to Add Each Layer

```
1. Optimize queries first     → Indexes, N+1 fixes, query analysis
2. Add caching (Redis)        → When DB reads are the bottleneck
3. Add read replicas          → When cache hit rate is high but DB is still saturated
4. Add async processing       → When any operation > 500ms blocks user responses
5. Shard or partition         → Last resort; high complexity, consider first if it's truly needed
```

**Decision rule:** At each level, measure before adding complexity. Profile and identify the actual bottleneck rather than speculating.

### Sync vs Async Decision

| Keep synchronous | Move to async (job queue) |
|-----------------|--------------------------|
| < 200ms operations | > 500ms operations |
| User needs immediate result | User can be notified later |
| Simple request/response | Multi-step workflows |
| Single service call | Fan-out to multiple services |

---

# Frontend

## Rendering Strategy

| Strategy | When to use | Trade-offs |
|----------|-------------|------------|
| **CSR** (client-side rendering / SPA) | Authenticated app-like experiences, heavy interactivity, no SEO needs | Slower first paint, larger JS, no SEO by default |
| **SSR** (server-side rendering) | Content that must be fast on first load and SEO-indexable (marketing, product pages, dashboards shared via link) | Server cost, complexity around auth and caching |
| **SSG** (static site generation) | Mostly static, content updated at build time (docs, blog, landing pages) | Rebuild required for updates; stale until next build |
| **ISR / on-demand revalidation** | Mostly static but needs occasional freshness (product catalogs) | Caching layer required |
| **Streaming / RSC** | Large pages with mixed fast/slow data; want early paint | Framework-dependent, harder to debug |

**Decision rule:** Start with the simplest strategy that meets SEO, perceived-latency, and data-freshness requirements. Mixed strategies (SSG shell + CSR islands) are common — don't force one strategy for the whole app.

---

## Component Architecture

### Composition patterns

| Pattern | Use when |
|---------|----------|
| **Presentational vs container** | Clear split between UI and data; easier to test UI in isolation |
| **Compound components** | Flexible APIs (e.g. `<Tabs><Tab/></Tabs>`); callers control layout |
| **Headless / hooks + primitives** | Accessibility and behavior separate from visuals (Radix, Headless UI); maximum reusability |
| **Render props / slots** | Inverted control when children need data from parent |

### Where to put logic

```
Component body          → Layout, rendering, event wiring
Custom hook             → Reusable behavior, stateful logic, side effects
Utility (pure function) → Formatting, derivations, no React dependency
Service module          → API calls, auth, storage; no React dependency
```

**Decision rule:** Default to small components, push logic out of JSX into hooks and utilities once it's non-trivial or reused. Avoid prop-drilling more than 2 levels — use context or a state library.

---

## Client State Management

Not every kind of state belongs in the same place. Separate these concerns first:

| State kind | Lives in | Notes |
|-----------|----------|-------|
| Server data (remote, cached) | Query library (React Query, SWR, RTK Query, urql) | Handles caching, revalidation, optimistic updates |
| URL state | Router params, search params | Shareable, bookmarkable, survives refresh |
| Ephemeral UI state | Component local (`useState`, `useReducer`) | Modal open, form draft, hover |
| Cross-page app state | Global store (Zustand, Redux, Jotai, Recoil, Signals) | Current user, theme, feature flags |
| Form state | Form library (React Hook Form, Formik, TanStack Form) | Validation, dirty tracking, submission |

**Decision rule:** Reach for a global store only when state is *truly* shared across unrelated routes. Most "global state" is actually server state in disguise — use a query library first.

---

## Routing & Data Fetching

| Question | Option A | Option B |
|----------|----------|----------|
| Where does data load? | Route-level loaders (framework-driven) | Component-level queries (library-driven) |
| How are errors shown? | Error boundary per route | Error state per component |
| How are auth-gated routes handled? | Route guards / middleware | Component-level redirects |
| How is code split? | Per route (lazy route) | Per feature (dynamic import) |

**Decision rule:** Prefer route-level loaders when the framework supports them (Remix, Next App Router, TanStack Router) — they fix waterfalls and make SSR coherent. Fall back to component-level queries for heavily dynamic, intra-page data.

---

## Design System & Styling

| Approach | Good for | Watch out for |
|----------|----------|---------------|
| **Design system components** (shadcn, MUI, Ant, Radix + Tailwind) | Consistency, accessibility defaults, speed | Matching brand exactly; bundle size of heavy kits |
| **Tailwind / utility CSS** | Rapid styling, co-located with markup, small per-change diffs | Long class strings; needs a convention for extraction |
| **CSS Modules / plain CSS** | Clear ownership, familiar to newcomers | Naming, no tokens out of the box |
| **CSS-in-JS (Emotion, styled-components)** | Dynamic theming, prop-driven styles | Runtime cost, SSR complexity; some ecosystems are deprecating |

**Decision rule:** Reuse existing design-system primitives whenever possible — the spec should list which components are reused vs net-new. Net-new primitives are a scope signal; justify them.

---

## Accessibility & Performance

### Accessibility floor (treat as non-negotiable)

- Semantic HTML first; ARIA only to close gaps
- All interactive elements reachable by keyboard, visible focus ring
- Form fields have labels; errors programmatically associated
- Color contrast meets WCAG AA (4.5:1 body, 3:1 large text)
- Respect `prefers-reduced-motion`

### Performance budgets (adjust to project, but always set numbers)

| Metric | Reasonable starting budget |
|--------|---------------------------|
| Initial JS (gzipped) | < 200KB |
| CSS (gzipped) | < 50KB |
| LCP (4G) | < 2.5s |
| INP | < 200ms |
| Long task (main thread) | < 50ms |

**Decision rule:** Specs for UI-heavy features should state the budget explicitly; otherwise you have no objective way to say "this is done" or "this regressed."

### Large-list / heavy-UI patterns

| Symptom | Remedy |
|---------|--------|
| List > ~200 items, slow scroll | Virtualize (`react-virtual`, `react-window`) |
| Slow filter/search | Debounce input + memoize derivations |
| Re-render storms | Stable callbacks, `memo`, split context |
| Large bundle on first load | Route split, dynamic import heavy deps, lazy-load below-the-fold |

---

# Shared

## Code Architecture

System architecture decides *what* services and stores exist. Code architecture decides *how the source is organized inside them* — layering, module boundaries, dependency direction, testability. A spec that ships clean system architecture but sloppy code architecture rots within a quarter.

### Layering & dependency direction

Decide what the layers are and which way dependencies point. A typical split:

| Layer | Backend | Frontend |
|-------|---------|----------|
| Domain / Core | Entities, value objects, invariants, domain services | Domain types, state machines, pure business rules |
| Application / Use case | Orchestrates domain to fulfill one request | Orchestrates data + interaction for one screen/flow |
| Adapters / Interface | HTTP handlers, CLI, queue consumers | Components, routes, form handlers |
| Infrastructure | DB, cache, external APIs, filesystem | Fetch client, local storage, analytics, telemetry |

**Rule: dependencies point inward.** Infrastructure imports domain; domain never imports infrastructure. Adapters depend on application ports (interfaces), not on concrete infrastructure. This is what keeps the core unit-testable in isolation and lets you swap a DB, a framework, or a transport without touching business logic.

**Decision rule:** enforce direction with import boundary tooling (`eslint-plugin-boundaries`, `dependency-cruiser`, `tach`, `archunit`). Without enforcement, the layering rots within a few months.

### Encapsulation & module boundaries

Every module has a **public** surface (what callers depend on) and a **private** surface (implementation detail). Default to closed — everything is private unless there's a reason to expose it.

| Rule | How to apply |
|------|--------------|
| One module, one public entry point | `index.ts` / package root re-exports the contract; deep imports into a module's internals are a smell |
| Types over shapes at boundaries | Export named types/interfaces so callers don't couple to internal structural types |
| No shared mutable state across modules | Pass state explicitly; export functions/hooks, not module-level singletons |
| Name the module's responsibility | One sentence — if it takes two, split it |

**Decision rule:** the spec should name each module, its single responsibility, and its public API. Anything not listed as public is internal and may change without a migration.

### Separation of concerns

Split by *reason to change*, not by technology:

- Business logic: pure functions / domain services — no I/O, no framework
- I/O (DB, HTTP, filesystem, local storage): behind an adapter that implements a domain-owned interface
- Rendering (JSX / templates): separate from data fetching, which is separate from domain rules
- Side effects: quarantined in event handlers, hooks, or use-case functions — never inline in render or constructors

**Decision rule:** if unit-testing the logic requires mocking five things, the logic is entangled with I/O. Refactor the seams before adding more.

### Testability as a design input

Good specs make the design *testable by construction*, not as an afterthought:

- Pure functions where possible — deterministic, no globals
- Ports (interfaces) for every external dependency so tests can pass fakes
- Constructor / parameter injection rather than module-level singletons
- Inject the clock and ID generator when they matter to behavior

### Frontend code architecture

| Question | Default answer |
|----------|----------------|
| Folder layout | Feature-folder (`features/orders/*`) over layer-folder (`components/`, `hooks/`, `utils/`) once the project exceeds ~20 screens — colocate things that change together |
| Logic placement | Pure function → custom hook → component, in that order. Never do I/O inside render |
| Data fetching | Isolated in hooks/query layer; components receive fetched data + loading/error state, nothing more |
| Design-system vs feature components | Primitives live in the design system; feature components compose primitives — they do not reinvent them |
| State colocation | Local first; lift only when siblings share it; globalize only when truly cross-route |

### Backend code architecture

| Question | Default answer |
|----------|----------------|
| Entry points | HTTP/CLI/queue handlers are thin — parse input, call a use case, format the response |
| Domain model vs DTO | Never serialize domain entities directly over HTTP; map to DTOs so the wire contract is independent of internal model shape |
| Data access | Behind a repository interface owned by the domain; ORM/SQL lives only in the infrastructure implementation |
| Transactions | Scoped to the use case, not the adapter; the use case opens and closes the unit of work |
| Cross-cutting concerns | Auth, logging, tracing, metrics go in middleware/decorators — not sprinkled through use cases |

### Common code-architecture mistakes

1. **Leaky domain** — HTTP error types, framework annotations, or ORM entities imported into the domain layer
2. **God module** — one module with five responsibilities because "they're all related"
3. **Hidden dependencies** — modules that reach for singletons, `process.env`, or global `fetch` instead of declaring ports
4. **Parallel hierarchies without reason** — `services/` / `controllers/` / `models/` splits that reflect no actual layering rule
5. **Public-by-default exports** — everything exported from every file, leaving no safe refactor surface
6. **Effects in render** — React components doing fetch / mutation / subscription setup in the function body
7. **Untestable seams** — hard-wired `new Client()` or `Date.now()` inside business logic, with no injection point

## Common Spec Mistakes

Avoid these in the tech spec:

1. **Underspecified error handling** — The spec lists happy paths but not what happens when external services fail, data is invalid, or operations time out. Frontend equivalent: no loading, empty, or error states.
2. **Missing capacity / usage analysis** — No estimates for data volume, request rate, concurrent users, or expected UI scale (list size, edit frequency) over 12 months.
3. **Implicit infrastructure or libraries** — Assuming Redis, Kafka, a charting library, a specific design system, etc. exists without confirming availability and cost.
4. **No migration plan** — Schema, API, route, or stored-preference changes without versioning or backward-compatibility strategy.
5. **Scope creep disguised as "Phase 1"** — A Phase 1 that is really a full-featured system. A true MVP should be shippable and valuable in isolation.
6. **Code leaked into the design** — Function bodies, full SQL DDL, or large JSON payloads instead of diagrams and tables. The spec should survive re-implementation in a different language.
7. **No diagrams** — Prose-only specs hide structure. Every non-trivial spec needs at least one architecture/component diagram and one behavior diagram (sequence or state).
