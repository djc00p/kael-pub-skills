# Future Enhancements (Pull Request Ideas)

## Vetter Note (2026-03-29)
ClawHub vetter classifies this skill as "high-risk" due to inherent RCE (running tests) and repo write access. No malice found — risks are structural to the skill's purpose. If we ever do a v2, consider adding a prominent risk disclosure notice at the top of SKILL.md and making `references/security.md` more prominent. Not urgent.

---

Local workflow integrations to consider upstream:

- **Automated RuboCop learning database** — Parse RuboCop offenses across multiple PRs and store patterns in `memory/semantic/rubocop-patterns.md` (e.g., "test files often have N > 15 expectations, use shared examples instead"); use patterns to suggest preventive rewrites before running auto-fix (pairs with `rails-tdd-standards`).

- **Factory error pattern matching and auto-recovery** — Build decision tree for common FactoryBot failures (missing role trait, wrong association key, join table without primary key); when detected in CI logs, auto-suggest and apply correct factory syntax from `rails-tdd-standards` patterns without human intervention.

- **Dependency conflict resolution automation** — When CI fails on bundle install or yarn lock issues, auto-attempt `bundle update` on a minimal subset of dependencies (those touched in PR) and re-test; log successful resolution patterns to mmlog for future reference (integration with `problem-solving-methodology`).

- **Test flakiness detection and reporting** — Track which specs fail intermittently across CI runs; highlight flaky tests in PR review comments with failure rate estimate; suggest determinism fixes (e.g., add explicit ordering, reduce timing dependencies) via `rails-tdd-standards` guidance.

- **mmlog integration for CI metrics** — Emit structured logs for each CI fix attempt (`mmlog --tags ci:fixed,test-type:rspec,attempts:2,reason:missing-trait`) so patterns can be analyzed over time; surface top failure categories to improve preventive linting (pairs with `self-improving-agent`).

Status: Prototype in local workspace; ready for contribution when time permits.
