# OpenClaw CLI

**AI 智能体的命令行接口**

[![Version](https://img.shields.io/badge/version-0.4.0-blue)](https://github.com/openclaw/openclaw-cli)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

**English Documentation**: [README.md](README.md)

---

## 🎯 什么是 OpenClaw CLI？

OpenClaw CLI 为 AI 智能体提供标准化的命令行接口，用于与各种软件和服务交互。可以把它想象成 **AI 时代的 Unix 工具**。

### 为什么选择 CLI？

- **结构化且可组合** - 文本命令与 LLM 输出格式天然匹配
- **自描述** - `--help` 提供自动文档
- **平台无关** - 适用于任何 AI 智能体（Claude Code、Cursor 等）
- **确定性** - 一致的结果支持可预测的智能体行为

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/openclaw/openclaw-cli.git
cd openclaw-cli

# 以开发模式安装
pip install -e .
```

### 验证安装

```bash
openclaw --help
openclaw workflow --help
```

---

## 📖 命令

### 文档操作

```bash
# 读取文档（自动检测格式）
openclaw doc read --file report.md
openclaw doc read --file document.docx
openclaw doc read --file webpage.html
openclaw doc read --file manual.pdf

# 写入文档
openclaw doc write --file output.md --content "# Hello"
openclaw doc write --file document.docx --content "Word content" --format docx

# 格式转换
openclaw doc convert --input docx --output markdown --file report.docx
openclaw doc convert --input markdown --output html --file readme.md

# 搜索文档内容
openclaw doc search --file report.md --pattern "TODO"
openclaw doc search --file code.py --pattern "def.*test"

# 合并文档
openclaw doc merge --file intro.md --file body.md --output book.md
```

### 智能体管理

```bash
# 生成专业智能体
openclaw agent spawn --role analyst --task "analyze codebase"
openclaw agent spawn --role writer --task "generate documentation"

# 列出活跃智能体
openclaw agent list

# 发送消息给智能体
openclaw agent send --target agent-analyst --message "Please review this"

# 使用 Map-Reduce 批量处理
openclaw agent batch-process --files "*.md" --map extract.py --reduce merge.py

# 终止智能体
openclaw agent kill --session sess_abc123
```

### 工作流引擎（v0.4.0 新增）

```bash
# 从 YAML 运行工作流
openclaw workflow run -f my-workflow.yml --verbose

# 验证工作流文件
openclaw workflow validate -f workflow.yml

# 列出可用模板
openclaw workflow list-templates

# 从模板初始化
openclaw workflow init -n document-conversion -o output.yml

# 交互式创建工作流
openclaw workflow create -n "My Workflow" -o my-workflow.yml

# 高级功能
openclaw workflow run -f workflow.yml -v --var ENV=production
openclaw workflow demo  # 运行演示工作流
```

---

## 📤 输出模式

### 人类可读（默认）

```bash
$ openclaw doc read --file report.md
✓ Success

Content:
# Report Title
Hello, this is the document content...
```

### JSON（智能体友好）

```bash
$ openclaw doc read --file report.md --json
{
  "success": true,
  "data": {
    "content": "# Report Title\nHello, this is the document content...",
    "metadata": {...}
  },
  "command": "doc read"
}
```

---

## 🔧 高级用法

### 从 CLI 设置变量

```bash
openclaw workflow run -f workflow.yml --var ENV=production --var DEBUG=true
```

### 并行执行

```yaml
steps:
  - name: 处理文件 1
    action: shell
    params:
      command: process.sh file1.md
    parallel: true
  
  - name: 处理文件 2
    action: shell
    params:
      command: process.sh file2.md
    parallel: true
```

### 条件执行

```yaml
steps:
  - name: 部署到生产环境
    action: shell
    params:
      command: deploy.sh
    condition: "${env} == production"
```

### 重试机制

```yaml
steps:
  - name: 不稳定的操作
    action: shell
    params:
      command: unstable_script.sh
    retry: 3
    timeout: 60
```

---

## 🏗️ 架构

```
openclaw-cli/
├── openclaw/
│   ├── cli.py                 # 主入口
│   ├── commands/              # 命令组
│   │   ├── doc.py             # 文档操作
│   │   ├── agent.py           # 智能体管理
│   │   └── workflow.py        # 工作流引擎
│   ├── core/
│   │   └── document.py        # 文档抽象
│   ├── handlers/              # 格式处理器
│   │   ├── markdown.py        # Markdown 支持
│   │   ├── text.py            # 纯文本
│   │   ├── docx.py            # Word 文档
│   │   ├── html.py            # HTML 文件
│   │   └── pdf.py             # PDF（只读）
│   └── utils/
│       └── output.py          # 输出格式化
├── workflows/                 # 示例工作流
├── tests/
├── scripts/                   # 工具脚本
├── setup.py
├── requirements.txt
└── README.md
```

---

## 🧪 开发

### 运行测试

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 带覆盖率运行
pytest --cov=openclaw tests/
```

### 代码格式化

```bash
# 格式化代码
black openclaw/

# 语法检查
ruff check openclaw/
```

---

## 🤝 贡献

欢迎贡献！请先阅读 [贡献指南](CONTRIBUTING.md)。

### 添加新命令

1. 在 `openclaw/commands/<command>.py` 创建命令
2. 在 `openclaw/cli.py` 注册
3. 添加测试
4. 更新文档

---

## 📝 路线图

### 已完成阶段
- [x] **Phase 1**: CLI 架构设计
- [x] **Phase 2**: 多格式文档支持 + 智能体管理
- [x] **Phase 3**: 工作流引擎（基于 YAML）
- [x] **Phase 4**: 高级工作流功能（条件/并行/变量）

### 即将推出
- [ ] **Phase 5**: 企业级功能（复杂条件、变量作用域）
- [ ] **Phase 6**: 工作流市场
- [ ] PyPI 发布
- [ ] Excel CLI
- [ ] PowerPoint CLI

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

---

## 🔗 链接

- **GitHub**: https://github.com/openclaw/openclaw-cli
- **OpenClaw**: https://github.com/openclaw/openclaw
- **文档**: https://docs.openclaw.ai
- **Discord**: https://discord.com/invite/clawd

---

*由 OpenClaw Team 用 ❤️ 构建*
