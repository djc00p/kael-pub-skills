#!/usr/bin/env python3
"""
Print all MemoryChunk entities linked to a given ontology entity
via the 'referenced_in' relation.

Usage:
  python3 linked_memories.py <entity_id>
Example:
  python3 linked_memories.py proj_openclaw
"""

import json
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: linked_memories.py <entity_id>")
        sys.exit(1)

    entity_id = sys.argv[1]
    graph_file = Path.home() / ".openclaw/shared-ontology/graph.jsonl"

    # First pass: collect all entities and then the referenced_in edges
    entities = {}
    incoming_ref_links = {}  # from -> to for referenced_in

    with open(graph_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            op = json.loads(line)
            op_type = op.get("op")
            if op_type == "create":
                e = op.get("entity", {})
                entities[e["id"]] = e
            elif op_type == "relate":
                if op.get("rel") == "referenced_in":
                    from_id = op.get("from")
                    to_id = op.get("to")
                    if to_id == entity_id:
                        incoming_ref_links[from_id] = True

    # Print linked MemoryChunks in reverse chronological by timestamp? We'll just print.
    linked_ids = [eid for eid in incoming_ref_links if eid in entities]
    if not linked_ids:
        print(f"No memory chunks linked to entity: {entity_id}")
        return

    print(f"MemoryChunks linked to {entity_id}:")
    for eid in linked_ids:
        e = entities[eid]
        if e.get("type") != "MemoryChunk":
            continue
        print(f"- [{eid}]:")
        print(f"  Content: {e['properties'].get('content')}")
        print(f"  Source:  {e['properties'].get('source', 'n/a')}")
        print(f"  Time:    {e['properties'].get('timestamp', 'n/a')}")
        print()

if __name__ == "__main__":
    main()