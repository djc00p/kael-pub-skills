# Future Enhancements (Pull Request Ideas)

Local workflow integrations to consider upstream:

- **Bidirectional relation validation and cascade rules** — Extend constraint system to enforce relationship consistency (e.g., if Task.blockers → Task_B, ensure Task_B.blocked_by → Task); support cascade delete rules (when Project deleted, archive all related Tasks). Log schema violations to mmlog for pattern detection.

- **Cross-skill state handoff via ontology** — Formalize skill contracts so `rails-ci-fixer` outputs Failure entities, `problem-solving-methodology` reads/updates ProblemDiagnosis entities, and `debug-methodology` logs RootCause entities; enables multi-skill workflows to compose via graph queries.

- **Entity lifecycle timeline and audit trail** — Add `_history` field to entities tracking all mutations (created, updated, property changes); query for "show all changes to this Task" or "who touched this commit?". Integrate with `self-improving-agent` to correlate outcome (success/rollback) with entity history.

- **GraphQL-like query interface** — Provide simplified `ontology.query("Task { id, title, blockers { title } }")` syntax (parse down to existing graph.py) for more intuitive multi-hop traversals from skills.

- **Constraint-based planning** — Extend planning-as-graph-transformation to auto-detect impossible plans (e.g., circular blockers) and suggest reordering; validate plan before execution returns confidence score based on constraint coverage.

Status: Prototype in local workspace; ready for contribution when time permits.
