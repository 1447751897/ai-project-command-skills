# 更新日志

## 2.0.0 - 2026-06-22

大版本升级：命令前缀统一为 zno-，新增立项评估和复盘沉淀，合并双目录为单一 source。

### 破坏n- 所有命令前缀从 ai- / 无前缀统一为 zno-（如 /zno-init、/zno-feature）
- claude-skills/ 和 skills/ 合并为单一 skills/ 目录
- 旧版 /ai-upgrade 无法升级到本版本，需重新安装

### 新增功能

- /zno-evaluate：立项评估，苏格拉底式提问验证项目价值，输出 做/不做/延期
- /zno-retro：复盘沉淀，阶段完成后回顾，提炼可复用规则写入 AI_DEVELOPMENT_RULES.md
- /zno-review：代码自审，5 维度审查（安全/性能/错误处理/SOLID/项目规范）
- TDD 流程：有测试框架时默认 Red-Green-Refactor
- 验证门禁：实现完成后必须提供至少 2 项证据才能标记完成
- 前端设计 Token 文件（15-frontend-design-tokens.json）：AI 写前端必须引用 token 值
- 渐进式文档生成：/zno-init 只建 8 个核心文件，其余按需触发时才创建

### 改进

- init_project_docs.py 新增 --scaffold 按需生成、--full 全量生成
- update_installed_skills.py 新增 rename 和内容替换兼容逻辑
- AI_DEVELOPMENT_RULES.md 模板新增 TDD、验证门禁、Token 约束规则
- README 改为中文优先，GitHub About 描述更新为中文

### 文档模板新增

- docs/development/16-retrospective.md：复盘记录模板
- docs/product/15-frontend-design-tokens.json：设计 Token 模板

## 0.2.1 - 2026-06-22

前端设计初始化和文档目录分类。

- 新增 docs/product/15-frontend-design.md 项目模板
- /init 现在会收集或推荐 UI 风格参考，记录设计关键词
- 项目文档移入父目录分类

## 0.2.0 - 2026-06-18

Claude Code 兼容。

- 新增自动检测安装脚本 install-all.ps1 / install-all.sh
- 新增 Claude Code 别名技能包
- 新增 /ai-* 命令别名避免与 Claude Code 内置命令冲突
- GitHub 自更新脚本支持 --tool codex|claude 参数

## 0.1.1 - 2026-06-17

文档更新。新增中文文档和本地技能更新脚本。

## 0.1.0 - 2026-06-17

首次开源发布。包含 15 个命令和完整项目文档模板。
