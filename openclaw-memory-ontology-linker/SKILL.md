---
name: openclaw-memory-ontology-linker
description: "Automatically connects Ollama memory search results to ontology entities (Projects, Tasks, People) by creating MemoryChunk entities and linking them via 'referenced_in'. Triggers during conversation when memory search is used and ontology entities are detected. Trigger phrases: 'link memory to ontology', 'connect memory', 'attach memory snippets', 'store memory in graph'."
metadata: {"clawdbot":{"emoji":"🔗","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]},"homepage":"https://clawhub.com/djc00p/openclaw-memory-ontology-linker"}
---

# Memory‑Ontology Linker

Bridges free‑form semantic memory (Ollama) with the structured ontology graph.

## Quick Start

1. Ensure `ontology` and `openclaw-ollama-memory` skills are installed
2. Place the shared ontology at `~/.openclaw/shared-ontology` and symlink each workspace's `memory/ontology` to it
3. Add plugin config to your agent's `openclaw.json`:
   ```json
   {
     "plugins": {
       "entries": {
         "memory-ontology-linker": {
           "enabled": true,
           "config": {
             "autoLink": true,
             "minScore": 0.5,
             "maxResults": 3
           }
         }
       }
     }
   }
   ```
4. Restart gateway

## Key Concepts

- **MemoryChunk**: a snippet from semantic search, stored as an ontology entity
- **referenced_in**: relation connecting a MemoryChunk to the entity it informs
- **autoLink**: if true, the agent will batch-apply linking after memory search

## Common Usage

Manual linking (one‑off):
```bash
python3 scripts/link_memory_to_entity.py <entity_id> "snippet 1" "snippet 2"
```

View linked memories:
```bash
python3 scripts/linked_memories.py <entity_id>
```

## References
- `references/schema-additions.md` — required MemoryChunk type and referenced_in relation
- `references/auto-linking-design.md` — how auto‑linking works and configuration details

## Common Mistakes to Avoid
- Forgetting to symlink workspace `memory/ontology` to the shared location
- Not adding the plugin entry to `openclaw.json`
- Setting `minScore` too high (nothing links) or too low (spam)
- Expecting instant linking in long conversations — it runs after memory search completes