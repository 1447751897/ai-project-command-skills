# AI Project Command Skills

简体中文 | [English](README.md)

面向 Codex 的文档优先工作流 skill 集合，用于项目初始化、功能开发、Goal 模式自动推进、交接和跨对话续接。

这个包会安装一组类似斜杠命令的 workflow skills，例如 `/init`、`/goal`、`/feature`、`/status`、`/continue`。这些 skill 会帮助 AI 编程助手先澄清需求、持续维护项目文档、在技术选型时做明确取舍，并把足够多的项目状态沉淀到仓库文件里，方便后续新的对话、其他 AI 或其他开发者继续接手。

## 命令

| 命令 | 用途 |
| --- | --- |
| `/init` | 启动新项目：先澄清需求、生成项目文档，并在正式开发前等待确认。 |
| `/goal` | 执行较长的项目或阶段目标，自动拆分任务并持续推进。 |
| `/goal --super` | 高自治 Goal 模式：AI 可以自行做普通产品/技术决策，并记录决策过程。 |
| `/super` | `/goal --super` 的兼容别名。 |
| `/feature` | 新增功能，同时更新文档、变更日志，并在结果中给出页面测试步骤。 |
| `/change` | 修改已有行为或业务规则，并记录影响范围。 |
| `/fix` | 定位、修复、验证并记录 bug 修复。 |
| `/tech` | 在采用重要依赖或架构方案前，对比技术选项。 |
| `/deploy` | 更新部署、环境变量、CI/CD、发布或回滚说明。 |
| `/handoff` | 更新新人介入、项目结构和交接说明。 |
| `/roadmap` | 更新阶段计划、MVP 范围、里程碑和优先级。 |
| `/plan` | 当你不确定下一步做什么时，让 AI 推荐后续功能或优化方向。 |
| `/status` | 写入当前进度快照，方便以后继续。 |
| `/continue` | 在新对话里读取项目文档和当前状态后继续开发。 |
| `/upgrade` | 从 GitHub 更新本地已安装的 skills，或把新版模板中缺失的文档/规则补进已有项目且不覆盖已有内容。 |

## 安装

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

安装脚本会把 skills 复制到：

```text
~/.agents/skills
```

安装完成后，重启 Codex desktop，让命令菜单重新扫描 skills。

## 常见用法

启动新项目：

```text
/init 构建一个团队任务管理应用，包含登录、项目、看板任务、成员邀请、基础权限、本地启动说明和部署文档。
```

用普通确认门禁执行完整目标：

```text
/goal 完成团队任务管理系统 MVP。
```

用高自治模式执行完整目标：

```text
/goal --super 完成团队任务管理系统 MVP。普通产品和技术决策由你自行选择并记录，只在涉及付费服务、破坏性操作、密钥、生产数据或安全合规风险时停止询问。
```

在新对话中继续：

```text
/continue
```

离开当前对话前记录状态：

```text
/status
```

升级一个已经用旧版本初始化过的项目：

```text
/upgrade
```

从 GitHub 最新包更新本地已安装的 skills：

```text
/upgrade 从 GitHub 更新我本地的 skills。
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
- 已有项目使用 `/upgrade`，不要破坏性重新初始化。
- 重要技术选型默认需要给出方案对比和确认。
- `/goal --super` 会跳过普通确认，但必须记录重要决策。
- 涉及页面的工作，结束时必须给出手工浏览器测试步骤。
- 跨对话连续性通过 `docs/10-current-status.md` 保存。
- 项目结构知识写入 `docs/11-project-structure.md`。
- 命令语义写入 `docs/13-command-reference.md`。
- 高自治决策写入 `docs/14-decision-log.md`。

## 仓库结构

```text
skills/                 安装到 ~/.agents/skills 的 skill 文件夹
install.ps1             Windows 安装脚本
install.sh              macOS/Linux 安装脚本
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

每个命令都被打包成独立 skill 文件夹，这样 Codex 可以在命令菜单中展示它。仓库会有意在不同命令别名下重复内置项目模板，以便安装简单、离线可用。

## 更新已安装的 Skills

如果这些 skills 已经安装到本机，可以直接让 Codex 运行更新器：

```text
/upgrade 从 GitHub 更新我本地的 skills。
```

更新器会从 `1447751897/ai-project-command-skills` 下载最新包，验证 skill 文件夹完整性，把旧版安装备份到 `~/.agents/skills/.backup/`，然后替换本地已安装的 skill 文件夹。更新完成后需要重启 Codex desktop。

手动更新也仍然可用。拉取最新仓库内容并重新运行安装脚本：

```bash
git pull
./install.sh
```

Windows：

```powershell
git pull
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

然后重启 Codex desktop。

如果某个项目已经用旧版本初始化过，请在该项目里运行：

```text
/upgrade
```

这会补充缺失的新文档和规则，不会覆盖项目自己的已有内容。
