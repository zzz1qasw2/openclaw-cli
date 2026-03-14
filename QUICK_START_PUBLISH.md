# 🚀 OpenClaw CLI GitHub 发布 - 快速操作清单

## ✅ 已完成的工作

- [x] 初始化 Git 仓库
- [x] 配置 Git 用户信息（StephenX-777）
- [x] 首次提交（47 个文件，8358 行代码）
- [x] 创建 GitHub Actions CI/CD 配置
- [x] 更新作者信息和仓库 URL
- [x] 创建发布指南文档

---

## 📋 你需要做的事（按顺序）

### 1️⃣ 创建 GitHub 仓库（2 分钟）

**访问**: https://github.com/new

**填写信息**:
```
仓库名：openclaw-cli
描述：OpenClaw CLI - 通用文档 CLI 工具，支持 Markdown/Word/HTML/PDF 读写转换和工作流自动化
可见性：✅ Public（公开）
❌ 不要勾选 "Add a README file"
❌ 不要勾选 "Add .gitignore"
```

**点击**: **Create repository**

---

### 2️⃣ 推送代码到 GitHub（1 分钟）

**复制并执行以下命令**：

```bash
cd /home/stephenx/.openclaw/workspace/openclaw-cli

# 添加远程仓库
git remote add origin https://github.com/StephenX-777/openclaw-cli.git

# 推送代码
git push -u origin main
```

**预期输出**：
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Delta compression using up to XX threads
Compressing objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), XX KiB | XX MiB/s, done.
Total XX (delta XX), reused XX (delta XX)
remote: Resolving deltas: 100% (XX/XX), done.
To https://github.com/StephenX-777/openclaw-cli.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

### 3️⃣ 注册 PyPI 账号（如果还没有）（5 分钟）

**访问**: https://pypi.org/account/register/

**填写信息**：
- 用户名
- 邮箱
- 密码

**验证邮箱**

---

### 4️⃣ 创建 PyPI API Token（2 分钟）

**访问**: https://pypi.org/manage/account/token/

**步骤**：
1. 点击 "Add API token"
2. 名称：`openclaw-cli-ci`
3. 范围：`All projects`
4. 点击 "Add token"
5. **复制 token**（格式类似 `pypi-AgEIcHlwaS5vcmc...`）

⚠️ **重要**: token 只显示一次，立即复制保存！

---

### 5️⃣ 添加 GitHub Secret（1 分钟）

**访问**: https://github.com/StephenX-777/openclaw-cli/settings/secrets/actions

**步骤**：
1. 点击 "New repository secret"
2. 填写：
   ```
   Name: PYPI_API_TOKEN
   Value: pypi-AgEIcHlwaS5vcmc...（粘贴你的 token）
   ```
3. 点击 "Add secret"

---

### 6️⃣ 创建第一个 Release（3 分钟）

**访问**: https://github.com/StephenX-777/openclaw-cli/releases/new

**填写信息**：

**Tag version**: `v0.4.0`

**Target**: `main`

**Release title**: `OpenClaw CLI v0.4.0 - Initial Release`

**Description**: 
```markdown
## 🎉 首次发布

### 核心功能
- ✅ 通用文档 CLI（支持 Markdown/Word/HTML/PDF/TXT）
- ✅ 工作流引擎（YAML 定义，条件/并行/变量/重试）
- ✅ 多 Agent 协同命令
- ✅ Rich 进度条和彩色输出
- ✅ 完整的测试套件

### 安装
```bash
pip install openclaw-cli
```

### 快速开始
```bash
# 读取文档
openclaw doc read --file report.md

# 格式转换
openclaw doc convert --input docx --output markdown --file report.docx

# 执行工作流
openclaw workflow run --file my-workflow.yaml
```

### 文档
- [README](https://github.com/StephenX-777/openclaw-cli/blob/main/README.md)
- [快速开始](https://github.com/StephenX-777/openclaw-cli/blob/main/QUICKSTART.md)
- [变更日志](https://github.com/StephenX-777/openclaw-cli/blob/main/CHANGELOG.md)

---

🦞 Built with OpenClaw
```

**点击**: **Publish release**

---

### 7️⃣ 等待 CI/CD 完成（5-10 分钟）

**访问**: https://github.com/StephenX-777/openclaw-cli/actions

**查看进度**：
- ✅ test (Python 3.10) - 运行中/完成
- ✅ test (Python 3.11) - 运行中/完成
- ✅ test (Python 3.12) - 运行中/完成
- ✅ build - 运行中/完成
- ✅ publish-pypi - 运行中/完成

**全部变绿** ✅ 表示发布成功！

---

### 8️⃣ 验证发布（2 分钟）

**访问 PyPI 页面**：
https://pypi.org/project/openclaw-cli/

**测试安装**：
```bash
# 创建新虚拟环境
python -m venv test-install
source test-install/bin/activate

# 安装
pip install openclaw-cli

# 验证
openclaw --version
openclaw doc --help
```

---

## 🎊 完成！

恭喜！你的 OpenClaw CLI 已经：
- ✅ 开源到 GitHub
- ✅ 发布到 PyPI
- ✅ 配置自动 CI/CD

---

## 📊 下一步

### 推广你的项目

1. **公众号文章** - 用「龙虾养成记」系列第 7 集！
2. **知乎专栏** - 技术分享文章
3. **V2EX** - 分享创造板块
4. **Twitter/X** - 英文推广
5. **Reddit** - r/Python, r/opensource

### 持续维护

- 响应用户 Issue
- 合并 Pull Request
- 定期发布新版本
- 更新文档

---

## 🆘 遇到问题？

### 常见问题速查

**问题**: `git push` 失败，提示权限错误  
**解决**: 检查 GitHub 用户名是否正确，或使用 SSH key

**问题**: PyPI 上传失败，403 Forbidden  
**解决**: 检查 token 是否正确，是否已添加到 Secrets

**问题**: 包名已被占用  
**解决**: 修改 `setup.py` 中的 `name` 字段

**问题**: CI 测试失败  
**解决**: 查看 Actions 日志，本地运行 `pytest tests/ -v`

---

## 📞 需要帮助？

查看完整指南：`GITHUB_PUBLISH_GUIDE.md`

---

*创建时间：2026-03-14*  
*小陌 🦞 出品*
