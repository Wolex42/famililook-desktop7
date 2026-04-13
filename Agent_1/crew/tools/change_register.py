#!/usr/bin/env python3
"""Unified Change Register — bridges all 3 tracking systems.

Used by the Change Manager agent to maintain a single view of all changes
across the FamiliLook platform.

Scans:
  1. .claude/change_log.md in every repo (Claude Code manual edits)
  2. download/ops_reports/ in every repo (ops_agents automated runs)
  3. ad_crew/output/ (marketing campaign output)
  4. git log across all repos (source of truth)

Outputs:
  - Unified change register (CSV or Markdown)
  - Gap report (commits without change_log entries)
  - Orphaned run report (started but never completed agent runs)
  - Stale state report (working_set.txt, hooks, etc.)

Usage:
    python change_register.py --scan          # Full scan, print report
    python change_register.py --gaps          # Show untracked commits only
    python change_register.py --orphans       # Show orphaned agent runs only
    python change_register.py --health        # Overall health check
    python change_register.py --register      # Output unified register as CSV
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from io import StringIO
from pathlib import Path
from typing import List, Optional


# ── Repo Configuration ──

@dataclass
class RepoConfig:
    name: str
    path: Path
    repo_type: str          # "FE" or "BE" or "parent"
    has_change_log: bool = False
    has_ops_reports: bool = False
    has_hook: bool = False
    test_command: str = ""


def discover_repos(base_dir: Path) -> List[RepoConfig]:
    """Discover all repos under the FML project directory."""
    repos = []

    candidates = [
        ("famililook-desktop2", "FE", "npm run test:run"),
        ("famililook-desktop3", "BE", "pytest tests/"),
        ("famililook-desktop4", "FE", "npm run test:run"),
        ("famililook-desktop5", "BE", "pytest tests/"),
        ("famililook-desktop6", "FE", "npm run test:run"),
        ("famililook-desktop7", "BE", "pytest tests/"),
    ]

    # Parent repo
    parent = RepoConfig(
        name="FML (parent)",
        path=base_dir,
        repo_type="parent",
        has_change_log=(base_dir / ".claude" / "change_log.md").exists(),
        has_ops_reports=(base_dir / "download" / "ops_reports").exists(),
        has_hook=(base_dir / ".git" / "hooks" / "pre-commit").exists(),
    )
    repos.append(parent)

    # Sub repos
    for name, rtype, test_cmd in candidates:
        rpath = base_dir / name
        if not rpath.exists():
            continue

        repos.append(RepoConfig(
            name=name,
            path=rpath,
            repo_type=rtype,
            has_change_log=(rpath / ".claude" / "change_log.md").exists(),
            has_ops_reports=(rpath / "download" / "ops_reports").exists(),
            has_hook=(rpath / ".git" / "hooks" / "pre-commit").exists(),
            test_command=test_cmd,
        ))

    return repos


# ── Git Log Scanner ──

@dataclass
class GitCommit:
    sha: str
    date: str
    author: str
    message: str
    repo: str


def get_recent_commits(repo_path: Path, repo_name: str, days: int = 14) -> List[GitCommit]:
    """Get recent git commits from a repo."""
    since = (date.today() - timedelta(days=days)).isoformat()
    try:
        result = subprocess.run(
            ["git", "log", f"--since={since}", "--format=%H|%aI|%an|%s", "--no-merges"],
            cwd=str(repo_path),
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return []

        commits = []
        for line in result.stdout.strip().split("\n"):
            if not line or "|" not in line:
                continue
            parts = line.split("|", 3)
            if len(parts) == 4:
                commits.append(GitCommit(
                    sha=parts[0][:8],
                    date=parts[1][:10],
                    author=parts[2],
                    message=parts[3],
                    repo=repo_name,
                ))
        return commits
    except Exception:
        return []


# ── Change Log Scanner ──

def get_change_log_entries(repo_path: Path) -> List[str]:
    """Extract Description lines from a change_log.md file."""
    log_path = repo_path / ".claude" / "change_log.md"
    if not log_path.exists():
        return []

    text = log_path.read_text(encoding="utf-8", errors="ignore")
    # Extract **Description**: lines
    return re.findall(r"\*\*Description\*\*:\s*(.+)", text)


# ── Ops Reports Scanner ──

@dataclass
class OpsRun:
    run_dir: str
    timestamp: str
    has_report: bool
    has_patch: bool
    verdict: str          # "APPROVE", "BLOCK", "UNKNOWN", "INCOMPLETE"
    repo: str


def scan_ops_reports(repo_path: Path, repo_name: str) -> List[OpsRun]:
    """Scan download/ops_reports/ for agent runs."""
    reports_dir = repo_path / "download" / "ops_reports"
    if not reports_dir.exists():
        return []

    runs = []
    for d in sorted(reports_dir.iterdir()):
        if not d.is_dir():
            continue

        run_files = list(d.glob("run_*.md"))
        patch_files = list(d.glob("patch_*.diff")) + list(d.glob("*.patch"))

        verdict = "UNKNOWN"
        for rf in run_files:
            try:
                content = rf.read_text(encoding="utf-8", errors="ignore")
                if "APPROVE" in content:
                    verdict = "APPROVE"
                elif "BLOCK" in content:
                    verdict = "BLOCK"
            except Exception:
                pass

        if not run_files:
            verdict = "INCOMPLETE"

        runs.append(OpsRun(
            run_dir=d.name,
            timestamp=d.name[:15] if len(d.name) >= 15 else d.name,
            has_report=bool(run_files),
            has_patch=bool(patch_files),
            verdict=verdict,
            repo=repo_name,
        ))

    return runs


# ── State Lock Scanner ──

def check_orphaned_runs(repo_path: Path) -> List[dict]:
    """Check .ops_state_lock.json for orphaned (started but never completed) runs."""
    lock_path = repo_path / "download" / "ops_reports" / ".ops_state_lock.json"
    if not lock_path.exists():
        return []

    try:
        data = json.loads(lock_path.read_text(encoding="utf-8"))
        orphaned = []
        for run in data.get("runs", []):
            if run.get("status") == "started" and not run.get("head_sha_after"):
                orphaned.append({
                    "run_day": run.get("run_day", "?"),
                    "issue": run.get("issue", "?"),
                    "started_at": run.get("started_at", "?"),
                })
        return orphaned
    except Exception:
        return []


# ── Ad Crew Output Scanner ──

@dataclass
class CampaignOutput:
    phase: str
    run_id: str
    files: List[str]
    has_crew_result: bool
    linked_to_event: bool


def scan_ad_crew_output(base_dir: Path) -> List[CampaignOutput]:
    """Scan ad_crew/output/ for campaign runs."""
    output_dir = base_dir / "Agent_1" / "ad_crew" / "output"
    if not output_dir.exists():
        return []

    campaigns = []
    for phase_dir in sorted(output_dir.iterdir()):
        if not phase_dir.is_dir() or phase_dir.name == "publish_queue":
            continue

        for run_dir in sorted(phase_dir.iterdir()):
            if not run_dir.is_dir():
                continue

            files = [f.name for f in run_dir.iterdir() if f.is_file()]
            has_result = any("crew_result" in f for f in files)

            campaigns.append(CampaignOutput(
                phase=phase_dir.name,
                run_id=run_dir.name,
                files=files,
                has_crew_result=has_result,
                linked_to_event=False,  # TODO: cross-ref with seasonal calendar
            ))

    return campaigns


# ── Working Set / Hook Check ──

def check_working_set(repo_path: Path) -> dict:
    """Check if working_set.txt exists and whether it's stale."""
    ws_path = repo_path / ".claude" / "working_set.txt"
    if not ws_path.exists():
        return {"exists": False, "stale": False, "files": []}

    text = ws_path.read_text(encoding="utf-8", errors="ignore").strip()
    files = [l.strip() for l in text.split("\n") if l.strip() and not l.startswith("#")]

    # Check modification time
    mtime = datetime.fromtimestamp(ws_path.stat().st_mtime)
    days_old = (datetime.now() - mtime).days

    return {
        "exists": True,
        "stale": days_old > 3,
        "days_old": days_old,
        "files": files,
        "last_modified": mtime.isoformat()[:10],
    }


