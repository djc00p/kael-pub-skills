# Auto‑Linking Design

This document describes how the `memory-ontology-linker` skill operates when `autoLink` is enabled.

## Trigger Conditions

The agent attempts auto‑linking when:
- Memory search is invoked (by the agent or via tool)
- At least one result meets `minScore` threshold
- The conversation contains detectable ontology entities

## Entity Detection

Current method: `trigger-phrases`
- Looks for explicit mentions like "Project X", "Task Y", "Work item Z"
- Extracts entity IDs by querying the ontology for entities with matching `name` (case‑insensitive)
- May be extended to include named entity recognition in future versions

## Workflow

1. Memory search returns snippets: `[ {content, score, source}, ... ]`
2. Filter snippets to those with `score >= config.minScore`
3. Limit to `config.maxResults` highest‑scoring snippets
4. For each snippet:
   - Determine candidate entity IDs (from entity detection step)
   - For each candidate, create a `MemoryChunk` entity with:
     - `id`: `mc_<timestamp>_<index>`
     - `type`: `MemoryChunk`
     - `properties.content`: snippet text
     - `properties.source`: memory source (e.g., "episodic", "semantic")
     - `properties.score`: similarity score
     - `properties.timestamp`: ISO timestamp
   - Create relation: `{"op":"relate","from":chunk_id,"rel":"referenced_in","to":entity_id}`
5. Append all ops to the shared graph in order

## Configuration Notes

- `maxResults` caps the number of *snippets*, not the number of `MemoryChunk` entities (each snippet produces one chunk per candidate entity). Keep `maxResults` modest to avoid graph spam.
- If multiple candidate entities are found for a snippet, the chunk will be linked to all of them (via multiple `referenced_in` edges). Consider refining entity detection to narrow candidates.
- Future options may include:
  - `deduplicateChunks`: avoid creating identical chunks for same snippet
  - `progressLogging`: log auto‑link runs to workspace `memory/episodic/`

## Failure Modes

- **No candidate entities**: The chunk is still created but remains unlinked; this is okay—manual linking can attach it later.
- **Validation errors**: If ontology schema rejects `MemoryChunk` or `referenced_in`, check `schema.yaml` and add definitions from `schema-additions.md`.
- **File write errors**: Ensure the shared ontology directory is writable and `graph.jsonl` exists.
