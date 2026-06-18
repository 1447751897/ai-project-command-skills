# 变更日志

简体中文 | [English](CHANGELOG.md)

## 0.2.0 - 2026-06-18

适配 Claude Code。

- 新增 `claude-skills/`，提供 Claude Code 专用别名 skills。
- 新增 Claude Code 安装脚本：`install-claude.ps1` 和 `install-claude.sh`。
- 为 Claude Code 新增 `/ai-*` 命令别名，避免和 `/init`、`/plan`、`/upgrade` 等内置命令冲突。
- 扩展 GitHub 自更新器，支持 `--tool codex|claude`；Codex 更新到 `~/.agents/skills`，Claude Code 更新到 `~/.claude/skills`。
- 更新英文和简体中文文档，补充双工具安装方式和命令对照表。

## 0.1.1 - 2026-06-17

文档更新。

- 新增简体中文文档，适配中文用户。
- 在英文和中文文档之间加入语言切换链接。
- 为 `/upgrade` 增加本地 skills 更新器，可以从 GitHub 最新包刷新本机已安装的 skills。

## 0.1.0 - 2026-06-17

首次开源发布。

包含命令：

- `/init`
- `/goal`
- `/goal --super`
- `/super` 兼容别名
- `/feature`
- `/change`
- `/fix`
- `/tech`
- `/deploy`
- `/handoff`
- `/roadmap`
- `/plan`
- `/status`
- `/continue`
- `/upgrade`

包含项目文档：

- `AI_DEVELOPMENT_RULES.md`
- `docs/00_START_HERE.md`
- `docs/01-requirements-clarification.md`
- `docs/02-development-principles.md`
- `docs/03-feature-changelog.md`
- `docs/04-tech-decisions.md`
- `docs/05-handoff-guide.md`
- `docs/06-roadmap.md`
- `docs/07-local-development.md`
- `docs/08-deployment.md`
- `docs/09-ai-project-start-prompt.md`
- `docs/10-current-status.md`
- `docs/11-project-structure.md`
- `docs/12-upgrade-history.md`
- `docs/13-command-reference.md`
- `docs/14-decision-log.md`
