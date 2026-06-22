# Project Docs Template

这是一套给 AI 开发助手使用的新项目启动文档模板。

## 推荐目录放置方式

把本文件夹内容复制到新项目的 `docs/` 目录：

```text
project-root/
  AI_DEVELOPMENT_RULES.md
  docs/
    00_START_HERE.md
    README.md
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
    15-frontend-design.md
```

## 文件级分类

### 核心规则

| 文档 | 作用 |
| --- | --- |
| `AI_DEVELOPMENT_RULES.md` | 项目的长期 AI 开发总规则 |
| `00_START_HERE.md` | 新项目启动流程，要求 AI 先澄清需求再开发 |
| `02-development-principles.md` | 记录项目级开发原则、代码组织、API、数据、安全和质量规则 |

### 需求与计划

| 文档 | 作用 |
| --- | --- |
| `01-requirements-clarification.md` | 记录项目目标、用户、功能、业务流程和验收标准 |
| `06-roadmap.md` | 阶段路线图和每个阶段的验收标准 |

### 设计与技术

| 文档 | 作用 |
| --- | --- |
| `04-tech-decisions.md` | 记录技术选型的目的、原因、备选方案和影响 |
| `11-project-structure.md` | 项目整体结构、目录职责、模块地图和新增文件放置规则 |
| `15-frontend-design.md` | 记录产品形态、UI 风格参考、设计关键词、色彩、布局、组件和交互状态 |

### 开发过程

| 文档 | 作用 |
| --- | --- |
| `03-feature-changelog.md` | 记录开发过程中新增、变更、删除和修复的功能 |
| `10-current-status.md` | 当前开发进度快照，用于跨对话和交接接续 |
| `14-decision-log.md` | 高自治模式和重要技术/产品决策记录 |

### 运行与交付

| 文档 | 作用 |
| --- | --- |
| `07-local-development.md` | 本地开发环境、启动命令、调试方式和常见问题 |
| `08-deployment.md` | 部署环境、构建命令、部署步骤、上线验证和回滚方案 |

### 交接与使用说明

| 文档 | 作用 |
| --- | --- |
| `05-handoff-guide.md` | 给后续开发者或 AI 助手的接手指南 |
| `README.md` | 文档入口和文件级分类说明 |
| `09-ai-project-start-prompt.md` | 新项目首次对话可直接复制的提示词 |
| `12-upgrade-history.md` | Skill 或模板升级记录，说明新增文档和规则如何补齐 |
| `13-command-reference.md` | 命令清单，说明每个命令的适用场景和作用 |

## 建议工作流

1. 新项目开始前，先放入 `AI_DEVELOPMENT_RULES.md` 和 `docs/` 模板。
2. 把 `09-ai-project-start-prompt.md` 里的提示词发给 AI。
3. AI 先复述需求，再提出澄清问题。
4. 用户确认后，AI 填充 `docs/` 下的项目文档；涉及界面的项目必须先收集 UI 风格参考并更新 `15-frontend-design.md`。
5. 文档确认后，再进入开发。
6. 每次新增功能后更新 `03-feature-changelog.md`。
7. 每次技术选型变化后更新 `04-tech-decisions.md`。
8. 每次启动、部署方式变化后更新 `07-local-development.md` 或 `08-deployment.md`。
9. 每次暂停、切换对话、阶段完成或交接前更新 `10-current-status.md`。
10. 每次目录结构或模块边界变化后更新 `11-project-structure.md`。
11. 每次使用 `/ai-upgrade` 补齐项目新模板后更新 `12-upgrade-history.md`；如果是更新本地已安装 skills，则运行本地 skills 更新器并提示重启 Claude Code。
12. 每次新增、删除或改变命令语义后更新 `13-command-reference.md`。
13. 每次产品形态、UI 风格、布局、组件策略或交互状态发生变化后更新 `15-frontend-design.md`。
14. 没有明确下一步时使用 `/ai-plan` 获取功能推荐和优先级建议。
15. 想让 AI 围绕一个最终目标自动推进时使用 `/ai-goal`。
16. 想让 AI 全程高自治推进、不等待普通确认时使用 `/ai-goal --super`，但关键决策必须记录到 `14-decision-log.md`。`/ai-super` 仅作为兼容别名。

## 中途新增需求

项目启动提示词只需要在项目开始时给一次。

后续开发过程中，用户可以直接描述新需求，不需要重复粘贴完整提示词。AI 必须自动根据 `00_START_HERE.md` 的“中途新增需求流程”执行：先判断影响范围，必要时澄清，再更新相关文档，最后进入开发。

## 跨对话接续

当前对话准备结束或要切换到新对话时，先执行：

```text
/ai-status 总结当前开发进度
```

新对话开始时执行：

```text
/ai-continue 继续上次开发
```

AI 必须先读取 `docs/10-current-status.md` 以及相关项目文档，再继续开发。

## 模板升级

如果项目已经初始化过，但 Skill 新版本增加了文档或规则，执行：

```text
/ai-upgrade
```

AI 必须只补齐缺失文档和新增规则，不覆盖已有项目内容，并更新 `docs/12-upgrade-history.md`。

如果用户要求更新本地已安装的 skills，例如“从 GitHub 更新本地 skills”或“刷新 ~/.claude/skills”，`/ai-upgrade` 应运行：

```text
python <installed-skills-dir>/ai-upgrade/scripts/update_installed_skills.py
```

该脚本会下载 GitHub 最新包、验证 skill 文件夹、备份旧安装并覆盖本地 skill 文件夹。完成后需要重启 Claude Code。
