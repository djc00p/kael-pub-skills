#!/usr/bin/env python3
"""
Link semantic memory chunks to an ontology entity.

This demo script accepts an entity ID and a list of memory snippets,
then creates MemoryChunk entities and links them to the given entity
using the 'referenced_in' relation.

Usage:
  python3 scripts/link_memory_to_entity.py <entity_id> "Snippet 1" "Snippet 2" ...
Example:
  python3 scripts/link_memory_to_entity.py proj_openclaw \
    "Discussed dual-agent setup" \
    "Planned shared-ontology schema"
"""

import json
import sys
from pathlib import Path
import time
from datetime import datetime, timezone

def main():
    if len(sys.argv) < 3:
        print("Usage: link_memory_to_entity.py <entity_id> <snippet> [<snippet> ...]")
        sys.exit(1)

    entity_id = sys.argv[1]
    snippets = sys.argv[2:]

    graph_path = Path.home() / ".openclaw/shared-ontology/graph.jsonl"

    # Generate a unique ID for each MemoryChunk
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    for i, content in enumerate(snippets):
        chunk_id = f"mc_{timestamp}_{i}"
        # Create MemoryChunk entity
        chunk = {
            "id": chunk_id,
            "type": "MemoryChunk",
            "properties": {
                "content": content,
                "source": "demo",   # could be 'episodic', 'semantic', etc.
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
        # Append create op
        with open(graph_path, 'a') as f:
            f.write(json.dumps({"op":"create","entity":chunk}) + "\n")
            # Append relate op: chunk referenced_in entity
            f.write(json.dumps({"op":"relate","from":chunk_id,"rel":"referenced_in","to":entity_id}) + "\n")

        print(f"Linked memory chunk {chunk_id} to {entity_id}")

if __name__ == "__main__":
    main()