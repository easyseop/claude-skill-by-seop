#!/usr/bin/env python3
"""Initialize deterministic authoring evidence for claude-skill-author.

The *.yaml outputs intentionally use JSON syntax, which is valid YAML 1.2.
Only Python's standard library is required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RULE_RE = re.compile(r"^##\s+((?:CC|[CPDEVSM])-\d{2,})\.\s+(.+?)\s*$")
ANTI_RE = re.compile(r"^##\s+(A(?:-CC)?-\d{2,})\.\s+(.+?)\s*$")
STAGE_RE = re.compile(r"^##\s+7\.(\d+)\s+(.+?)\s*$")
STAGE_ORDER = ["R", "P", "I", "V", "F", "O", "D", "G", "X"]
TARGET_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def section_end(lines: list[str], start_index: int, level: int = 2) -> int:
    """Return exclusive end index for a heading section."""
    prefix = "#" * level
    for i in range(start_index + 1, len(lines)):
        line = lines[i]
        if line.startswith("#"):
            hashes = len(line) - len(line.lstrip("#"))
            if hashes <= level:
                return i
    return len(lines)


def extract(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    rules: list[dict[str, Any]] = []
    anti: list[dict[str, Any]] = []
    stages: dict[str, dict[str, Any]] = {}

    for i, line in enumerate(lines):
        m = RULE_RE.match(line)
        if m:
            end = section_end(lines, i, 2)
            rid, title = m.groups()
            rules.append({
                "id": rid,
                "title": title,
                "category": rid.split("-", 1)[0],
                "source_file": str(path),
                "start_line": i + 1,
                "end_line": end,
                "text": "\n".join(lines[i:end]).strip(),
            })
            continue
        m = ANTI_RE.match(line)
        if m:
            end = section_end(lines, i, 2)
            rid, title = m.groups()
            anti.append({
                "id": rid,
                "title": title,
                "source_file": str(path),
                "start_line": i + 1,
                "end_line": end,
                "text": "\n".join(lines[i:end]).strip(),
            })
            continue
        m = STAGE_RE.match(line)
        if m:
            idx = int(m.group(1)) - 1
            if 0 <= idx < len(STAGE_ORDER):
                end = section_end(lines, i, 2)
                code = STAGE_ORDER[idx]
                stages[code] = {
                    "code": code,
                    "title": m.group(2),
                    "source_file": str(path),
                    "start_line": i + 1,
                    "end_line": end,
                    "text": "\n".join(lines[i:end]).strip(),
                }
    return {"rules": rules, "anti_patterns": anti, "stage_modules": stages}


def dump(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--project-root", default=".")
    p.add_argument("--target", required=True)
    p.add_argument("--mode", choices=["full", "spec", "build", "audit"], default="full")
    p.add_argument("--common-rules", required=True)
    p.add_argument("--claude-rules", required=True)
    p.add_argument("--design", action="append", default=[])
    p.add_argument("--resume", action="store_true")
    p.add_argument("--reset", action="store_true")
    args = p.parse_args()

    if not TARGET_RE.fullmatch(args.target):
        print("ERROR: target must use lowercase letters, digits, and hyphens only", file=sys.stderr)
        return 2

    root = Path(args.project_root).expanduser().resolve()
    common = Path(args.common_rules).expanduser().resolve()
    claude = Path(args.claude_rules).expanduser().resolve()
    for source in [common, claude]:
        if not source.is_file():
            print(f"ERROR: missing rule source: {source}", file=sys.stderr)
            return 2

    design_paths: list[str] = []
    missing_design: list[str] = []
    for item in args.design:
        candidate = Path(item).expanduser()
        if not candidate.is_absolute():
            candidate = root / candidate
        candidate = candidate.resolve()
        design_paths.append(str(candidate))
        if not candidate.exists():
            missing_design.append(str(candidate))
    if missing_design:
        print("ERROR: missing design documents:\n- " + "\n- ".join(missing_design), file=sys.stderr)
        return 2

    evidence = root / ".claude" / "skill-authoring" / args.target
    skill = root / ".claude" / "skills" / args.target
    evidence.mkdir(parents=True, exist_ok=True)

    if args.reset and evidence.exists():
        archive = evidence.parent / "_archive" / f"{args.target}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
        archive.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(evidence, archive)
        for child in evidence.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

    common_data = extract(common)
    claude_data = extract(claude)
    all_rules = common_data["rules"] + claude_data["rules"]
    all_anti = common_data["anti_patterns"] + claude_data["anti_patterns"]
    stages = {**common_data["stage_modules"], **claude_data["stage_modules"]}

    ids = [r["id"] for r in all_rules]
    duplicates = sorted({rid for rid in ids if ids.count(rid) > 1})
    anti_ids = [r["id"] for r in all_anti]
    anti_duplicates = sorted({rid for rid in anti_ids if anti_ids.count(rid) > 1})
    if duplicates or anti_duplicates:
        print(f"ERROR: duplicate IDs rules={duplicates} anti_patterns={anti_duplicates}", file=sys.stderr)
        return 2

    manifest = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_documents": [
            {"path": str(common), "sha256": sha256(common)},
            {"path": str(claude), "sha256": sha256(claude)},
        ],
        "counts": {
            "rules": len(all_rules),
            "anti_patterns": len(all_anti),
            "stage_modules": len(stages),
        },
        "rules": all_rules,
        "anti_patterns": all_anti,
        "stage_modules": stages,
    }
    dump(evidence / "RULE_MANIFEST.yaml", manifest)

    operation = "revise" if (skill / "SKILL.md").exists() else "new"

    design_requirements_path = evidence / "DESIGN_REQUIREMENTS.yaml"
    design_template_path = Path(__file__).resolve().parent.parent / "assets" / "DESIGN_REQUIREMENTS.template.yaml"
    if not design_requirements_path.exists() or not args.resume:
        design_requirements = json.loads(design_template_path.read_text(encoding="utf-8"))
        design_requirements["target_skill"] = args.target
        design_requirements["source_documents"] = [
            {"path": path, "sha256": sha256(Path(path))}
            for path in design_paths
        ]
        dump(design_requirements_path, design_requirements)
    elif args.resume:
        try:
            design_requirements = json.loads(design_requirements_path.read_text(encoding="utf-8"))
            design_requirements["source_documents"] = [
                {"path": path, "sha256": sha256(Path(path))}
                for path in design_paths
            ] or design_requirements.get("source_documents", [])
            dump(design_requirements_path, design_requirements)
        except json.JSONDecodeError as exc:
            print(f"ERROR: invalid DESIGN_REQUIREMENTS.yaml: {exc}", file=sys.stderr)
            return 2

    spec_path = evidence / "COMMAND_SPEC.yaml"
    if not spec_path.exists() or not args.resume:
        template_path = Path(__file__).resolve().parent.parent / "assets" / "COMMAND_SPEC.template.yaml"
        spec = json.loads(template_path.read_text(encoding="utf-8"))
        spec["target_skill"] = args.target
        spec["operation"] = operation
        spec["invocation"]["command"] = f"/{args.target}"
        spec["inputs"]["design_documents"] = design_paths
        dump(spec_path, spec)

    coverage_path = evidence / "RULE_COVERAGE.yaml"
    if not coverage_path.exists() or not args.resume:
        coverage = {
            "schema_version": "1.0",
            "target_skill": args.target,
            "rules": {
                rule["id"]: {
                    "status": "UNCLASSIFIED",
                    "rationale": "",
                    "planned_locations": [],
                    "targets": [],
                    "external_controls": [],
                }
                for rule in all_rules
            },
            "anti_patterns": {
                item["id"]: {"status": "UNCHECKED", "evidence": ""}
                for item in all_anti
            },
            "stage_modules": {
                "primary": "",
                "secondary": [],
                "applied": {code: False for code in STAGE_ORDER},
            },
            "summary": {
                "source_rule_count": len(all_rules),
                "classified_rule_count": 0,
                "missing_rule_count": len(all_rules),
                "duplicate_rule_count": 0,
                "unknown_rule_count": 0,
            },
        }
        dump(coverage_path, coverage)

    for template, output in [
        ("SPEC_REVIEW.template.md", "SPEC_REVIEW.md"),
        ("AUTHORING_REVIEW.template.md", "AUTHORING_REVIEW.md"),
        ("AUDIT_REPORT.template.md", "AUDIT_REPORT.md"),
    ]:
        output_path = evidence / output
        if not output_path.exists() or not args.resume:
            text = (Path(__file__).resolve().parent.parent / "assets" / template).read_text(encoding="utf-8")
            output_path.write_text(text.replace("__TARGET__", args.target), encoding="utf-8")

    active_dir = root / ".claude" / "skill-authoring"
    active_dir.mkdir(parents=True, exist_ok=True)
    active = {
        "target": args.target,
        "mode": args.mode,
        "phase": "SPEC" if args.mode in {"full", "spec"} else args.mode.upper(),
        "status": "IN_PROGRESS",
        "project_root": str(root),
        "evidence_dir": str(evidence),
        "skill_dir": str(skill),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    dump(active_dir / ".active.json", active)

    print(json.dumps({
        "ok": True,
        "target": args.target,
        "operation": operation,
        "evidence_dir": str(evidence),
        "skill_dir": str(skill),
        "design_requirements": str(design_requirements_path),
        "counts": manifest["counts"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
