# Cache Optimization Patterns

Prompt caching saves cost by reusing previously processed context. Most providers charge ~10% of normal input price for cache reads — up to 90% savings on repeated context.

## What Caches Well

- System prompts (static instructions, personas, rules)
- Large documents loaded repeatedly (codebases, docs, schemas)
- Repeated tool definitions
- Shared base prompts across multiple sub-agents

## What Doesn't Cache

- Dynamic content that changes every request (timestamps, random values)
- Very short prompts (not worth caching)
- One-off requests with unique context

## Key Patterns

### Keep system prompts stable
Put static instructions at the top of your system prompt. They get cached after the first request and reused on every call — avoid injecting dynamic values (timestamps, session IDs) into the system prompt.

```
[CACHED] System prompt with rules, persona, tools
[NOT CACHED] Current user message
```

### Large document analysis
Load the document once, then ask questions in follow-up turns.

```
Turn 1: "Here is the codebase: [large content]" → cache miss, full price
Turn 2: "What does the auth module do?"         → cache hit, ~90% cheaper
Turn 3: "Find all API endpoints"                → cache hit, ~90% cheaper
```

### Sub-agent prompts
When spawning many sub-agents with the same base prompt, put shared context first — it gets cached across all of them.

```
[SHARED — gets cached across all agents]
You are a test fixer. Rules: never comment out tests...

[UNIQUE per agent]
Fix this specific failure: <paste failure>
```

### Order matters
Always put static content before dynamic content. Providers cache from the beginning of the prompt — anything after a dynamic section won't be cached.

## Provider Cache Notes

| Provider | Cache Behavior |
|----------|---------------|
| Anthropic | Automatic on repeated prefixes; ~90% discount on cache reads |
| OpenAI | Automatic on prompts >1024 tokens; ~50% discount on cache reads |
| Google | Context caching via API; charged per cache storage + reads |

Check your provider's docs for the exact cache TTL and minimum token threshold.

## Quick Wins

1. **Stable system prompts** — biggest single win
2. **Order: static first, dynamic last**
3. **Batch similar sub-agents** — same base prompt = shared cache
4. **Monitor cache hit rate** — most providers expose this in dashboards or API responses
