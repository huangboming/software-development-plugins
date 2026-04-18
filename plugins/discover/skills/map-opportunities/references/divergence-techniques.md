# Divergence Techniques

Prompts and tactics for generating multiple branches at each level of the opportunity solution tree. Read when a sub-outcome or solution branch feels thin, or when the user is converging too early.

## For Generating Sub-Outcomes

The root outcome is broad. Split it along one of these cuts:

### Journey slicing

What does the user experience before, during, and after the outcome is achieved? Each stage becomes a candidate sub-outcome.

- Before: what signals that the outcome is needed?
- During: what friction blocks the outcome?
- After: what confirms the outcome held?

### Context slicing

Who experiences this outcome differently based on situation?

- First-time vs. returning
- Solo vs. team
- Manual vs. automated workflow
- High-trust vs. low-trust context (new account, regulated industry)

### Job-to-be-done decomposition

What specific jobs does the user hire a solution to do? Each job is a sub-outcome candidate. Mine the jobs from: synthesized research themes, signal tags, support ticket clusters, sales-call transcripts.

### Unmet-need prompt

Ask: "What specifically is the user missing today?" Each missing piece is a candidate sub-outcome. This is Teresa Torres' canonical cut and the one most grounded in research.

## For Generating Solutions

### HMW ("How might we...") reframing

Convert each sub-outcome into a how-might-we question, then answer it several times. Example:

> Sub-outcome: A new admin knows which inherited settings still apply to their team.
>
> HMW help a new admin distinguish inherited settings that still apply from ones that don't?
>
> Answers:
> - annotate each setting with provenance and last-edited metadata
> - show a diff view against a sane-default template
> - offer a one-click "safe mode" that resets non-essential settings
> - ask for a 30-second context intake and filter settings by stated team size / industry

One HMW per sub-outcome usually surfaces 4–6 solution candidates.

### Analogous domains

Ask how another industry or product category handles a similar pattern. Useful when the team's own domain is producing same-shaped ideas.

- How does a pilot onboard into a new cockpit with unfamiliar config?
- How does a doctor inherit a patient with a complex medication list?
- How does a chef inherit a kitchen and decide what to change?

Analogies surface mechanics that do not already exist in the current domain.

### Constraint removal

Remove one constraint and see what becomes possible:

- If build time were zero, what would you ship?
- If you had infinite engineering, what mechanic would you choose?
- If you had only one hour to ship, what is the smallest mechanic that works?
- If users trusted you completely, what could you do on their behalf?

Each answer is a candidate solution — including the extreme ones, which often anchor a useful middle-ground option.

### 10x prompts

- What would a 10x simpler solution look like? Usually exposes an assumption in the current framing.
- What would a 10x more capable solution look like? Usually reveals the middle-ground solution was timid.

### Inversion

Ask: "What would make this problem worse?" Then invert each aggravator into a solution. This produces solutions that actively remove friction rather than adding features on top of it.

### Reach-branch prompts

Every sub-outcome deserves at least one reach. Prompts:

- What would a competitor known for being unconventional (e.g., Muji, Linear, Notion, Arc) do here?
- What would an entirely automated solution look like? An entirely manual one?
- What would a human concierge do instead of software?
- What if this were a physical product?
- What if the user had to pay per use instead of subscribing?

A reach is not for selection — its job is to stretch the evaluation space. It often reveals that a middle-ground branch was underexplored.

## Knowing When to Stop

Stop diverging at a node when any of these is true:

- New branches repeat the mechanics of earlier branches with different labels.
- New branches fall outside the sub-outcome they are meant to serve — they belong to a different branch or a different tree.
- The user surfaces evaluation criteria unprompted ("we can't build that because..."). That is the signal to move to convergence in step 4 of the skill.

See `tree-template.md` for productive branch-count ranges per node — that file is canonical.
