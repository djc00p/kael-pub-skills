---
name: rails-ci-fixer
description: Autonomously fix failing CI on Rails PRs using a tiered fix loop. Use when a Rails pull request has failing CI (RSpec failures, RuboCop offenses, migration errors, factory issues). Handles the full cycle: pull logs, attempt fix with Haiku, escalate to debug sub-agent + Opus if needed, notify human when green or stuck. Never merges — human always merges. Triggers on phrases like "fix CI", "CI is failing", "watch the PR", "fix the tests", or when a PR has a failing CI run.
---

# Rails CI Fixer

Autonomously fix failing Rails CI using a tiered escalation loop.

## Fix Loop

### Attempt 1 & 2 — Claude Code on Haiku
1. Pull failure logs: `gh run view <run_id> --repo <owner/repo> --log-failed 2>&1 | grep -E "Failure|Error:|rspec \./|RecordInvalid|[0-9]+ example" | head -40`
2. Fix with Claude Code on Haiku:
   ```bash
   claude --model claude-haiku-4-5-20251001 --permission-mode bypassPermissions --print 'Fix these CI failures: <paste failures>'
   ```
3. Verify locally: `rbenv exec bundle exec rspec spec/path/to/failing_spec.rb`
4. Run RuboCop: `rbenv exec bundle exec rubocop -A app/ spec/`
5. Commit and push → watch CI

### Attempt 3 — Debug sub-agent + Opus
1. Spawn a debug sub-agent that adds `pp object` / `raise object.inspect` at the failure point
2. Sub-agent runs the spec and reports back state at failure
3. Fix with Claude Code on Opus armed with debug findings:
   ```bash
   claude --permission-mode bypassPermissions --print 'Fix these CI failures. Debug output: <findings>'
   ```
4. Verify, RuboCop, commit, push

### Attempt 4 — Stop and notify human
- Message human with: what failed, what was tried, debug output
- Do NOT attempt further fixes without human input

## Hard Rules

- **NEVER comment out existing tests** — fix the root cause
- **NEVER merge** — human always merges
- **Notify on green**: `openclaw system event --text "PR #X CI is green ✅ — ready to merge" --mode now`

## Common Rails CI Failures

See `references/common-failures.md` for patterns and fixes.

## RuboCop
- Run `rubocop -A app/ spec/` after every fix
- `Metrics/ModuleLength` — optional, skip if not auto-fixable
- Commit RuboCop changes separately: `style: RuboCop auto-corrections`
- Never change single-expectation test patterns
