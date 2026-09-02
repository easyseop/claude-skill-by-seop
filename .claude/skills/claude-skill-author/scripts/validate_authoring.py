#!/usr/bin/env python3
"""Deterministic completeness and freshness validator for v1.3 authoring evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

VALID_RULE_STATUS = {"APPLY", "TRANSFORM", "EXCLUDE", "EXTERNAL"}
VALID_ANTI_STATUS = {"PASS", "NOT_APPLICABLE"}
VALID_DESIGN_STATUS = {"RESOLVED"}
VALID_STAGE = {"R", "P", "I", "V", "F", "O", "D", "G", "X"}
VALID_AGENT_MODE = {"auto", "required", "forbidden"}
VALID_AGENT_DECISION = {"required", "not-required"}
VALID_AGENT_INTEGRATION = {"none", "skill-context-fork", "agent-preloads-skill", "standalone-agent"}
VALID_QUESTION_CLASS = {"USER_DECISION", "REPOSITORY_RESEARCH", "SAFE_DEFAULT", "NON_BLOCKING_UNCERTAINTY"}
VALID_INTAKE_TYPE = {"USER_EXPLICIT", "USER_DECISION", "REPOSITORY_FACT", "SAFE_DEFAULT", "PROPOSAL", "NON_BLOCKING_UNCERTAINTY"}
VALID_INTAKE_STATUS = {"RESOLVED", "OPEN"}
PHASES = ["design", "spec", "build", "audit"]
REQUIRED_DESIGN_FIELDS = {
    "purpose", "user_outcome", "use_when", "do_not_use_when",
    "invocation_examples", "inputs_and_defaults", "trusted_and_untrusted_sources",
    "scope_include", "scope_exclude", "scope_conditional", "permissions_allow",
    "permissions_deny", "approval_required", "workflow", "outputs", "validation",
    "failure_handling", "completion_conditions",
}
DESIGN_HEADINGS = [
    "## 1. 스킬 개요", "## 2. 사용 시점", "## 3. 사용하지 않는 시점", "## 4. 호출 예",
    "## 5. 입력과 기본값", "## 6. 신뢰할 수 있는 근거와 외부 데이터", "## 7. 포함 범위",
    "## 8. 제외 범위", "## 9. 조건부 범위", "## 10. 허용 행동과 도구", "## 11. 금지 행동",
    "## 12. 사용자 승인 필요 행동", "## 13. 수행 절차", "## 14. 출력 파일과 최종 보고 형식",
    "## 15. 검증 기준", "## 16. 실패·재시도·중단·복구", "## 17. 완료 조건",
    "## 18. 알려진 실패 사례와 반례", "## 19. 기존 프로젝트 규칙과 관련 파일", "## 20. 미결정 사항",
]
PLACEHOLDERS = {"", "TODO", "TBD", "UNKNOWN", "__TARGET__", "DRAFT", "UNRESOLVED"}
REQUIRED_SPEC_FIELDS = {
    "target_skill", "artifact_type", "operation", "purpose", "user_outcome", "primary_stage",
    "secondary_stages", "invocation", "inputs", "scope", "side_effect_level", "permissions",
    "execution", "outputs", "validation", "failure_handling", "completion_conditions",
    "agent_requirement", "status",
}
TARGET_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
REQ_ID_RE = re.compile(r"^REQ-\d{3,}$")
VERDICT_RE = re.compile(r"^- 판정:\s*(PASS|CONDITIONAL|FAIL)\s*$", re.MULTILINE)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json_yaml(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON-compatible YAML: {path}: {exc}")


def dump(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_sha(data: Any) -> str:
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def is_filled(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() not in PLACEHOLDERS
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def parse_scalar(value: str) -> Any:
    v = value.strip().strip("'\"")
    if v.lower() in {"true", "yes", "on", "1"}:
        return True
    if v.lower() in {"false", "no", "off", "0"}:
        return False
    return v


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"markdown has no opening frontmatter delimiter: {path}")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise ValueError(f"markdown has no closing frontmatter delimiter: {path}")
    result: dict[str, Any] = {}
    current_list_key: str | None = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", raw)
        if match:
            key, value = match.groups()
            current_list_key = None
            if value in (None, "", ">", "|"):
                result[key] = "" if value not in (">", "|") else value
                current_list_key = key if value in (None, "") else None
            elif value.strip().startswith("[") and value.strip().endswith("]"):
                result[key] = [parse_scalar(item) for item in value.strip()[1:-1].split(",") if item.strip()]
            else:
                result[key] = parse_scalar(value)
            continue
        match = re.match(r"^\s+-\s+(.+)$", raw)
        if match and current_list_key:
            if not isinstance(result[current_list_key], list):
                result[current_list_key] = []
            result[current_list_key].append(parse_scalar(match.group(1)))
    return result, text


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def file_record(root: Path, path: Path, role: str) -> dict[str, Any]:
    return {"path": rel(root, path), "sha256": sha256(path), "role": role, "kind": "file"}


def tree_record(root: Path, path: Path, role: str) -> dict[str, Any]:
    members = []
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        members.append({"path": rel(path, item), "sha256": sha256(item)})
    return {
        "path": rel(root, path), "sha256": canonical_sha(members), "role": role,
        "kind": "tree", "members": len(members),
    }


def unique_file_records(root: Path, items: Iterable[tuple[Path, str]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    for path, role in items:
        resolved = path.resolve()
        key = str(resolved)
        if key in seen:
            continue
        seen.add(key)
        if not resolved.is_file():
            raise ValueError(f"missing attestation input: {resolved}")
        records.append(file_record(root, resolved, role))
    return records


def resolve_target_path(project_root: Path, skill_dir: Path, raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    if raw.startswith(".claude/") or raw.startswith("docs/"):
        return project_root / raw
    return skill_dir / raw


def target_exists(project_root: Path, skill_dir: Path, target: dict[str, Any]) -> tuple[bool, str]:
    raw = target.get("file")
    contains = target.get("contains")
    if not isinstance(raw, str) or not raw.strip():
        return False, "target.file is empty"
    path = resolve_target_path(project_root, skill_dir, raw)
    if not path.exists():
        return False, f"missing target file: {raw}"
    if contains:
        text = path.read_text(encoding="utf-8", errors="replace")
        if str(contains) not in text:
            return False, f"target text not found in {raw}: {contains}"
    return True, ""


def validate_source_records(root: Path, records: Any, label: str, errors: list[str], require_one: bool = False) -> set[str]:
    found: set[str] = set()
    if not isinstance(records, list):
        errors.append(f"{label} must be a list")
        return found
    if require_one and not records:
        errors.append(f"{label} must contain at least one source")
    for item in records:
        if not isinstance(item, dict):
            errors.append(f"{label} entry must be an object")
            continue
        raw = item.get("path")
        if not is_filled(raw):
            errors.append(f"{label} entry path is empty")
            continue
        path = Path(str(raw))
        if not path.is_absolute():
            path = root / path
        path = path.resolve()
        found.add(str(path))
        if not path.is_file():
            errors.append(f"{label} file does not exist: {path}")
            continue
        expected = item.get("sha256")
        if is_filled(expected) and sha256(path) != expected:
            errors.append(f"{label} digest changed since initialization: {path}")
    return found


def audit_verdict(path: Path, label: str, errors: list[str]) -> str | None:
    if not path.exists():
        errors.append(f"missing {label}: {path.name}")
        return None
    values = VERDICT_RE.findall(path.read_text(encoding="utf-8"))
    if len(values) != 1:
        errors.append(f"{path.name} must contain exactly one '- 판정: ...' line")
        return None
    verdict = values[0]
    if verdict != "PASS":
        errors.append(f"{label} is not PASS: {verdict}")
    return verdict


def validate_source_lock(root: Path, evidence: Path, state: dict[str, Any], errors: list[str]) -> None:
    expected_path = evidence / "SOURCE_REQUEST.md"
    lock = state.get("source_request_lock", {})
    if not isinstance(lock, dict):
        errors.append("AUTHORING_STATE source_request_lock must be an object")
        return
    raw = lock.get("path")
    expected_sha = lock.get("sha256")
    if not is_filled(raw) or not is_filled(expected_sha):
        errors.append("SOURCE_REQUEST is not locked in AUTHORING_STATE")
        return
    path = Path(str(raw))
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    if path != expected_path.resolve():
        errors.append("SOURCE_REQUEST lock path must be the target evidence SOURCE_REQUEST.md")
    if not path.is_file():
        errors.append(f"locked SOURCE_REQUEST does not exist: {path}")
    elif sha256(path) != expected_sha:
        errors.append("SOURCE_REQUEST changed after immutable lock; restore it and record later decisions in SOURCE_DECISIONS.md")


def meaningful_section(text: str) -> bool:
    cleaned: list[str] = []
    in_fence = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not line:
            continue
        if line.startswith("###"):
            continue
        if line in {"-", "- 없음 / 항목과 결정 주체", "- 없음 / ...", "- 없음"}:
            continue
        if re.search(r"<[^>]+>", line):
            continue
        if line in {"다음 요청에서 사용한다.", "다음 요청에서는 사용하지 않는다.", "다음 조건을 모두 충족해야 완료다."}:
            continue
        if line.startswith("> 이 문서는"):
            continue
        cleaned.append(line)
    return bool(cleaned)


def validate_design_document(path: Path, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"primary DESIGN.md does not exist: {path}")
        return ""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    indices: dict[str, int] = {}
    for heading in DESIGN_HEADINGS:
        matches = [idx for idx, line in enumerate(lines) if line.strip() == heading]
        if len(matches) != 1:
            errors.append(f"DESIGN.md must contain heading exactly once: {heading}")
        else:
            indices[heading] = matches[0]
    ordered = [indices[h] for h in DESIGN_HEADINGS if h in indices]
    if ordered and ordered != sorted(ordered):
        errors.append("DESIGN.md canonical sections are out of order")
    for index, heading in enumerate(DESIGN_HEADINGS):
        if heading not in indices:
            continue
        start = indices[heading] + 1
        following = [indices[h] for h in DESIGN_HEADINGS[index + 1:] if h in indices]
        end = min(following) if following else len(lines)
        if not meaningful_section("\n".join(lines[start:end])):
            errors.append(f"DESIGN.md section has no concrete content: {heading}")
    return text


def source_anchor_exists(root: Path, source: Any) -> bool:
    if isinstance(source, str):
        return bool(source.strip())
    if not isinstance(source, dict):
        return False
    raw = source.get("path")
    if not is_filled(raw):
        return False
    path = Path(str(raw))
    if not path.is_absolute():
        path = root / path
    if not path.is_file():
        return False
    anchor = source.get("anchor")
    if is_filled(anchor) and str(anchor) not in path.read_text(encoding="utf-8", errors="replace"):
        return False
    return True


def validate_intake(root: Path, evidence: Path, intake: dict[str, Any], design_text: str, errors: list[str]) -> dict[str, int]:
    if intake.get("target_skill") != evidence.name:
        errors.append("REQUIREMENT_INTAKE target_skill does not match requested target")
    validate_source_records(root, intake.get("source_request_documents", []), "intake source_request_documents", errors, require_one=True)
    validate_source_records(root, intake.get("decision_documents", []), "intake decision_documents", errors, require_one=False)
    requirements = intake.get("requirements", [])
    if not isinstance(requirements, list):
        errors.append("REQUIREMENT_INTAKE requirements must be a list")
        requirements = []
    seen: set[str] = set()
    counts = {key: 0 for key in ["total", "user_explicit", "user_decision", "repository_fact", "safe_default", "proposal", "non_blocking_uncertainty", "resolved", "blocking_open"]}
    for idx, req in enumerate(requirements):
        counts["total"] += 1
        if not isinstance(req, dict):
            errors.append(f"intake requirement[{idx}] must be an object")
            continue
        rid = str(req.get("id", ""))
        if not REQ_ID_RE.fullmatch(rid):
            errors.append(f"invalid intake requirement id: {rid}")
        elif rid in seen:
            errors.append(f"duplicate intake requirement id: {rid}")
        seen.add(rid)
        rtype = req.get("type")
        if rtype not in VALID_INTAKE_TYPE:
            errors.append(f"{rid or idx}: invalid requirement type: {rtype}")
        else:
            counts[rtype.lower()] += 1
        status = req.get("status")
        if status not in VALID_INTAKE_STATUS:
            errors.append(f"{rid or idx}: invalid requirement status: {status}")
        elif status == "RESOLVED":
            counts["resolved"] += 1
        if not is_filled(req.get("text")):
            errors.append(f"{rid or idx}: requirement text is empty")
        sources = req.get("sources", [])
        if not isinstance(sources, list) or not sources or any(not source_anchor_exists(root, source) for source in sources):
            errors.append(f"{rid or idx}: requirement needs traceable existing sources")
        blocking = req.get("blocking") is True
        if blocking and status != "RESOLVED":
            counts["blocking_open"] += 1
            errors.append(f"{rid or idx}: blocking intake requirement is unresolved")
        links = req.get("design_links", [])
        if status == "RESOLVED":
            if not isinstance(links, list) or not links:
                errors.append(f"{rid or idx}: resolved requirement needs design_links")
            else:
                for link in links:
                    if not is_filled(link) or str(link) not in design_text:
                        errors.append(f"{rid or idx}: design link not found in DESIGN.md: {link}")
    if counts["user_explicit"] < 1:
        errors.append("REQUIREMENT_INTAKE must contain at least one USER_EXPLICIT requirement")
    questions = intake.get("open_questions", [])
    if not isinstance(questions, list):
        errors.append("REQUIREMENT_INTAKE open_questions must be a list")
    else:
        for idx, question in enumerate(questions):
            if not isinstance(question, dict):
                errors.append(f"intake open_questions[{idx}] must be an object")
                continue
            if question.get("blocking") is True and str(question.get("status", "OPEN")).upper() != "RESOLVED":
                errors.append(f"blocking intake question is unresolved: {question.get('question', idx)}")
                counts["blocking_open"] += 1
    if intake.get("status") != "APPROVED":
        errors.append("REQUIREMENT_INTAKE status must be APPROVED")
    intake["summary"] = counts
    dump(evidence / "REQUIREMENT_INTAKE.yaml", intake)
    return counts


def expected_design_attestation_inputs(root: Path, evidence: Path, design: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[tuple[Path, str]] = [
        (evidence / "SOURCE_REQUEST.md", "source-request"),
        (evidence / "REQUIREMENT_INTAKE.yaml", "requirement-intake"),
        (evidence / "DESIGN_REQUIREMENTS.yaml", "design-requirements"),
    ]
    decisions = evidence / "SOURCE_DECISIONS.md"
    if decisions.exists():
        items.append((decisions, "source-decisions"))
    for record in design.get("source_documents", []):
        if isinstance(record, dict) and record.get("path"):
            items.append((Path(str(record["path"])), str(record.get("type", "design-source"))))
    return unique_file_records(root, items)


def expected_final_attestation_inputs(root: Path, evidence: Path, target: str, spec: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[tuple[Path, str]] = [
        (evidence / "DESIGN_AUDIT_ATTESTATION.yaml", "design-audit-attestation"),
        (evidence / "RULE_MANIFEST.yaml", "rule-manifest"),
        (evidence / "RULE_COVERAGE.yaml", "rule-coverage"),
        (evidence / "COMMAND_SPEC.yaml", "command-spec"),
        (evidence / "AUTHORING_REVIEW.md", "authoring-review"),
        (evidence / "VALIDATION_DESIGN.json", "design-validation"),
        (evidence / "VALIDATION_SPEC.json", "spec-validation"),
        (evidence / "VALIDATION_BUILD.json", "build-validation"),
    ]
    records = unique_file_records(root, items)
    skill_dir = root / ".claude" / "skills" / target
    if not skill_dir.is_dir():
        raise ValueError(f"missing runtime skill directory: {skill_dir}")
    records.append(tree_record(root, skill_dir, "runtime-skill-tree"))
    agent = spec.get("agent_requirement", {})
    if isinstance(agent, dict) and agent.get("decision") == "required" and agent.get("path"):
        agent_path = root / str(agent["path"])
        if not agent_path.is_file():
            raise ValueError(f"missing generated Agent.md: {agent_path}")
        records.append(file_record(root, agent_path, "generated-agent"))
    return records


def validate_attestation(root: Path, evidence: Path, target: str, kind: str, expected_inputs: list[dict[str, Any]], errors: list[str]) -> dict[str, Any] | None:
    filename = "DESIGN_AUDIT_ATTESTATION.yaml" if kind == "design" else "AUDIT_ATTESTATION.yaml"
    report_name = "DESIGN_AUDIT_REPORT.md" if kind == "design" else "AUDIT_REPORT.md"
    role = "skill-design-auditor" if kind == "design" else "skill-author-auditor"
    path = evidence / filename
    try:
        data = load_json_yaml(path)
    except ValueError as exc:
        errors.append(str(exc))
        return None
    if data.get("target_skill") != target or data.get("audit_kind") != kind:
        errors.append(f"{filename} target or audit_kind mismatch")
    if data.get("auditor_role") != role:
        errors.append(f"{filename} auditor_role must be {role}")
    if data.get("verdict") != "PASS":
        errors.append(f"{filename} verdict must be PASS")
    actual_inputs = data.get("inputs", [])
    normalize = lambda values: sorted((x.get("path"), x.get("sha256"), x.get("role"), x.get("kind")) for x in values if isinstance(x, dict))
    if normalize(actual_inputs) != normalize(expected_inputs):
        errors.append(f"{filename} inputs do not match current audited files")
    if data.get("input_fingerprint") != canonical_sha(actual_inputs):
        errors.append(f"{filename} input_fingerprint is invalid")
    report = evidence / report_name
    report_record = data.get("report", {})
    if not report.is_file() or report_record.get("sha256") != (sha256(report) if report.is_file() else None):
        errors.append(f"{filename} report digest does not match current {report_name}")
    if report_record.get("path") not in {rel(root, report), str(report.resolve())}:
        errors.append(f"{filename} report path mismatch")
    if not is_filled(data.get("attested_at")):
        errors.append(f"{filename} attested_at is empty")
    return data


def validate_design(root: Path, evidence: Path, target: str, design: dict[str, Any], intake: dict[str, Any], state: dict[str, Any], errors: list[str]) -> tuple[int, str | None, dict[str, int]]:
    validate_source_lock(root, evidence, state, errors)
    if design.get("target_skill") != target:
        errors.append("DESIGN_REQUIREMENTS target_skill does not match requested target")
    design_docs = validate_source_records(root, design.get("source_documents", []), "design source_documents", errors, require_one=True)
    request_docs = validate_source_records(root, design.get("source_request_documents", []), "source_request_documents", errors, require_one=True)
    validate_source_records(root, design.get("decision_documents", []), "decision_documents", errors, require_one=False)
    if design_docs & request_docs:
        errors.append("a source file must not be both design and source request")
    primary_raw = design.get("primary_design_document")
    primary = Path(str(primary_raw)) if is_filled(primary_raw) else Path()
    if primary and not primary.is_absolute():
        primary = root / primary
    design_text = validate_design_document(primary.resolve(), errors) if is_filled(primary_raw) else ""
    if not is_filled(primary_raw):
        errors.append("primary_design_document is empty")
    intake_path = design.get("requirement_intake_document")
    if not is_filled(intake_path) or Path(str(intake_path)).resolve() != (evidence / "REQUIREMENT_INTAKE.yaml").resolve():
        errors.append("requirement_intake_document must point to the target REQUIREMENT_INTAKE.yaml")
    intake_counts = validate_intake(root, evidence, intake, design_text, errors)

    requirements = design.get("requirements", {})
    if not isinstance(requirements, dict):
        errors.append("DESIGN_REQUIREMENTS requirements must be an object")
        requirements = {}
    missing_fields = sorted(REQUIRED_DESIGN_FIELDS - set(requirements))
    if missing_fields:
        errors.append(f"missing design requirement fields: {missing_fields}")
    resolved = 0
    for key in sorted(REQUIRED_DESIGN_FIELDS & set(requirements)):
        entry = requirements.get(key)
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
        if not isinstance(sources, list) or not sources or any(not is_filled(item) for item in sources):
            errors.append(f"design requirement has no traceable source: {key}")
        if is_filled(content) and isinstance(sources, list) and sources and all(is_filled(item) for item in sources):
            resolved += 1

    decisions = design.get("decision_register", {})
    if not isinstance(decisions, dict):
        errors.append("decision_register must be an object")
    else:
        for bucket in ["user_decisions", "repository_research", "safe_defaults", "non_blocking_uncertainties"]:
            if not isinstance(decisions.get(bucket), list):
                errors.append(f"decision_register.{bucket} must be a list")
    open_questions = design.get("open_questions", [])
    if not isinstance(open_questions, list):
        errors.append("open_questions must be a list")
    else:
        for index, question in enumerate(open_questions):
            if not isinstance(question, dict):
                errors.append(f"open_questions[{index}] must be a structured object")
                continue
            qclass = question.get("class")
            if qclass not in VALID_QUESTION_CLASS:
                errors.append(f"open_questions[{index}] has invalid class: {qclass}")
            if question.get("blocking") is True and str(question.get("status", "OPEN")).upper() != "RESOLVED":
                errors.append(f"blocking design question is unresolved: {question.get('question', index)}")
    if design.get("status") != "APPROVED":
        errors.append("DESIGN_REQUIREMENTS status must be APPROVED")
    verdict = audit_verdict(evidence / "DESIGN_AUDIT_REPORT.md", "independent design audit", errors)
    try:
        expected = expected_design_attestation_inputs(root, evidence, design)
        validate_attestation(root, evidence, target, "design", expected, errors)
    except ValueError as exc:
        errors.append(str(exc))
    return resolved, verdict, intake_counts


def validate_agent_requirement(root: Path, skill_dir: Path, spec: dict[str, Any], skill_front: dict[str, Any] | None, phase: str, errors: list[str]) -> None:
    agent = spec.get("agent_requirement")
    if not isinstance(agent, dict):
        errors.append("agent_requirement must be an object")
        return
    mode, decision, integration = agent.get("mode"), agent.get("decision"), agent.get("integration")
    rationale = str(agent.get("rationale", "")).strip()
    if mode not in VALID_AGENT_MODE:
        errors.append(f"invalid agent_requirement.mode: {mode}")
    if decision not in VALID_AGENT_DECISION:
        errors.append(f"invalid agent_requirement.decision: {decision}")
    if len(rationale) < 20:
        errors.append("agent_requirement.rationale must explain the concrete decision")
    if integration not in VALID_AGENT_INTEGRATION:
        errors.append(f"invalid agent_requirement.integration: {integration}")
    criteria = agent.get("criteria")
    if not isinstance(criteria, dict) or not criteria or any(not isinstance(value, bool) for value in criteria.values()):
        errors.append("agent_requirement.criteria must be a non-empty boolean map")
    if mode == "required" and decision != "required":
        errors.append("agent mode required must produce decision required")
    if mode == "forbidden" and decision != "not-required":
        errors.append("agent mode forbidden must produce decision not-required")
    artifact_type = spec.get("artifact_type")
    if decision == "required":
        if artifact_type != "skill-and-agent":
            errors.append("artifact_type must be skill-and-agent when Agent.md is required")
        name, raw = str(agent.get("name", "")), str(agent.get("path", ""))
        if not TARGET_RE.fullmatch(name):
            errors.append(f"invalid generated agent name: {name}")
        if not raw.startswith(".claude/agents/") or not raw.endswith(".md"):
            errors.append("generated agent path must be under .claude/agents/ and end with .md")
        if integration == "none":
            errors.append("required Agent.md needs a concrete integration mode")
        if phase in {"build", "audit"} and raw:
            path = root / raw
            if not path.exists():
                errors.append(f"required generated Agent.md is missing: {raw}")
            else:
                try:
                    front, _ = parse_frontmatter(path)
                    if front.get("name") != name:
                        errors.append("generated Agent.md frontmatter name does not match COMMAND_SPEC")
                    if not is_filled(front.get("description")):
                        errors.append("generated Agent.md description is missing")
                    if integration == "agent-preloads-skill":
                        skills = front.get("skills", [])
                        if isinstance(skills, str):
                            skills = [item for item in re.split(r"[\s,]+", skills) if item]
                        if spec.get("target_skill") not in (skills or []):
                            errors.append("Agent.md must preload the target skill for agent-preloads-skill integration")
                        if skill_front and skill_front.get("disable-model-invocation") is True:
                            errors.append("manual-only skill cannot be preloaded into Agent.md")
                except ValueError as exc:
                    errors.append(str(exc))
        if phase in {"build", "audit"} and integration == "skill-context-fork" and skill_front:
            if skill_front.get("context") != "fork":
                errors.append("SKILL.md must set context: fork for skill-context-fork integration")
            if skill_front.get("agent") != name:
                errors.append("SKILL.md agent field must match generated Agent.md name")
    else:
        if artifact_type != "skill":
            errors.append("artifact_type must be skill when Agent.md is not required")
        if integration != "none":
            errors.append("agent integration must be none when Agent.md is not required")


def design_fingerprint(root: Path, evidence: Path) -> str:
    paths = [
        evidence / "SOURCE_REQUEST.md", evidence / "SOURCE_DECISIONS.md", evidence / "REQUIREMENT_INTAKE.yaml",
        evidence / "DESIGN_REQUIREMENTS.yaml", evidence / "DESIGN_AUDIT_REPORT.md", evidence / "DESIGN_AUDIT_ATTESTATION.yaml",
    ]
    design = load_json_yaml(evidence / "DESIGN_REQUIREMENTS.yaml")
    for item in design.get("source_documents", []):
        if isinstance(item, dict) and item.get("path"):
            paths.append(Path(str(item["path"])))
    records = unique_file_records(root, [(path, "design-phase") for path in paths])
    return canonical_sha(records)


def spec_coverage_projection(coverage: dict[str, Any]) -> dict[str, Any]:
    projected_rules: dict[str, Any] = {}
    for rid, entry in sorted((coverage.get("rules") or {}).items()):
        controls = []
        for control in entry.get("external_controls", []) or []:
            if isinstance(control, dict):
                controls.append({
                    "type": control.get("type"),
                    "path": control.get("path"),
                    "required_for_pass": control.get("required_for_pass", False),
                })
        projected_rules[rid] = {
            "status": entry.get("status"),
            "rationale": entry.get("rationale"),
            "planned_locations": entry.get("planned_locations", []),
            "external_controls": controls,
        }
    return {"rules": projected_rules, "stage_modules": coverage.get("stage_modules", {})}


def spec_fingerprint(root: Path, evidence: Path) -> str:
    records = unique_file_records(root, [
        (evidence / "RULE_MANIFEST.yaml", "rule-manifest"),
        (evidence / "COMMAND_SPEC.yaml", "command-spec"),
        (evidence / "SPEC_REVIEW.md", "spec-review"),
    ])
    coverage = load_json_yaml(evidence / "RULE_COVERAGE.yaml")
    return canonical_sha({
        "design": design_fingerprint(root, evidence),
        "files": records,
        "coverage_spec": spec_coverage_projection(coverage),
    })


def build_fingerprint(root: Path, evidence: Path, target: str) -> str:
    skill_dir = root / ".claude" / "skills" / target
    spec = load_json_yaml(evidence / "COMMAND_SPEC.yaml")
    records: list[dict[str, Any]] = [
        tree_record(root, skill_dir, "runtime-skill-tree"),
        file_record(root, evidence / "AUTHORING_REVIEW.md", "authoring-review"),
        file_record(root, evidence / "RULE_COVERAGE.yaml", "rule-coverage-final"),
    ]
    agent = spec.get("agent_requirement", {})
    if isinstance(agent, dict) and agent.get("decision") == "required" and agent.get("path"):
        records.append(file_record(root, root / str(agent["path"]), "generated-agent"))
    return canonical_sha({"spec": spec_fingerprint(root, evidence), "files": records})


def audit_fingerprint(root: Path, evidence: Path, target: str) -> str:
    records = unique_file_records(root, [
        (evidence / "AUDIT_REPORT.md", "audit-report"),
        (evidence / "AUDIT_ATTESTATION.yaml", "audit-attestation"),
    ])
    return canonical_sha({"build": build_fingerprint(root, evidence, target), "files": records})


def current_fingerprint(root: Path, evidence: Path, target: str, phase: str) -> str:
    if phase == "design":
        return design_fingerprint(root, evidence)
    if phase == "spec":
        return spec_fingerprint(root, evidence)
    if phase == "build":
        return build_fingerprint(root, evidence, target)
    return audit_fingerprint(root, evidence, target)


def validate_prior_phases(root: Path, evidence: Path, target: str, phase: str, state: dict[str, Any], errors: list[str]) -> None:
    index = PHASES.index(phase)
    for prior in PHASES[:index]:
        entry = state.get("phases", {}).get(prior, {})
        if entry.get("status") != "PASS":
            errors.append(f"prior phase is not PASS: {prior}: {entry.get('status')}")
            continue
        try:
            current = current_fingerprint(root, evidence, target, prior)
        except (ValueError, FileNotFoundError) as exc:
            errors.append(f"cannot recompute {prior} fingerprint: {exc}")
            continue
        if entry.get("fingerprint") != current:
            errors.append(f"prior phase is STALE because inputs changed: {prior}")


def validate(args: argparse.Namespace) -> tuple[list[str], list[str], dict[str, Any]]:
    root = Path(args.project_root).expanduser().resolve()
    evidence = root / ".claude" / "skill-authoring" / args.target
    skill_dir = root / ".claude" / "skills" / args.target
    errors: list[str] = []
    warnings: list[str] = []
    try:
        state = load_json_yaml(evidence / "AUTHORING_STATE.yaml")
        design = load_json_yaml(evidence / "DESIGN_REQUIREMENTS.yaml")
        intake = load_json_yaml(evidence / "REQUIREMENT_INTAKE.yaml")
    except ValueError as exc:
        return [str(exc)], warnings, {}
    validate_prior_phases(root, evidence, args.target, args.phase, state, errors)
    resolved_design, design_verdict, intake_counts = validate_design(root, evidence, args.target, design, intake, state, errors)

    if args.phase == "design":
        fingerprint = ""
        if not errors:
            try:
                fingerprint = design_fingerprint(root, evidence)
            except (ValueError, FileNotFoundError) as exc:
                errors.append(str(exc))
        result = {
            "schema_version": "1.3", "target": args.target, "phase": args.phase, "ok": not errors,
            "errors": errors, "warnings": warnings,
            "counts": {"design_requirements": len(REQUIRED_DESIGN_FIELDS), "resolved_design_requirements": resolved_design, **{f"intake_{k}": v for k, v in intake_counts.items()}},
            "design_audit_verdict": design_verdict, "fingerprint": fingerprint, "validated_at": now(),
        }
        return errors, warnings, result

    try:
        manifest = load_json_yaml(evidence / "RULE_MANIFEST.yaml")
        coverage = load_json_yaml(evidence / "RULE_COVERAGE.yaml")
        spec = load_json_yaml(evidence / "COMMAND_SPEC.yaml")
    except ValueError as exc:
        return [str(exc)], warnings, {}

    source_ids = [rule.get("id") for rule in manifest.get("rules", [])]
    source_set = set(source_ids)
    coverage_rules = coverage.get("rules", {})
    coverage_set = set(coverage_rules)
    duplicate_source = sorted({rid for rid in source_ids if source_ids.count(rid) > 1})
    missing, unknown = sorted(source_set - coverage_set), sorted(coverage_set - source_set)
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
            if args.phase == "spec" and not entry.get("planned_locations", []):
                errors.append(f"{rid}: APPLY/TRANSFORM needs planned_locations during spec")
            if args.phase in {"build", "audit"}:
                targets = entry.get("targets", [])
                if not targets:
                    errors.append(f"{rid}: APPLY/TRANSFORM has no final target")
                for target in targets:
                    ok, reason = target_exists(root, skill_dir, target)
                    if not ok:
                        errors.append(f"{rid}: {reason}")
        elif status == "EXCLUDE" and len(rationale) < 20:
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
                    elif not (root / str(control.get("path"))).exists():
                        errors.append(f"{rid}: implemented external control path does not exist: {control.get('path')}")
    coverage.setdefault("summary", {}).update({
        "source_rule_count": len(source_ids), "classified_rule_count": classified,
        "missing_rule_count": len(missing), "duplicate_rule_count": len(duplicate_source), "unknown_rule_count": len(unknown),
    })
    dump(evidence / "RULE_COVERAGE.yaml", coverage)

    missing_fields = sorted(REQUIRED_SPEC_FIELDS - set(spec))
    if missing_fields:
        errors.append(f"missing spec fields: {missing_fields}")
    if spec.get("target_skill") != args.target:
        errors.append("COMMAND_SPEC target_skill does not match requested target")
    if spec.get("artifact_type") not in {"skill", "skill-and-agent"}:
        errors.append(f"invalid artifact_type: {spec.get('artifact_type')}")
    if spec.get("primary_stage") not in VALID_STAGE:
        errors.append(f"invalid primary_stage: {spec.get('primary_stage')}")
    secondary = spec.get("secondary_stages", [])
    if not isinstance(secondary, list) or any(stage not in VALID_STAGE for stage in secondary):
        errors.append("secondary_stages contains invalid values")
        secondary = []
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
    requirements = design.get("requirements", {})
    if requirements.get("purpose", {}).get("status") == "RESOLVED" and spec.get("purpose") != requirements.get("purpose", {}).get("value"):
        errors.append("COMMAND_SPEC purpose must match approved DESIGN_REQUIREMENTS purpose")
    if requirements.get("user_outcome", {}).get("status") == "RESOLVED" and spec.get("user_outcome") != requirements.get("user_outcome", {}).get("value"):
        errors.append("COMMAND_SPEC user_outcome must match approved DESIGN_REQUIREMENTS user_outcome")
    design_paths = {str(Path(item.get("path")).resolve()) for item in design.get("source_documents", []) if isinstance(item, dict) and is_filled(item.get("path"))}
    request_paths = {str(Path(item.get("path")).resolve()) for item in design.get("source_request_documents", []) if isinstance(item, dict) and is_filled(item.get("path"))}
    decision_paths = {str(Path(item.get("path")).resolve()) for item in design.get("decision_documents", []) if isinstance(item, dict) and is_filled(item.get("path"))}
    spec_inputs = spec.get("inputs", {})
    if design_paths - {str(Path(path).resolve()) for path in spec_inputs.get("design_documents", []) or []}:
        errors.append("COMMAND_SPEC inputs.design_documents omits approved design sources")
    if request_paths - {str(Path(path).resolve()) for path in spec_inputs.get("source_request_documents", []) or []}:
        errors.append("COMMAND_SPEC inputs.source_request_documents omits request sources")
    if decision_paths - {str(Path(path).resolve()) for path in spec_inputs.get("decision_documents", []) or []}:
        errors.append("COMMAND_SPEC inputs.decision_documents omits decision sources")
    if str(Path(spec_inputs.get("requirement_intake_document", "")).resolve()) != str((evidence / "REQUIREMENT_INTAKE.yaml").resolve()):
        errors.append("COMMAND_SPEC must reference REQUIREMENT_INTAKE.yaml")
    stage_info = coverage.get("stage_modules", {})
    if stage_info.get("primary") != spec.get("primary_stage"):
        errors.append("coverage stage_modules.primary must match spec primary_stage")
    applied = stage_info.get("applied", {})
    for stage in [spec.get("primary_stage"), *secondary]:
        if stage and applied.get(stage) is not True:
            errors.append(f"stage module not marked applied: {stage}")

    skill_front: dict[str, Any] | None = None
    if args.phase in {"build", "audit"}:
        skill_path = skill_dir / "SKILL.md"
        if not skill_path.exists():
            errors.append(f"missing runtime skill: {skill_path}")
        else:
            try:
                skill_front, text = parse_frontmatter(skill_path)
                if not is_filled(skill_front.get("description")):
                    errors.append("SKILL.md frontmatter description is missing")
                if len(text.splitlines()) > 500:
                    warnings.append("SKILL.md exceeds 500 lines; consider progressive disclosure")
                if skill_dir.name != args.target:
                    errors.append("skill directory name does not match target command")
                named_args = skill_front.get("arguments", [])
                if isinstance(named_args, str):
                    named_args = [item for item in re.split(r"[\s,]+", named_args) if item]
                used_named = set(re.findall(r"\$([A-Za-z_][A-Za-z0-9_-]*)", text)) - {"ARGUMENTS"}
                undeclared = sorted(used_named - set(named_args or []))
                if undeclared:
                    errors.append(f"undeclared named placeholders: {undeclared}")
            except ValueError as exc:
                errors.append(str(exc))
        review = evidence / "AUTHORING_REVIEW.md"
        if not review.exists():
            errors.append("missing AUTHORING_REVIEW.md")
        else:
            review_text = review.read_text(encoding="utf-8")
            for heading in ["## 규칙 집계", "## Agent.md 필요성 판정", "## 문장별 최종 검토", "## 기계 검사 결과"]:
                if heading not in review_text:
                    errors.append(f"AUTHORING_REVIEW.md missing heading: {heading}")
        anti_source = {item.get("id") for item in manifest.get("anti_patterns", [])}
        anti_cov = coverage.get("anti_patterns", {})
        if set(anti_cov) != anti_source:
            errors.append("anti-pattern coverage IDs do not match manifest")
        for aid, entry in anti_cov.items():
            if entry.get("status") not in VALID_ANTI_STATUS:
                errors.append(f"{aid}: anti-pattern status must be PASS or NOT_APPLICABLE")
            if len(str(entry.get("evidence", "")).strip()) < 8:
                errors.append(f"{aid}: anti-pattern evidence is too weak")
    validate_agent_requirement(root, skill_dir, spec, skill_front, args.phase, errors)

    final_verdict = None
    if args.phase == "audit":
        final_verdict = audit_verdict(evidence / "AUDIT_REPORT.md", "independent final skill audit", errors)
        try:
            expected_final = expected_final_attestation_inputs(root, evidence, args.target, spec)
            validate_attestation(root, evidence, args.target, "final", expected_final, errors)
        except ValueError as exc:
            errors.append(str(exc))

    fingerprint = ""
    if not errors:
        try:
            fingerprint = current_fingerprint(root, evidence, args.target, args.phase)
        except (ValueError, FileNotFoundError) as exc:
            errors.append(str(exc))
    result = {
        "schema_version": "1.3", "target": args.target, "phase": args.phase, "ok": not errors,
        "errors": errors, "warnings": warnings,
        "counts": {
            "source_rules": len(source_ids), "classified_rules": classified, "missing_rules": len(missing),
            "unknown_rules": len(unknown), "duplicate_rules": len(duplicate_source),
            "design_requirements": len(REQUIRED_DESIGN_FIELDS), "resolved_design_requirements": resolved_design,
            **{f"intake_{key}": value for key, value in intake_counts.items()},
        },
        "design_audit_verdict": design_verdict, "audit_verdict": final_verdict,
        "fingerprint": fingerprint, "validated_at": now(),
    }
    return errors, warnings, result


def invalidate_later(state: dict[str, Any], phase: str, status: str = "STALE") -> None:
    index = PHASES.index(phase)
    for later in PHASES[index + 1:]:
        entry = state.setdefault("phases", {}).setdefault(later, {})
        entry.update({"status": status, "fingerprint": "", "validated_at": ""})


def update_state(state: dict[str, Any], phase: str, result: dict[str, Any], errors: list[str]) -> None:
    entry = state.setdefault("phases", {}).setdefault(phase, {})
    previous_fp = entry.get("fingerprint")
    if errors:
        entry.update({"status": "FAILED", "fingerprint": "", "validated_at": result.get("validated_at", now())})
        invalidate_later(state, phase)
    else:
        new_fp = result.get("fingerprint", "")
        changed = previous_fp != new_fp or entry.get("status") != "PASS"
        entry.update({"status": "PASS", "fingerprint": new_fp, "validated_at": result.get("validated_at", now()), "validation_file": f"VALIDATION_{phase.upper()}.json"})
        if changed:
            invalidate_later(state, phase)
    state["updated_at"] = now()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--target", required=True)
    parser.add_argument("--phase", choices=PHASES, required=True)
    args = parser.parse_args()
    errors, warnings, result = validate(args)
    root = Path(args.project_root).expanduser().resolve()
    evidence = root / ".claude" / "skill-authoring" / args.target
    if evidence.exists():
        dump(evidence / f"VALIDATION_{args.phase.upper()}.json", result)
        state_path = evidence / "AUTHORING_STATE.yaml"
        if state_path.exists():
            try:
                state = load_json_yaml(state_path)
                update_state(state, args.phase, result, errors)
                dump(state_path, state)
            except ValueError:
                pass
        active_path = root / ".claude" / "skill-authoring" / ".active.json"
        if active_path.exists():
            try:
                active = load_json_yaml(active_path)
                if active.get("target") == args.target:
                    active["phase"] = args.phase.upper()
                    active["status"] = "PASS" if not errors else "FAILED"
                    active["updated_at"] = now()
                    dump(active_path, active)
            except ValueError:
                pass
        if args.phase == "design" and not errors:
            active = load_json_yaml(active_path) if active_path.exists() else {}
            if active.get("mode") == "design":
                dump(evidence / "FINAL_STATUS.json", {
                    "schema_version": "1.3", "target": args.target, "status": "PASS", "scope": "DESIGN",
                    "validated_at": result["validated_at"], "fingerprints": {"design": result["fingerprint"]},
                    "validation_files": ["VALIDATION_DESIGN.json"],
                })
        if args.phase == "audit" and not errors:
            state = load_json_yaml(state_path)
            phases = state.get("phases", {})
            if all(phases.get(phase, {}).get("status") == "PASS" for phase in PHASES):
                dump(evidence / "FINAL_STATUS.json", {
                    "schema_version": "1.3", "target": args.target, "status": "PASS", "scope": "FULL",
                    "validated_at": result["validated_at"],
                    "fingerprints": {phase: phases[phase]["fingerprint"] for phase in PHASES},
                    "validation_files": [f"VALIDATION_{phase.upper()}.json" for phase in PHASES],
                })
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
