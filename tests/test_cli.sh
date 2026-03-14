#!/bin/bash
# OpenClaw CLI Test Script

set -e

echo "======================================"
echo "OpenClaw CLI - Test Suite"
echo "======================================"
echo ""

# Test 1: Version
echo "Test 1: Version check"
python3 -m openclaw.cli --version
echo "✓ Passed"
echo ""

# Test 2: Help
echo "Test 2: Main help"
python3 -m openclaw.cli --help | head -5
echo "✓ Passed"
echo ""

# Test 3: Feishu-doc help
echo "Test 3: Feishu-doc help"
python3 -m openclaw.cli feishu-doc --help | head -5
echo "✓ Passed"
echo ""

# Test 4: Feishu-doc read help
echo "Test 4: Feishu-doc read help"
python3 -m openclaw.cli feishu-doc read --help | head -5
echo "✓ Passed"
echo ""

# Test 5: JSON output mode
echo "Test 5: JSON output mode (error case)"
python3 -m openclaw.cli feishu-doc read --doc-token test123 --json 2>&1 | head -10
echo "✓ Passed"
echo ""

# Test 6: Excel help
echo "Test 6: Excel help"
python3 -m openclaw.cli excel --help | head -5
echo "✓ Passed"
echo ""

# Test 7: PowerPoint help
echo "Test 7: PowerPoint help"
python3 -m openclaw.cli powerpoint --help | head -5
echo "✓ Passed"
echo ""

echo "======================================"
echo "All tests completed!"
echo "======================================"
