#!/bin/bash
# Pre-commit hook for Famililook
# ================================
# Enforces regression gates before any commit.
#
# Installation:
#   Copy this file to .git/hooks/pre-commit
#   Or run: cp .claude/pre-commit-hook.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
#
# What it checks:
#   1. Frontend tests pass (npm run test:run)
#   2. Frontend build succeeds (npm run build)
#   3. E2E tests pass (optional, can be skipped with --no-verify)

set -e

echo "========================================"
echo "  PRE-COMMIT: Running Regression Gates"
echo "========================================"

# Step 0: Scan for secrets in staged files
HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$(git rev-parse --show-toplevel)/.claude"
if [[ -f "$CLAUDE_DIR/scan-secrets.sh" ]]; then
    echo ""
    echo "[0/3] Scanning for secrets..."
    if bash "$CLAUDE_DIR/scan-secrets.sh"; then
        echo "✓ Secret scan passed"
    else
        echo "✗ Secret scan FAILED — remove secrets before committing"
        exit 1
    fi
    echo ""
fi

# Detect which repo we're in
REPO_ROOT=$(git rev-parse --show-toplevel)
REPO_NAME=$(basename "$REPO_ROOT")

# Frontend checks (famililook-desktop2)
if [[ -f "$REPO_ROOT/famililook-desktop2/package.json" ]]; then
    FE_DIR="$REPO_ROOT/famililook-desktop2"
elif [[ -f "$REPO_ROOT/package.json" ]] && [[ "$REPO_NAME" == *"desktop2"* ]]; then
    FE_DIR="$REPO_ROOT"
else
    FE_DIR=""
fi

if [[ -n "$FE_DIR" ]]; then
    echo ""
    cd "$FE_DIR"

    # Use quality gate script if available (enforces quality-floor.json)
    if [[ -f "scripts/quality-gate.js" ]]; then
        echo "[FE] Running Quality Gate (unit tests + build vs quality-floor.json)..."
        if node scripts/quality-gate.js --unit-only; then
            echo "✓ Quality gate passed"
        else
            echo "✗ Quality gate FAILED — metrics below quality-floor.json"
            echo ""
            echo "Commit blocked. Run 'npm run gate:report' to see floor."
            exit 1
        fi
    else
        # Fallback: run tests + build directly
        echo "[1/2] Running Frontend Tests..."
        if npm run test:run; then
            echo "✓ Frontend tests passed"
        else
            echo "✗ Frontend tests FAILED"
            echo "Commit blocked. Fix tests before committing."
            exit 1
        fi

        echo ""
        echo "[2/2] Running Frontend Build..."
        if npm run build; then
            echo "✓ Frontend build passed"
        else
            echo "✗ Frontend build FAILED"
            echo "Commit blocked. Fix build errors before committing."
            exit 1
        fi
    fi
fi

# Backend checks (famililook-desktop3)
if [[ -f "$REPO_ROOT/famililook-desktop3/requirements.txt" ]]; then
    BE_DIR="$REPO_ROOT/famililook-desktop3"
elif [[ -f "$REPO_ROOT/requirements.txt" ]] && [[ "$REPO_NAME" == *"desktop3"* ]]; then
    BE_DIR="$REPO_ROOT"
else
    BE_DIR=""
fi

if [[ -n "$BE_DIR" ]]; then
    echo ""
    echo "[3/3] Running Backend Tests..."
    cd "$BE_DIR"

    # Use the venv python if available
    if [[ -f ".venv/Scripts/python.exe" ]]; then
        PYTHON=".venv/Scripts/python.exe"
    elif [[ -f ".venv/bin/python" ]]; then
        PYTHON=".venv/bin/python"
    else
        PYTHON="python"
    fi

    if $PYTHON -m pytest tests/ -q --tb=short; then
        echo "✓ Backend tests passed"
    else
        echo "✗ Backend tests FAILED"
        echo ""
        echo "Commit blocked. Fix tests before committing."
        exit 1
    fi
fi

echo ""
echo "========================================"
echo "  ALL GATES PASSED - Commit allowed"
echo "========================================"
exit 0
