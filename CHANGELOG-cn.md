# 变更日志

本项目的所有重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 计划中
- Phase 5: 企业级功能（复杂条件、变量作用域）
- Phase 6: 工作流市场
- PyPI 发布

## [0.4.0] - 2026-03-13

### 新增
- **条件执行**: 支持工作流中的 if/else 逻辑
  - 条件语法：`${var} == value`, `${var} != value`, `${var}`
  - 步骤可根据变量值跳过
- **并行执行**: 同时运行多个步骤
  - 步骤的 `parallel: true` 标志
  - 可配置最大工作线程数（`--max-workers`）
  - 使用 ThreadPoolExecutor 并发执行
- **变量系统**: 在步骤间传递数据
  - `set` 动作定义变量
  - `${var}` 和 `$var` 插值语法
  - `output_var` 捕获步骤输出
  - `--var KEY=value` CLI 选项
- **Rich 进度条**: 美观的执行进度显示
  - 旋转图标、进度条、百分比、已用时间
  - 彩色输出（成功/失败/跳过）
  - 并行步骤分组显示
- **重试机制**: 失败时自动重试
  - 可配置重试次数（`retry: N`）
  - 可配置超时时间（`timeout: N`）
  - 重试间隔 1 秒
- **Demo 命令**: `workflow demo` 展示功能

### 更改
- 使用高级功能重写工作流引擎
- 增强错误处理和报告
- 改进 CLI 帮助信息

### 修复
- 修复命令中特殊字符的 YAML 解析
- 修复变量插值边界情况

## [0.3.0] - 2026-03-13

### 新增
- **工作流引擎**: 基于 YAML 的工作流定义和执行
  - `workflow run` - 执行工作流
  - `workflow validate` - 验证 YAML 文件
  - `workflow list-templates` - 列出可用模板
  - `workflow init` - 从模板初始化
  - `workflow create` - 交互式创建
- **模板系统**: 预构建的工作流模板
  - document-conversion
  - batch-process
  - content-pipeline
- **示例工作流**: 即用型示例

### 更改
- 更新 README 添加工作流文档
- 增强输出格式化

## [0.2.0] - 2026-03-12

### 新增
- **多格式文档支持**:
  - Word (.docx) 读/写
  - HTML 读/写
  - PDF 只读
- **智能体管理命令**:
  - `agent spawn` - 创建专业智能体
  - `agent list` - 列出活跃智能体
  - `agent send` - 发送消息
  - `agent batch-process` - Map-Reduce 处理
  - `agent kill` - 终止智能体

### 更改
- 统一的文档处理器接口
- 双输出模式（人类可读 + JSON）

## [0.1.0] - 2026-03-12

### 新增
- 初始 CLI 架构
- 文档操作:
  - `doc read` - 读取文档
  - `doc write` - 写入文档
  - `doc convert` - 格式转换
  - `doc merge` - 合并文档
  - `doc search` - 搜索内容
- Markdown 和纯文本支持
- 基础输出格式化

---

[未发布]: https://github.com/openclaw/openclaw-cli/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/openclaw/openclaw-cli/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/openclaw/openclaw-cli/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/openclaw/openclaw-cli/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/openclaw/openclaw-cli/releases/tag/v0.1.0
