# Ontology Schema Additions (for this skill)

This skill assumes the shared ontology (`~/.openclaw/shared-ontology/schema.yaml`) includes:

## New types

```yaml
MemoryChunk:
  required: [content]
  properties:
    content: string
    source?: string
    score?: float
    timestamp?: date
```

## New relations

```yaml
referenced_in:
  from: [MemoryChunk]
  to: [*]   # any ontology entity
  cardinality: many_to_one
```

If these are missing, the scripts will still create entities of that type, but the validator (if used) may reject them. You can either add these definitions to your `schema.yaml` or upgrade the validator to be permissive about unknown types (depending on your setup).
