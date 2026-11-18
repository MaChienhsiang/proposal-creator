#!/usr/bin/env python3
"""Locate original dependency skills without changing or installing anything."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

ROLE_SKILLS = {
    "writer": ["nsfc-write", "domain-modeling", "anti-defensive-writing", "humanizer-zh"],
    "foundation": ["nsfc-write"],
    "figure": ["nsfc-figure", "nature-figure", "humanizer-zh"],
    "evidence": ["nsfc-literature"],
    "reviewer": ["grilling", "nsfc-write"],
}


def roots_for(extra: list[str]) -> list[Path]:
    roots = [Path(x).expanduser() for x in extra]
    roots.append(Path(__file__).resolve().parents[2])
    codex_root = os.environ.get("CODEX_HOME")
    if codex_root:
        roots.append(Path(codex_root) / "skills")
    roots.extend([Path.home() / ".codex" / "skills", Path.home() / ".agents" / "skills"])
    unique: list[Path] = []
    for root in roots:
        if root not in unique:
            unique.append(root)
    return unique


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--role", choices=["all", *ROLE_SKILLS], default="all")
    parser.add_argument("--skills-root", action="append", default=[])
    parser.add_argument("--funding-family", choices=["nsfc", "other", "unspecified"], default="unspecified")
    args = parser.parse_args()
    names = sorted({name for role, values in ROLE_SKILLS.items()
                    if args.role == "all" or role == args.role for name in values})
    roots = roots_for(args.skills_root)
    results = []
    optional = ["grill-with-docs"]
    if args.role in {"all", "evidence"}:
        if args.funding_family == "nsfc":
            names.append("nsfc-policy")
        else:
            optional.append("nsfc-policy")
    for name in names + optional:
        match = next((root / name / "SKILL.md" for root in roots
                      if (root / name / "SKILL.md").is_file()), None)
        results.append({"skill": name, "required": name in names,
                        "found": match is not None, "path": str(match) if match else None})
    missing = [row["skill"] for row in results if row["required"] and not row["found"]]
    print(json.dumps({"role": args.role, "funding_family": args.funding_family, "dependencies": results, "missing": missing,
                      "note": "仅检查 SKILL.md 存在，不代表依赖脚本或绘图运行时已验证。"},
                     ensure_ascii=False, indent=2))
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
