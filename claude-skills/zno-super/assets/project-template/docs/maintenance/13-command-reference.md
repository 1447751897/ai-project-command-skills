# Command Reference

本文档说明本项目可使用的 AI 开发命令、适用场景和会更新的文档。新成员、后续 AI 助手或切换对话时，应先了解这些命令。

## 1. 命令总览

| 命令 | 适用场景 | 主要作用 | 常更新文档 |
| --- | --- | --- | --- |
| `/zno-init` | 新项目开始 | 需求澄清、初始化项目文档、确认后进入开发 | 全部初始文档 |
| `/zno-upgrade` | 更新本地 skills，或已有项目接入/Skill 模板升级 | 本地 skills 更新时从 GitHub 拉取最新包并覆盖安装；项目文档升级时只补齐缺失文档和新增规则，不覆盖已有内容 | `maintenance/12-upgrade-history.md`, `development/10-current-status.md` |
| `/zno-continue` | 新对话继续开发 | 读取项目规则、当前状态、路线图、技术决策后继续 | 视任务而定 |
| `/zno-status` | 暂停、切换对话、阶段完成、交接前 | 更新当前开发进度快照 | `development/10-current-status.md` |
| `/zno-feature` | 新增功能 | 澄清需求、评估影响、更新文档、实现功能 | `01`, `03`, `04`, `06`, `10`, `11` |
| `/zno-change` | 修改已有功能或业务规则 | 评估影响范围、更新相关文档、实现变更 | `01`, `03`, `04`, `06`, `10` |
| `/zno-fix` | 修复 bug 或回归问题 | 定位、修复、验证，必要时记录变更 | `03`, `10` |
| `/zno-tech` | 技术选型、架构调整、重大依赖 | 给出 2-3 个方案，等待确认后记录并实现 | `04`, `10`, `11` |
| `/zno-deploy` | 部署、环境变量、发布、回滚、CI/CD | 更新部署和本地开发说明 | `07`, `08`, `10` |
| `/zno-handoff` | 交接、接手指南、项目结构说明 | 更新接手路径、关键目录、注意事项 | `05`, `10`, `11` |
| `/zno-roadmap` | 阶段计划、MVP、优先级、里程碑调整 | 更新阶段路线图和受影响范围 | `06`, `10` |
| `/zno-plan` | 没有头绪、想要功能推荐或下一步规划 | 基于现有文档推荐功能方向、优化项和优先级，等待用户选择 | `06`, `10`，确认后视情况更新 `01`, `04`, `11` |
| `/zno-goal` | 想围绕一个最终目标自动推进 | 创建/进入目标推进模式，自动拆解、开发、更新文档，只在关键确认或阻塞时停下 | 全部相关文档 |
| `/zno-goal --super` | 想让 AI 全程高自治推进，不等待普通确认 | AI 自主做技术/产品/实现决策并继续推进，最后输出决策过程 | `development/14-decision-log.md` 及相关文档 |

文档编号说明：

```text
README = docs/README.md
01 = docs/product/01-requirements-clarification.md
03 = docs/development/03-feature-changelog.md
04 = docs/engineering/04-tech-decisions.md
05 = docs/handoff/05-handoff-guide.md
06 = docs/product/06-roadmap.md
07 = docs/operations/07-local-development.md
08 = docs/operations/08-deployment.md
10 = docs/development/10-current-status.md
11 = docs/engineering/11-project-structure.md
12 = docs/maintenance/12-upgrade-history.md
15 = docs/product/15-frontend-design.md
```

## 2. 推荐使用流程

新项目：

```text
/zno-init 项目需求说明
```

自动推进一个完整目标：

```text
/zno-goal 完成团队任务管理系统 MVP，包括登录、项目管理、任务看板、成员邀请、基础权限、本地启动和部署说明
```

高自治自动推进：

```text
/zno-goal --super 完成团队任务管理系统 MVP，全程由 AI 自主决策并记录决策过程
```

已有项目接入：

```text
/zno-upgrade 把当前项目接入 AI 项目文档规范，不覆盖已有内容
```

更新本地已安装的 skills：

```text
/zno-upgrade 从 GitHub 更新我本地的 skills
```

新增功能：

```text
/zno-feature 新增用户邀请功能，管理员可以邀请成员加入团队
```

技术选型：

```text
/zno-tech 选择邮件发送方案
```

没有头绪，需要推荐下一步：

```text
/zno-plan 初版已经完成了，但我不知道后面该加什么
```

离开当前对话前：

```text
/zno-status 总结当前开发进度
```

新对话继续：

```text
/zno-continue 继续上次开发
```

## 3. 技术选型门禁

涉及以下内容时，AI 不能直接实现，必须先给出 2-3 个方案并等待用户确认：

1. 前端/后端框架、构建工具、运行时。
2. 数据库、缓存、消息队列、搜索、对象存储。
3. 鉴权、权限、支付、邮件、短信、推送、第三方登录。
4. 部署平台、CI/CD、容器化、监控、日志、任务调度。
5. 图表、富文本、地图、表格、文件预览等重型前端依赖。
6. 会影响性能、成本、安全、维护方式的新增依赖或服务。

方案推荐必须包含：

```text
技术需求：
约束条件：
候选方案：
推荐方案：
推荐理由：
性能影响：
维护成本：
风险与回退：
需要用户确认的问题：
```

## 4. 命令使用原则