# ── Gap Detection ──

def find_untracked_commits(
    commits: List[GitCommit],
    change_log_entries: List[str],
) -> List[GitCommit]:
    """Find commits that don't have a corresponding change_log entry."""
    # Simple heuristic: check if any word from the commit message appears in change_log
    untracked = []
    cl_text = " ".join(change_log_entries).lower()

    for c in commits:
        msg_words = set(c.message.lower().split())
        # Remove common words
        msg_words -= {"feat:", "fix:", "chore:", "docs:", "the", "a", "an", "and", "or", "for", "in", "to"}
        # If fewer than 2 significant words match, likely untracked
        matches = sum(1 for w in msg_words if w in cl_text and len(w) > 3)
        if matches < 2:
            untracked.append(c)

    return untracked


# ── Report Generation ──

def generate_health_report(base_dir: Path, days: int = 14) -> str:
    """Generate the full Change Health Report."""
    repos = discover_repos(base_dir)
    lines = [
        "═══════════════════════════════════════════════════════════",
        f"  CHANGE HEALTH REPORT — {date.today().isoformat()}",
        "═══════════════════════════════════════════════════════════",
        "",
    ]

    # Repo status
    issues = 0
    lines.append("REPO STATUS:")
    for r in repos:
        cl = "✅" if r.has_change_log else "❌"
        ops = "✅" if r.has_ops_reports else "—"
        hook = "✅" if r.has_hook else "❌"
        status = f"  {r.name}: change_log {cl} | ops_reports {ops} | hook {hook}"
        if not r.has_change_log:
            status += " — ACTION: create .claude/change_log.md"
            issues += 1
        if not r.has_hook and r.repo_type != "parent":
            issues += 1
        lines.append(status)
    lines.append("")

    # Untracked commits
    all_untracked = []
    for r in repos:
        commits = get_recent_commits(r.path, r.name, days)
        cl_entries = get_change_log_entries(r.path)
        untracked = find_untracked_commits(commits, cl_entries)
        all_untracked.extend(untracked)

    if all_untracked:
        lines.append(f"UNTRACKED CHANGES ({len(all_untracked)} commits without change_log entries):")
        for c in all_untracked[:20]:  # Cap at 20
            lines.append(f"  {c.sha} {c.date} [{c.repo}] {c.message}")
        if len(all_untracked) > 20:
            lines.append(f"  ... and {len(all_untracked) - 20} more")
        issues += len(all_untracked)
    else:
        lines.append("UNTRACKED CHANGES: ✅ None — all commits have change_log coverage")
    lines.append("")

    # Orphaned runs
    all_orphans = []
    for r in repos:
        orphans = check_orphaned_runs(r.path)
        for o in orphans:
            o["repo"] = r.name
        all_orphans.extend(orphans)

    if all_orphans:
        lines.append(f"ORPHANED RUNS ({len(all_orphans)} started but never completed):")
        for o in all_orphans:
            lines.append(f"  [{o['repo']}] {o['run_day']} — {o['issue']} — started: {o['started_at']}")
        issues += len(all_orphans)
    else:
        lines.append("ORPHANED RUNS: ✅ None")
    lines.append("")

    # Working set
    for r in repos:
        ws = check_working_set(r.path)
        if ws["exists"] and ws["stale"]:
            lines.append(f"STALE STATE: working_set.txt in {r.name}")
            lines.append(f"  Last modified: {ws['last_modified']} ({ws['days_old']} days ago)")
            lines.append(f"  Files: {', '.join(ws['files'][:5])}")
            lines.append(f"  ACTION: Update for current task or clear")
            issues += 1

    # Ad crew output
    campaigns = scan_ad_crew_output(base_dir)
    if campaigns:
        unlinked = [c for c in campaigns if not c.linked_to_event]
        if unlinked:
            lines.append(f"\nAD CREW OUTPUT ({len(unlinked)} campaigns without event linkage):")
            for c in unlinked:
                lines.append(f"  {c.phase}/{c.run_id} — {len(c.files)} files — crew_result: {'✅' if c.has_crew_result else '❌'}")
            issues += len(unlinked)
    lines.append("")

    # Overall verdict
    if issues == 0:
        verdict = "🟢 Clean"
    elif issues <= 5:
        verdict = "🟡 Gaps Found"
    else:
        verdict = "🔴 Audit Failures"

    lines.insert(3, f"OVERALL: {verdict} ({issues} issues)")
    lines.insert(4, "")

    # Actions
    lines.append("═══════════════════════════════════════════════════════════")

    return "\n".join(lines)


