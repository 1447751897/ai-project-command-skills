from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "project-template"
LEGACY_DOC_PATHS = {
    Path("docs/product/01-requirements-clarification.md"): Path(
        "docs/01-requirements-clarification.md"
    ),
    Path("docs/product/06-roadmap.md"): Path("docs/06-roadmap.md"),
    Path("docs/product/15-frontend-design.md"): Path("docs/15-frontend-design.md"),
    Path("docs/engineering/02-development-principles.md"): Path(
        "docs/02-development-principles.md"
    ),
    Path("docs/engineering/04-tech-decisions.md"): Path("docs/04-tech-decisions.md"),
    Path("docs/engineering/11-project-structure.md"): Path("docs/11-project-structure.md"),
    Path("docs/development/03-feature-changelog.md"): Path("docs/03-feature-changelog.md"),
    Path("docs/development/10-current-status.md"): Path("docs/10-current-status.md"),
    Path("docs/development/14-decision-log.md"): Path("docs/14-decision-log.md"),
    Path("docs/operations/07-local-development.md"): Path("docs/07-local-development.md"),
    Path("docs/operations/08-deployment.md"): Path("docs/08-deployment.md"),
    Path("docs/handoff/05-handoff-guide.md"): Path("docs/05-handoff-guide.md"),
    Path("docs/maintenance/09-ai-project-start-prompt.md"): Path(
        "docs/09-ai-project-start-prompt.md"
    ),
    Path("docs/maintenance/12-upgrade-history.md"): Path("docs/12-upgrade-history.md"),
    Path("docs/maintenance/13-command-reference.md"): Path("docs/13-command-reference.md"),
}


def template_files() -> list[Path]:
    return [path.relative_to(TEMPLATE_ROOT) for path in TEMPLATE_ROOT.rglob("*") if path.is_file()]


def source_for_missing_file(project_root: Path, relative: Path) -> Path:
    legacy_relative = LEGACY_DOC_PATHS.get(relative)
    if legacy_relative is not None:
        legacy_source = project_root / legacy_relative
        if legacy_source.exists():
            return legacy_source
    return TEMPLATE_ROOT / relative


def append_upgrade_record(project_root: Path, written: list[Path]) -> None:
    history = project_root / "docs" / "maintenance" / "12-upgrade-history.md"
    history.parent.mkdir(parents=True, exist_ok=True)
    if not history.exists():
        template_history = TEMPLATE_ROOT / "docs" / "maintenance" / "12-upgrade-history.md"
        shutil.copy2(template_history, history)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "",
        f"### {now} - Skill template upgrade",
        "",
        "版本：project-kickoff-docs current",
        "",
        "升级原因：补齐当前 Skill 模板中新增或缺失的文档。",
        "",
        "新增内容：",
        "",
    ]
    if written:
        lines.extend([f"1. `{path.as_posix()}`" for path in written])
    else:
        lines.append("1. 无新增文件，当前项目文档已齐全。")
    lines.extend(
        [
            "",
            "变更内容：",
            "",
            "1. 未覆盖已有项目文档。",
            "",
            "未自动处理内容：",
            "",
            "1. 已有文档中的旧规则需要 AI 根据项目实际情况增量合并。",
            "",
            "验证方式：",
            "",
            "```bash",
            "python scripts/upgrade_project_docs.py <project-root>",
            "```",
            "",
            "后续注意：",
            "",
            "1. 如新增文档为空模板，需要根据当前项目补充真实内容。",
            "",
        ]
    )
    with history.open("a", encoding="utf-8", newline="") as file:
        file.write("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Upgrade AI project docs by copying missing template files only."
    )
    parser.add_argument("project_root", help="Target project root directory")
    parser.add_argument("--check", action="store_true", help="List missing docs without writing")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if not project_root.is_dir():
        raise SystemExit(f"Project root is not a directory: {project_root}")

    missing = [relative for relative in template_files() if not (project_root / relative).exists()]

    if args.check:
        if missing:
            print("Missing project docs:")
            for relative in missing:
                print(f"- {project_root / relative}")
        else:
            print("No missing project docs.")
        return 0

    written: list[Path] = []
    for relative in missing:
        source = source_for_missing_file(project_root, relative)
        target = project_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        written.append(relative)

    append_upgrade_record(project_root, written)

    if written:
        print("Upgraded project docs:")
        for relative in written:
            print(f"- {project_root / relative}")
    else:
        print("No missing project docs. Upgrade history updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
