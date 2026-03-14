# OpenClaw CLI - 快速开始指南

## 🚀 安装

```bash
cd ~/.openclaw/workspace/openclaw-cli

# 测试运行（无需安装）
python3 -m openclaw.cli --help

# 或者安装到本地
pip3 install -e .
```

---

## 📖 核心命令

### 读取文档

```bash
# 读取 Markdown 文件
openclaw doc read --file report.md

# 读取并输出 JSON
openclaw doc read --file report.md --json

# 读取纯文本
openclaw doc read --file readme.txt --format text
```

**输出示例**：
```bash
$ openclaw doc read --file test.md
✓ Success

Content:
# Report Title

This is the content...
```

---

### 写入文档

```bash
# 创建 Markdown 文件
openclaw doc write --file output.md --content "# Hello\n\nWorld"

# 从文件读取内容
openclaw doc write --file output.md --content @input.txt

# 创建纯文本文件
openclaw doc write --file readme.txt --content "Plain text" --format text
```

---

### 搜索文档

```bash
# 搜索关键词
openclaw doc search --file report.md --pattern "TODO"

# 正则搜索
openclaw doc search --file code.py --pattern "def.*test"

# 忽略大小写
openclaw doc search --file report.md --pattern "todo" --ignore-case

# JSON 输出
openclaw doc search --file report.md --pattern "TODO" --json
```

**输出示例**：
```bash
$ openclaw doc search --file test.md --pattern "TODO"
✓ Success

┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Field         ┃ Value                    ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ pattern       │ TODO                     │
│ total_matches │ 1                        │
│ matches       │ [                        │
│               │   {                      │
│               │     "line": 17,          │
│               │     "match": "TODO",     │
│               │     "context": "## TODO" │
│               │   }                      │
│               │ ]                        │
└───────────────┴──────────────────────────┘
```

---

### 合并文档

```bash
# 合并多个文件
openclaw doc merge --file intro.md --file body.md --file conclusion.md --output book.md

# 自定义分隔符
openclaw doc merge --file a.md --file b.md --output merged.md --separator "\n\n"
```

---

### 格式转换

```bash
# Markdown 转文本
openclaw doc convert --input markdown --output text --file report.md

# Markdown 转 HTML
openclaw doc convert --input markdown --output html --file readme.md --output-file readme.html

# 输出到 stdout
openclaw doc convert --input markdown --output text --file report.md
```

---

## 💡 实用场景

### 场景 1: 批量处理文档

```bash
# 合并所有章节
for chapter in chapter-*.md; do
    files="$files --file $chapter"
done
openclaw doc merge $files --output book.md
```

### 场景 2: 文档搜索工作流

```bash
# 搜索所有 TODO
openclaw doc search --file report.md --pattern "TODO" --json | \
  jq '.data.matches[] | "\(.line): \(.context)"'
```

### 场景 3: 自动化文档生成

```bash
# 生成报告
openclaw doc write --file report.md --content "# Daily Report\n\n$(date)"
openclaw doc search --file *.md --pattern "TODO" >> report.md
```

### 场景 4: Agent 工作流

```bash
# Claude Code / Cursor 中使用
/openclaw doc read --file spec.md --json | \
  jq -r '.data.content' | \
  python process.py | \
  /openclaw doc write --file output.md --content @-
```

---

## 🔧 高级选项

### 全局选项

```bash
# JSON 输出（所有命令）
openclaw --json doc read --file test.md

# 详细模式
openclaw -v doc read --file test.md

# 调试模式
openclaw --debug doc read --file test.md
```

### 命令选项

```bash
# doc read
--file PATH              # 文件路径（必需）
--format [markdown|text|auto]  # 格式（默认：auto）
--json                   # JSON 输出

# doc write
--file PATH              # 输出路径（必需）
--content TEXT           # 内容（必需）
--format [markdown|text] # 格式（默认：markdown）

# doc search
--file PATH              # 文件路径（必需）
--pattern REGEX          # 搜索模式（必需）
--ignore-case            # 忽略大小写
--json                   # JSON 输出

# doc merge
--file PATH              # 输入文件（可多次）
--output PATH            # 输出路径（必需）
--separator TEXT         # 分隔符（默认：\n\n---\n\n）

# doc convert
--input FORMAT           # 输入格式（必需）
--output FORMAT          # 输出格式（必需）
--file PATH              # 输入文件（必需）
--output-file PATH       # 输出文件（可选）
```

---

## 📊 支持的格式

| 格式 | 扩展名 | 读取 | 写入 | 转换 |
|-----|-------|-----|-----|-----|
| Markdown | .md, .markdown | ✅ | ✅ | ✅ |
| 纯文本 | .txt, .text | ✅ | ✅ | ✅ |
| HTML | .html, .htm | ⏳ | ⏳ | ✅ |
| Word | .docx | ⏳ | ⏳ | ⏳ |
| PDF | .pdf | ⏳ (仅文本) | ❌ | ⏳ |

**图例**: ✅ 已支持 | ⏳ 计划中 | ❌ 不支持

---

## 🧪 测试

```bash
# 运行测试套件
bash tests/test_doc.sh

# 运行特定测试
python3 -m openclaw.cli doc read --file test.md
python3 -m openclaw.cli doc write --file output.md --content "# Test"
python3 -m openclaw.cli doc search --file test.md --pattern "TODO"
```

---

## 🤝 贡献

### 添加新格式支持

1. 在 `openclaw/handlers/` 创建新处理器
2. 实现 `DocumentHandler` 接口
3. 在 `openclaw/commands/doc.py` 中注册
4. 添加测试

### 添加新命令

1. 在 `openclaw/commands/doc.py` 添加新子命令
2. 实现业务逻辑
3. 添加帮助文档
4. 编写测试

---

## 📝 常见问题

### Q: 如何读取非 UTF-8 编码的文件？
A: 目前仅支持 UTF-8 编码。如需其他编码，请先转换。

### Q: 支持大文件吗？
A: 支持，但大文件（>100MB）可能影响性能。

### Q: 如何在脚本中使用？
A: 使用 `--json` 输出，配合 `jq` 或其他 JSON 工具处理。

### Q: 支持管道吗？
A: 支持！大部分命令可以从 stdin 读取或输出到 stdout。

---

## 🔗 相关资源

- **架构文档**: `docs/cli-architecture.md`
- **GitHub**: https://github.com/openclaw/openclaw-cli
- **OpenClaw 文档**: https://docs.openclaw.ai

---

*最后更新：2026-03-12*  
*版本：0.2.0*
