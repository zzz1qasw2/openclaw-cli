# OpenClaw CLI 文档结构

## 📚 多语言文档

本项目提供中英文双语支持，**默认语言为英文**。

### 核心文档

| 文件 | 语言 | 说明 |
|------|------|------|
| `README.md` | 🇬🇧 英文 | 主文档（默认） |
| `README-cn.md` | 🇨🇳 中文 | 中文翻译版 |
| `CONTRIBUTING.md` | 🇬🇧 英文 | 贡献指南（默认） |
| `CONTRIBUTING-cn.md` | 🇨🇳 中文 | 中文贡献指南 |
| `CHANGELOG.md` | 🇬🇧 英文 | 变更日志（默认） |
| `CHANGELOG-cn.md` | 🇨🇳 中文 | 中文变更日志 |
| `LICENSE` | 🇬🇧 英文 | 开源协议（仅英文版） |

### 文档命名约定

- **英文文档**: `<name>.md`（默认）
- **中文文档**: `<name>-cn.md`

### 交叉引用

所有文档都在开头提供语言切换链接：

```markdown
**中文文档**: [README-cn.md](README-cn.md)
```

```markdown
**English Documentation**: [README.md](README.md)
```

---

## 📁 完整目录结构

```
openclaw-cli/
├── openclaw/                    # 源代码
│   ├── cli.py                   # CLI 入口
│   ├── commands/                # 命令实现
│   │   ├── doc.py               # 文档命令
│   │   ├── agent.py             # 智能体命令
│   │   └── workflow.py          # 工作流命令
│   ├── core/                    # 核心模块
│   ├── handlers/                # 格式处理器
│   └── utils/                   # 工具函数
│
├── workflows/                   # 示例工作流
│   ├── convert-document.yml
│   └── batch-process.yml
│
├── tests/                       # 测试文件
│   ├── test_workflow.sh
│   └── test_doc.sh
│
├── scripts/                     # 工具脚本
│   ├── release-check.sh         # 发布检查
│   └── GITHUB_RELEASE_TEMPLATE.md
│
├── README.md                    # 🇬🇧 英文主文档
├── README-cn.md                 # 🇨🇳 中文主文档
├── CONTRIBUTING.md              # 🇬🇧 英文贡献指南
├── CONTRIBUTING-cn.md           # 🇨🇳 中文贡献指南
├── CHANGELOG.md                 # 🇬🇧 英文变更日志
├── CHANGELOG-cn.md              # 🇨🇳 中文变更日志
├── LICENSE                      # 🇬🇧 MIT 协议
├── env.example                  # 环境变量模板
├── setup.py                     # 安装配置
├── requirements.txt             # Python 依赖
└── .gitignore                   # Git 忽略规则
```

---

## 🌍 翻译指南

### 添加新语言

如需添加其他语言（如西班牙语、法语等），遵循以下模式：

1. **文件名**: `<name>-<lang>.md`
   - 例如：`README-es.md`（西班牙语）
   - 例如：`README-fr.md`（法语）

2. **在英文文档开头添加链接**:
   ```markdown
   **中文文档**: [README-cn.md](README-cn.md)
   **Español**: [README-es.md](README-es.md)
   **Français**: [README-fr.md](README-fr.md)
   ```

3. **在翻译文档开头添加英文链接**:
   ```markdown
   **English Documentation**: [README.md](README.md)
   **中文文档**: [README-cn.md](README-cn.md)
   ```

### 翻译检查清单

- [ ] 保持格式一致（标题、列表、代码块）
- [ ] 翻译所有文本（包括注释、示例）
- [ ] 保留代码示例不变（除非有语言特定版本）
- [ ] 更新交叉引用链接
- [ ] 在英文文档中添加新语言链接

---

## 📝 文档更新流程

### 更新英文文档

1. 编辑英文文件（如 `README.md`）
2. 提交更改
3. **通知翻译者**更新对应语言版本

### 更新中文文档

1. 确保英文文档已更新
2. 编辑中文文件（如 `README-cn.md`）
3. 同步版本号、功能描述等
4. 提交更改

### 版本发布时

1. 更新 `CHANGELOG.md`（英文）
2. 更新 `CHANGELOG-cn.md`（中文）
3. 更新 `setup.py` 中的版本号
4. 更新 `README.md` 和 `README-cn.md` 中的版本徽章

---

## 🔧 工具脚本

### release-check.sh

自动检查文档完整性：

```bash
bash scripts/release-check.sh
```

检查项目：
- ✅ 所有必需文档存在
- ✅ 中英文版本都存在
- ✅ 版本号一致
- ✅ 无敏感信息泄露

---

## 💡 最佳实践

1. **始终先更新英文文档**
2. **保持中英文版本同步**（功能描述、版本号等）
3. **使用简单清晰的中文**（避免过度直译）
4. **保留专业术语的英文原文**（如 CLI、Workflow、Agent）
5. **代码示例保持英文**（注释可翻译）

---

*最后更新：2026-03-13*  
*版本：0.4.0*
