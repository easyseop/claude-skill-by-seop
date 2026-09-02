#!/usr/bin/env python3
"""Initialize deterministic evidence for claude-skill-author v1.3.

The *.yaml outputs use JSON syntax, which is valid YAML 1.2. Only the Python
standard library is required.
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
PHASES = ["design", "spec", "build", "audit"]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_sha(data: Any) -> str:
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def dump(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def section_end(lines: list[str], start_index: int, level: int = 2) -> int:
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
        match = RULE_RE.match(line)
        if match:
            end = section_end(lines, i, 2)
            rid, title = match.groups()
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
        match = ANTI_RE.match(line)
        if match:
            end = section_end(lines, i, 2)
            rid, title = match.groups()
            anti.append({
                "id": rid,
                "title": title,
                "source_file": str(path),
                "start_line": i + 1,
                "end_line": end,
                "text": "\n".join(lines[i:end]).strip(),
            })
            continue
        match = STAGE_RE.match(line)
        if match:
            idx = int(match.group(1)) - 1
            if 0 <= idx < len(STAGE_ORDER):
                end = section_end(lines, i, 2)
                code = STAGE_ORDER[idx]
                stages[code] = {
                    "code": code,
                    "title": match.group(2),
                    "source_file": str(path),
                    "start_line": i + 1,
                    "end_line": end,
                    "text": "\n".join(lines[i:end]).strip(),
                }
    return {"rules": rules, "anti_patterns": anti, "stage_modules": stages}


def resolve_files(root: Path, values: list[str], label: str, required: bool = False) -> tuple[list[str], list[str]]:
    resolved: list[str] = []
    missing: list[str] = []
    for item in values:
        candidate = Path(item).expanduser()
        if not candidate.is_absolute():
            candidate = root / candidate
        candidate = candidate.resolve()
        resolved.append(str(candidate))
        if not candidate.is_file():
            missing.append(str(candidate))
    if required and not values:
        print(f"ERROR: at least one {label} is required", file=sys.stderr)
        missing.append(f"<{label}:missing>")
    if missing:
        print(f"ERROR: missing {label}:\n- " + "\n- ".join(missing), file=sys.stderr)
    return resolved, missing


def source_records(paths: list[str], source_type: str) -> list[dict[str, str]]:
    return [{"path": path, "sha256": sha256(Path(path)), "type": source_type} for path in paths]


def stable_manifest_fingerprint(manifest: dict[str, Any]) -> str:
    projection = {
        "source_documents": manifest.get("source_documents", []),
        "counts": manifest.get("counts", {}),
        "rules": manifest.get("rules", []),
        "anti_patterns": manifest.get("anti_patterns", []),
        "stage_modules": manifest.get("stage_modules", {}),
    }
    return canonical_sha(projection)


def default_state(target: str, mode: str, source_path: Path | None) -> dict[str, Any]:
    lock = {"path": "", "sha256": "", "locked_at": ""}
    if source_path is not None:
        lock = {"path": str(source_path), "sha256": sha256(source_path), "locked_at": now()}
    return {
        "schema_version": "1.3",
        "target_skill": target,
        "mode": mode,
        "source_request_lock": lock,
        "phases": {
            phase: {
                "status": "PENDING",
                "fingerprint": "",
                "validated_at": "",
                "validation_file": f"VALIDATION_{phase.upper()}.json",
            }
            for phase in PHASES
        },
        "updated_at": now(),
    }


def invalidate_from(state: dict[str, Any], phase: str, status: str = "STALE") -> None:
    start = PHASES.index(phase)
    for item in PHASES[start:]:
        entry = state.setdefault("phases", {}).setdefault(item, {})
        entry.update({"status": status, "fingerprint": "", "validated_at": ""})
    state["updated_at"] = now()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--target", required=True)
    parser.add_argument("--mode", choices=["full", "design", "spec", "build", "audit"], default="full")
    parser.add_argument("--common-rules", required=True)
    parser.add_argument("--claude-rules", required=True)
    parser.add_argument("--design", action="append", default=[])
    parser.add_argument("--source-request", action="append", default=[])
    parser.add_argument("--decision-document", action="append", default=[])
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

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

    design_paths, missing_design = resolve_files(root, args.design, "design documents", required=args.mode in {"full", "design", "spec"})
    request_paths, missing_requests = resolve_files(root, args.source_request, "source request documents", required=args.mode in {"full", "design", "spec"})
    decision_paths, missing_decisions = resolve_files(root, args.decision_document, "decision documents", required=False)
    if missing_design or missing_requests or missing_decisions:
        return 2

    evidence = root / ".claude" / "skill-authoring" / args.target
    skill = root / ".claude" / "skills" / args.target

    if args.reset and evidence.exists():
        archive = evidence.parent / "_archive" / f"{args.target}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
        archive.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(evidence, archive)
        shutil.rmtree(evidence)

    existing_core = evidence / "AUTHORING_STATE.yaml"
    if evidence.exists() and existing_core.exists() and not (args.resume or args.reset):
        print("ERROR: authoring evidence already exists; use --resume or --reset", file=sys.stderr)
        return 2
    evidence.mkdir(parents=True, exist_ok=True)

    # Ensure a dedicated append-only follow-up decision file exists.
    default_decisions = evidence / "SOURCE_DECISIONS.md"
    if not default_decisions.exists():
        template = Path(__file__).resolve().parent.parent / "assets" / "SOURCE_DECISIONS.template.md"
        default_decisions.write_text(template.read_text(encoding="utf-8").replace("<스킬명>", args.target), encoding="utf-8")
    if str(default_decisions.resolve()) not in decision_paths:
        decision_paths.append(str(default_decisions.resolve()))

    state_path = evidence / "AUTHORING_STATE.yaml"
    source_path = Path(request_paths[0]) if request_paths else None
    if state_path.exists():
        try:
            state = load(state_path)
        except json.JSONDecodeError as exc:
            print(f"ERROR: invalid AUTHORING_STATE.yaml: {exc}", file=sys.stderr)
            return 2
        lock = state.get("source_request_lock", {})
        if source_path is not None:
            locked_path = str(lock.get("path", ""))
            locked_sha = str(lock.get("sha256", ""))
            current_sha = sha256(source_path)
            if locked_path and str(source_path.resolve()) != str(Path(locked_path).resolve()):
                print("ERROR: initial SOURCE_REQUEST path is immutable; use SOURCE_DECISIONS.md for later decisions or --reset for a new intake", file=sys.stderr)
                return 2
            if locked_sha and current_sha != locked_sha:
                print("ERROR: initial SOURCE_REQUEST content changed after lock; restore it and append later decisions to SOURCE_DECISIONS.md", file=sys.stderr)
                return 2
            if not locked_sha:
                state["source_request_lock"] = {"path": str(source_path), "sha256": current_sha, "locked_at": now()}
        state["mode"] = args.mode
    else:
        state = default_state(args.target, args.mode, source_path)
    dump(state_path, state)

    old_design_inputs = None
    old_manifest_fingerprint = None
    old_manifest_data = None
    old_design_path = evidence / "DESIGN_REQUIREMENTS.yaml"
    if args.resume and old_design_path.exists():
        try:
            previous_design = load(old_design_path)
            old_design_inputs = canonical_sha({
                "primary": previous_design.get("primary_design_document", ""),
                "design": previous_design.get("source_documents", []),
                "request": previous_design.get("source_request_documents", []),
                "decisions": previous_design.get("decision_documents", []),
            })
        except Exception:
            old_design_inputs = None
    old_manifest_path = evidence / "RULE_MANIFEST.yaml"
    if args.resume and old_manifest_path.exists():
        try:
            old_manifest_data = load(old_manifest_path)
            old_manifest_fingerprint = stable_manifest_fingerprint(old_manifest_data)
        except Exception:
            old_manifest_fingerprint = None
            old_manifest_data = None

    common_data = extract(common)
    claude_data = extract(claude)
    all_rules = common_data["rules"] + claude_data["rules"]
    all_anti = common_data["anti_patterns"] + claude_data["anti_patterns"]
    stages = {**common_data["stage_modules"], **claude_data["stage_modules"]}
    ids = [rule["id"] for rule in all_rules]
    duplicates = sorted({rid for rid in ids if ids.count(rid) > 1})
    anti_ids = [item["id"] for item in all_anti]
    anti_duplicates = sorted({rid for rid in anti_ids if anti_ids.count(rid) > 1})
    if duplicates or anti_duplicates:
        print(f"ERROR: duplicate IDs rules={duplicates} anti_patterns={anti_duplicates}", file=sys.stderr)
        return 2

    manifest = {
        "schema_version": "1.3",
        "generated_at": now(),
        "source_documents": [
            {"path": str(common), "sha256": sha256(common)},
            {"path": str(claude), "sha256": sha256(claude)},
        ],
        "counts": {"rules": len(all_rules), "anti_patterns": len(all_anti), "stage_modules": len(stages)},
        "rules": all_rules,
        "anti_patterns": all_anti,
        "stage_modules": stages,
    }
    new_manifest_fingerprint_prewrite = stable_manifest_fingerprint(manifest)
    if args.resume and old_manifest_data is not None and old_manifest_fingerprint == new_manifest_fingerprint_prewrite:
        manifest = old_manifest_data
    else:
        dump(evidence / "RULE_MANIFEST.yaml", manifest)

    operation = "revise" if (skill / "SKILL.md").exists() else "new"
    design_records = source_records(design_paths, "design")
    request_records = source_records(request_paths, "source_request")
    decision_records = source_records(decision_paths, "source_decision")

    # REQUIREMENT_INTAKE is the explicit bridge from raw request to DESIGN.md.
    intake_path = evidence / "REQUIREMENT_INTAKE.yaml"
    intake_template = Path(__file__).resolve().parent.parent / "assets" / "REQUIREMENT_INTAKE.template.yaml"
    if not intake_path.exists():
        intake = load(intake_template)
        intake["target_skill"] = args.target
    else:
        intake = load(intake_path)
        if intake.get("target_skill") not in {None, "", "__TARGET__", args.target}:
            print("ERROR: REQUIREMENT_INTAKE target_skill does not match requested target", file=sys.stderr)
            return 2
        intake["target_skill"] = args.target
    intake["source_request_documents"] = request_records
    intake["decision_documents"] = decision_records
    dump(intake_path, intake)

    design_requirements_path = evidence / "DESIGN_REQUIREMENTS.yaml"
    design_template_path = Path(__file__).resolve().parent.parent / "assets" / "DESIGN_REQUIREMENTS.template.yaml"
    if not design_requirements_path.exists() or not args.resume:
        design_requirements = load(design_template_path)
        design_requirements["target_skill"] = args.target
        design_requirements["primary_design_document"] = design_paths[0] if design_paths else ""
        design_requirements["source_documents"] = design_records
        design_requirements["source_request_documents"] = request_records
        design_requirements["decision_documents"] = decision_records
        design_requirements["requirement_intake_document"] = str(intake_path.resolve())
        dump(design_requirements_path, design_requirements)
    else:
        design_requirements = load(design_requirements_path)
        design_requirements["primary_design_document"] = design_paths[0] if design_paths else design_requirements.get("primary_design_document", "")
        design_requirements["source_documents"] = design_records
        design_requirements["source_request_documents"] = request_records
        design_requirements["decision_documents"] = decision_records
        design_requirements["requirement_intake_document"] = str(intake_path.resolve())
        dump(design_requirements_path, design_requirements)

    spec_path = evidence / "COMMAND_SPEC.yaml"
    spec_template = Path(__file__).resolve().parent.parent / "assets" / "COMMAND_SPEC.template.yaml"
    if not spec_path.exists() or not args.resume:
        spec = load(spec_template)
        spec["target_skill"] = args.target
        spec["operation"] = operation
        spec["invocation"]["command"] = f"/{args.target}"
        spec["inputs"]["design_documents"] = design_paths
        spec["inputs"]["source_request_documents"] = request_paths
        spec["inputs"]["decision_documents"] = decision_paths
        spec["inputs"]["requirement_intake_document"] = str(intake_path.resolve())
        dump(spec_path, spec)
    else:
        spec = load(spec_path)
        spec.setdefault("inputs", {})["design_documents"] = design_paths
        spec.setdefault("inputs", {})["source_request_documents"] = request_paths
        spec.setdefault("inputs", {})["decision_documents"] = decision_paths
        spec.setdefault("inputs", {})["requirement_intake_document"] = str(intake_path.resolve())
        dump(spec_path, spec)

    coverage_path = evidence / "RULE_COVERAGE.yaml"
    if not coverage_path.exists() or not args.resume:
        coverage = {
            "schema_version": "1.3",
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
            "anti_patterns": {item["id"]: {"status": "UNCHECKED", "evidence": ""} for item in all_anti},
            "stage_modules": {"primary": "", "secondary": [], "applied": {code: False for code in STAGE_ORDER}},
            "summary": {
                "source_rule_count": len(all_rules),
                "classified_rule_count": 0,
                "missing_rule_count": len(all_rules),
                "duplicate_rule_count": 0,
                "unknown_rule_count": 0,
            },
        }
        dump(coverage_path, coverage)

    for template_name, output_name in [
        ("DESIGN_AUDIT_REPORT.template.md", "DESIGN_AUDIT_REPORT.md"),
        ("DESIGN_AUDIT_ATTESTATION.template.yaml", "DESIGN_AUDIT_ATTESTATION.yaml"),
        ("SPEC_REVIEW.template.md", "SPEC_REVIEW.md"),
        ("AUTHORING_REVIEW.template.md", "AUTHORING_REVIEW.md"),
        ("AUDIT_REPORT.template.md", "AUDIT_REPORT.md"),
        ("AUDIT_ATTESTATION.template.yaml", "AUDIT_ATTESTATION.yaml"),
    ]:
        output = evidence / output_name
        if not output.exists() or not args.resume:
            text = (Path(__file__).resolve().parent.parent / "assets" / template_name).read_text(encoding="utf-8")
            output.write_text(text.replace("__TARGET__", args.target), encoding="utf-8")

    # Invalidate only when acknowledged inputs actually changed.
    if args.resume:
        new_design_inputs = canonical_sha({
            "primary": design_requirements.get("primary_design_document", ""),
            "design": design_requirements.get("source_documents", []),
            "request": design_requirements.get("source_request_documents", []),
            "decisions": design_requirements.get("decision_documents", []),
        })
        new_manifest_fingerprint = stable_manifest_fingerprint(manifest)
        if old_design_inputs is not None and old_design_inputs != new_design_inputs:
            invalidate_from(state, "design")
        elif old_manifest_fingerprint is not None and old_manifest_fingerprint != new_manifest_fingerprint:
            invalidate_from(state, "spec")
        state["mode"] = args.mode
        state["updated_at"] = now()
        dump(state_path, state)

    active_dir = root / ".claude" / "skill-authoring"
    active_dir.mkdir(parents=True, exist_ok=True)
    initial_phase = "DESIGN" if args.mode in {"full", "design", "spec"} else args.mode.upper()
    active = {
        "target": args.target,
        "mode": args.mode,
        "phase": initial_phase,
        "status": "IN_PROGRESS",
        "project_root": str(root),
        "evidence_dir": str(evidence),
        "skill_dir": str(skill),
        "updated_at": now(),
    }
    dump(active_dir / ".active.json", active)

    print(json.dumps({
        "ok": True,
        "target": args.target,
        "operation": operation,
        "evidence_dir": str(evidence),
        "skill_dir": str(skill),
        "requirement_intake": str(intake_path),
        "design_requirements": str(design_requirements_path),
        "design_documents": design_paths,
        "source_request_documents": request_paths,
        "decision_documents": decision_paths,
        "counts": manifest["counts"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
