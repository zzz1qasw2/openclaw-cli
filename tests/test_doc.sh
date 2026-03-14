#!/bin/bash
# OpenClaw CLI - Document Commands Test

set -e

echo "======================================"
echo "OpenClaw CLI - Document Tests"
echo "======================================"
echo ""

cd ~/.openclaw/workspace/openclaw-cli

# Test 1: Read markdown
echo "Test 1: Read markdown file"
python3 -m openclaw.cli doc read --file test.md | head -5
echo "✓ Passed"
echo ""

# Test 2: Read with JSON
echo "Test 2: Read with JSON output"
python3 -m openclaw.cli doc read --file test.md --json | head -10
echo "✓ Passed"
echo ""

# Test 3: Write markdown
echo "Test 3: Write markdown file"
python3 -m openclaw.cli doc write --file test_output.md --content "# Test\n\nContent here"
echo "✓ Passed"
echo ""

# Test 4: Search
echo "Test 4: Search in document"
python3 -m openclaw.cli doc search --file test.md --pattern "TODO"
echo "✓ Passed"
echo ""

# Test 5: Merge
echo "Test 5: Merge documents"
python3 -m openclaw.cli doc merge --file test.md --file test_output.md --output merged_test.md
echo "✓ Passed"
echo ""

# Test 6: Convert markdown to text
echo "Test 6: Convert markdown to text"
python3 -m openclaw.cli doc convert --input markdown --output text --file test.md --output-file test.txt
echo "✓ Passed"
echo ""

# Cleanup
rm -f test_output.md merged_test.md test.txt

echo "======================================"
echo "All tests completed!"
echo "======================================"
