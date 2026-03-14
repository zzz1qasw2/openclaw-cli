# 🦞 OpenClaw CLI v0.4.0 - 首次公开发布

## 🎉 发布信息

**版本**: v0.4.0  
**发布日期**: 2026-03-14  
**作者**: StephenX-777  
**仓库**: https://github.com/zzz1qasw2/openclaw-cli

---

## ✨ 核心功能

### 📄 通用文档 CLI
支持 **5 种格式** 的读写和转换：
- ✅ Markdown (.md)
- ✅ Word (.docx)
- ✅ HTML (.html)
- ✅ PDF (.pdf) - 只读
- ✅ 纯文本 (.txt)

**常用命令**：
```bash
# 读取文档
openclaw doc read --file report.md
openclaw doc read --file document.docx

# 格式转换
openclaw doc convert --input docx --output markdown --file report.docx

# 搜索内容
openclaw doc search --file code.py --pattern "def.*:"

# 合并文档
openclaw doc merge --file a.md --file b.md --output combined.md
```

---

### ⚙️ 工作流引擎
用 **YAML** 定义自动化流程，支持：

**高级功能**：
- ✅ 条件分支（if/else 逻辑）
- ✅ 并行执行（多线程）
- ✅ 变量系统（步骤间传递数据）
- ✅ 重试机制（失败自动重试）
- ✅ 超时控制
- ✅ Rich 进度条

**示例工作流**：
```yaml
workflow:
  name: "文档处理流水线"
  variables:
    input_dir: "./input"
    output_dir: "./output"
  steps:
    - name: "准备目录"
      command: "mkdir -p ${input_dir} ${output_dir}"
    
    - name: "转换文档"
      parallel:
        - name: "转换 Markdown"
          command: "openclaw doc convert --input markdown --output text --file ${input_dir}/report.md"
        - name: "转换 Word"
          command: "openclaw doc convert --input docx --output markdown --file ${input_dir}/report.docx"
    
    - name: "验证输出"
      command: "ls -la ${output_dir}"
```

**执行**：
```bash
openclaw workflow run --file my-workflow.yaml -v
```

---

### 🤖 多 Agent 协同
创建和管理专业 AI 智能体：

```bash
# 创建分析师智能体
openclaw agent spawn --role analyst --task "analyze codebase"

# 创建作家智能体
openclaw agent spawn --role writer --task "generate documentation"

# 批量处理（Map-Reduce）
openclaw agent batch-process --files "*.md" --map extract.py --reduce merge.py
```

---

## 📦 安装

### 从 PyPI 安装（推荐）
```bash
pip install openclaw-cli
```

### 从源码安装
```bash
git clone https://github.com/zzz1qasw2/openclaw-cli.git
cd openclaw-cli
pip install -e .
```

### 依赖
- Python 3.10+
- click >= 8.0
- rich >= 13.0
- pyyaml >= 6.0

---

## 🚀 快速开始

### 1. 读取文档
```bash
openclaw doc read --file report.md
```

### 2. 格式转换
```bash
openclaw doc convert --input docx --output markdown --file report.docx
```

### 3. 执行工作流
```bash
# 列出模板
openclaw workflow list-templates

# 从模板初始化
openclaw workflow init --template document-conversion

# 执行工作流
openclaw workflow run --file document-conversion.yaml -v
```

### 4. 查看帮助
```bash
openclaw --help
openclaw doc --help
openclaw workflow --help
```

---

## 📊 项目统计

| 指标 | 数值 |
|------|------|
| 代码行数 | 8,358+ |
| 文件格式支持 | 5 种 |
| CLI 命令 | 10+ |
| 工作流模板 | 4 个 |
| 测试用例 | 27+ |
| 测试通过率 | 100% |

---

## 📝 更新日志

### v0.4.0 (2026-03-13)
**新增**：
- 条件执行：支持工作流中的 if/else 逻辑
- 并行执行：同时运行多个步骤
- 变量系统：在步骤间传递数据
- Rich 进度条：美观的执行进度显示
- 重试机制：失败时自动重试
- Demo 命令：`workflow demo` 展示功能

**修复**：
- 修复命令中特殊字符的 YAML 解析
- 修复变量插值边界情况

### v0.3.0 (2026-03-13)
- 工作流引擎：基于 YAML 的工作流定义和执行
- 模板系统：预构建的工作流模板

### v0.2.0 (2026-03-12)
- 多格式文档支持：Word/HTML/PDF
- 智能体管理命令

---

## 📚 文档

- [README](https://github.com/zzz1qasw2/openclaw-cli/blob/main/README.md) - 项目介绍
- [快速开始](https://github.com/zzz1qasw2/openclaw-cli/blob/main/QUICKSTART.md) - 新手指南
- [变更日志](https://github.com/zzz1qasw2/openclaw-cli/blob/main/CHANGELOG.md) - 版本历史
- [贡献指南](https://github.com/zzz1qasw2/openclaw-cli/blob/main/CONTRIBUTING.md) - 如何贡献

---

## 🦞 龙虾养成记

这个项目是「龙虾养成记」系列的成果：

- **Day 1**: 决定搞副业
- **Day 2**: 正式上岗
- **Day 3**: 学会分身术（多 Agent 协同）
- **Day 4**: 市场调研
- **Day 5**: 开发 CLI 工具
- **Day 6**: 开发工作流引擎
- **Day 7**: 开源发布！🎉

**每一集，都是一次蜕皮。就像龙虾一样，一次次变强。**

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](https://github.com/zzz1qasw2/openclaw-cli/blob/main/LICENSE) 文件了解详情。

---

## 🙏 致谢

- Built with **OpenClaw** 🦞
- 感谢所有贡献者和用户！

---

**🦞 龙虾出品，必属精品！**

*作者：StephenX-777*  
*项目地址：https://github.com/zzz1qasw2/openclaw-cli*
