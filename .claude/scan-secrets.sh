#!/bin/bash
# Scan for secrets before commit
# ================================
# Catches API keys, tokens, passwords, and other secrets in staged files.
# Prevents accidental exposure like the admin key leak (audit C5).
#
# Installation:
#   Integrate into pre-commit-hook.sh or run standalone.
#   chmod +x .claude/scan-secrets.sh

set -e

echo "========================================"
echo "  SECRET SCAN: Checking staged files"
echo "========================================"

REPO_ROOT=$(git rev-parse --show-toplevel)
FOUND_SECRETS=0

# Get staged files (only added/modified, skip deleted)
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)

if [[ -z "$STAGED_FILES" ]]; then
    echo "No staged files to scan."
    echo "========================================"
    exit 0
fi

# Patterns that indicate secrets (case-insensitive where appropriate)
SECRET_PATTERNS=(
    # API keys and tokens
    'VITE_[A-Z_]*KEY\s*=\s*[^\s]+'
    'API[_-]?KEY\s*=\s*[^\s]+'
    'SECRET[_-]?KEY\s*=\s*[^\s]+'
    'ACCESS[_-]?TOKEN\s*=\s*[^\s]+'
    'AUTH[_-]?TOKEN\s*=\s*[^\s]+'
    'PRIVATE[_-]?KEY\s*=\s*[^\s]+'
    # Stripe
    'sk_live_[a-zA-Z0-9]+'
    'sk_test_[a-zA-Z0-9]+'
    'pk_live_[a-zA-Z0-9]+'
    'whsec_[a-zA-Z0-9]+'
    # AWS
    'AKIA[0-9A-Z]{16}'
    # Generic passwords
    'password\s*=\s*["\x27][^\s"'\'']{8,}'
    'passwd\s*=\s*["\x27][^\s"'\'']{8,}'
    # Connection strings
    'mongodb(\+srv)?://[^\s]+'
    'postgres(ql)?://[^\s]+'
    'mysql://[^\s]+'
    'redis://[^\s]+'
    # Raw admin key pattern (specific to FamiliLook)
    'fl-admin-[a-zA-Z0-9]+'
)

# Files to always skip
SKIP_PATTERNS='(node_modules|\.git|dist|build|\.venv|__pycache__|\.lock$|\.png$|\.jpg$|\.jpeg$|\.gif$|\.ico$|\.woff|\.ttf|\.map$|\.test\.|\.spec\.|scan-secrets\.sh)'

for file in $STAGED_FILES; do
    # Skip binary and irrelevant files
    if echo "$file" | grep -qE "$SKIP_PATTERNS"; then
        continue
    fi

    # Skip if file doesn't exist (deleted)
    if [[ ! -f "$REPO_ROOT/$file" ]]; then
        continue
    fi

    for pattern in "${SECRET_PATTERNS[@]}"; do
        MATCHES=$(grep -nEi "$pattern" "$REPO_ROOT/$file" 2>/dev/null || true)
        if [[ -n "$MATCHES" ]]; then
            # Skip matches in comments, test fixtures, and hash comparisons
            REAL_MATCHES=$(echo "$MATCHES" | grep -v '^\s*//' | grep -v '^\s*#' | grep -v '^\s*\*' | grep -v 'HASH' | grep -v 'hash' | grep -v 'example' | grep -v 'placeholder' || true)
            if [[ -n "$REAL_MATCHES" ]]; then
                echo ""
                echo "⚠ POTENTIAL SECRET in $file:"
                echo "$REAL_MATCHES" | head -3
                FOUND_SECRETS=$((FOUND_SECRETS + 1))
            fi
        fi
    done
done

echo ""
if [[ $FOUND_SECRETS -gt 0 ]]; then
    echo "========================================"
    echo "  ⚠ FOUND $FOUND_SECRETS POTENTIAL SECRET(S)"
    echo "  Review above and remove before committing."
    echo "  Use .env.local for secrets (gitignored)."
    echo "========================================"
    exit 1
else
    echo "✓ No secrets detected in staged files"
    echo "========================================"
    exit 0
fi
