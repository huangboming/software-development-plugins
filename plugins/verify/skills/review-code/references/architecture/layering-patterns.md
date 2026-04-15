# Layering & Separation of Concerns

## Table of Contents

- [Architecture Models](#architecture-models)
- [Layer Definitions & Rules](#layer-definitions--rules)
- [Ports and Adapters](#ports-and-adapters)
- [Layer Violation Detection](#layer-violation-detection)

## Architecture Models

All modern layered models share one inviolable rule: **dependencies point inward only**.

| Model | Core Principle | Dependency Direction | Innermost Layer |
|-------|---------------|---------------------|-----------------|
| N-Tier | Presentation → Business → Data | Top-down | Database |
| Clean Architecture | Concentric rings; use cases at center | Always inward | Entities (Domain) |
| Hexagonal (Ports & Adapters) | Application core + ports; adapters outside | Toward application core | Domain |
| Onion Architecture | Domain model at center | Inward | Domain Model |

### Identifying Which Model a Codebase Uses

**Clean Architecture signals:**
- Directory structure: `entities/`, `use_cases/` (or `interactors/`), `interfaces/`, `frameworks/`
- Use case classes with single `execute()` method
- Explicit boundary interfaces between layers

**Hexagonal signals:**
- Directory structure: `domain/`, `ports/`, `adapters/` (or `infrastructure/`)
- Port interfaces defined inside the application core
- Adapters implement ports and live at the outer boundary

**Onion signals:**
- Directory structure: `domain/`, `application/`, `infrastructure/`
- Similar to Clean but without explicit use case objects

**N-Tier signals:**
- Directory structure: `controllers/` (or `views/`), `services/`, `repositories/` (or `dal/`)
- Linear dependency chain: controller → service → repository → database

**No clear model:**
- Flat structure with mixed responsibilities per directory
- Business logic scattered across controllers, models, and utilities
- This itself is a finding (Big Ball of Mud tendency)

## Layer Definitions & Rules

### Domain Layer (innermost)

**Contains:** Entities, value objects, domain events, domain services, aggregates, repository interfaces.

**Allowed imports:** Nothing outside itself. Zero framework dependencies.

**Violations:**
- `import sqlalchemy` / `import mongoose` / `@Entity` annotations in domain objects
- HTTP-related imports or annotations
- Direct file I/O or network calls
- References to DTOs or API-layer types

### Application Layer

**Contains:** Use cases, application services, command/query handlers, application events, port interfaces (in hexagonal).

**Allowed imports:** Domain layer only. External contracts via interfaces defined here.

**Violations:**
- `import express` / `import flask` / HTTP framework imports
- `import pg` / direct database driver imports
- Concrete infrastructure class references (should reference port interfaces only)
- Constructing infrastructure objects directly instead of via dependency injection

### Infrastructure / Adapters (outermost)

**Contains:** HTTP controllers, repository implementations, database clients, external API clients, message queue consumers, CLI handlers.

**Allowed imports:** Application ports (to implement them); domain types (to map); any external library.

**Violations:**
- Infrastructure adapter calling another adapter directly, bypassing the application layer
- Business logic in controllers (if/else business rules instead of delegating to use cases)
- Domain entities returned directly from API endpoints without DTO transformation

## Ports and Adapters

**Port** = an interface defined inside the application core specifying what the application needs from the outside world.
- Examples: `UserRepository`, `EmailSender`, `PaymentGateway`
- Ports belong to the application layer, NOT the infrastructure layer

**Primary adapter** = translates inbound requests into application calls.
- Examples: HTTP controllers, gRPC handlers, CLI commands, message queue consumers

**Secondary adapter** = implements a port to connect to external systems.
- Examples: `PostgresUserRepository implements UserRepository`, `SendGridEmailSender implements EmailSender`

**Violation:** Any concrete infrastructure class referenced by name inside the application core (should only reference the port interface).

## Layer Violation Detection

### Import Direction Analysis

Parse imports at the file level and check dependency direction:

1. **Classify each file into its layer** based on directory structure and naming conventions
2. **For each import, verify it points inward** (or at worst, laterally within the same layer)
3. **Flag any outward-pointing import**: inner layer importing outer layer code

### Common Violation Patterns

| Violation | What It Looks Like | Why It's Bad |
|-----------|-------------------|-------------|
| **Repository bypass** | Application/domain code calling database/ORM APIs directly | Couples business logic to storage; untestable |
| **Framework bleed** | Domain entities with `@Entity`, `@Column`, `@JsonProperty` annotations | Domain polluted with infrastructure concerns |
| **Direct adapter instantiation** | `new PostgresUserRepo()` in application service | Bypasses DI; untestable; violates DIP |
| **Business logic in controllers** | HTTP handlers with if/else business rules | Logic untestable without HTTP context; scattered rules |
| **Domain objects as DTOs** | Domain entities returned directly from API endpoints | Leaks internal structure; couples API shape to domain |
| **Cross-adapter calls** | One infrastructure adapter importing another | Bypasses application orchestration; hidden coupling |
| **Shared mutable state** | Global/singleton state accessed across layers | Implicit coupling; race conditions; untestable |
