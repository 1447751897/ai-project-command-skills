# AI Project Command Skills

简体中文 | [English](README.md)

面向 AI 编程助手的文档优先工作流 skills，支持 Codex 和 Claude Code。它用于项目初始化、功能开发、Goal 模式自动推进、交接和跨对话续接。

这些 skill 会帮助 AI 编程助手先澄清需求、持续维护项目文档、在技术选型时做明确取舍，并把足够多的项目状态沉淀到仓库文件里，方便后续新的对话、其他 AI 或其他开发者继续接手。

## 命令名称

Codex 使用原始命令名。Claude Code 使用带 `ai-` 前缀的别名，避免和 Claude Code 自带的 `/init`、`/plan`、`/upgrade` 等命令冲突。

| 用途 | Codex | Claude Code |
| --- | --- | --- |
| 启动新项目 | `/init` | `/ai-init` |
| 执行较长项目或阶段目标 | `/goal` | `/ai-goal` |
| 高自治 Goal 模式 | `/goal --super` | `/ai-goal --super` |
| 高自治兼容别名 | `/super` | `/ai-super` |
| 新增功能 | `/feature` | `/ai-feature` |
| 修改已有行为或规则 | `/change` | `/ai-change` |
| 定位并修复 bug | `/fix` | `/ai-fix` |
| 对比技术选型 | `/tech` | `/ai-tech` |
| 更新部署或发布说明 | `/deploy` | `/ai-deploy` |
| 更新接手和交接说明 | `/handoff` | `/ai-handoff` |
| 更新阶段、里程碑和优先级 | `/roadmap` | `/ai-roadmap` |
| 推荐下一步功能或优化 | `/plan` | `/ai-plan` |
| 写入当前进度快照 | `/status` | `/ai-status` |
| 在新对话继续开发 | `/continue` | `/ai-continue` |
| 更新本地 skills 或项目文档 | `/upgrade` | `/ai-upgrade` |

## 安装到 Codex

克隆仓库或下载源码压缩包，然后在仓库根目录运行安装脚本。

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

### macOS/Linux

```bash
chmod +x ./install.sh
./install.sh
```

Codex 安装脚本会把 skills 复制到：

```text
~/.agents/skills
```

安装完成后，重启 Codex desktop，让命令菜单重新扫描 skills。

## 安装到 Claude Code

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\install-claude.ps1
```

### macOS/Linux

```bash
chmod +x ./install-claude.sh
./install-claude.sh
```

Claude Code 安装脚本会把别名 skills 复制到：

```text
~/.claude/skills
```

安装完成后，重启 Claude Code，让它重新扫描 skills。在 Claude Code 里使用 `/ai-init`、`/ai-goal`、`/ai-feature` 等 `ai-` 命令。

## 常见用法

启动新项目：

```text
/init 构建一个团队任务管理应用，包含登录、项目、看板任务、成员邀请、基础权限、本地启动说明和部署文档。
```

Claude Code 对应写法：

```text
/ai-init 构建一个团队任务管理应用，包含登录、项目、看板任务、成员邀请、基础权限、本地启动说明和部署文档。
```

用高自治模式执行完整目标：

```text
/goal --super 完成团队任务管理系统 MVP。普通产品和技术决策由你自行选择并记录，只在涉及付费服务、破坏性操作、密钥、生产数据或安全合规风险时停止询问。
```

Claude Code 对应写法：

```text
/ai-goal --super 完成团队任务管理系统 MVP。普通产品和技术决策由你自行选择并记录，只在涉及付费服务、破坏性操作、密钥、生产数据或安全合规风险时停止询问。
```

在新对话中继续：

```text
/continue
```

离开当前对话前记录状态：

```text
/status
```

从 GitHub 最新包更新本地已安装的 skills：

```text
/upgrade 从 GitHub 更新我本地的 skills。
```

Claude Code 对应写法：

```text
/ai-upgrade 从 GitHub 更新我本地的 skills。
```

## Skill 会创建的项目文档

项目初始化后，会得到类似下面的文档集合：

```text
AI_DEVELOPMENT_RULES.md
docs/
  00_START_HERE.md
  01-requirements-clarification.md
  02-development-principles.md
  03-feature-changelog.md
  04-tech-decisions.md
  05-handoff-guide.md
  06-roadmap.md
  07-local-development.md
  08-deployment.md
  09-ai-project-start-prompt.md
  10-current-status.md
  11-project-structure.md
  12-upgrade-history.md
  13-command-reference.md
  14-decision-log.md
```

这些文件是项目的连续性层。它们能让另一个对话、另一个 AI 助手或另一个开发者理解已经做过的决策，以及后面还要做什么。

## 设计原则

- 新项目先澄清需求并生成文档，再进入实现。
- 已有项目使用 `/upgrade` 或 `/ai-upgrade`，不要破坏性重新初始化。
- 重要技术选型默认需要给出方案对比和确认。
- `--super` 会跳过普通确认，但必须记录重要决策。
- 涉及页面的工作，结束时必须给出手工浏览器测试步骤。
- 跨对话连续性通过 `docs/10-current-status.md` 保存。
- 项目结构知识写入 `docs/11-project-structure.md`。
- 命令语义写入 `docs/13-command-reference.md`。
- 高自治决策写入 `docs/14-decision-log.md`。

## 仓库结构

```text
skills/                 安装到 ~/.agents/skills 的 Codex skill 文件夹
claude-skills/          安装到 ~/.claude/skills 的 Claude Code 别名 skill 文件夹
install.ps1             Codex Windows 安装脚本
install.sh              Codex macOS/Linux 安装脚本
install-claude.ps1      Claude Code Windows 安装脚本
install-claude.sh       Claude Code macOS/Linux 安装脚本
README.md               英文项目说明
README.zh-CN.md         简体中文项目说明
LICENSE                 MIT 许可证
CHANGELOG.md            英文变更日志
CHANGELOG.zh-CN.md      简体中文变更日志
CONTRIBUTING.md         英文贡献指南
CONTRIBUTING.zh-CN.md   简体中文贡献指南
SECURITY.md             英文安全策略
SECURITY.zh-CN.md       简体中文安全策略
```

每个命令都被打包成独立 skill 文件夹。仓库会有意在不同命令别名下重复内置项目模板，以便安装简单、离线可用。

## 更新已安装的 Skills

Codex：

```text
/upgrade 从 GitHub 更新我本地的 skills。
```

Claude Code：

```text
/ai-upgrade 从 GitHub 更新我本地的 skills。
```

更新器会从 `1447751897/ai-project-command-skills` 下载最新包，验证 skill 文件夹完整性，把旧版安装备份到对应工具目录下的 `.backup/`，然后替换本地已安装的 skill 文件夹。更新完成后需要重启对应工具。

手动更新也仍然可用。拉取最新仓库内容并重新运行安装脚本：

```bash
git pull
./install.sh
./install-claude.sh
```

Windows：

```powershell
git pull
powershell -ExecutionPolicy Bypass -File .\install.ps1
powershell -ExecutionPolicy Bypass -File .\install-claude.ps1
```

如果某个项目已经用旧版本初始化过，请在 Codex 里运行 `/upgrade`，或在 Claude Code 里运行 `/ai-upgrade`。这会补充缺失的新文档和规则，不会覆盖项目自己的已有内容。
