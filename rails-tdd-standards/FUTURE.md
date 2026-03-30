# Future Enhancements (Pull Request Ideas)

Local workflow integrations to consider upstream:

- **Factory spec linting and validation** — Create analyzer that parses factory definitions and detects issues (missing required associations, role traits not matching model validations, wrong association keys); emit as pre-commit hook or CI check to catch factory bugs before tests run (pairs with `rails-ci-fixer` for CI-level detection).

- **Single-expectation enforcement via AST** — Parse spec files and warn when `it` blocks contain multiple expect() calls; auto-suggest refactoring into multiple specs grouped by behavior; integrate into spec-writing workflow as a linter (pairs with `rails-ci-fixer` for CI feedback).

- **Test coverage gap analysis** — Cross-reference factories and test specs to detect untested associations/validations; generate report suggesting specs to add; tie to PRs via `github-pr-writer` integration to suggest test additions in PR template.

- **Shared example library recommendation engine** — Analyze specs across the workspace; detect repeated patterns (e.g., "validates presence of email"), and suggest extracting to RSpec `shared_examples`; log patterns to mmlog so common test patterns can be shared across projects (pairs with `self-improving-agent`).

- **Debugging helper for test failures** — When a test fails with factory or association errors, auto-suggest common fixes (missing trait, wrong key, RecordInvalid diagnosis) and link to relevant sections in this skill; reduce time spent debugging test infrastructure (pairs with `debug-methodology`).

Status: Prototype in local workspace; ready for contribution when time permits.
