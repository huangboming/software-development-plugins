# Coupling & Cohesion Metrics

## Table of Contents

- [Component Coupling Metrics](#component-coupling-metrics)
- [Danger Zones](#danger-zones)
- [Component Coupling Principles](#component-coupling-principles)
- [Dependency Graph Analysis](#dependency-graph-analysis)
- [Practical Thresholds](#practical-thresholds)

## Component Coupling Metrics

Robert Martin's metrics computed at the package/module/component level:

| Metric | Formula | Range | Meaning |
|--------|---------|-------|---------|
| **Ca** (Afferent Coupling) | External components depending on this one | 0–∞ | Incoming deps; indicates responsibility |
| **Ce** (Efferent Coupling) | External components this one depends on | 0–∞ | Outgoing deps; indicates dependence |
| **I** (Instability) | `Ce / (Ca + Ce)` | 0–1 | 0 = maximally stable, 1 = maximally unstable |
| **A** (Abstractness) | `Abstract types / Total types` | 0–1 | 0 = fully concrete, 1 = fully abstract |
| **D** (Distance from Main Sequence) | `\|A + I - 1\|` | 0–1 | 0 = optimal balance, 1 = worst |

### Healthy Thresholds

- **D < 0.1**: Excellent
- **D 0.1–0.3**: Acceptable
- **D > 0.3**: Warning — component is in a danger zone
- **Ce > 20**: Instability warning — too many outgoing dependencies

## Danger Zones

### Zone of Pain (A ≈ 0, I ≈ 0)

Completely concrete and maximally stable. Many incoming dependents but no abstractions. Any change breaks everything depending on it.

**Example:** A utility library with no interfaces — widely depended upon but impossible to extend without modification.

**Fix:** Introduce abstractions (interfaces/protocols) to allow extension.

### Zone of Uselessness (A ≈ 1, I ≈ 1)

Completely abstract and maximally unstable. No concrete implementations and nothing depends on it.

**Example:** An interface package with no implementations and no consumers.

**Fix:** Remove dead abstractions or implement them.

## Component Coupling Principles

### Acyclic Dependencies Principle (ADP)

**Rule:** The dependency graph of components must have no cycles.

**Detection:**
1. Build the import/dependency graph at the module/package level
2. Find strongly connected components (Tarjan's algorithm)
3. Any SCC with size > 1 is a cycle violation
4. Report the cycle path: `A → B → C → A`

**Consequence of violation:** Components in the cycle cannot be independently developed, tested, or deployed. A change in any component potentially requires changes in every other.

**Resolution strategies:**
- Dependency Inversion: introduce an interface in the depended-upon component
- Extract shared dependency into a new component
- Merge tightly coupled components

### Stable Dependencies Principle (SDP)

**Rule:** Depend only on components more stable than yourself (`I(A) >= I(B)` for edge A → B).

**Detection:**
- For each dependency edge A → B, compute I(A) and I(B)
- Flag any edge where `I(A) < I(B)` — stable component depending on a volatile one

**Consequence:** Stable components become hostage to volatile ones; cannot change without risk.

### Stable Abstractions Principle (SAP)

**Rule:** A component should be as abstract as it is stable (`A + I ≈ 1`).

**Detection:**
- Compute D for each component
- Flag components with D > 0.3
- Categorize into Zone of Pain vs Zone of Uselessness

## Dependency Graph Analysis

### Healthy vs Unhealthy Graphs

| Characteristic | Healthy | Unhealthy |
|---------------|---------|-----------|
| Structure | DAG (no cycles) | Contains cycles |
| Direction | Flows toward stable/abstract | Volatile deps from stable code |
| Layer crossing | Inward only | Outward (inner → outer) |
| Fan-out per component | < 10–15 direct deps | Hub components with 30+ deps |
| Zone of Pain | None | Core components with D > 0.3 |

### Hub Nodes

A component with both high Ca and high Ce is a **Global Hub** — it is both widely depended upon and depends on many others. Any change is both risky (high Ca) and likely to be triggered by external changes (high Ce).

**Detection:** Components where both Ca > 5 and Ce > 10.

## Practical Thresholds

| Signal | Threshold | Implication |
|--------|-----------|-------------|
| File-level direct dependencies | > 10 imports | File coupling warning |
| Method calling distinct classes | > 7 classes | Dispersed coupling |
| Component efferent coupling | Ce > 20 | High instability risk |
| Cycle in dependency graph | SCC size > 1 | ADP violation |
| SDP violation | I(A) < I(B) for A → B | Stable depending on volatile |
| Distance from Main Sequence | D > 0.3 | Zone of Pain or Uselessness |
| Third-party coupling spread | Same library imported in > 5 modules | Frameworkitis risk |
