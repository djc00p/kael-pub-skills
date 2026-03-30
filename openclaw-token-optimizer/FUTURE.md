# Future Enhancements (Pull Request Ideas)

Local workflow integrations to consider upstream:

- **Lazy skill loading automation** — Extend `context_optimizer.py` to generate per-workspace `SKILLS.md` catalog with when-to-load heuristics; automatically detect which skills are relevant to a task via description matching and recommend loading only those SKILL.md files (biggest token savings after context pruning).

- **Per-prompt cost prediction model** — Build lightweight decision tree (or cached lookup) that predicts token count for a given user prompt and active context; use to warn user before expensive operations or auto-switch to cheaper model if approaching daily budget (pairs with `agent-cost-strategy`).

- **Provider health monitoring and auto-fallback** — Monitor latencies/error rates for each provider (Anthropic, OpenRouter, Together); if primary provider becomes slow/unavailable, auto-route to fallback provider and log incident to mmlog for pattern detection (integration with `problem-solving-methodology` for root cause).

- **mmlog integration for cost tracking** — When `token_tracker.py` logs budget status or `model_router.py` makes routing decisions, emit structured mmlog entries with parseable tags (`cost:daily-budget`, `routing:tier-change`) so `self-improving-agent` can analyze patterns over time.

- **Cronjob cost audit and optimization** — Scan `openclaw.json` cronjob definitions and estimate monthly cost; flag cronjobs using expensive models for routine tasks and suggest model downgrades with impact estimates; propose interval adjustments to reduce total execution count.

Status: Prototype in local workspace; ready for contribution when time permits.
