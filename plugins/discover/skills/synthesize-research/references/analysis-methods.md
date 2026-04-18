# Analysis Methods

Two methods for synthesizing qualitative research. Choose based on input type and research goal.

## Method Selection

| Input shape | Goal | Method |
|-------------|------|--------|
| Open-ended qualitative data (interview transcripts, diary entries, verbatim feedback) | Discover emergent patterns without imposing structure | Affinity mapping |
| Any qualitative data with pre-existing research questions | Map evidence to known questions while staying open to surprises | Thematic analysis |
| Mixed methods (interviews + surveys + usability) | Triangulate across data types | Thematic analysis with triangulation notes |

Default to **affinity mapping** when the user has no hypothesis. Default to **thematic analysis** when research questions already exist.

## Affinity Mapping

Bottom-up grouping: observations cluster into themes based on natural similarity, not predefined categories.

### Procedure

1. **Extract observations** — Read each source and pull out atomic observations: one fact, one quote, one data point per observation. Strip interpretation. Aim for 5-15 observations per source, depending on density.
2. **Look for clusters** — Group observations that describe the same underlying phenomenon. Name each cluster with a descriptive phrase (not a category label). A good cluster name completes the sentence "Users experience..."
3. **Merge and split** — If a cluster has 8+ observations, it may be too broad — split it. If two clusters overlap significantly, merge them. Target 3-8 themes.
4. **Write theme insights** — For each cluster, write a one-sentence insight that captures what the grouped evidence reveals. The insight is an interpretation, not a summary.

### Critical: bottom-up, not top-down

The most common synthesis failure is starting with expected categories ("onboarding", "pricing", "performance") and sorting observations into them. This confirms priors instead of revealing patterns.

Start from individual observations. Let groupings emerge. Name groups after patterns form, not before.

**Test:** If theme names match the interview guide sections, the grouping is likely top-down. Re-examine.

## Thematic Analysis

Structured coding against research questions, with room for emergent themes.

### Procedure

1. **Define codes** — Derive an initial code set from the research questions. Keep codes specific ("confusion about pricing tiers") not vague ("pricing issues"). Add 2-3 open codes: `unexpected`, `contradiction`, `strong-emotion` to catch what falls outside the frame.
2. **Code the data** — Tag each observation with one or more codes. If an observation doesn't fit any code, create a new one — this is where discoveries happen.
3. **Collapse codes into themes** — Group related codes. Each theme should answer or complicate one of the original research questions. Codes that don't fit any question become their own theme or go into Contradictions and Tensions.
4. **Write theme insights** — Same as affinity mapping: one-sentence insight per theme, grounded in the coded evidence.

## Cross-Method Triangulation

When synthesizing data from multiple research methods (e.g., interviews + survey + usability test):

- **Convergence** — Same finding from different methods strengthens confidence. Note which methods agree.
- **Complementarity** — Different methods illuminate different facets of the same theme. Note what each method uniquely contributed.
- **Divergence** — Methods contradict each other. This is valuable — capture in Contradictions and Tensions with a note on why the methods may disagree (different populations, different contexts, different question framing).

## Common Failure Modes

- **Premature convergence** — Stopping at 2-3 obvious themes when the data contains subtler patterns. After your first pass, ask: "What am I not seeing?"
- **Solution leakage** — Themes that are actually feature requests ("users want dark mode") rather than observed patterns ("users report eye strain during evening use"). Keep themes observational.
- **Homogeneous evidence** — Every quote in a theme comes from the same participant or segment. A theme needs independent corroboration.
- **Lost contradictions** — Discarding observations that don't fit. Contradictions often reveal the most interesting nuance. Always capture them.
