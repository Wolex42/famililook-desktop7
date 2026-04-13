#!/usr/bin/env python3
"""
FMEA Regression Coverage Checker
---------------------------------
Scans test files across desktop2/4/6 for @dfmea markers and verifies
that every fixed FMEA ID has at least one regression test covering it.

Exit 0: All fixed FMs are covered by tests.
Exit 1: One or more fixed FMs lack regression test coverage.
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

# ── Fixed FMEA IDs from sprints ──────────────────────────────────────────────

FIXED_FMEA_IDS = {
    # Sprint 0A
    "FM-001", "FM-002", "FM-003", "FM-004", "FM-005",
    # Sprint 0B
    "FP-001", "FP-003", "FP-006", "FP-007", "FL-003", "FL-004", "FL-006",
    # Sprint 1
    "FL-024", "FL-002", "GAP-01", "FM-012", "FL-009", "GAP-02",
    # Sprint 2
    "FL-007", "FP-015", "DFMEA-FM-16", "FM-006", "FM-009", "DFMEA-FM-05",
}

# ── Scan paths (relative to repo root) ───────────────────────────────────────

SCAN_GLOBS = [
    "famililook-desktop2/tests/**/*.test.*",
    "famililook-desktop2/src/test/**/*.test.*",
    "famililook-desktop4/tests/**/*.test.*",
    "famililook-desktop6/tests/**/*.test.*",
    "famililook-desktop2/e2e/**/*.spec.*",
]

# ── Marker patterns ──────────────────────────────────────────────────────────
# Matches:  @dfmea FM-001   or   @dfmea FMEA-FM-16   or   @dfmea DFMEA-FM-05
DFMEA_PATTERN = re.compile(r"@dfmea\s+((?:DFMEA-)?(?:FM|FP|FL|GAP)-\d+)", re.IGNORECASE)

# Pattern to extract the nearest test/it/describe name after the marker
TEST_NAME_PATTERN = re.compile(
    r"""(?:test|it|describe)\s*\(\s*['"`]([^'"`]+)['"`]""",
    re.IGNORECASE,
)


def find_repo_root() -> Path:
    """Walk up from script location to find the FML repo root."""
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / "famililook-desktop2").is_dir():
        return candidate
    # Fallback: try CWD
    cwd = Path.cwd()
    if (cwd / "famililook-desktop2").is_dir():
        return cwd
    print(f"ERROR: Cannot locate repo root from {candidate} or {cwd}", file=sys.stderr)
    sys.exit(2)


def collect_test_files(repo_root: Path) -> list[Path]:
    """Expand SCAN_GLOBS into a deduplicated list of existing test files."""
    files: set[Path] = set()
    for pattern in SCAN_GLOBS:
        for path in repo_root.glob(pattern):
            if path.is_file():
                files.add(path)
    return sorted(files)


def extract_markers(file_path: Path) -> list[tuple[str, str]]:
    """
    Return list of (fm_id, test_name) tuples found in the file.
    fm_id is normalised to uppercase.
    """
    results = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return results

    lines = content.splitlines()
    for i, line in enumerate(lines):
        for match in DFMEA_PATTERN.finditer(line):
            fm_id = match.group(1).upper()
            # Look ahead up to 5 lines for the test name
            test_name = "(unnamed test)"
            for look in range(i, min(i + 6, len(lines))):
                name_match = TEST_NAME_PATTERN.search(lines[look])
                if name_match:
                    test_name = name_match.group(1)
                    break
            results.append((fm_id, test_name))
    return results


def main() -> int:
    repo_root = find_repo_root()
    print(f"Repo root: {repo_root}")
    print(f"Fixed FMEA IDs: {len(FIXED_FMEA_IDS)}")
    print()

    # ── Collect test files ────────────────────────────────────────────────
    test_files = collect_test_files(repo_root)
    print(f"Test files found: {len(test_files)}")

    # ── Build coverage map: FM_ID -> [(file, test_name)] ──────────────────
    coverage_map: dict[str, list[tuple[str, str]]] = defaultdict(list)
    all_referenced_ids: set[str] = set()

    for tf in test_files:
        markers = extract_markers(tf)
        for fm_id, test_name in markers:
            rel_path = str(tf.relative_to(repo_root))
            coverage_map[fm_id].append((rel_path, test_name))
            all_referenced_ids.add(fm_id)

    # ── Report ────────────────────────────────────────────────────────────
    covered = []
    uncovered = []
    orphaned = []

    # Check each fixed FM
    for fm_id in sorted(FIXED_FMEA_IDS):
        if fm_id in coverage_map:
            covered.append(fm_id)
        else:
            uncovered.append(fm_id)

    # Check for orphaned markers (reference an FM not in the fixed list)
    for fm_id in sorted(all_referenced_ids):
        if fm_id not in FIXED_FMEA_IDS:
            orphaned.append(fm_id)

    # ── Print results ─────────────────────────────────────────────────────
    print("=" * 60)
    print("FMEA REGRESSION COVERAGE REPORT")
    print("=" * 60)

    if covered:
        print(f"\nCOVERED ({len(covered)}/{len(FIXED_FMEA_IDS)}):")
        for fm_id in covered:
            tests = coverage_map[fm_id]
            for file_path, test_name in tests:
                print(f"  {fm_id} -> {file_path} :: {test_name}")

    if uncovered:
        print(f"\nUNCOVERED ({len(uncovered)}/{len(FIXED_FMEA_IDS)}) -- WARNING:")
        for fm_id in uncovered:
            print(f"  {fm_id} -- no regression test found")

    if orphaned:
        print(f"\nORPHANED ({len(orphaned)}) -- INFO:")
        for fm_id in orphaned:
            tests = coverage_map[fm_id]
            for file_path, test_name in tests:
                print(f"  {fm_id} -> {file_path} :: {test_name}")

    print()
    print(f"Summary: {len(covered)} covered, {len(uncovered)} uncovered, {len(orphaned)} orphaned")

    if uncovered:
        print("\nRESULT: FAIL -- uncovered FMEA fixes need regression tests")
        return 1
    else:
        print("\nRESULT: PASS -- all fixed FMEA IDs have regression test coverage")
        return 0


if __name__ == "__main__":
    sys.exit(main())
