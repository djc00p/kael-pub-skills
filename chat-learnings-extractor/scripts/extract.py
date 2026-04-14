#!/usr/bin/env python3
"""
Extract structured learnings from AI conversation exports using a local Ollama model or OpenAI-compatible API.

Usage:
    python3 extract.py --dir /path/to/exports [--limit 3] [--dry-run]
    python3 extract.py --file single-conversation.json
    python3 extract.py --dir /path/to/exports --since 2026-04-01 --model gpt-4o-mini

Flags:
    --dir DIR              Directory of conversation export JSON files
    --file FILE            Single conversation export file
    --limit N              Process only first N conversations
    --since YYYY-MM-DD     Skip conversations before this date
    --model MODEL          Model name (default: gemma4:26b for Ollama, gpt-4o-mini for OpenAI)
    --dry-run              Print output without writing to disk

Environment Variables:
    OLLAMA_BASE_URL        Ollama API endpoint (default: http://127.0.0.1:11434)
    OPENAI_API_KEY         OpenAI API key (enables OpenAI-compatible mode)
    OPENAI_BASE_URL        OpenAI-compatible API base URL (default: https://api.openai.com/v1)
"""

import sys
import os
import json
import argparse
import urllib.request
from pathlib import Path
from datetime import datetime
from typing import Generator, Optional, Dict, List

# Import parsers bundled with this skill (from chat-history-importer)
parser_dir = Path(__file__).parent
sys.path.insert(0, str(parser_dir))
from parse_openai import parse as parse_openai
from parse_anthropic import parse as parse_anthropic


def get_workspace() -> Path:
    """Get workspace path from env or fallback."""
    workspace = Path.home() / ".openclaw" / "workspace"
    if (env_ws := os.environ.get("OPENCLAW_WORKSPACE")):
        workspace = Path(env_ws)
    return workspace


def use_openai_api() -> bool:
    """Check if OpenAI API key is configured."""
    return bool(os.environ.get("OPENAI_API_KEY"))


def openai_extract(summary: str, model: str = "gpt-4o-mini") -> str:
    """Send prompt to OpenAI-compatible API and return extracted learnings."""
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not set", file=sys.stderr)
        return ""
    
    prompt = f"""You are an expert at identifying actionable insights from AI conversations.

Given a conversation summary, extract four categories of learnings:

1. **Lessons Learned** — What worked, what didn't, what was surprising
2. **Decisions Made** — Architectural, technical, or product choices discussed
3. **Patterns Noticed** — Recurring problems, approaches, or themes
4. **Dead Ends** — Things tried that failed or were abandoned

Keep responses focused and concise. Use bullet points. Skip categories if nothing notable applies.

---

{summary}

---

Return ONLY the structured markdown below. No preamble or explanation:

## Lessons Learned
[bullet points or "None"]

## Decisions Made
[bullet points or "None"]

## Patterns Noticed
[bullet points or "None"]

## Dead Ends
[bullet points or "None"]
"""

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }).encode()

    url = f"{base_url}/chat/completions"
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            if "choices" in result and result["choices"]:
                return result["choices"][0]["message"]["content"]
            return ""
    except Exception as e:
        print(f"Error querying OpenAI API: {e}", file=sys.stderr)
        return ""


def ollama_extract(summary: str, model: str = "gemma4:26b") -> str:
    """Send prompt to Ollama and return extracted learnings."""
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    
    prompt = f"""You are an expert at identifying actionable insights from AI conversations.

Given a conversation summary, extract four categories of learnings:

1. **Lessons Learned** — What worked, what didn't, what was surprising
2. **Decisions Made** — Architectural, technical, or product choices discussed
3. **Patterns Noticed** — Recurring problems, approaches, or themes
4. **Dead Ends** — Things tried that failed or were abandoned

Keep responses focused and concise. Use bullet points. Skip categories if nothing notable applies.

---

{summary}

---

Return ONLY the structured markdown below. No preamble or explanation:

## Lessons Learned
[bullet points or "None"]

## Decisions Made
[bullet points or "None"]

## Patterns Noticed
[bullet points or "None"]

## Dead Ends
[bullet points or "None"]
"""

    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False
    }).encode()

    url = f"{base_url}/api/generate"
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            return result.get("response", "")
    except Exception as e:
        print(f"Error querying Ollama: {e}", file=sys.stderr)
        return ""