def generate_register_csv(base_dir: Path, days: int = 30) -> str:
    """Generate unified change register as CSV."""
    repos = discover_repos(base_dir)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Timestamp", "Repo", "Change Type", "Description",
        "PRD/Event", "Risk Tier", "Approved By", "ops_report", "Status",
    ])

    for r in repos:
        commits = get_recent_commits(r.path, r.name, days)
        for c in commits:
            # Determine change type from commit message prefix
            ctype = "Code"
            if c.message.startswith("docs"):
                ctype = "Docs"
            elif c.message.startswith("chore"):
                ctype = "Config"

            writer.writerow([
                c.date, r.name, ctype, c.message,
                "", "", "", "", "Committed",
            ])

    return output.getvalue()


# ── CLI ──

def main():
    parser = argparse.ArgumentParser(description="Unified Change Register — Change Manager tool")
    parser.add_argument("--scan", action="store_true", help="Full health scan")
    parser.add_argument("--gaps", action="store_true", help="Show untracked commits only")
    parser.add_argument("--orphans", action="store_true", help="Show orphaned agent runs")
    parser.add_argument("--health", action="store_true", help="Overall health check (default)")
    parser.add_argument("--register", action="store_true", help="Output unified register as CSV")
    parser.add_argument("--days", type=int, default=14, help="Lookback days (default 14)")
    parser.add_argument("--base-dir", type=str, default=None, help="Project root directory")

    args = parser.parse_args()

    # Auto-detect base directory
    if args.base_dir:
        base = Path(args.base_dir)
    else:
        # Try Documents first, then OneDrive
        candidates = [
            Path(r"C:\Users\wole\Documents\FML"),
            Path(r"C:\Users\wole\OneDrive\FML"),
        ]
        base = next((p for p in candidates if p.exists()), candidates[0])

    if args.register:
        print(generate_register_csv(base, args.days))
    elif args.gaps:
        repos = discover_repos(base)
        for r in repos:
            commits = get_recent_commits(r.path, r.name, args.days)
            cl = get_change_log_entries(r.path)
            untracked = find_untracked_commits(commits, cl)
            if untracked:
                print(f"\n{r.name} — {len(untracked)} untracked commits:")
                for c in untracked:
                    print(f"  {c.sha} {c.date} {c.message}")
    elif args.orphans:
        repos = discover_repos(base)
        for r in repos:
            orphans = check_orphaned_runs(r.path)
            if orphans:
                print(f"\n{r.name} — {len(orphans)} orphaned runs:")
                for o in orphans:
                    print(f"  {o['run_day']} — {o['issue']}")
    else:
        # Default: full health report
        print(generate_health_report(base, args.days))


if __name__ == "__main__":
    main()
