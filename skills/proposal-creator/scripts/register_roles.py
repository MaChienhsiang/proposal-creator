"""Expose the installed proposal roles as sibling, explicitly callable skills."""

import argparse
from pathlib import Path


ROLES = {
    "writer": "按已确认的研究方向规划、起草和修订申请书正文",
    "foundation": "从内部资料提炼研究基础、可行性与证据缺口",
    "figure": "按现有方案或数据制作科研配图并验收",
    "evidence": "核验外部论断、文献引用和政策依据",
    "reviewer": "独立评审申请书、提出问题并复核修改",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", type=Path, default=Path(__file__).absolute().parents[2],
                        help="Host skills directory containing proposal-creator")
    root = parser.parse_args().skills_root
    package = root / "proposal-creator"
    if not (package / "SKILL.md").is_file():
        parser.exit(1, f"Missing base skill: {package}\n")
    pending = {}
    for role, description in ROLES.items():
        reference = f"references/{role}.md"
        if not (package / reference).is_file():
            parser.exit(1, f"Missing role: {reference}\n")
        name = f"proposal-creator-{role}"
        target = root / name / "SKILL.md"
        content = (
            f"---\nname: {name}\ndescription: {description}。\n---\n\n"
            f"只执行 {role}。读取[主入口](../proposal-creator/SKILL.md)的启动规则和"
            f"[角色说明](../proposal-creator/{reference})，遵循单角色任务范围。\n"
        )
        if target.is_file() and target.read_text(encoding="utf-8") == content:
            continue
        if target.parent.exists():
            parser.exit(1, f"Existing skill differs: {target.parent}\n")
        pending[target] = content
    for target, content in pending.items():
        target.parent.mkdir()
        target.write_text(content, encoding="utf-8")
    print(f"Registered {len(ROLES)} proposal roles in {root} ({len(pending)} created).")


if __name__ == "__main__":
    main()
