---
name: rails-ci-fixer
description: Autonomously fix failing CI on Rails PRs using a tiered escalation loop. Works with any AI coding agent (built and tested with Claude). Use when a Rails pull request has failing CI — RSpec failures, RuboCop offenses, migration errors, factory issues, or seed data problems. Handles the full cycle: pull logs, attempt fix with a fast/cheap model, escalate to a stronger model if needed, notify human when green or stuck. Never merges — human always merges. Triggers on phrases like "fix CI", "CI is failing", "watch the PR", "fix the tests", or when a PR has a failing CI run.
---

# Rails CI Fixer

Autonomously fix failing Rails CI using a tiered escalation loop.

## Setup

Requires:
- `gh` CLI authenticated (`gh auth login`)
- `bundle exec rspec` working locally
- `bundle exec rubocop` installed

## Fix Loop

### Attempt 1 & 2 — Fast fix with a lightweight model
1. Pull failure logs:
   ```bash
   gh run view <run_id> --repo <owner/repo> --log-failed 2>&1 | grep -E "Failure|Error:|rspec \./|RecordInvalid|[0-9]+ example" | head -40
   ```
2. Use a fast/cheap coding agent to attempt the fix (e.g. Claude Haiku, GPT-4o-mini, Gemini Flash)
3. Verify locally:
   ```bash
   bundle exec rspec spec/path/to/failing_spec.rb
   ```
4. Run RuboCop:
   ```bash
   bundle exec rubocop -A app/ spec/
   ```
5. Commit and push → watch CI

### Attempt 3 — Debug sub-agent + stronger model
1. Spawn a debug sub-agent that adds `pp`/`raise inspect` at the failure point
2. Sub-agent runs the spec and reports back the state at failure
3. Escalate to a stronger model (e.g. Claude Sonnet/Opus, GPT-4o, Gemini Pro) armed with debug findings
4. Verify, RuboCop, commit, push

### Attempt 4 — Stop and notify human
- Message human with: what failed, what was tried, debug output
- Do NOT attempt further fixes without human input

## Hard Rules

- **NEVER comment out existing tests** — fix the root cause always
- **NEVER merge** — human always reviews and merges
- **Notify on green**: use your platform's notification mechanism

## RuboCop

- Run `rubocop -A app/ spec/` after every fix
- Commit RuboCop changes separately: `style: RuboCop auto-corrections`
- Never alter single-expectation test patterns in specs

## Common Failure Patterns

See `references/common-failures.md` for patterns and fixes.
