# 贡献指南

感谢你改进 AI Project Command Skills。

## 开发约定

- 命令行为必须同时记录在 SKILL.md 和项目模板的 `docs/maintenance/13-command-reference.md` 中
- 新增项目文档模板时，需要同步更新：
  - `docs/00_START_HERE.md`
  - `docs/README.md`
  - `init_project_docs.py`（ESSENTIAL_FILES 或 ON_DEMAND_MAP）
  - 顶层 `README.md`
- 所有 15 个 skill 目录共享同一份 SKILL.md 正文，修改时只改 `zno-init/SKILL.md`，然后同步到其余目录（保留各自 frontmatter）
- `/zno-super` 保持为 `/zno-goal --super` 的兼容别名
- 仓库只有一个 `skills/` 目录，所有平台共用，安装脚本决定目标路径

## 验证步骤

发布变更前：

1. 本地安装：

```bash
./install-all.sh --tool all --dry-run
```

```powershell
powershell -ExecutionPolicy Bypass -File .\install-all.ps1 -Tool all -DryRun
```

2. 核心命令验证：

```text
/zno-init 测试项目
/zno-goal 测试目标
/zno-goal --super 测试目标
/zno-evaluate 测试想法
/zno-upgrade
/zno-status
/zno-continue
/zno-retro
/zno-review
```

3. Python 脚本语法检查：

```bash
python -c "import ast; ast.parse(open('skills/zno-init/scripts/init_project_docs.py', encoding='utf-8').read())"
python -c "import ast; ast.parse(open('skills/zno-upgrade/scripts/update_installed_skills.py', encoding='utf-8').read())"
```

## Pull Request 要求

请包含：

- 改了哪个命令或文档行为
- 哪些模板文件被更新
- 是否已同步到所有 15 个 skill 目录
- 如何验证的
