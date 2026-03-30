# Future Enhancements (Pull Request Ideas)

Local workflow integrations to consider upstream:

- **Continuous baseline tracking and regression alerts** — Automatically snapshot `/context json` metrics on each new session; track cost/context trends over time in `memory/semantic/optimization-baseline.md`; alert if token usage spikes >20% vs. rolling 7-day average (pairs with `agent-cost-strategy` for corrective routing).

- **Bootstrap bloat deep-dive automation** — Parse all always-injected files (SOUL.md, AGENTS.md, MEMORY.md, skills/) and generate per-file token attribution report with "lazy-load candidates" (e.g., "MEMORY.md contributes 8K tokens but is only used in direct chats, not group channels"); suggest migration path with rollback plan.

- **Skill ambient visibility audit** — Analyze workspace skills list vs. actual skill usage in recent transcripts; flag "always-visible" specialist skills (e.g., rails-tdd-standards, tailwind-rails) that could move to on-demand subagent spawning; estimate context savings.

- **Model routing performance evaluation** — After applying model-tier recommendations from this skill, auto-measure quality/latency across tiers on sample tasks; generate report showing whether cost savings trade-off is acceptable for this workspace (integration with `self-improving-agent` for learning loop).

- **Optimization rollback simulation** — Before approving changes, simulate rollback by generating comparison before/after context metrics (token counts, skill list, bootstrap size); allow user to A/B test on parallel isolated sessions before committing.

Status: Prototype in local workspace; ready for contribution when time permits.
