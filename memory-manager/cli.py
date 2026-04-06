#!/usr/bin/env python3
import sys, os, json, argparse
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_LOG = os.path.abspath(os.path.join(BASE_DIR, 'memory', 'entries.json'))
MEMORY_SUMMARY = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'MEMORY.md'))

def ensure_log():
    os.makedirs(os.path.dirname(MEMORY_LOG), exist_ok=True)
    if not os.path.exists(MEMORY_LOG):
        with open(MEMORY_LOG, 'w') as f:
            json.dump([], f)
    return MEMORY_LOG

def load_entries():
    ensure_log()
    with open(MEMORY_LOG, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_entries(entries):
    with open(MEMORY_LOG, 'w') as f:
        json.dump(entries, f, indent=2)

def log_entry(content, tags=None, entry_type='note', source='local'):
    entries = load_entries()
    entry = {
        'id': int(datetime.now(timezone.utc).timestamp()),
        'timestamp': datetime.now(timezone.utc).isoformat() + 'Z',
        'type': entry_type,
        'content': content,
        'tags': tags or [],
        'source': source
    }
    entries.append(entry)
    save_entries(entries)
    return entry

def recall(query, limit=5):
    entries = load_entries()
    q = (query or '').lower()
    matches = []
    for e in entries:
        text = str(e.get('content',''))
        tags = ' '.join(e.get('tags', []))
        if q in text.lower() or q in tags.lower():
            matches.append(e)
    matches = sorted(matches, key=lambda x: x.get('timestamp',''), reverse=True)
    return matches[:max(0, int(limit))]

def summarize():
    entries = load_entries()
    if not entries:
        summary = '# MEMORY.md - Curated Long-Term Memory\n\nNo entries yet.\n'
    else:
        summary_lines = ['# MEMORY.md - Curated Long-Term Memory\n']
        summary_lines.append('\nLast 10 entries:\n')
        for e in sorted(entries, key=lambda x: x.get('timestamp',''), reverse=True)[:10]:
            ts = e.get('timestamp','')
            content = (e.get('content','')[:200] + ('...' if len(e.get('content','')) > 200 else ''))
            summary_lines.append(f"- [{ts}] {content} (tags: {', '.join(e.get('tags', []))})")
        summary = '\n'.join(summary_lines) + '\n'
    with open(MEMORY_SUMMARY, 'w') as f:
        f.write(summary)
    return summary

def main():
    parser = argparse.ArgumentParser(description='Memory Manager CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)

    parser_log = subparsers.add_parser('log', help='Add a memory entry')
    parser_log.add_argument('--content', required=True, help='Entry content')
    parser_log.add_argument('--tags', default='', help='Comma-separated tags')
    parser_log.add_argument('--type', default='note', choices=['note','decision','preference','lesson','fact'], help='Entry type')
    parser_log.add_argument('--source', default='local', help='Source of the entry')

    parser_recall = subparsers.add_parser('recall', help='Search memory entries')
    parser_recall.add_argument('--query', required=True, help='Search query')
    parser_recall.add_argument('--limit', type=int, default=5, help='Maximum results')

    subparsers.add_parser('summarize', help='Refresh MEMORY.md summary')

    args = parser.parse_args()

    if args.command == 'log':
        tags = [t.strip() for t in args.tags.split(',') if t.strip()] if args.tags else []
        entry = log_entry(args.content, tags=tags, entry_type=args.type, source=args.source)
        print(f"Logged entry id={entry['id']}")
    elif args.command == 'recall':
        results = recall(args.query, args.limit)
        for e in results:
            print(f"- [{e.get('timestamp')}] {e.get('content')} (tags: {', '.join(e.get('tags', []))})")
    elif args.command == 'summarize':
        print(summarize())

if __name__ == '__main__':
    main()