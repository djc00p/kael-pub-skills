# Future Enhancements (Pull Request Ideas)

Local workflow integrations to consider upstream:

- **Interactive bisect with step-by-step logging** — When running `git bisect run`, emit detailed progress logs to `memory/episodic/YYYY-MM-DD.md` with commit metadata (author, timestamp, message) so debugging patterns can be correlated with release notes or deployment history (pairs with `self-improving-agent` for historical analysis).

- **Worktree conflict detection and merge strategy suggestion** — Before creating a worktree from a branch with recent merges, check for potential conflicts via `git diff --stat` and suggest merge strategy or rebase order to minimize headaches later.

- **Subtree update automation with changelog generation** — After `git subtree pull`, parse commit messages from upstream and generate a `SUBTREE_UPDATES.md` with summary of what changed; suggest which files in main repo might be affected.

- **Reflog recovery with safety confirmation** — When recovering lost commits via reflog, automatically propose a temporary branch (e.g., `recovery/HEAD@{N}`) for user to inspect before force-pushing; integrate safeguard messages via `ontology` to track recovery actions.

- **Cherry-pick conflict automation for cross-repo workflows** — When cherry-picking from one repo to another with namespace/path differences, auto-detect renames and suggest `--rename-strategy` or equivalent regex rewrites; log conflict resolution patterns to mmlog for future reference.

Status: Prototype in local workspace; ready for contribution when time permits.
