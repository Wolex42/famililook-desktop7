#!/bin/bash
# Session start context — orientation for new Claude Code sessions
# ================================================================
# Prints current branch, recent commits, stash status, and open PRs
# so each session starts with full situational awareness.
#
# Usage:
#   Run at the start of any Claude Code session.
#   bash .claude/session-start.sh

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)

if [[ -z "$REPO_ROOT" ]]; then
    echo "Not inside a git repository."
    exit 0
fi

REPO_NAME=$(basename "$REPO_ROOT")

echo "========================================"
echo "  SESSION START: $REPO_NAME"
echo "  $(date '+%Y-%m-%d %H:%M')"
echo "========================================"

# Current branch
BRANCH=$(git branch --show-current 2>/dev/null || echo "detached")
echo ""
echo "Branch: $BRANCH"

# Remote tracking status
UPSTREAM=$(git rev-parse --abbrev-ref @{upstream} 2>/dev/null || echo "none")
if [[ "$UPSTREAM" != "none" ]]; then
    AHEAD=$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "?")
    BEHIND=$(git rev-list --count HEAD..@{upstream} 2>/dev/null || echo "?")
    echo "Tracking: $UPSTREAM (ahead: $AHEAD, behind: $BEHIND)"
fi

# Uncommitted changes summary
STAGED=$(git diff --cached --stat 2>/dev/null | tail -1)
UNSTAGED=$(git diff --stat 2>/dev/null | tail -1)
UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo "Working tree:"
if [[ -n "$STAGED" ]]; then
    echo "  Staged: $STAGED"
else
    echo "  Staged: clean"
fi
if [[ -n "$UNSTAGED" ]]; then
    echo "  Unstaged: $UNSTAGED"
else
    echo "  Unstaged: clean"
fi
echo "  Untracked: $UNTRACKED file(s)"

# Stash
STASH_COUNT=$(git stash list 2>/dev/null | wc -l | tr -d ' ')
if [[ "$STASH_COUNT" -gt 0 ]]; then
    echo ""
    echo "Stash: $STASH_COUNT entries"
    git stash list --format="  %gd: %s" 2>/dev/null | head -3
fi

# Recent commits (last 5)
echo ""
echo "Recent commits:"
git log --oneline -5 2>/dev/null | sed 's/^/  /'

# Sub-repos status (desktop2/4/6)
echo ""
echo "Sub-repos:"
for dir in famililook-desktop2 famililook-desktop4 famililook-desktop6; do
    if [[ -d "$REPO_ROOT/$dir/.git" ]]; then
        SUB_BRANCH=$(cd "$REPO_ROOT/$dir" && git branch --show-current 2>/dev/null || echo "?")
        SUB_DIRTY=$(cd "$REPO_ROOT/$dir" && git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
        echo "  $dir: $SUB_BRANCH ($SUB_DIRTY uncommitted)"
    fi
done

# Working set
if [[ -f "$REPO_ROOT/.claude/working_set.txt" ]]; then
    WS_COUNT=$(wc -l < "$REPO_ROOT/.claude/working_set.txt" | tr -d ' ')
    echo ""
    echo "Working set: $WS_COUNT file(s)"
    cat "$REPO_ROOT/.claude/working_set.txt" | sed 's/^/  /'
fi

echo ""
echo "========================================"
