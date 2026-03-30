# Future Enhancements (Pull Request Ideas)

Local workflow integrations to consider upstream:

- **Prompt performance measurement and A/B testing** — Create minimal test harnesses that run the same task against original vs. refined prompts; measure consistency (variance in outputs), latency, and token efficiency; log results to mmlog with tags so patterns compound across optimizations (pairs with `self-improving-agent`).

- **Anti-pattern detection across workspace skills** — Scan all SKILL.md files and detect common issues (ambiguous triggers, missing context requirements, over-broad descriptions); auto-suggest rewrites that improve clarity and trigger accuracy; integrate with skill-creator workflow.

- **Prompt caching optimization for repeated context** — Detect when same system prompts or instructions are used repeatedly; suggest stable "evergreen" prompt sections that can be cached (Anthropic prompt caching) vs. dynamic sections; estimate token savings (pairs with `token-optimizer`).

- **Cross-skill instruction coherence checking** — Validate that instructions across different SKILL.md files (e.g., debug-methodology, problem-solving-methodology) don't contradict each other; suggest harmonization where philosophies align; log conflicts to mmlog for user awareness.

- **Dynamic instruction injection based on task** — Create lightweight decision tree that selects relevant prompt sections based on detected task type (e.g., "this is a Rails issue" → inject rails-tdd-standards context; "this is a cost question" → inject agent-cost-strategy context); reduces context bloat while maintaining relevance.

Status: Prototype in local workspace; ready for contribution when time permits.
