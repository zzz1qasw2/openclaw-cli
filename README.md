# OpenClaw CLI

**Agent-Native Interface for AI Assistants**

[![Version](https://img.shields.io/badge/version-0.4.0-blue)](https://github.com/openclaw/openclaw-cli)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

**中文文档**: [README-cn.md](README-cn.md)

---

## 🎯 What is OpenClaw CLI?

OpenClaw CLI provides standardized command-line interfaces for AI assistants to interact with various software and services. Think of it as **Unix tools for the AI age**.

### Why CLI?

- **Structured & Composable** - Text commands match LLM output format
- **Self-Describing** - `--help` provides automatic documentation
- **Platform Agnostic** - Works with any AI agent (Claude Code, Cursor, etc.)
- **Deterministic** - Consistent results enable predictable agent behavior

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/openclaw/openclaw-cli.git
cd openclaw-cli

# Install in development mode
pip install -e .
```

### Verify Installation

```bash
openclaw --help
openclaw workflow --help
```

---

## 📖 Commands

### Document Operations

```bash
# Read a document (auto-detect format)
openclaw doc read --file report.md
openclaw doc read --file document.docx
openclaw doc read --file webpage.html
openclaw doc read --file manual.pdf

# Write a document
openclaw doc write --file output.md --content "# Hello"
openclaw doc write --file document.docx --content "Word content" --format docx

# Convert format
openclaw doc convert --input docx --output markdown --file report.docx
openclaw doc convert --input markdown --output html --file readme.md

# Search within document
openclaw doc search --file report.md --pattern "TODO"
openclaw doc search --file code.py --pattern "def.*test"

# Merge documents
openclaw doc merge --file intro.md --file body.md --output book.md
```

### Agent Management

```bash
# Spawn a specialist agent
openclaw agent spawn --role analyst --task "analyze codebase"
openclaw agent spawn --role writer --task "generate documentation"

# List active agents
openclaw agent list

# Send message to agent
openclaw agent send --target agent-analyst --message "Please review this"

# Batch process with Map-Reduce
openclaw agent batch-process --files "*.md" --map extract.py --reduce merge.py

# Kill an agent
openclaw agent kill --session sess_abc123
```

### Workflow Engine (NEW in v0.4.0)

```bash
# Run a workflow from YAML
openclaw workflow run -f my-workflow.yml --verbose

# Validate workflow file
openclaw workflow validate -f workflow.yml

# List available templates
openclaw workflow list-templates

# Initialize from template
openclaw workflow init -n document-conversion -o output.yml

# Create workflow interactively
openclaw workflow create -n "My Workflow" -o my-workflow.yml

# Advanced features
openclaw workflow run -f workflow.yml -v --var ENV=production
openclaw workflow demo  # Run demo workflow
```

---

## 📤 Output Modes

### Human-Readable (Default)

```bash
$ openclaw doc read --file report.md
✓ Success

Content:
# Report Title
Hello, this is the document content...
```

### JSON (For Agents)

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

## 🔧 Advanced Usage

### Set Variables from CLI

```bash
openclaw workflow run -f workflow.yml --var ENV=production --var DEBUG=true
```

### Parallel Execution

```yaml
steps:
  - name: Process file 1
    action: shell
    params:
      command: process.sh file1.md
    parallel: true
  
  - name: Process file 2
    action: shell
    params:
      command: process.sh file2.md
    parallel: true
```

### Conditional Execution

```yaml
steps:
  - name: Deploy to production
    action: shell
    params:
      command: deploy.sh
    condition: "${env} == production"
```

### Retry Mechanism

```yaml
steps:
  - name: Flaky operation
    action: shell
    params:
      command: unstable_script.sh
    retry: 3
    timeout: 60
```

---

## 🏗️ Architecture

```
openclaw-cli/
├── openclaw/
│   ├── cli.py                 # Main entry point
│   ├── commands/              # Command groups
│   │   ├── doc.py             # Document operations
│   │   ├── agent.py           # Agent management
│   │   └── workflow.py        # Workflow engine
│   ├── core/
│   │   └── document.py        # Document abstraction
│   ├── handlers/              # Format handlers
│   │   ├── markdown.py        # Markdown support
│   │   ├── text.py            # Plain text
│   │   ├── docx.py            # Word documents
│   │   ├── html.py            # HTML files
│   │   └── pdf.py             # PDF (read-only)
│   └── utils/
│       └── output.py          # Output formatting
├── workflows/                 # Example workflows
├── tests/
├── scripts/                   # Utility scripts
├── setup.py
├── requirements.txt
└── README.md
```

---

## 🧪 Development

### Run Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=openclaw tests/
```

### Code Formatting

```bash
# Format code
black openclaw/

# Lint
ruff check openclaw/
```

---

## 🤝 Contributing

Contributions welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

### Adding a New Command

1. Create command in `openclaw/commands/<command>.py`
2. Register in `openclaw/cli.py`
3. Add tests
4. Update documentation

---

## 📝 Roadmap

### Completed Phases
- [x] **Phase 1**: CLI architecture design
- [x] **Phase 2**: Multi-format document support + Agent management
- [x] **Phase 3**: Workflow engine (YAML-based)
- [x] **Phase 4**: Advanced workflow features (conditions, parallel, variables)

### Upcoming
- [ ] **Phase 5**: Enterprise features (complex conditions, variable scopes)
- [ ] **Phase 6**: Workflow marketplace
- [ ] PyPI release
- [ ] Excel CLI
- [ ] PowerPoint CLI

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🔗 Links

- **GitHub**: https://github.com/openclaw/openclaw-cli
- **OpenClaw**: https://github.com/openclaw/openclaw
- **Docs**: https://docs.openclaw.ai
- **Discord**: https://discord.com/invite/clawd

---

*Built with ❤️ by the OpenClaw Team*
# openclaw-cli
# openclaw-cli
