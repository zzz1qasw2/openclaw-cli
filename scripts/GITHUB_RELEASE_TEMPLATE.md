# OpenClaw CLI v0.4.0

## 🎉 Release Highlights

This release introduces **advanced workflow features** that make OpenClaw CLI production-ready for complex automation tasks!

### ✨ New Features

#### 1. Conditional Execution
Add if/else logic to your workflows:
```yaml
steps:
  - name: Deploy to production
    action: shell
    params:
      command: deploy.sh
    condition: "${env} == production"
```

#### 2. Parallel Execution
Run multiple steps concurrently for faster execution:
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

#### 3. Variable System
Pass data between steps with variable interpolation:
```yaml
steps:
  - name: Set environment
    action: set
    params:
      name: environment
      value: production
  
  - name: Use variable
    action: shell
    params:
      command: echo "Deploying to ${environment}"
```

#### 4. Rich Progress Bars
Beautiful execution progress with colors and real-time updates:
```
🚀 Starting workflow: My Workflow
   Steps: 7

[1/7] Step 1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:02
✓ Workflow complete: 6 succeeded, 0 failed, 1 skipped
```

#### 5. Retry Mechanism
Automatic retry on failure with configurable attempts:
```yaml
steps:
  - name: Flaky operation
    action: shell
    params:
      command: unstable_script.sh
    retry: 3
    timeout: 60
```

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/openclaw/openclaw-cli.git
cd openclaw-cli

# Install in development mode
pip install -e .

# Verify installation
openclaw workflow --help
```

## 🚀 Quick Start

### Run a workflow
```bash
openclaw workflow run -f my-workflow.yml --verbose
```

### Initialize from template
```bash
openclaw workflow init -n document-conversion -o workflow.yml
openclaw workflow run -f workflow.yml
```

### Run demo
```bash
openclaw workflow demo
openclaw workflow run -f /tmp/demo-workflow.yml -v
```

## 📋 What's Changed

### New Commands
- `workflow demo` - Run demo workflow showcasing all features
- `workflow run --var KEY=value` - Set variables from CLI
- `workflow run --max-workers N` - Control parallelism

### Enhanced Features
- Conditional step execution with flexible syntax
- Parallel execution with ThreadPoolExecutor
- Variable system with interpolation
- Rich progress bars and colored output
- Retry mechanism with backoff

### Bug Fixes
- Fixed YAML parsing for special characters
- Improved error handling and reporting
- Better variable interpolation edge cases

## 📖 Documentation

- **README**: https://github.com/openclaw/openclaw-cli/blob/main/README.md
- **CHANGELOG**: https://github.com/openclaw/openclaw-cli/blob/main/CHANGELOG.md
- **CONTRIBUTING**: https://github.com/openclaw/openclaw-cli/blob/main/CONTRIBUTING.md

## 🔧 Technical Details

### Dependencies
- click>=8.0
- rich>=13.0
- pyyaml>=6.0
- python-docx>=0.8.10
- beautifulsoup4>=4.12.0
- pdfplumber>=0.10.0

### Python Support
- Python 3.10+
- Tested on Linux, macOS

## 🙏 Acknowledgments

Thanks to all contributors and the OpenClaw community!

## 📄 License

MIT License - see [LICENSE](https://github.com/openclaw/openclaw-cli/blob/main/LICENSE) for details.

---

**Full Changelog**: https://github.com/openclaw/openclaw-cli/compare/v0.3.0...v0.4.0
