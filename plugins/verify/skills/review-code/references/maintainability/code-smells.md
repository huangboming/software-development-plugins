# Code Smells, Design Anti-Patterns & SOLID Violations

Detection catalog for clean code review. Each entry: pattern name, detection heuristic, severity, risk.

## Table of Contents

- [Bloaters](#bloaters)
- [Object-Orientation Abusers](#object-orientation-abusers)
- [Change Preventers](#change-preventers)
- [Couplers](#couplers)
- [SOLID Violations](#solid-violations)
- [Naming & Readability](#naming--readability)

---

## Bloaters

Code that has grown excessively, making it hard to work with.

### Long Method / Function

- **Detect**: Function body > 30-40 LOC; multiple levels of abstraction; need to scroll to read
- **Severity**: High
- **Risk**: Hard to understand, test, and reuse. Often masks multiple responsibilities

### Large Class / Module

- **Detect**: Class > 300 LOC; > 10 public methods; > 7 instance variables; class name includes "Manager", "Processor", "Handler", "Utils"
- **Severity**: High
- **Risk**: Violates SRP, attracts unrelated changes, resists testing

### Long Parameter List

- **Detect**: Function takes > 4 parameters; boolean "flag" parameters; parameters that always travel together
- **Severity**: Medium
- **Risk**: Hard to call correctly, signals the function does too much or needs a parameter object

### Data Clumps

- **Detect**: Same 3+ variables appear together repeatedly (e.g., `start_date, end_date, timezone`); function signatures share parameter groups
- **Severity**: Medium
- **Risk**: Missing abstraction; changes to the group require shotgun surgery

### Primitive Obsession

- **Detect**: Strings used for structured data (emails, phone numbers, currencies, IDs); integers used as enums or status codes without type safety; raw dicts where a data class fits
- **Severity**: Medium
- **Risk**: Validation scattered everywhere; no domain semantics; easy to mix up values of the same primitive type

---

## Object-Orientation Abusers

Misuse of OOP constructs.

### Feature Envy

- **Detect**: Method accesses another object's data more than its own; chains like `order.customer.address.city`; method would be simpler if moved to the class it envies
- **Severity**: Medium
- **Risk**: Logic in the wrong place; changes to the envied class ripple here

### Refused Bequest

- **Detect**: Subclass overrides parent methods to no-op or raise `NotImplementedError`; subclass uses < 50% of inherited interface
- **Severity**: Medium
- **Risk**: Inheritance hierarchy is wrong; violates LSP

### Temporary Field

- **Detect**: Instance variable only set/used in some code paths; fields initialized to `None` and checked with `if self.x is not None` throughout
- **Severity**: Low–Medium
- **Risk**: Unclear object state; partial initialization bugs

### Data Class (Anemic Domain Model)

- **Detect**: Class has only getters/setters/properties with no behavior; all business logic lives in separate "service" classes that manipulate data classes
- **Severity**: Medium
- **Risk**: Behavior and data separated; logic scattered across services; hard to enforce invariants
- **See also**: `architecture/anti-patterns.md` for system-level implications of the Anemic Domain Model pattern

---

## Change Preventers

Patterns that make changes expensive.

### Divergent Change

- **Detect**: One class is modified for many different reasons; git history shows the same file changed in unrelated PRs
- **Severity**: High
- **Risk**: SRP violation; merge conflicts; high blast radius per change

### Shotgun Surgery

- **Detect**: A single logical change requires touching many files/classes; adding a new field requires updating 5+ places
- **Severity**: High
- **Risk**: Easy to miss a spot; changes are error-prone and slow

### Parallel Inheritance Hierarchies

- **Detect**: Creating a subclass of one class always requires creating a subclass of another; prefixes match across hierarchies
- **Severity**: Medium
- **Risk**: Multiplied maintenance; easy to get hierarchies out of sync

---

## Couplers

Excessive coupling between classes.

### Inappropriate Intimacy

- **Detect**: Class accesses private/internal members of another; two classes frequently modified together; bidirectional references
- **Severity**: High
- **Risk**: Tight coupling; changes cascade; hard to modify independently

### Message Chains

- **Detect**: `a.getB().getC().getD().doSomething()`; > 2 dots in a chain (Law of Demeter violations)
- **Severity**: Medium
- **Risk**: Fragile to structural changes; client knows too much about the object graph

### Middle Man

- **Detect**: Class delegates > 50% of its methods to another object without adding value; wrapper that just forwards calls
- **Severity**: Low–Medium
- **Risk**: Unnecessary indirection; adds complexity without benefit

### Speculative Generality

- **Detect**: Abstract classes/interfaces with only one implementor; unused parameters "for future use"; generic frameworks wrapping simple operations; type parameters that are always the same concrete type
- **Severity**: Medium
- **Risk**: Complexity without benefit; the anticipated future use rarely arrives

---

## SOLID Violations

### Single Responsibility Principle (SRP)

- **Detect**: Class name includes "And" or is vague ("Manager", "Handler", "Processor", "Service" without qualifier); class has methods that serve unrelated stakeholders; constructor injects unrelated dependencies (e.g., both `EmailClient` and `DatabaseConnection`); class changes for unrelated reasons in git history
- **Severity**: High
- **Risk**: High change frequency; hard to test; merge conflicts

### Open/Closed Principle (OCP)

- **Detect**: Adding a new variant requires modifying existing `if/elif/else` or `switch` chains; enum-driven dispatch where adding a value means editing multiple functions; direct modification of working code to add features
- **Severity**: Medium
- **Risk**: Regression risk; existing tests may break; growing complexity in branching

### Liskov Substitution Principle (LSP)

- **Detect**: Subclass overrides method to raise `NotImplementedError` or silently do nothing; client code checks `isinstance` before calling methods; subclass changes method semantics (e.g., different return type meaning)
- **Severity**: High
- **Risk**: Runtime errors; client code can't safely use the abstraction

### Interface Segregation Principle (ISP)

- **Detect**: Interface/protocol with > 8 methods; implementors leave methods as no-ops or raise exceptions; clients use < 50% of an interface's methods
- **Severity**: Medium
- **Risk**: Forced dependencies; implementors burdened with irrelevant methods

### Dependency Inversion Principle (DIP)

- **Detect**: High-level modules import concrete low-level modules directly; business logic instantiates infrastructure (e.g., `db = PostgresConnection()` inside domain code); no dependency injection; tests require real infrastructure
- **Severity**: High
- **Risk**: Untestable; infrastructure changes ripple through business logic

---

## Naming & Readability

### Misleading Names

- **Detect**: Function name doesn't match its side effects (e.g., `getUser` that also modifies state); boolean variable without `is_/has_/can_/should_` prefix; name says "list" but type is dict
- **Severity**: Medium
- **Risk**: Callers make wrong assumptions; bugs from misunderstanding

### Inconsistent Vocabulary

- **Detect**: Same concept uses different words across codebase (e.g., `user`/`account`/`member` for the same entity; `fetch`/`get`/`retrieve`/`load` interchangeably)
- **Severity**: Medium
- **Risk**: Cognitive overhead; hard to search; domain model ambiguity

### Abbreviations & Cryptic Names

- **Detect**: Single-letter variables outside tiny loops; unexplained abbreviations (`mgr`, `ctx`, `proc`); acronyms without context
- **Severity**: Low–Medium
- **Risk**: Slows comprehension; especially painful for new team members

### Boolean Parameter Blindness

- **Detect**: `process(data, True, False)`; boolean params that are unclear at call site; function behavior forks on a boolean flag
- **Severity**: Medium
- **Risk**: Caller doesn't know what `True` means; function likely has two responsibilities

### Magic Numbers / Strings

- **Detect**: Literal values in logic without named constants; `if status == 3`; `timeout = 30`; string comparisons against unlabeled values
- **Severity**: Low–Medium
- **Risk**: Meaning unclear; changes require finding all occurrences

### Deep Nesting

- **Detect**: > 3 levels of indentation; nested `if` inside `for` inside `try` inside `if`; arrow-shaped code
- **Severity**: Medium
- **Risk**: Hard to follow control flow; high cognitive load; error-prone

### Cognitive Complexity

- **Detect**: Function requires mental state tracking of > 3-4 variables simultaneously; mixed levels of abstraction in one function (high-level orchestration mixed with low-level string parsing)
- **Severity**: Medium
- **Risk**: Bugs hide in complexity; review and maintenance are slow
