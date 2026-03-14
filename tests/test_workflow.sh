#!/bin/bash
# 测试工作流引擎

set -e

echo "========================================"
echo "OpenClaw CLI 工作流引擎测试"
echo "========================================"

cd "$(dirname "$0")/.."

# 测试 1: 帮助命令
echo -e "\n[测试 1] 工作流帮助命令"
echo "命令：python -m openclaw workflow --help"
python -m openclaw workflow --help

# 测试 2: 列出模板
echo -e "\n[测试 2] 列出工作流模板"
echo "命令：python -m openclaw workflow list-templates"
python -m openclaw workflow list-templates

# 测试 3: 验证工作流文件
echo -e "\n[测试 3] 验证工作流 YAML 文件"
echo "命令：python -m openclaw workflow validate -f workflows/convert-document.yml"
python -m openclaw workflow validate -f workflows/convert-document.yml

# 测试 4: 从模板初始化
echo -e "\n[测试 4] 从模板初始化工作流"
echo "命令：python -m openclaw workflow init -n document-conversion -o test-workflow.yml"
python -m openclaw workflow init -n document-conversion -o test-workflow.yml
echo "生成的文件:"
cat test-workflow.yml

# 测试 5: 验证生成的工作流
echo -e "\n[测试 5] 验证生成的工作流"
echo "命令：python -m openclaw workflow validate -f test-workflow.yml --json"
python -m openclaw workflow validate -f test-workflow.yml --json

# 清理
echo -e "\n[清理] 删除测试文件"
rm -f test-workflow.yml

echo -e "\n========================================"
echo "✓ 所有测试完成!"
echo "========================================"
