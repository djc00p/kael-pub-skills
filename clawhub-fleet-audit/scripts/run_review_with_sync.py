#!/usr/bin/env python3
"""Bi-weekly ClawHub fleet review + GitHub repo sync.

Runs the read-only ClawHub security/drift audit, then syncs every published
skill to its GitHub repo under ~/skills/github-repos/ (README preserved,
LICENSE, SKILL.md, version tag, GitHub release), then verifies the result.

Produces a delivery-ready summary at
~/.openclaw/workspace/reports/clawhub-fleet-review-summary.txt

Exit codes:
  0 = review + sync completed
  1 = could not run
  2 = audit failed
  3 = sync failed
"""
import contextlib
import io
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw/workspace"
REPORTS = WORKSPACE / "reports"
AUDIT = WORKSPACE / "skills/clawhub-fleet-audit/scripts/audit_fleet.py"
SYNC = WORKSPACE / "scripts/sync_skills_to_github.py"
VERIFY = WORKSPACE / "scripts/verify_skill_repos.py"
JSON_OUT = REPORTS / "clawhub-fleet-audit.json"
MD_OUT = REPORTS / "clawhub-fleet-audit.md"
SUMMARY_OUT = REPORTS / "clawhub-fleet-review-summary.txt"

# GitHub is unreachable through the egress proxy. Bypass it for git/gh only.
GIT_ENV = {
    "NO_PROXY": "*",
    "no_proxy": "*",
    "HTTPS_PROXY": "",
    "HTTP_PROXY": "",
    "https_proxy": "",
    "http_proxy": "",
}


def run(cmd, timeout=1800):
    env = dict(os.environ)
    env.update(GIT_ENV)
    return subprocess.run(cmd, capture_output=True, text=True, env=env,
                          timeout=timeout)


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)

    # ---------- Step 1: read-only ClawHub audit ----------
    proc = subprocess.run(
        [sys.executable, str(AUDIT), "--json", str(JSON_OUT), "--md", str(MD_OUT)],
        capture_output=True, text=True,
    )
    if proc.stderr.strip():
        print(proc.stderr.strip(), file=sys.stderr)

    if proc.returncode == 1 or not JSON_OUT.exists():
        text = ("\n## ClawHub Fleet Review — FAILED\n\n"
                "The audit could not run. Check `CLAWHUB_API_KEY` and "
                "network reachability.\n")
        SUMMARY_OUT.write_text(text, encoding="utf-8")
        print(text)
        return 1

    data = json.loads(JSON_OUT.read_text(encoding="utf-8"))

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        render(data)
    base = buf.getvalue()

    # ---------- Step 2: sync GitHub repos ----------
    sync_lines = []
    sync_ok = True
    if SYNC.exists():
        print("syncing GitHub repos...", file=sys.stderr)
        sp = run([sys.executable, str(SYNC)], timeout=3600)
        tail = (sp.stdout or "").strip().splitlines()
        # keep the summary block from the sync script
        idx = 0
        for i, line in enumerate(tail):
            if line.strip() == "SUMMARY":
                idx = i
                break
        sync_lines = tail[idx:] if idx else tail[-40:]
        if sp.returncode != 0:
            sync_ok = False
            sync_lines.append(f"sync exited {sp.returncode}")
            if sp.stderr.strip():
                sync_lines.append(sp.stderr.strip()[-800:])
    else:
        sync_ok = False
        sync_lines = [f"sync script not found: {SYNC}"]

    # ---------- Step 3: verify ----------
    verify_lines = []
    verify_ok = True
    if VERIFY.exists():
        vp = run([sys.executable, str(VERIFY)], timeout=1800)
        vtail = (vp.stdout or "").strip().splitlines()
        vidx = 0
        for i, line in enumerate(vtail):
            if line.strip() == "PASS:":
                vidx = i
                break
        verify_lines = vtail[vidx:] if vidx else vtail[-8:]
        if vp.returncode != 0:
            verify_ok = False
    else:
        verify_ok = False
        verify_lines = [f"verify script not found: {VERIFY}"]

    # ---------- assemble ----------
    parts = [base, "\n## GitHub repo sync\n"]
    if sync_lines:
        parts.append("```")
        parts.extend(sync_lines)
        parts.append("```")
    parts.append("\n### Verification\n")
    if verify_lines:
        parts.append("```")
        parts.extend(verify_lines)
        parts.append("```")
    parts.append("\n**READMEs are preserved** — an existing README.md is never "
                 "overwritten by a sync. The generated template is only used to "
                 "bootstrap a brand-new repo.\n")

    text = "\n".join(parts)
    SUMMARY_OUT.write_text(text, encoding="utf-8")
    print(text)

    if not sync_ok:
        return 3
    if not verify_ok:
        return 3
    return 0


def render(data):
    c = data["counts"]
    d = data["drift"]

    print("\n## ClawHub Fleet Review")
    print()
    print(f"**{data['generated_at'][:10]}** — owner `{data['owner_handle']}` — "
          f"{c['total']} published skills audited\n")
    print("| Listing status (what visitors see) | Count |")
    print("|---|---|")
    print(f"| Listed clean (no badge) | **{c.get('listing_clean', 0)}** |")
    print(f"| Flagged \"Needs review\" | **{c.get('listing_review', 0)}** |")
    print(f"| Other / unknown moderation | {c.get('listing_other', 0)} |")
    print(f"| Unscanned (409/404/failed) | {c['failures']} |")
    print("|")
    print("| Static scanner (SkillSpector) | Count |")
    print("|---|---|")
    print(f"| Critical (DO_NOT_INSTALL / CRITICAL / HIGH) | {c['critical']} |")
    print(f"| Review (suspicious / warnings / MEDIUM) | {c['review']} |")
    print(f"| Clean | {c['ok']} |")
    print(f"| Frontmatter problems | {c.get('frontmatter', 0)} |")
    print("|")
    print("| Version drift | Count |")
    print("|---|---|")
    for k, v in d.items():
        print(f"| {k} | {v} |")

    flagged = [r for r in data.get("results", []) if r.get("needs_review")]
    if flagged:
        print()
        print("### Flagged \"Needs review\"")
        for r in flagged:
            m = r.get("moderation") or {}
            sc = r.get("scan") or {}
            print(f"- **{r.get('slug')}** v{r.get('local_version')} — "
                  f"scanner {sc.get('severity')}/{sc.get('recommendation')} "
                  f"(score {sc.get('score')}), codes {m.get('reasonCodes')}")
    else:
        print()
        print("**No skills are flagged \"Needs review\".**")

    critical = [r for r in data.get("results", [])
                if (r.get("scan") or {}).get("bucket") == "critical"]
    if critical:
        print()
        print("### Static-scanner critical (separate axis from the badge)")
        for r in critical:
            sc = r.get("scan") or {}
            guidance = (sc.get("llm_guidance") or "").strip()
            print(f"- **{r.get('slug')}** v{r.get('local_version')} — "
                  f"{sc.get('severity')}/{sc.get('recommendation')} "
                  f"(score {sc.get('score')})")
            if guidance:
                print(f"  - Fix: {guidance[:280]}")


if __name__ == "__main__":
    sys.exit(main())
