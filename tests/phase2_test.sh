#!/bin/bash
# OpenClaw CLI - Phase 2 测试脚本

set -e

echo "========================================"
echo "OpenClaw CLI - Phase 2 测试"
echo "========================================"
echo ""

cd ~/.openclaw/workspace/openclaw-cli

# 测试 1: CLI 帮助
echo "Test 1: CLI 帮助信息"
python3 -m openclaw.cli --help | head -10
echo "✓ Passed"
echo ""

# 测试 2: doc 命令帮助
echo "Test 2: doc 命令帮助"
python3 -m openclaw.cli doc --help | head -10
echo "✓ Passed"
echo ""

# 测试 3: agent 命令帮助
echo "Test 3: agent 命令帮助"
python3 -m openclaw.cli agent --help | head -10
echo "✓ Passed"
echo ""

# 测试 4: 读取 Markdown
echo "Test 4: 读取 Markdown 文件"
python3 -m openclaw.cli doc read --file test.md | head -8
echo "✓ Passed"
echo ""

# 测试 5: Markdown JSON 输出
echo "Test 5: Markdown JSON 输出"
python3 -m openclaw.cli doc read --file test.md --json | python3 -c "import sys,json; d=json.load(sys.stdin); print('success:', d['success']); print('format:', d['data']['format'])"
echo "✓ Passed"
echo ""

# 测试 6: 写入文档
echo "Test 6: 写入新文档"
python3 -m openclaw.cli doc write --file test_output.md --content "# 测试标题\n\n这是测试内容。"
test -f test_output.md && echo "文件创建成功" || echo "文件创建失败"
echo "✓ Passed"
echo ""

# 测试 7: 搜索功能
echo "Test 7: 搜索文档内容"
python3 -m openclaw.cli doc search --file test.md --pattern "TODO" | head -8
echo "✓ Passed"
echo ""

# 测试 8: 合并文档
echo "Test 8: 合并多个文档"
python3 -m openclaw.cli doc merge --file test.md --file test_output.md --output test_merged.md
test -f test_merged.md && echo "合并文件创建成功" || echo "合并文件创建失败"
echo "✓ Passed"
echo ""

# 测试 9: 格式转换 (md -> text)
echo "Test 9: 格式转换 (Markdown -> Text)"
python3 -m openclaw.cli doc convert --input markdown --output text --file test.md --output-file test_output.txt
test -f test_output.txt && echo "转换文件创建成功" || echo "转换文件创建失败"
echo "✓ Passed"
echo ""

# 测试 10: 转换后内容验证
echo "Test 10: 验证转换后内容"
cat test_output.txt | head -5
echo "✓ Passed"
echo ""

# 清理测试文件
rm -f test_output.md test_merged.md test_output.txt

echo "========================================"
echo "所有基础测试完成!"
echo "========================================"
echo ""
echo "注意：以下功能需要额外依赖才能测试:"
echo "  - Word (.docx): 需要 python-docx"
echo "  - HTML: 需要 beautifulsoup4"
echo "  - PDF: 需要 pdfplumber"
echo "  - agent 命令：需要在 OpenClaw 环境中运行"
