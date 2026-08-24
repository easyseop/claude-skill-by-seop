#!/usr/bin/env python3
"""Structural completeness validator for claude-skill-author evidence."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VALID_RULE_STATUS = {"APPLY", "TRANSFORM", "EXCLUDE", "EXTERNAL"}
VALID_ANTI_STATUS = {"PASS", "NOT_APPLICABLE"}
VALID_DESIGN_STATUS = {"RESOLVED"}
VALID_STAGE = {"R", "P", "I", "V", "F", "O", "D", "G", "X"}
REQUIRED_DESIGN_FIELDS = {
    "purpose", "user_outcome", "use_when", "do_not_use_when",
    "invocation_examples", "inputs_and_defaults",
    "trusted_and_untrusted_sources", "scope_include", "scope_exclude",
    "scope_conditional", "permissions_allow", "permissions_deny",
    "approval_required", "workflow", "outputs", "validation",
    "failure_handling", "completion_conditions",
}
PLACEHOLDERS = {"", "TODO", "TBD", "UNKNOWN", "__TARGET__", "DRAFT"}
REQUIRED_SPEC_FIELDS = {
    "target_skill", "artifact_type", "operation", "purpose", "user_outcome",
    "primary_stage", "secondary_stages", "invocation", "inputs", "scope",
    "side_effect_level", "permissions", "execution", "outputs", "validation",
    "failure_handling", "completion_conditions", "status",
}


def load_json_yaml(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid JSON-compatible YAML: {path}: {e}")


def dump(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def is_filled(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() not in PLACEHOLDERS
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"SKILL.md has no opening frontmatter delimiter: {path}")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise ValueError(f"SKILL.md has no closing frontmatter delimiter: {path}")
    front_lines = lines[1:end]
    result: dict[str, Any] = {}
    current_list_key: str | None = None
    for raw in front_lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", raw)
        if m:
            key, value = m.groups()
            current_list_key = None
            if value in (None, ""):
                result[key] = ""
                current_list_key = key
            elif value.strip().startswith("[") and value.strip().endswith("]"):
                result[key] = [x.strip().strip("'\"") for x in value.strip()[1:-1].split(",") if x.strip()]
            else:
                result[key] = value.strip().strip("'\"")
            continue
        m = re.match(r"^\s+-\s+(.+)$", raw)
        if m and current_list_key:
            if not isinstance(result[current_list_key], list):
                result[current_list_key] = []
            result[current_list_key].append(m.group(1).strip().strip("'\""))
    return result, text


def target_exists(root: Path, target: dict[str, Any]) -> tuple[bool, str]:
    rel = target.get("file")
    contains = target.get("contains")
    if not isinstance(rel, str) or not rel.strip():
        return False, "target.file is empty"
    path = root / rel
    if not path.exists():
        return False, f"missing target file: {rel}"
    if contains:
        text = path.read_text(encoding="utf-8", errors="replace")
        if str(contains) not in text:
            return False, f"target text not found in {rel}: {contains}"
    return True, ""


def validate(args: argparse.Namespace) -> tuple[list[str], list[str], dict[str, Any]]:
    root = Path(args.project_root).expanduser().resolve()
    evidence = root / ".claude" / "skill-authoring" / args.target
    skill_dir = root / ".claude" / "skills" / args.target
    errors: list[str] = []
    warnings: list[str] = []

    try:
        manifest = load_json_yaml(evidence / "RULE_MANIFEST.yaml")
        coverage = load_json_yaml(evidence / "RULE_COVERAGE.yaml")
        design = load_json_yaml(evidence / "DESIGN_REQUIREMENTS.yaml")
        spec = load_json_yaml(evidence / "COMMAND_SPEC.yaml")
    except ValueError as e:
        return [str(e)], warnings, {}

    if design.get("target_skill") != args.target:
        errors.append("DESIGN_REQUIREMENTS target_skill does not match requested target")
    design_requirements = design.get("requirements", {})
    if not isinstance(design_requirements, dict):
        errors.append("DESIGN_REQUIREMENTS requirements must be an object")
        design_requirements = {}
    missing_design_fields = sorted(REQUIRED_DESIGN_FIELDS - set(design_requirements))
    if missing_design_fields:
        errors.append(f"missing design requirement fields: {missing_design_fields}")
    resolved_design = 0
    for key in sorted(REQUIRED_DESIGN_FIELDS & set(design_requirements)):
        entry = design_requirements.get(key)
        if not isinstance(entry, dict):
            errors.append(f"design requirement must be an object: {key}")
            continue
        status = entry.get("status")
        if status not in VALID_DESIGN_STATUS:
            errors.append(f"design requirement is unresolved: {key}: {status}")
            continue
        content = entry.get("value") if "value" in entry else entry.get("items")
        if not is_filled(content):
            errors.append(f"design requirement has no concrete content: {key}")
        sources = entry.get("sources", [])
        if not isinstance(sources, list) or not sources or any(not is_filled(x) for x in sources):
            errors.append(f"design requirement has no traceable source: {key}")
        if is_filled(content) and isinstance(sources, list) and sources and all(is_filled(x) for x in sources):
            resolved_design += 1
    if design.get("status") != "APPROVED":
        errors.append("DESIGN_REQUIREMENTS status must be APPROVED")

    source_ids = [r.get("id") for r in manifest.get("rules", [])]
    source_set = set(source_ids)
    coverage_rules = coverage.get("rules", {})
    coverage_set = set(coverage_rules)
    duplicate_source = sorted({rid for rid in source_ids if source_ids.count(rid) > 1})
    missing = sorted(source_set - coverage_set)
    unknown = sorted(coverage_set - source_set)
    if duplicate_source:
        errors.append(f"duplicate source rule IDs: {duplicate_source}")
    if missing:
        errors.append(f"missing rule IDs in coverage: {missing}")
    if unknown:
        errors.append(f"unknown rule IDs in coverage: {unknown}")

    classified = 0
    for rid in sorted(source_set & coverage_set):
        entry = coverage_rules[rid]
        status = entry.get("status")
        rationale = str(entry.get("rationale", "")).strip()
        if status not in VALID_RULE_STATUS:
            errors.append(f"{rid}: invalid or unclassified status: {status}")
            continue
        classified += 1
        if len(rationale) < 12:
            errors.append(f"{rid}: rationale must explain the concrete decision")
        if status in {"APPLY", "TRANSFORM"}:
            planned = entry.get("planned_locations", [])
            if args.phase == "spec" and not planned:
                errors.append(f"{rid}: APPLY/TRANSFORM needs planned_locations during spec")
            if args.phase in {"build", "audit"}:
                targets = entry.get("targets", [])
                if not targets:
                    errors.append(f"{rid}: APPLY/TRANSFORM has no final target")
                for target in targets:
                    ok, why = target_exists(skill_dir, target)
                    if not ok:
                        errors.append(f"{rid}: {why}")
        elif status == "EXCLUDE":
            if len(rationale) < 20:
                errors.append(f"{rid}: EXCLUDE needs a specific non-applicability reason")
        elif status == "EXTERNAL":
            controls = entry.get("external_controls", [])
            if not controls:
                errors.append(f"{rid}: EXTERNAL needs at least one technical control")
            for control in controls:
                if control.get("type") not in {"permission", "hook", "ci", "script", "sandbox", "policy"}:
                    errors.append(f"{rid}: invalid external control type: {control.get('type')}")
                if not is_filled(control.get("path")):
                    errors.append(f"{rid}: external control path is empty")
                if args.phase == "audit" and control.get("required_for_pass") is True:
                    if control.get("state") != "implemented":
                        errors.append(f"{rid}: required external control is not implemented")
                    else:
                        cpath = root / str(control.get("path"))
                        if not cpath.exists():
                            errors.append(f"{rid}: implemented external control path does not exist: {cpath}")

    summary = coverage.setdefault("summary", {})
    summary.update({
        "source_rule_count": len(source_ids),
        "classified_rule_count": classified,
        "missing_rule_count": len(missing),
        "duplicate_rule_count": len(duplicate_source),
        "unknown_rule_count": len(unknown),
    })
    dump(evidence / "RULE_COVERAGE.yaml", coverage)

    missing_spec_fields = sorted(REQUIRED_SPEC_FIELDS - set(spec))
    if missing_spec_fields:
        errors.append(f"missing spec fields: {missing_spec_fields}")
    if spec.get("target_skill") != args.target:
        errors.append("COMMAND_SPEC target_skill does not match requested target")
    if spec.get("primary_stage") not in VALID_STAGE:
        errors.append(f"invalid primary_stage: {spec.get('primary_stage')}")
    secondary = spec.get("secondary_stages", [])
    if not isinstance(secondary, list) or any(s not in VALID_STAGE for s in secondary):
        errors.append("secondary_stages contains invalid values")
    if spec.get("primary_stage") in secondary:
        errors.append("primary_stage must not be repeated in secondary_stages")
    for key in ["purpose", "user_outcome", "side_effect_level", "completion_conditions"]:
        if not is_filled(spec.get(key)):
            errors.append(f"spec field is not filled: {key}")
    for key in ["invocation", "inputs", "scope", "permissions", "execution", "outputs", "validation", "failure_handling"]:
        if not isinstance(spec.get(key), dict):
            errors.append(f"spec field must be an object: {key}")
    if spec.get("status") != "APPROVED":
        errors.append("COMMAND_SPEC status must be APPROVED")

    purpose_entry = design_requirements.get("purpose", {})
    outcome_entry = design_requirements.get("user_outcome", {})
    if purpose_entry.get("status") == "RESOLVED" and spec.get("purpose") != purpose_entry.get("value"):
        errors.append("COMMAND_SPEC purpose must match approved DESIGN_REQUIREMENTS purpose")
    if outcome_entry.get("status") == "RESOLVED" and spec.get("user_outcome") != outcome_entry.get("value"):
        errors.append("COMMAND_SPEC user_outcome must match approved DESIGN_REQUIREMENTS user_outcome")
    design_paths = {
        str(item.get("path"))
        for item in design.get("source_documents", [])
        if isinstance(item, dict) and is_filled(item.get("path"))
    }
    spec_design_paths = set(spec.get("inputs", {}).get("design_documents", []) or [])
    missing_spec_designs = sorted(design_paths - spec_design_paths)
    if missing_spec_designs:
        errors.append(f"COMMAND_SPEC inputs.design_documents omits design sources: {missing_spec_designs}")

    stage_info = coverage.get("stage_modules", {})
    if stage_info.get("primary") != spec.get("primary_stage"):
        errors.append("coverage stage_modules.primary must match spec primary_stage")
    applied = stage_info.get("applied", {})
    for stage in [spec.get("primary_stage"), *secondary]:
        if stage and applied.get(stage) is not True:
            errors.append(f"stage module not marked applied: {stage}")

    if args.phase in {"build", "audit"}:
        skill_path = skill_dir / "SKILL.md"
        if not skill_path.exists():
            errors.append(f"missing runtime skill: {skill_path}")
        else:
            try:
                front, text = parse_frontmatter(skill_path)
                if not is_filled(front.get("description")):
                    errors.append("SKILL.md frontmatter description is missing")
                if len(text.splitlines()) > 500:
                    warnings.append("SKILL.md exceeds 500 lines; consider progressive disclosure")
                command_name = skill_dir.name
                if command_name != args.target:
                    errors.append("skill directory name does not match target command")
                named_args = front.get("arguments", [])
                if isinstance(named_args, str):
                    named_args = [x for x in re.split(r"[\s,]+", named_args) if x]
                used_named = set(re.findall(r"\$([A-Za-z_][A-Za-z0-9_-]*)", text)) - {"ARGUMENTS"}
                undeclared = sorted(used_named - set(named_args or []))
                if undeclared:
                    errors.append(f"undeclared named placeholders: {undeclared}")
            except ValueError as e:
                errors.append(str(e))

        authoring_review = evidence / "AUTHORING_REVIEW.md"
        if not authoring_review.exists():
            errors.append("missing AUTHORING_REVIEW.md")
        else:
            review_text = authoring_review.read_text(encoding="utf-8")
            for heading in ["## 규칙 집계", "## 문장별 최종 검토", "## 기계 검사 결과"]:
                if heading not in review_text:
                    errors.append(f"AUTHORING_REVIEW.md missing heading: {heading}")

        anti_source = {x.get("id") for x in manifest.get("anti_patterns", [])}
        anti_cov = coverage.get("anti_patterns", {})
        if set(anti_cov) != anti_source:
            errors.append("anti-pattern coverage IDs do not match manifest")
        for aid, entry in anti_cov.items():
            if entry.get("status") not in VALID_ANTI_STATUS:
                errors.append(f"{aid}: anti-pattern status must be PASS or NOT_APPLICABLE")
            if len(str(entry.get("evidence", "")).strip()) < 8:
                errors.append(f"{aid}: anti-pattern evidence is too weak")

    audit_verdict = None
    if args.phase == "audit":
        audit_path = evidence / "AUDIT_REPORT.md"
        if not audit_path.exists():
            errors.append("missing AUDIT_REPORT.md")
        else:
            audit_text = audit_path.read_text(encoding="utf-8")
            verdicts = re.findall(r"^- 판정:\s*(PASS|CONDITIONAL|FAIL)\s*$", audit_text, re.MULTILINE)
            if len(verdicts) != 1:
                errors.append("AUDIT_REPORT.md must contain exactly one '- 판정: ...' line")
            else:
                audit_verdict = verdicts[0]
                if audit_verdict != "PASS":
                    errors.append(f"independent audit is not PASS: {audit_verdict}")

    result = {
        "schema_version": "1.0",
        "target": args.target,
        "phase": args.phase,
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "source_rules": len(source_ids),
            "classified_rules": classified,
            "missing_rules": len(missing),
            "unknown_rules": len(unknown),
            "duplicate_rules": len(duplicate_source),
            "design_requirements": len(REQUIRED_DESIGN_FIELDS),
            "resolved_design_requirements": resolved_design,
        },
        "audit_verdict": audit_verdict,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    return errors, warnings, result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--project-root", default=".")
    p.add_argument("--target", required=True)
    p.add_argument("--phase", choices=["spec", "build", "audit"], required=True)
    args = p.parse_args()

    errors, warnings, result = validate(args)
    root = Path(args.project_root).expanduser().resolve()
    evidence = root / ".claude" / "skill-authoring" / args.target
    if evidence.exists():
        dump(evidence / f"VALIDATION_{args.phase.upper()}.json", result)
        active_path = root / ".claude" / "skill-authoring" / ".active.json"
        if active_path.exists():
            try:
                active = load_json_yaml(active_path)
                if active.get("target") == args.target:
                    active["phase"] = args.phase.upper()
                    active["status"] = "PASS" if not errors else "FAILED"
                    active["updated_at"] = datetime.now(timezone.utc).isoformat()
                    dump(active_path, active)
            except ValueError:
                pass
        if args.phase == "audit" and not errors:
            final_status = {
                "target": args.target,
                "status": "PASS",
                "validated_at": result["validated_at"],
                "validation_files": [
                    "VALIDATION_SPEC.json",
                    "VALIDATION_BUILD.json",
                    "VALIDATION_AUDIT.json",
                ],
            }
            dump(evidence / "FINAL_STATUS.json", final_status)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
