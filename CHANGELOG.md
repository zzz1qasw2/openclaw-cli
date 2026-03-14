# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Phase 5: Enterprise features (complex conditions, variable scopes)
- Phase 6: Workflow marketplace
- PyPI release

## [0.4.0] - 2026-03-13

### Added
- **Conditional Execution**: Support for if/else logic in workflows
  - Condition syntax: `${var} == value`, `${var} != value`, `${var}`
  - Steps can be skipped based on variable values
- **Parallel Execution**: Run multiple steps concurrently
  - `parallel: true` flag for steps
  - Configurable max workers (`--max-workers`)
  - ThreadPoolExecutor for concurrent execution
- **Variable System**: Pass data between steps
  - `set` action to define variables
  - `${var}` and `$var` interpolation syntax
  - `output_var` to capture step output
  - `--var KEY=value` CLI option
- **Rich Progress Bars**: Beautiful execution progress display
  - Spinner, progress bar, percentage, elapsed time
  - Color-coded output (success/failure/skipped)
  - Parallel step grouping
- **Retry Mechanism**: Automatic retry on failure
  - Configurable retry count (`retry: N`)
  - Configurable timeout (`timeout: N`)
  - 1-second backoff between retries
- **Demo Command**: `workflow demo` to showcase features

### Changed
- Workflow engine rewritten with advanced features
- Enhanced error handling and reporting
- Improved CLI help messages

### Fixed
- YAML parsing for special characters in commands
- Variable interpolation edge cases

## [0.3.0] - 2026-03-13

### Added
- **Workflow Engine**: YAML-based workflow definition and execution
  - `workflow run` - Execute workflows
  - `workflow validate` - Validate YAML files
  - `workflow list-templates` - List available templates
  - `workflow init` - Initialize from template
  - `workflow create` - Interactive creation
- **Template System**: Pre-built workflow templates
  - document-conversion
  - batch-process
  - content-pipeline
- **Example Workflows**: Ready-to-use examples

### Changed
- Updated README with workflow documentation
- Enhanced output formatting

## [0.2.0] - 2026-03-12

### Added
- **Multi-format Document Support**:
  - Word (.docx) read/write
  - HTML read/write
  - PDF read-only
- **Agent Management Commands**:
  - `agent spawn` - Create specialist agents
  - `agent list` - List active agents
  - `agent send` - Send messages
  - `agent batch-process` - Map-Reduce processing
  - `agent kill` - Terminate agents

### Changed
- Unified document handler interface
- Dual output modes (human-readable + JSON)

## [0.1.0] - 2026-03-12

### Added
- Initial CLI architecture
- Document operations:
  - `doc read` - Read documents
  - `doc write` - Write documents
  - `doc convert` - Format conversion
  - `doc merge` - Merge documents
  - `doc search` - Search content
- Markdown and plain text support
- Basic output formatting

---

[Unreleased]: https://github.com/openclaw/openclaw-cli/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/openclaw/openclaw-cli/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/openclaw/openclaw-cli/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/openclaw/openclaw-cli/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/openclaw/openclaw-cli/releases/tag/v0.1.0
