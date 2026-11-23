#!/usr/bin/env python3
"""Validate the bundled role routes, local references and shared contracts."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROLES = ["writer", "foundation", "figure", "evidence", "reviewer"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.skills_root.resolve()
    checks: list[dict] = []

    def check(text: str, passed: bool, evidence: str = "") -> None:
        checks.append({"text": text, "passed": bool(passed), "evidence": evidence})

    name = "proposal-creator"
    main_root = root / name
    path = main_root / "SKILL.md"
    if not path.is_file():
        parser.exit(1, f"Missing entrypoint: {path}\n")
    check("single-entrypoint", list(main_root.rglob("SKILL.md")) == [path])
    value = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", value, flags=re.S)
    check(f"frontmatter:{name}", bool(match))
    check(f"name:{name}", bool(match and f"name: {name}\n" in match.group(1) + "\n"))
    check(f"description:{name}", bool(match and "description:" in match.group(1)))
    check(f"length:{name}", len(value.splitlines()) < 500)
    ui_path = root / name / "agents/openai.yaml"
    check(f"ui-config:{name}", ui_path.is_file())
    if ui_path.is_file():
        ui = ui_path.read_text(encoding="utf-8")
        display = re.search(r'  display_name: "([^"\n]+)"', ui)
        blurb = re.search(r'  short_description: "([^"\n]+)"', ui)
        prompt = re.search(r'  default_prompt: "([^"\n]+)"', ui)
        check(f"ui-description:{name}", bool(blurb and 25 <= len(blurb.group(1)) <= 64))
        check(f"ui-english-name:{name}", bool(display and display.group(1) == name))
        check(f"ui-prompt:{name}", bool(prompt and f"${name}" in prompt.group(1)))
    for role in ROLES:
        check(f"role-route:{role}", f"$proposal-creator {role}`" in value
              and f"(references/{role}.md)" in value)
    files = main_root.rglob("*.md")
    for path in files:
        value = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", value):
            if target.startswith(("http:", "https:", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            resolved = (path.parent / target).resolve()
            check(f"link:{path.relative_to(root)}:{target}", resolved.is_relative_to(main_root) and resolved.is_file())
    dependencies = (main_root / "references/dependencies.md").read_text(encoding="utf-8")
    for skill in ["nsfc-write", "nsfc-policy", "nsfc-literature", "nsfc-figure", "nature-figure",
                  "grilling", "domain-modeling", "anti-defensive-writing", "humanizer-zh", "lieflat-less-ai-tone"]:
        check(f"dependency-route:{skill}", skill in dependencies)
    reviewer = (main_root / "references/reviewer.md").read_text(encoding="utf-8")
    workflow = (main_root / "references/workflow.md").read_text(encoding="utf-8")
    figure = (main_root / "references/figure.md").read_text(encoding="utf-8")
    check("E-leads-grilling", "加载 grilling" in reviewer and "不直接改主稿" in reviewer)
    check("autopilot-delegation", "delegated" in reviewer and "问题交给 A 回答" in reviewer)
    check("interactive-frontier", "互不依赖" in reviewer and "等待" in workflow)
    check("figure-routing", "nsfc-figure" in figure and "nature-figure" in figure
          and "不能伪造为已实现结果" in figure)
    count = sum(item["passed"] for item in checks)
    print(json.dumps({"summary": {"passed": count, "failed": len(checks) - count,
                                  "total": len(checks)}, "checks": checks},
                     ensure_ascii=False, indent=2))
    return 0 if count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
