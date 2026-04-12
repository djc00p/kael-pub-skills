import { execFileSync } from "child_process";
import { existsSync, readFileSync, appendFileSync } from "fs";
import { homedir } from "os";
import { join } from "path";

const GRAPH_PATH = join(homedir(), ".openclaw/shared-ontology/graph.jsonl");
const MIN_SCORE = 0.4;

interface MemoryResult {
  snippet: string;
  score: number;
  path: string;
}

interface OntologyEntity {
  id: string;
  type: string;
  properties: Record<string, string>;
}

function loadEntities(): OntologyEntity[] {
  if (!existsSync(GRAPH_PATH)) return [];
  const lines = readFileSync(GRAPH_PATH, "utf-8").trim().split("\n").filter(Boolean);
  const entities: Record<string, OntologyEntity> = {};
  for (const line of lines) {
    try {
      const op = JSON.parse(line);
      if (op.op === "create" && op.entity) {
        entities[op.entity.id] = op.entity;
      } else if (op.op === "delete" && op.id) {
        delete entities[op.id];
      }
    } catch {}
  }
  return Object.values(entities);
}

function extractMemoryResults(transcript: string): MemoryResult[] {
  const results: MemoryResult[] = [];
  // Match memory_search tool results in session JSON
  const snippetRegex = /"snippet":\s*"([^"]+)"[^}]*"score":\s*([\d.]+)/g;
  let match;
  while ((match = snippetRegex.exec(transcript)) !== null) {
    const score = parseFloat(match[2]);
    if (score >= MIN_SCORE) {
      results.push({ snippet: match[1], score, path: "" });
    }
  }
  return results;
}

function findMatchingEntities(snippet: string, entities: OntologyEntity[]): string[] {
  const lower = snippet.toLowerCase();
  const matches: string[] = [];
  for (const entity of entities) {
    if (entity.type === "MemoryChunk" || entity.type === "Agent") continue;
    const name = (entity.properties?.name || "").toLowerCase();
    const title = (entity.properties?.title || "").toLowerCase();
    if (name && lower.includes(name)) matches.push(entity.id);
    else if (title && lower.includes(title)) matches.push(entity.id);
  }
  return matches;
}

function appendToGraph(lines: string[]) {
  if (lines.length === 0) return;
  appendFileSync(GRAPH_PATH, lines.join("\n") + "\n", "utf-8");
}

const handler = async (event: any) => {
  if (!["command:new", "command:reset", "command"].includes(event.type)) return;
  if (event.action !== "new" && event.action !== "reset") return;

  if (!existsSync(GRAPH_PATH)) return;

  // Get previous session transcript
  const session = event.context?.previousSessionEntry || event.context?.sessionEntry;
  if (!session) return;

  const transcript = JSON.stringify(session);
  const memoryResults = extractMemoryResults(transcript);
  if (memoryResults.length === 0) return;

  const entities = loadEntities();
  if (entities.length === 0) return;

  const timestamp = new Date().toISOString().replace(/[-:.]/g, "").slice(0, 15);
  const ops: string[] = [];
  let linkedCount = 0;

  for (let i = 0; i < memoryResults.length; i++) {
    const result = memoryResults[i];
    const matchedEntityIds = findMatchingEntities(result.snippet, entities);
    if (matchedEntityIds.length === 0) continue;

    const chunkId = `mc_${timestamp}_${i}`;
    const chunk = {
      id: chunkId,
      type: "MemoryChunk",
      properties: {
        content: result.snippet.replace(/\\n/g, " ").slice(0, 300),
        source: "memory_search",
        score: String(result.score),
        timestamp: new Date().toISOString(),
      },
    };

    ops.push(JSON.stringify({ op: "create", entity: chunk }));
    for (const entityId of matchedEntityIds) {
      ops.push(JSON.stringify({ op: "relate", from: chunkId, rel: "referenced_in", to: entityId }));
      linkedCount++;
    }
  }

  if (ops.length > 0) {
    appendToGraph(ops);
    event.messages.push(`🔗 Linked ${linkedCount} memory snippet(s) to ontology`);
  }
};

export default handler;
