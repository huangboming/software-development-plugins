# Item Quality Guide

Standards for backlog item descriptions, source attributions, and granularity.

## Writing Good Descriptions

Each backlog item needs a description specific enough to score. One sentence, focused on *what* and *why* — not *how*.

| Weak | Strong | Why It's Better |
|------|--------|-----------------|
| "Improve performance" | "Reduce dashboard load time — currently 8s, target <2s — top customer complaint in Q4" | Names the specific problem, quantifies current state and target, cites evidence |
| "Search feature" | "Full-text search across documents — users currently browse manually, losing ~10 min/session" | Specifies scope, names the user pain, quantifies impact |
| "Fix bugs" | "Fix CSV export truncating rows beyond 10,000 — affects enterprise customers with large datasets" | Names the exact bug, identifies affected segment |

## Writing Good Source Attributions

Source should be specific enough to trace back and assess credibility.

| Weak | Strong |
|------|--------|
| "Feedback" | "Customer feedback — 12 requests via support in Q1 2026" |
| "Stakeholder" | "VP Sales request — tied to Enterprise deal pipeline (3 accounts)" |
| "PRD" | "Extracted from .product/prd/reporting/v2.md, user story #3" |

## Granularity Check

Items should be at the **feature or capability level** — scorable independently, deliverable in one cycle.

| Too Big (Epic) | Right Level (Feature) | Too Small (Task) |
|---|---|---|
| "Rebuild the reporting system" | "Add CSV export to reports" | "Write the CSV serializer" |
| "Improve user onboarding" | "Interactive product tour for new users" | "Create tooltip component" |
| "Mobile support" | "Responsive layout for dashboard views" | "Fix padding on mobile nav" |

If too big, split into features before adding. If too small, it belongs in a sprint board, not the product backlog.

If an item is too vague to score, ask: "Which part of the product? What specific problem does this solve?" Apply the description standards in the first table above to decide whether it clears the bar.
