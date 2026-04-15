# Architectural Anti-Patterns

## Table of Contents

- [Structural Anti-Patterns](#structural-anti-patterns)
- [System-Level Anti-Patterns](#system-level-anti-patterns)

> **Cross-reference:** For class-level code smells that overlap with architectural concerns (Feature Envy, Shotgun Surgery, Message Chains, ISP violations), see `maintainability/code-smells.md`. This file focuses on system and module-level patterns.

## Structural Anti-Patterns

### God Class

A single class implementing large, non-cohesive blocks of functionality.

**Detection heuristics:**
- \> 20 public methods or > 15 fields
- Accesses data from > 5 foreign classes
- Low LCOM (Lack of Cohesion in Methods)
- Single file > 500 lines with multiple unrelated responsibilities

**Severity:** High — untestable; any change has wide blast radius.

### Brain Class / Brain Method

A class implementing significant system intelligence via one or more complex methods.

**Detection heuristics:**
- Method with high LOC + high cyclomatic complexity + deep nesting (> 3 levels) + many temporary variables
- Class has low cohesion despite containing complex logic
- Method > 50 lines with > 5 branching paths

**Severity:** High — masks complexity, hard to test, contains implicit invariants.

### Anemic Domain Model

Domain objects are pure data containers (getters/setters only) with business logic pushed into service layers.

**Detection heuristics:**
- Domain classes with zero non-trivial methods (only accessors/mutators)
- All business rules live in `*Service`, `*Manager`, or `*Handler` classes
- Service classes grow to 500+ lines while domain classes remain small data bags
- Domain objects are structurally identical to DTOs

**Severity:** Medium-High — business rules scatter and duplicate; violates encapsulation.

### Circular Dependencies

Two or more classes/modules mutually depend on each other.

**Detection heuristics:**
- Import graph contains cycles: `A → B → C → A`
- Initialization order problems or runtime import errors
- Unable to test a module without importing its dependents

**Severity:** High — breaks independent deployability, creates build/initialization issues.

### Dispersed / Intensive Coupling

Dispersed: method depends on many unrelated classes with shallow interaction. Intensive: method makes many calls into one or two specific classes.

**Detection heuristics:**
- Dispersed: method accesses > 7 different classes
- Intensive: method makes > 5 calls into the same foreign class

**Severity:** Medium.

## System-Level Anti-Patterns

### Big Ball of Mud

No discernible architecture — ad hoc structure, haphazard dependencies, unregulated growth.

**Detection heuristics:**
- Cannot draw component boundaries without extensive research
- Dependency graph is fully connected or near-fully connected
- Changes in one area cause unrelated breakage
- No consistent naming conventions, no identifiable layering
- No clear module boundaries; everything imports everything

**Severity:** Critical — system is effectively unmaintainable.

### Distributed Monolith

Deployed as microservices but with tight runtime coupling — services share databases, have synchronous dependency chains, cannot be deployed independently.

**Detection heuristics:**
- Services share the same database schema or tables
- Changing one service requires coordinated deployment of others
- A call to one service triggers a cascade through 5+ others
- No service can be tested in isolation
- Shared libraries with business logic (not just utilities)

**Severity:** Critical — worst of both worlds: microservice overhead with monolith coupling.

### Leaky Abstraction

An abstraction fails to hide its underlying implementation — consumers must understand the implementation to use it correctly.

**Detection heuristics:**
- Callers must write raw SQL/queries to work around ORM limitations
- Performance behavior varies for logically equivalent operations
- Error types or exceptions from underlying layers surface to callers
- Configuration of the underlying system leaks into consumer code

**Severity:** Medium-High — increases cognitive load; couples consumers to implementation.
