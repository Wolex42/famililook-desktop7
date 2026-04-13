#!/usr/bin/env python3
# STATUS: ADVISORY ONLY — not invoked by pre-commit hook or any automation.
# This script is retired as active enforcement as of 2026-04-10.
# Governance is enforced by: diff preview + CEO approval + pre-commit hook (tests + build).
# Do not rely on this script to block edits. Update working_set.txt for reference only.

"""
Scope Validator for Claude Code
================================
Enforces file access controls similar to ops_agents/tools_readonly.py

Usage:
    python .claude/validate_scope.py <file_path> [--mode read|edit]

Returns:
    Exit 0 = ALLOWED
    Exit 1 = BLOCKED (with reason)
    Exit 2 = REQUIRES_APPROVAL (backend file)
"""

import sys
import os
import json
from pathlib import Path

# =============================================================================
# CONFIGURATION (matches guardrails.json)
# =============================================================================

# Always blocked - secrets, credentials, sensitive files
ALWAYS_BLOCKED = (
    ".env",
    ".pem",
    ".key",
    "id_rsa",
    "id_ed25519",
    "credentials",
    "secret",
    "token",
    "apikey",
    "password",
)

# Always allowed - governance files that must never be blocked.
# Added 2026-04-10 to fix the CLAUDE.md / validator contradiction:
# CLAUDE.md Step 5 of the pre-edit checklist mandates change_log.md updates every session,
# but this validator was blocking them whenever working_set.txt was non-empty (since
# change_log.md was never in any working_set entry). The contradiction broke governance
# discipline for Sessions B/C/D/E. Validator is now ADVISORY ONLY (see header comment).
ALWAYS_ALLOWED = (
    ".claude/change_log.md",
    ".claude/working_set.txt",
)

# Blocked fragments - build output, backups, vendor
BLOCKED_FRAGMENTS = (
    "node_modules",
    "dist",
    "/build/",
    "/build",
    ".git",
    "__pycache__",
    ".cache",
    "backup",
    "bkup",
    "bckp",
    ".bak",
    "legacy",
    "archive",
)

# Backend paths - require explicit approval
BACKEND_PATHS = (
    "famililook-desktop3/",
    "app/",
    ".py",
)

# Frontend allowlist - safe to modify
FRONTEND_ALLOWLIST = (
    "src/",
    "public/",
    "tests/",
    "e2e/",
)

# Ops reports - change audit trail (like ops_agents)
OPS_REPORTS_ALLOWLIST = (
    "download/ops_reports/",
    "ops_reports/",
)

# Config files - allowed but careful
CONFIG_ALLOWLIST = (
    "package.json",
    "tsconfig.json",
    "vite.config",
    "vitest.config",
    "playwright.config",
    "tailwind.config",
)

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def normalize_path(path: str) -> str:
    """Normalize path separators and case for comparison."""
    return path.replace("\\", "/").lower()


def has_fragment(path: str, fragments: tuple) -> bool:
    """Check if any fragment appears in the path."""
    path_lower = normalize_path(path)
    return any(f.lower() in path_lower for f in fragments)


def is_backend_file(path: str) -> bool:
    """Check if file is a backend file requiring approval."""
    path_norm = normalize_path(path)
    return any(be.lower() in path_norm for be in BACKEND_PATHS)


def is_frontend_allowed(path: str) -> bool:
    """Check if file is in frontend allowlist."""
    path_norm = normalize_path(path)
    return any(path_norm.startswith(fe.lower()) or f"/{fe.lower()}" in path_norm
               for fe in FRONTEND_ALLOWLIST)


def is_config_file(path: str) -> bool:
    """Check if file is an allowed config file."""
    path_norm = normalize_path(path)
    return any(cfg.lower() in path_norm for cfg in CONFIG_ALLOWLIST)


def is_ops_report(path: str) -> bool:
    """Check if file is in ops_reports folder (change audit trail)."""
    path_norm = normalize_path(path)
    return any(ops.lower() in path_norm for ops in OPS_REPORTS_ALLOWLIST)


def load_working_set() -> set:
    """Load working set file if it exists."""
    working_set_path = Path(__file__).parent / "working_set.txt"
    if not working_set_path.exists():
        return set()

    files = set()
    for line in working_set_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            files.add(normalize_path(line))
    return files


def validate_file(path: str, mode: str = "edit") -> tuple:
    """
    Validate if a file can be accessed.

    Returns:
        (status, message) where status is:
        - "ALLOWED" - file can be accessed
        - "BLOCKED" - file is blocked
        - "REQUIRES_APPROVAL" - needs explicit user approval
    """
    path_norm = normalize_path(path)

    # 1. Check always-blocked (secrets, credentials)
    if has_fragment(path, ALWAYS_BLOCKED):
        return ("BLOCKED", f"Sensitive file pattern detected: {path}")

    # 1b. Check always-allowed (governance files — never blocked except for security above)
    if any(allow.lower() in path_norm for allow in ALWAYS_ALLOWED):
        return ("ALLOWED", f"Governance file (always allowed): {path}")

    # 2. Check blocked fragments (node_modules, dist, etc.)
    if has_fragment(path, BLOCKED_FRAGMENTS):
        return ("BLOCKED", f"Blocked directory/pattern: {path}")

    # 3. Check working set (if defined, restricts to explicit list)
    working_set = load_working_set()
    in_working_set = False
    if working_set:
        if path_norm in working_set or any(path_norm.startswith(ws) or ws in path_norm for ws in working_set):
            in_working_set = True
        else:
            return ("BLOCKED", f"Not in working set: {path}")

    # 4. Check if backend file (requires approval for edit)
    if mode == "edit" and is_backend_file(path):
        return ("REQUIRES_APPROVAL", f"Backend file requires developer approval: {path}")

    # 4b. If in working set and not backend, allow it
    if in_working_set:
        return ("ALLOWED", f"File in working set: {path}")

    # 5. Check frontend allowlist
    if is_frontend_allowed(path):
        return ("ALLOWED", f"Frontend file allowed: {path}")

    # 6. Check config files
    if is_config_file(path):
        return ("ALLOWED", f"Config file allowed: {path}")

    # 7. Check ops_reports folder (change audit trail)
    if is_ops_report(path):
        return ("ALLOWED", f"Ops report allowed: {path}")

    # 8. Read mode is more permissive
    if mode == "read":
        return ("ALLOWED", f"Read access allowed: {path}")

    # 9. Default: block unknown files for edit
    return ("BLOCKED", f"File not in allowlist: {path}")


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_scope.py <file_path> [--mode read|edit]")
        sys.exit(1)

    file_path = sys.argv[1]
    mode = "edit"  # default

    if "--mode" in sys.argv:
        idx = sys.argv.index("--mode")
        if idx + 1 < len(sys.argv):
            mode = sys.argv[idx + 1]

    status, message = validate_file(file_path, mode)

    print(f"[{status}] {message}")

    if status == "ALLOWED":
        sys.exit(0)
    elif status == "BLOCKED":
        sys.exit(1)
    elif status == "REQUIRES_APPROVAL":
        sys.exit(2)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()