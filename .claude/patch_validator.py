#!/usr/bin/env python3
"""
Patch Validator for Claude Code
================================
Validates that edit operations are correct BEFORE applying.

Checks:
    1. File exists
    2. old_string is found in file
    3. old_string appears exactly once (unique match)
    4. old_string is not hallucinated (fuzzy match detection)

Usage:
    python .claude/patch_validator.py <file_path> --old "text to find" --new "replacement"
"""

import sys
import argparse
import difflib
from pathlib import Path
from typing import Tuple, List, Optional


def find_occurrences(content: str, search: str) -> List[int]:
    """Find all occurrences of search string in content."""
    occurrences = []
    start = 0
    while True:
        idx = content.find(search, start)
        if idx == -1:
            break
        occurrences.append(idx)
        start = idx + 1
    return occurrences


def find_similar_lines(content: str, search: str, threshold: float = 0.8) -> List[Tuple[int, str, float]]:
    """Find lines similar to search string (for hallucination detection)."""
    search_lines = search.strip().split('\n')
    content_lines = content.split('\n')

    if not search_lines:
        return []

    first_search = search_lines[0].strip()
    if not first_search:
        return []

    similar = []
    for i, line in enumerate(content_lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        ratio = difflib.SequenceMatcher(None, first_search, line_stripped).ratio()
        if ratio >= threshold:
            similar.append((i + 1, line, ratio))

    return sorted(similar, key=lambda x: -x[2])[:5]


def validate_edit(file_path: str, old_string: str, new_string: str) -> Tuple[bool, str, Optional[str]]:
    """Validate an edit operation. Returns (valid, message, suggestion)."""
    path = Path(file_path)

    if not path.exists():
        return (False, f"File not found: {file_path}", None)

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return (False, f"Cannot read file: {e}", None)

    occurrences = find_occurrences(content, old_string)

    if len(occurrences) == 0:
        similar = find_similar_lines(content, old_string)
        if similar:
            suggestion = "Did you mean one of these?\n"
            for line_num, line, score in similar[:3]:
                suggestion += f"  Line {line_num} ({score:.0%}): {line[:80]}\n"
            return (False, "old_string NOT FOUND. LLM may have hallucinated content.", suggestion)
        return (False, "old_string NOT FOUND in file.", None)

    if len(occurrences) > 1:
        positions = ", ".join(str(o) for o in occurrences[:5])
        return (False, f"old_string found {len(occurrences)} times. Must be unique.", None)

    if old_string == new_string:
        return (False, "old_string and new_string are identical (no-op)", None)

    match_pos = occurrences[0]
    line_num = content[:match_pos].count('\n') + 1
    return (True, f"VALID: Found at line {line_num}. Edit will succeed.", None)


def main():
    parser = argparse.ArgumentParser(description="Validate Claude Code edit operations")
    parser.add_argument("file_path", help="Path to file being edited")
    parser.add_argument("--old", required=True, help="old_string to find")
    parser.add_argument("--new", required=True, help="new_string replacement")

    args = parser.parse_args()
    valid, message, suggestion = validate_edit(args.file_path, args.old, args.new)

    print(f"[{'VALID' if valid else 'INVALID'}] {message}")
    if suggestion:
        print(f"\n{suggestion}")
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()