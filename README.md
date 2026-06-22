# AI Project Command Skills

文档驱动的 AI 编程工作流技能包。覆盖从立项评估到复盘沉淀的完整项目生命周期，支持 Claude Code、Codex 等 AI 编程工具。

## 项目生命周期

```
/zno-evaluate  立项评估（值不值得做？）
      |
/zno-init      需求澄清 + 文档初始化 + 设计方向
      |
/zno-tech      技术选型门禁（2-3 方案对比）
      |
/zno-feature   迭代开发（TDD + 验证门禁）
      |
/zno-review    代码自审（5 维度）
      |
/zno-deploy    发布上线
      |
/zno-retro     复盘沉淀（踩坑 -> 写规则 -> 下个项目受益）
```

## 命令一览

| 命令 | 用途 |
| --- | --- |
| /zno-evaluate | 立项评估：苏格拉底式提问验证项目价值，输出 做/不做/延期 |
| /zno-init | 初始化项目：澄清需求、生成核心文档、确定设计方向和 token |
| /zno-goal | 目标模式：自动串起所有步骤，只在关键节点停下确认 |
| /zno-goal --super | 高自治模式：AI 全权决策并记录 |
| /zno-feature | 新功能：TDD 流程 + 验证门禁 |
| /zno-change | 行为变更：识别影响范围再实现 |
| /zno-fix | 修 bug：复现、定位、修复、验证 |
| /zno-tech | 技术选型：2-3 方案对比，用户确认后实现 |
| /zno-deploy | 部署发布：环境/迁移/验证/回滚 |
| /zno-review | 代码审查：安全/性能/错误处理/SOLID/项目规范 |
| /zno-retro | 复盘：原计划 vs 实际，提炼可复用规则 |
| /zno-plan | 功能推荐：不确定做什么时，给出 3-7 个方向 |
| /zno-status | 状态快照：保存当前进度，方便续接 |
| /zno-continue | 续接：新会话恢复上次状态继续开发 |
| /zno-handoff | 交接：生成接手文档 |
| /zno-roadmap | 路线图：调整优先级和里程碑 |
| /zno-upgrade | 升级：拉取最新 skill 版本 |

## 快速安装

### 一键安装（推荐）

自动检测本机安装的 AI 工具并安装对应技能包：

macOS/Linux:

```bash
git clone https://github.com/1447751897/ai-project-command-skills.git
cd ai-project-command-skills
chmod +x install-all.sh && ./install-all.sh
```

Windows:

```powershell
git clone https://github.com/1447751897/ai-project-command-skills.git
cd ai-project-command-skills
powershell -ExecutionPolicy Bypass -File .\install-all.ps1
```

### 仅安装到 Claude Code

```bash
chmod +x install-claude.sh && ./install-claude.sh
```

安装目标：`~/.claude/skills/zno-*/`

### 仅安装到 Codex

```bash
chmod +x install.sh && ./install.sh
```

安装目标：`~/.agents/skills/zno-*/`

### 安装后

重启对应的 AI 工具，然后输入 `/zno-init` 开始使用。

## 从旧版本升级（ai- 到 zno-）

如果你之前安装的是 `ai-*` 前缀版本（v1.x），**不能用旧的 /ai-upgrade 升级**，需要重新安装一次：

```bash
git clone https://github.com/1447751897/ai-project-command-skills.git
cd ai-project-command-skills
./install-all.sh

# 删除旧的 ai-* 目录（可选）
rm -rf ~/.claude/skills/ai-*
rm -rf ~/.agents/skills/ai-*
```

重装后，后续用 `/zno-upgrade` 即可正常增量更新。

## 核心设计理念

1. **文档驱动** — 先澄清需求、写文档，确认后才写代码
2. **渐进生成** — /zno-init 只建必要文件，其余按需触发时才创建
3. **质量内建** — TDD 流程 + 验证门禁 + 代码自审，不是事后补
4. **设计 Token 约束** — 前端颜色/间距/圆角必须引用 token，禁止硬写入 AI_DEVELOPMENT_RULES.md，下个项目自动遵守
6. **跨会话续接** — /zno-status 保存、/zno-continue 恢复，不怕断

## 项目文档结构

`/zno-init` 后生成的核心文档（渐进式，按需补充）：

```
AI_DEVELOPMENT_RULES.md               AI 开发规范（项目级）
docs/
  product/
    01-requirements-clarification.md   需求澄清
    06-roadmap.md                      路线图
    15-frontend-design.md              设计方向
    15-frontend-design-tokens.json     设计 Token（可执行约束）
  engineering/
    02-development-principles.md       开发原则
    04-tech-decisions.md               技术选型记录（按需）
  development/
    03-feature-changelog.md            功能变更记录（按需）
    10-current-status.md               当前状态快照（按需）
    14-decision-log.md                 自治决策记录（按需）
    16-retrospective.md                复盘记录（按需）
  operations/
    07-local-development.md            本地开发说明（按需）
    08-deployment.md                   部署说明（按需）
  handoff/
    05-handoff-guide.md                接手指南（按需）
```

## 典型使用示例

```text
# 评估一个想法
/zno-evaluate 我想做一个团队任务管理工具，带看板和成员邀请

# 确认要做后，初始化项目
/zno-init 团队任务管理工具，支持登录、项目、看板任务、成员邀请、基本权限

# 全自动推进
/zno-goal --super 完成团队任务管理 MVP

# 开发中途保存状态
/zno-status

# 新会话续接P 阶段已完成

# 升级到最新版本
/zno-upgrade
```

## 在线升级

安装后可直接通过命令升级，无需重新 clone：

```text
/zno-upgrade
```

脚本会从 GitHub 下载最新版本，备份旧版本后替换。重启工具即可生效。

## 仓库结构

```
skills/                 技能包目录（统一 source，所有平台共用）
install-all.sh/.ps1     自动检测安装脚本
install-claude.sh/.ps1  Claude Code 安装脚本
install.sh/.ps1         Codex 安装脚本
README.md               项目文档
CHANGELOG.md            更新日志
LICENSE                 MIT 协议
```

## 许可

MIT
