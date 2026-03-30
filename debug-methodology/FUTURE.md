# Future Enhancements (Pull Request Ideas)

Local workflow integrations to consider upstream:

- **Automated patch-chain detection with reflog integration** — When 2 fix attempts fail in sequence, automatically trigger `git reflog` inspection and suggest revert points; log the failed attempts to mmlog with patch-chain detection tag for learning (integration with `git-workflows` for recovery patterns).

- **Root cause gate enforcement in skill contracts** — Define optional `debug_contract` in SKILL.md frontmatter (e.g., `must_diagnose: true` for deployment skills); agent checks if root cause was confirmed before applying fixes to production-adjacent changes.

- **Workaround detection via AST/regex patterns** — Scan proposed fixes for common workaround patterns (e.g., "use different model instead of fixing slow query", "catch exception instead of validating input"); flag for user confirmation before applying.

- **Post-fix regression test automation** — Generate minimal regression test suite after fix is applied (e.g., "you fixed the auth timeout, write test that timeout no longer occurs"); integrate with `rails-tdd-standards` for Rails projects.

- **Environment forensics logging** — When encountering environment-specific bugs, auto-capture system state (versions, venv status, config files) to `memory/episodic/debug-forensics.md` so patterns across similar bugs can be detected later by `self-improving-agent`.

Status: Prototype in local workspace; ready for contribution when time permits.
