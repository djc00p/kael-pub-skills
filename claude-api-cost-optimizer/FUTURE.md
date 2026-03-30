# Future Enhancements (Pull Request Ideas)

## Known Issue
ClawHub registry panel shows "no required env vars" even though SKILL.md metadata correctly declares `ANTHROPIC_API_KEY` in the `env` array. This may be a registry sync lag or a parsing inconsistency on ClawHub's side. Monitor across future versions — if it persists, report to ClawHub.

---

Local workflow integrations to consider upstream:

- Add explicit cache security examples — `chmod 600`, `.gitignore` entry, TTL configuration — directly in `references/implementation.md` as a dedicated "Safe Caching Setup" section.
- Add a `scripts/clear-cache.sh` helper that removes `~/.claude_cache/` and log files safely.
- Cross-skill trigger: when cost tracking shows runaway Opus usage, suggest `agent-cost-strategy` for multi-agent routing decisions.
- Add Batch API polling pattern to `references/implementation.md` — async submission + result retrieval loop with `mmlog` on completion.
- Consider a `cost-dashboard` command that reads `costs.log` and outputs a summary table (model breakdown, cache hit rate, projected monthly).

Status: Prototype in local workspace; ready for contribution when time permits.