def condense_conversation(chat: Dict) -> str:
    """Condense conversation to key excerpts for context."""
    title = chat.get("title", "Untitled")
    date = chat.get("date", "")
    messages = chat.get("messages", [])

    # Build a summary with key messages only (skip long content)
    lines = [f"Title: {title}", f"Date: {date}", ""]

    for msg in messages:
        role = msg.get("role", "unknown").upper()
        content = msg.get("content", "")[:200]  # Truncate long messages
        timestamp = msg.get("timestamp", "")[:10]  # Date only
        lines.append(f"[{timestamp}] {role}: {content}")

    return "\n".join(lines)


def parse_conversations(file_path: Path) -> Generator[Dict, None, None]:
    """Auto-detect format and parse conversation file."""
    if file_path.suffix != ".json":
        return

    try:
        chats = list(parse_anthropic(str(file_path)))
        if chats:
            yield from chats
            return
    except Exception:
        pass

    try:
        chats = list(parse_openai(str(file_path)))
        if chats:
            yield from chats
            return
    except Exception:
        print(f"Warning: Could not parse {file_path}", file=sys.stderr)
        return


def load_processed_ids(workspace: Path) -> set:
    """Load set of already-processed chat IDs."""
    processed_file = workspace / ".processed_ids"
    if processed_file.exists():
        return set(processed_file.read_text().strip().split("\n"))
    return set()


def save_processed_ids(workspace: Path, processed: set) -> None:
    """Save set of processed chat IDs."""
    processed_file = workspace / ".processed_ids"
    processed_file.write_text("\n".join(sorted(processed)))


def main():
    parser = argparse.ArgumentParser(description="Extract learnings from conversation exports")
    parser.add_argument("--dir", type=Path, help="Directory of export files")
    parser.add_argument("--file", type=Path, help="Single export file")
    parser.add_argument("--limit", type=int, default=None, help="Process first N conversations")
    parser.add_argument("--since", type=str, help="Skip conversations before YYYY-MM-DD")
    parser.add_argument("--model", type=str, default=None, help="Model name (auto-selected by default)")
    parser.add_argument("--dry-run", action="store_true", help="Print without writing")

    args = parser.parse_args()

    if not args.dir and not args.file:
        print("Error: provide --dir or --file", file=sys.stderr)
        sys.exit(1)

    # Determine model if not specified
    if args.model is None:
        args.model = "gpt-4o-mini" if use_openai_api() else "gemma4:26b"

    workspace = get_workspace()
    processed = load_processed_ids(workspace)
    since_date = datetime.fromisoformat(args.since) if args.since else None

    output_file = workspace / "memory" / "semantic" / "learnings-from-exports.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Collect export files
    export_files = []
    if args.file:
        export_files = [args.file]
    elif args.dir:
        export_files = sorted(args.dir.glob("*.json"))

    count = 0
    for file_path in export_files:
        if count >= (args.limit or float("inf")):
            break

        for chat in parse_conversations(file_path):
            chat_id = chat.get("id")
            if chat_id in processed:
                continue

            # Check date filter first (before counting toward limit)
            chat_date = datetime.fromisoformat(chat.get("date", ""))
            if since_date and chat_date < since_date:
                continue

            # Now check limit
            if args.limit and count >= args.limit:
                break

            # Extract learnings
            summary = condense_conversation(chat)
            print(f"Processing {chat_id}...", file=sys.stderr)
            
            if use_openai_api():
                learnings = openai_extract(summary, args.model)
            else:
                learnings = ollama_extract(summary, args.model)

            # Format output
            output = f"\n## {chat.get('title', 'Untitled')} ({chat.get('date')})\n\n{learnings}\n"

            if args.dry_run:
                print(output)
            else:
                with open(output_file, "a") as f:
                    f.write(output)

            processed.add(chat_id)
            count += 1

    # Save dedup state
    if not args.dry_run:
        save_processed_ids(workspace, processed)
        print(f"Processed {count} conversations. Saved to {output_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