1. `/zno-init` 通常只在新项目开始时使用一次。
2. 已有项目不要重新 `/zno-init`，优先使用 `/zno-upgrade`。
3. 当用户要求“更新本地 skills / 更新命令 / 从 GitHub 拉最新包 / 刷新 ~/.claude/skills”时，`/zno-upgrade` 应运行 `scripts/update_installed_skills.py`，而不是项目文档升级流程。
4. 日常开发可以直接描述需求；命令用于明确意图和增强稳定性。
5. 切换对话前使用 `/zno-status`，新对话使用 `/zno-continue`。
6. 如果文档已经清楚说明需求，AI 不应重复澄清；如果文档缺失、冲突或影响实现决策，AI 必须先澄清。
7. 当用户没有明确需求、想要建议或不知道下一步时，优先使用 `/zno-plan`，AI 只做推荐和规划，不能直接实现。
8. 完成需求开发后，最终回复必须给出可直接在页面上验证的手动测试步骤；不涉及页面时说明替代验证方式。
9. 当用户想要“给一个目标后自动推进”，优先使用 `/zno-goal`。`/zno-goal` 会尽量自动推进，但不能绕过技术选型确认、需求关键澄清和安全/数据/部署等高风险门禁。
10. 当用户使用 `/zno-goal --super` 时，AI 可以跳过默认确认门禁，自主选择方案并继续推进，但必须记录关键决策过程、风险和回退方式。
11. 新项目涉及界面时，`/zno-init` 必须先收集或推荐 UI 风格参考，并在 `docs/product/15-frontend-design.md` 中记录产品形态、设计关键词、色彩、布局、组件风格、交互状态和需要避免的问题。
12. 后续需求如果影响产品形态、UI 风格、布局、组件策略或交互状态，必须反向更新 `docs/product/15-frontend-design.md`。

## 5. 完成后的页面测试步骤

每次完成 `/zno-feature`、`/zno-change`、`/zno-fix` 或其他涉及页面的开发后，最终回复必须包含：

```text
页面测试步骤：
1. 打开：
2. 前置条件：
3. 操作：
4. 输入：
5. 预期结果：
6. 异常/边界验证：
```

要求：

1. 步骤必须能让用户直接在浏览器页面操作。
2. 不要只给命令行验证。
3. 至少包含一个正常流程。
4. 有明显边界时，补充异常或边界流程。
5. 如果本次是纯后端、脚本、配置或文档改动，说明“本次无页面手测步骤”，并给出 API、命令或配置验证方式。

## 6. `/zno-plan` 输出要求

`/zno-plan` 必须先读取现有项目文档，再给出建议：

```text
必须读取：
- docs/product/01-requirements-clarification.md
- docs/development/03-feature-changelog.md
- docs/product/06-roadmap.md
- docs/development/10-current-status.md
- docs/engineering/11-project-structure.md
```

推荐结果应包含：

1. 当前项目阶段判断。
2. 当前核心闭环是否完整。
3. 3-7 个候选方向。
4. 每个方向的用户价值、实现复杂度、优先级、依赖条件。
5. 性能、安全、部署或技术选型影响。
6. 推荐先做哪 1-2 个。
7. 明确询问用户选择哪个方向。

`/zno-plan` 不直接写代码。只有用户选择某个方向后，才进入 `/zno-feature`、`/zno-change`、`/zno-tech` 或 `/zno-roadmap` 流程。

## 7. `/zno-goal` 自动推进规则

`/zno-goal` 用于 Claude Code Goal 模式或类似长期目标模式。它的目标是减少用户反复输入命令，让 AI 围绕最终目标持续推进。

`/zno-goal` 必须执行：

1. 如果运行环境支持 Claude Code Goal 工具，先创建或使用一个明确目标。
2. 如果项目未初始化，自动执行 `/zno-init` 的需求澄清和文档初始化流程。
3. 如果项目已初始化，自动读取 `/zno-continue` 所需文档。
4. 自动拆分阶段任务和近期可执行任务。
5. 自动按 `/zno-feature`、`/zno-change`、`/zno-fix`、`/zno-tech`、`/zno-deploy` 等规则推进，不要求用户反复输入命令。
6. 每完成一个功能，自动更新相关文档和 `docs/development/10-current-status.md`。
7. 涉及页面功能时，最终回复必须给出页面手动测试步骤。
8. 只有遇到以下情况才停下来问用户：
   - 需求关键边界不清楚。
   - 核心技术选型需要确认。
   - 涉及付费服务、生产部署、安全、权限、数据删除或合规风险。
   - 出现无法自行解决的阻塞。

推荐提示：

```text
/zno-goal 完成某个项目或阶段。低风险实现细节由 AI 自主决定并记录；高风险技术选型、付费服务、安全/权限/数据结构变化必须先问我。
```

## 8. `/zno-goal --super` 高自治模式

`/zno-goal --super` 用于用户明确希望 AI 全程自动推进、不反复询问确认的场景。

`/zno-goal --super` 的行为：

1. 自动进入 `/zno-goal` 的长期目标推进流程。
2. 遇到技术选型、功能细节、实现路径、依赖选择时，AI 可以直接选择推荐方案并继续实现。
3. 每个关键决策必须记录到 `docs/development/14-decision-log.md`。
4. 最终回复必须总结主要决策过程、取舍、风险和已验证内容。
5. 页面功能仍必须输出页面手动测试步骤。

`/zno-goal --super` 仍然不能做以下事情，除非用户明确授权：

1. 使用真实付费服务或产生费用。
2. 删除生产数据或执行不可逆操作。
3. 泄露、提交或硬编码密钥。
4. 绕过明显的安全、权限或合规风险。
5. 执行破坏性 Git 操作，例如 `git reset --hard`。

推荐提示：

```text
/zno-goal --super 完成某个项目或阶段。全程由 AI 自主决策并推进，关键决策写入 docs/development/14-decision-log.md，遇到付费、生产数据、安全合规或不可逆操作时再问我。
```

兼容别名：

```text
/zno-super <目标>
```

`/zno-super` 等价于 `/zno-goal --super <目标>`，但推荐优先使用 `/zno-goal --super`。
