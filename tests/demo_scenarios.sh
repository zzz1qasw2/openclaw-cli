#!/bin/bash
# OpenClaw CLI - 实际使用场景演示

set -e

echo "========================================"
echo "OpenClaw CLI - 实际使用场景演示"
echo "========================================"
echo ""

cd ~/.openclaw/workspace/openclaw-cli

# 使用 python3 -m 方式运行，避免与系统 openclaw 命令冲突
CLI="python3 -m openclaw.cli"

# 场景 1: 项目文档自动化
echo "📁 场景 1: 项目文档自动化"
echo "----------------------------------------"

# 创建项目文档结构
echo "步骤 1: 创建 README"
$CLI doc write --file README_demo.md --content "# 项目演示\n\n这是一个 OpenClaw CLI 演示项目。\n\n## 功能\n- 文档读取\n- 文档写入\n- 格式转换\n- 内容搜索\n"

echo "步骤 2: 创建 CHANGELOG"
$CLI doc write --file CHANGELOG_demo.md --content "# 变更日志\n\n## v0.3.0\n- 新增 Word 支持\n- 新增 HTML 支持\n- 新增 PDF 读取\n- 多 Agent 协同\n\n## v0.2.0\n- 通用文档 CLI\n- 基础命令实现\n"

echo "步骤 3: 合并为完整文档"
$CLI doc merge --file README_demo.md --file CHANGELOG_demo.md --output PROJECT_DOC.md

echo "步骤 4: 搜索版本信息"
$CLI doc search --file PROJECT_DOC.md --pattern "v0\.[0-9]"

echo ""
echo "✓ 场景 1 完成"
echo ""


# 场景 2: 代码文档提取
echo "📁 场景 2: 代码文档提取"
echo "----------------------------------------"

# 创建示例代码文件
echo "步骤 1: 创建示例 Python 文件"
cat > example_code.py << 'EOF'
# 示例模块
# 作者：Demo
# 版本：1.0

def hello():
    """打招呼函数"""
    print("Hello, World!")

def add(a, b):
    """加法函数"""
    return a + b

# TODO: 实现减法函数
# TODO: 添加错误处理
EOF

echo "步骤 2: 提取所有函数定义"
$CLI doc search --file example_code.py --pattern "def.*:"

echo "步骤 3: 提取所有 TODO"
$CLI doc search --file example_code.py --pattern "TODO" --json | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'找到 {d[\"data\"][\"total_matches\"]} 个 TODO 项')"

echo ""
echo "✓ 场景 2 完成"
echo ""


# 场景 3: 多格式工作流
echo "📁 场景 3: 多格式工作流"
echo "----------------------------------------"

echo "步骤 1: 创建 Markdown 报告"
$CLI doc write --file report.md --content "# 周报\n\n## 完成工作\n- Phase 1: 核心功能\n- Phase 2: 格式扩展\n\n## 下周计划\n- Phase 3: 高级功能\n"

echo "步骤 2: 转为纯文本（用于邮件）"
$CLI doc convert --input markdown --output text --file report.md --output-file report.txt

echo "步骤 3: 转为 HTML（用于网页）"
$CLI doc convert --input markdown --output html --file report.md --output-file report.html

echo "步骤 4: 查看各格式大小"
echo "Markdown: $(wc -c < report.md) bytes"
echo "Text: $(wc -c < report.txt) bytes"
echo "HTML: $(wc -c < report.html) bytes"

echo ""
echo "✓ 场景 3 完成"
echo ""


# 场景 4: 批量文档处理
echo "📁 场景 4: 批量文档处理（模拟）"
echo "----------------------------------------"

# 创建多个章节文件
for i in 1 2 3; do
    $CLI doc write --file chapter_$i.md --content "# 第$i章\n\n这是第$i章的内容。\n\n## 要点\n- 要点 1\n- 要点 2\n"
done

echo "步骤 1: 创建 3 个章节文件"
ls -la chapter_*.md | awk '{print "  " $9 " - " $5 " bytes"}'

echo "步骤 2: 合并为完整书籍"
$CLI doc merge --file chapter_1.md --file chapter_2.md --file chapter_3.md --output book.md

echo "步骤 3: 统计总章节数"
$CLI doc search --file book.md --pattern "^# 第" --json | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  总共 {d[\"data\"][\"total_matches\"]} 章')"

echo ""
echo "✓ 场景 4 完成"
echo ""


# 清理
rm -f README_demo.md CHANGELOG_demo.md PROJECT_DOC.md
rm -f example_code.py
rm -f report.md report.txt report.html
rm -f chapter_*.md book.md

echo "========================================"
echo "所有场景演示完成!"
echo "========================================"
echo ""
echo "💡 提示："
echo "  - 以上所有命令都可以用于真实项目"
echo "  - JSON 输出便于与其他工具集成"
echo "  - agent 命令需要在 OpenClaw 环境中运行"
