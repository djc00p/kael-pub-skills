---
name: openclaw-memory-ontology-linker
description: "Manually links free-form memory snippets to ontology entities (Projects, Tasks, People) by creating MemoryChunk entities connected via 'referenced_in'. Use when you find a memory snippet worth attaching to a specific project or task, or during memory review to surface context. Trigger phrases: 'link memory to ontology', 'connect memory', 'attach memory snippets', 'what memory is linked to', 'show memory for project'."
metadata: {"clawdbot":{"emoji":"🔗","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

# Memory‑Ontology Linker

Links free-form memory snippets to structured ontology entities. Useful during memory review to attach relevant episodic/semantic context to active projects and tasks.

## Quick Start

**Link a memory snippet to an entity:**
```bash
python3 ~/.openclaw/workspace/skills/openclaw-memory-ontology-linker/scripts/link_memory_to_entity.py <entity_id> "snippet"
```

**View all memory linked to an entity:**
```bash
python3 ~/.openclaw/workspace/skills/openclaw-memory-ontology-linker/scripts/linked_memories.py <entity_id>
```

**Example:**
```bash
python3 ~/.openclaw/workspace/skills/openclaw-memory-ontology-linker/scripts/link_memory_to_entity.py proj_mypridri \
  "Ratings PR #47 ready to merge — 860 tests passing"
```

## Key Concepts

- **MemoryChunk**: a snippet stored as an ontology entity, linked to a project/task
- **referenced_in**: relation connecting a MemoryChunk to the entity it informs
- **Manual workflow**: run the scripts intentionally when you find something worth persisting — not automatic

## Common Usage

**During memory review (heartbeat):**
1. Read recent episodic files
2. Find snippets relevant to active projects
3. Run `link_memory_to_entity.py` to attach them
4. Run `linked_memories.py` to verify and surface context next session

**Check what's linked to an active project:**
```bash
python3 ~/.openclaw/workspace/skills/openclaw-memory-ontology-linker/scripts/linked_memories.py proj_mypridri
```

## When to Use

- You find a key insight in episodic memory that should be attached to a project
- You want to surface past decisions when returning to a task
- Memory review turns up something worth preserving beyond the flat `.md` file

## References
- `references/schema-additions.md` — MemoryChunk type and referenced_in relation definitions
- `references/auto-linking-design.md` — workflow design notes

## Tracking
This skill is on trial. Usage is tracked via `task_memory-ontology-linker-trial` in the ontology.
Log each time the scripts produce useful output: `ont create --type Learning --id learn_mol-$(date +%s) --props '{"name":"memory-linker-used","status":"active","goal":"<what was linked and whether it was useful>"}'`
