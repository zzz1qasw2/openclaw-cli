#!/bin/bash
# GitHub Release Checklist for OpenClaw CLI

set -e

echo "=========================================="
echo "OpenClaw CLI - GitHub Release Checklist"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    exit 1
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "1. Checking for sensitive information..."
echo "----------------------------------------"

# Check for API keys and tokens
if grep -r "sk-[a-zA-Z0-9]\{20,\}" --include="*.py" --include="*.yml" --include="*.json" . 2>/dev/null | grep -v ".git" | grep -v "Binary"; then
    check_fail "Found potential API keys!"
else
    check_pass "No API keys found"
fi

# Check for .env files
if [ -f ".env" ]; then
    check_fail ".env file exists! Add to .gitignore"
else
    check_pass "No .env file"
fi

# Check for local config
if [ -f "config.local.json" ]; then
    check_fail "config.local.json exists!"
else
    check_pass "No local config files"
fi

echo ""
echo "2. Checking required files..."
echo "----------------------------------------"

# Required files
required_files=(
    "README.md"
    "README-cn.md"
    "LICENSE"
    "setup.py"
    "requirements.txt"
    ".gitignore"
    "CHANGELOG.md"
    "CHANGELOG-cn.md"
    "CONTRIBUTING.md"
    "CONTRIBUTING-cn.md"
    "env.example"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        check_pass "$file exists"
    else
        check_fail "$file missing!"
    fi
done

echo ""
echo "3. Checking Python code quality..."
echo "----------------------------------------"

# Check if black is available
if command -v black &> /dev/null; then
    if black --check openclaw/ 2>/dev/null; then
        check_pass "Code is formatted (Black)"
    else
        check_warn "Code needs formatting. Run: black openclaw/"
    fi
else
    check_warn "Black not installed. Install with: pip install black"
fi

# Check if ruff is available
if command -v ruff &> /dev/null; then
    if ruff check openclaw/ 2>/dev/null; then
        check_pass "No linting errors (Ruff)"
    else
        check_warn "Linting errors found. Run: ruff check openclaw/"
    fi
else
    check_warn "Ruff not installed. Install with: pip install ruff"
fi

echo ""
echo "4. Checking documentation..."
echo "----------------------------------------"

# Check README has installation instructions
if grep -q "pip install" README.md; then
    check_pass "README has installation instructions"
else
    check_warn "README missing installation instructions"
fi

# Check README has usage examples
if grep -q "openclaw" README.md; then
    check_pass "README has usage examples"
else
    check_warn "README missing usage examples"
fi

echo ""
echo "5. Checking version consistency..."
echo "----------------------------------------"

# Extract version from setup.py
setup_version=$(grep 'version=' setup.py | head -1 | sed 's/.*version="\([^"]*\)".*/\1/')

# Extract version from CHANGELOG (skip [Unreleased])
changelog_version=$(grep "^## \[" CHANGELOG.md | grep -v Unreleased | head -1 | grep -oE "[0-9]+\.[0-9]+\.[0-9]+" || echo "0.0.0")

if [ "$setup_version" = "$changelog_version" ]; then
    check_pass "Version consistent: $setup_version"
else
    check_warn "Version mismatch: setup.py=$setup_version, CHANGELOG=$changelog_version"
fi

echo ""
echo "6. Git status..."
echo "----------------------------------------"

if git status --porcelain 2>/dev/null | grep -v ".gitignore"; then
    check_warn "Uncommitted changes exist"
    echo ""
    echo "Uncommitted files:"
    git status --porcelain
else
    check_pass "Working tree clean"
fi

echo ""
echo "=========================================="
echo "Pre-flight check complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Fix any issues marked with ${RED}✗${NC}"
echo "2. Review warnings marked with ${YELLOW}⚠${NC}"
echo "3. Commit all changes"
echo "4. Create tag: git tag v$setup_version"
echo "5. Push: git push && git push --tags"
echo "6. Create GitHub release"
echo ""
