# 🦞 OpenClaw CLI 开源发布指南

## 📋 发布前准备

### 1. 创建 GitHub 仓库

访问：https://github.com/new

**仓库信息：**
- **仓库名**: `openclaw-cli`
- **描述**: OpenClaw CLI - 通用文档 CLI 工具，支持 Markdown/Word/HTML/PDF 读写转换和工作流自动化
- **可见性**: Public（公开）
- **初始化**: ❌ 不要勾选 "Add a README file" 或 "Add .gitignore"

点击 **Create repository**

---

### 2. 推送代码到 GitHub

```bash
cd /home/stephenx/.openclaw/workspace/openclaw-cli

# 添加远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/StephenX-777/openclaw-cli.git

# 推送代码
git branch -M main
git push -u origin main
```

---

### 3. 配置 PyPI Secrets（用于自动发布）

#### 3.1 注册 PyPI 账号

- **正式环境**: https://pypi.org/account/register/
- **测试环境**: https://test.pypi.org/account/register/

#### 3.2 创建 API Token

**PyPI:**
1. 访问 https://pypi.org/manage/account/token/
2. 点击 "Add API token"
3. 名称：`openclaw-cli-ci`
4. 范围：`All projects`
5. 复制生成的 token（格式类似 `pypi-AgEIcHlwaS5vcmc...`）

**TestPyPI:**
1. 访问 https://test.pypi.org/manage/account/token/
2. 同样步骤创建 token

#### 3.3 添加到 GitHub Secrets

1. 打开你的仓库：https://github.com/StephenX-777/openclaw-cli/settings/secrets/actions
2. 点击 "New repository secret"
3. 添加以下 secrets：

```
Name: PYPI_API_TOKEN
Value: pypi-AgEIcHlwaS5vcmc...（你的 PyPI token）

Name: TESTPYPI_API_TOKEN
Value: pypi-AgEIcHlwaS5vcmc...（你的 TestPyPI token）
```

---

### 4. 检查包名可用性

```bash
# 检查 PyPI 上是否已有同名包
pip search openclaw-cli  # （已废弃，用下面的方法）

# 访问 PyPI 检查
# https://pypi.org/project/openclaw-cli/
```

如果包名已被占用，需要修改 `setup.py` 中的 `name` 字段：

```python
setup(
    name="openclaw-cli-tool",  # 或其他唯一名称
    ...
)
```

---

## 🚀 发布流程

### 方式一：自动发布（推荐）

#### 创建 GitHub Release

1. 访问：https://github.com/StephenX-777/openclaw-cli/releases/new
2. **Tag version**: `v0.4.0`（与 setup.py 中的版本一致）
3. **Release title**: `OpenClaw CLI v0.4.0`
4. **Description**: 使用 `CHANGELOG.md` 的内容
5. 点击 **Publish release**

#### 自动触发

创建 Release 后，GitHub Actions 会自动：
1. ✅ 运行测试（Python 3.10/3.11/3.12）
2. ✅ 构建 Python 包
3. ✅ 发布到 PyPI 和 TestPyPI

#### 查看进度

访问：https://github.com/StephenX-777/openclaw-cli/actions

---

### 方式二：手动发布

```bash
cd /home/stephenx/.openclaw/workspace/openclaw-cli

# 安装构建工具
pip install build twine

# 构建包
python -m build

# 检查包
twine check dist/*

# 发布到 TestPyPI（先测试）
twine upload --repository testpypi dist/*

# 发布到 PyPI（正式）
twine upload dist/*
```

---

## ✅ 验证发布

### 1. 检查 PyPI 页面

访问：https://pypi.org/project/openclaw-cli/

应该能看到：
- 项目描述
- 版本信息
- 下载链接
- GitHub 仓库链接

### 2. 测试安装

```bash
# 创建虚拟环境
python -m venv test-env
source test-env/bin/activate  # Windows: test-env\Scripts\activate

# 从 PyPI 安装
pip install openclaw-cli

# 验证安装
openclaw --help
openclaw doc --help
openclaw workflow --help
```

### 3. 测试基本功能

```bash
# 测试文档读取
openclaw doc read --file test.md

# 测试工作流
openclaw workflow list-templates

# 测试帮助
openclaw --version
```

---

## 📝 后续维护

### 发布新版本

1. **更新版本号** (`setup.py`):
   ```python
   version="0.5.0",  # 递增版本号
   ```

2. **更新 CHANGELOG** (`CHANGELOG.md`):
   ```markdown
   ## v0.5.0 (2026-03-15)
   - 新增功能
   - 修复问题
   - 改进优化
   ```

3. **提交并推送**:
   ```bash
   git add .
   git commit -m "Release v0.5.0"
   git push
   ```

4. **创建 GitHub Release**（同上）

---

### 常见问题

#### 1. PyPI 上传失败：403 Forbidden

**原因**: Token 无效或过期

**解决**:
- 重新生成 PyPI token
- 检查 GitHub Secrets 是否正确
- 确认 token 没有过期

#### 2. 包名冲突

**原因**: PyPI 上已有同名包

**解决**:
- 修改 `setup.py` 中的 `name` 字段
- 或使用不同的包名（如 `openclaw-cli-tool`）

#### 3. CI/CD 测试失败

**原因**: 测试用例不通过

**解决**:
- 查看 GitHub Actions 日志
- 本地运行测试：`pytest tests/ -v`
- 修复后重新推送

#### 4. 依赖冲突

**原因**: 某些依赖版本不兼容

**解决**:
- 检查 `requirements.txt`
- 使用版本范围：`rich>=13.0,<14.0`
- 测试不同 Python 版本

---

## 🎯 推广建议

### 1. 完善 README

- ✅ 添加安装指南
- ✅ 添加使用示例
- ✅ 添加 Badge（CI 状态、版本、下载量）
- ✅ 添加贡献指南

### 2. 社交媒体

- 发布到 Twitter/X
- 发布到 LinkedIn
- 分享到相关 Reddit 社区（r/Python, r/opensource）
- 分享到 Hacker News

### 3. 中文社区

- 知乎专栏文章
- 掘金技术文章
- V2EX 分享
- 微信公众号（用我们的龙虾养成记！）

### 4. 开源平台

- 添加至 Python 主题列表
- 提交到 awesome-python
- 提交到 awesome-openclaw-usecases-zh

---

## 📊 统计指标

发布后关注：
- PyPI 下载量：https://pypistats.org/packages/openclaw-cli
- GitHub Stars
- GitHub Forks
- Issue 数量
- 贡献者数量

---

## 🦞 龙虾寄语

恭喜你完成开源发布！

从 0 到 1 是最难的，你已经做到了。

接下来：
- 持续迭代
- 响应用户反馈
- 吸引更多贡献者
- 建立社区

**开源不是终点，而是新的起点。**

加油！🦞

---

*最后更新：2026-03-14*  
*作者：小陌 🦞*
