# Future Enhancements (Pull Request Ideas)

Local workflow integrations to consider upstream:

- **Diff-based template auto-fill** — Parse `git diff HEAD..main` and auto-populate Description of Changes section with file-level summaries (new files, deletions, major edits); then user reviews and refines rather than filling from scratch.

- **Cross-PR impact detection** — Scan PR branches against open PRs in the same repo; detect if changes overlap or create merge conflicts; suggest coordination mentions or review ordering (pairs with `ontology` for tracking PR dependency graphs).

- **Test coverage estimation from diff** — Analyze which files changed and cross-reference with spec files; estimate % of changes covered by tests and warn if coverage drops below threshold; integrate with `rails-tdd-standards` for test quality feedback.

- **Automated changelog entry generation** — Based on PR type (feature/fix/breaking) and description, generate a semantic changelog entry (CHANGELOG.md format) and include in PR as a suggested commit; pairs with release automation workflows.

- **Template A/B testing and quality metrics** — Log each filled template to mmlog with tags (clear/unclear sections, test coverage, impact assessment completeness); over time, suggest template improvements based on which sections correlate with fast reviews vs. slow reviews.

Status: Prototype in local workspace; ready for contribution when time permits.
