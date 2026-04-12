---
name: memory-ontology-linker
description: "At session reset or /new, scans the session transcript for memory_search results, detects ontology entity mentions, and links matching memory chunks to entities in the shared ontology graph."
metadata:
  {"openclaw":{"emoji":"🔗","events":["command:new","command:reset"],"requires":{"bins":["python3"]},"os":["darwin","linux"]}}
---

# Memory-Ontology Linker Hook

Automatically bridges semantic memory search results to the shared ontology graph.

## What It Does

When you issue `/new` or `/reset`:

1. Scans the previous session transcript for `memory_search` tool results
2. Extracts memory snippets from those results
3. Loads all entities from `~/.openclaw/shared-ontology/graph.jsonl`
4. Matches snippet content against entity names/properties
5. Creates `MemoryChunk` entities and `referenced_in` relations for matches

## Requirements

- Python 3 on PATH
- `~/.openclaw/shared-ontology/graph.jsonl` must exist
- Ontology entities must have a `name` property to match against

## Configuration

No configuration needed. Runs automatically on `/new` and `/reset`.
