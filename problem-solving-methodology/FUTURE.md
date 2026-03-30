# Future Enhancements (Pull Request Ideas)

Local workflow integrations to consider upstream:

- **Automated root cause validation via git archaeology** — When diagnosing a problem, automatically run `git log -S` (pickaxe) to find when a suspicious variable/function was introduced; compare commit dates against when problem started; use as evidence for root cause confirmation (integration with `git-workflows`).

- **Diagnostic experiment automation for unclear causes** — Generate minimal-case tests (e.g., "change X, observe Y") and auto-run them to narrow root cause; log each experiment result to `memory/episodic/` with outcome so patterns can be detected by `self-improving-agent`.

- **Multi-option comparison scoring** — Score each candidate solution on risk/complexity/reversibility dimensions; auto-generate pros/cons lists with probability estimates; suggest user-confirmable recommendation with confidence score based on diagnostic evidence quality.

- **Postmortem template auto-population** — After fix is verified, auto-fill postmortem template with gathered diagnostic info (duration, symptom, root cause, solution, regression tests); emit to mmlog so lessons compound across sessions (pairs with `self-improving-agent` for pattern detection).

- **Deployment safety context injection** — Detect if problem is production-related; inject safety guardrails into execution phase (require approval before restart, add health check verification step, enable rollback recording); integrate with `debug-methodology` for hardened SCP flow enforcement.

Status: Prototype in local workspace; ready for contribution when time permits.
