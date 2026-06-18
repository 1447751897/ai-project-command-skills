# 贡献指南

简体中文 | [English](CONTRIBUTING.md)

感谢你改进 AI Project Command Skills。

## 开发注意事项

- 命令行为需要同时写在 skill 指令里，以及内置项目模板的 `docs/13-command-reference.md` 中。
- 如果新增项目文档模板，请同步更新：
  - `docs/00_START_HERE.md`
  - `docs/README.md`
  - `docs/09-ai-project-start-prompt.md`
  - 如有必要，更新 `docs/12-upgrade-history.md` 的预期说明
- 如果修改技术决策行为，请同步更新 `docs/04-tech-decisions.md`，必要时也更新 `docs/14-decision-log.md`。
- 如果修改 Codex 可安装命令名称，请同时更新 `install.ps1` 和 `install.sh`。
- 如果新增或重命名 workflow skill，请保持 `skills/` 和 `claude-skills/` 同步。Claude Code 别名应保留 `ai-` 前缀。
- 如果修改 Claude Code 命令名称，请同时更新 `install-claude.ps1` 和 `install-claude.sh`。
- 保留 `/super` 作为 `/goal --super` 的兼容别名。
- 如果修改面向用户的顶层英文文档，请同步维护对应的 `*.zh-CN.md` 中文文档。

## 验证

发布变更前，请完成：

1. 使用当前平台的安装脚本在本地安装。
2. 重启 Codex desktop。
3. 确认命令菜单能找到被修改的命令。
4. 至少测试：

```text
/init 测试项目
/goal 测试目标
/goal --super 测试目标
/upgrade
/status
/continue
```

Claude Code 兼容性还需要验证别名包：

```text
/ai-init 测试项目
/ai-goal 测试目标
/ai-goal --super 测试目标
/ai-upgrade
/ai-status
/ai-continue
```

## Pull Request

请在 PR 中说明：

- 哪个命令或文档行为发生了变化。
- 哪些内置模板被更新。
- 如果适用，Codex skills 和 Claude Code 别名 skills 是否都已同步。
- 英文/中文文档是否都已同步。
- 你如何验证这次变更。
