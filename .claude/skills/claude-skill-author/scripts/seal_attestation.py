#!/usr/bin/env python3
"""Bind an independent audit report to the exact files it reviewed.

The attestation is not a cryptographic signature. It is a deterministic digest
chain that prevents an old PASS report from being reused after inputs change.
Only the Python standard library is required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

VERDICT_RE = re.compile(r"^- 판정:\s*(PASS|CONDITIONAL|FAIL)\s*$", re.MULTILINE)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json_sha(data: Any) -> str:
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def file_record(root: Path, path: Path, role: str) -> dict[str, str]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"path": rel(root, path), "sha256": sha256_file(path), "role": role, "kind": "file"}


def tree_record(root: Path, path: Path, role: str) -> dict[str, Any]:
    if not path.is_dir():
        raise FileNotFoundError(path)
    members = []
    for item in sorted(p for p in path.rglob("*") if p.is_file()):
        members.append({"path": rel(path, item), "sha256": sha256_file(item)})
    return {
        "path": rel(root, path),
        "sha256": canonical_json_sha(members),
        "role": role,
        "kind": "tree",
        "members": len(members),
    }


def unique_paths(items: Iterable[tuple[Path, str]]) -> list[tuple[Path, str]]:
    seen: set[str] = set()
    out: list[tuple[Path, str]] = []
    for path, role in items:
        key = str(path.resolve())
        if key not in seen:
            seen.add(key)
            out.append((path, role))
    return out


def verdict(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    values = VERDICT_RE.findall(text)
    if len(values) != 1:
        raise ValueError(f"{path.name} must contain exactly one '- 판정: ...' line")
    return values[0]


def design_inputs(root: Path, evidence: Path) -> list[dict[str, Any]]:
    req = load(evidence / "DESIGN_REQUIREMENTS.yaml")
    candidates: list[tuple[Path, str]] = [
        (evidence / "SOURCE_REQUEST.md", "source-request"),
        (evidence / "REQUIREMENT_INTAKE.yaml", "requirement-intake"),
        (evidence / "DESIGN_REQUIREMENTS.yaml", "design-requirements"),
    ]
    decisions = evidence / "SOURCE_DECISIONS.md"
    if decisions.exists():
        candidates.append((decisions, "source-decisions"))
    for item in req.get("source_documents", []):
        if isinstance(item, dict) and item.get("path"):
            candidates.append((Path(str(item["path"])), str(item.get("type", "design-source"))))
    return [file_record(root, path, role) for path, role in unique_paths(candidates)]


def final_inputs(root: Path, evidence: Path, target: str) -> list[dict[str, Any]]:
    candidates: list[tuple[Path, str]] = [
        (evidence / "DESIGN_AUDIT_ATTESTATION.yaml", "design-audit-attestation"),
        (evidence / "RULE_MANIFEST.yaml", "rule-manifest"),
        (evidence / "RULE_COVERAGE.yaml", "rule-coverage"),
        (evidence / "COMMAND_SPEC.yaml", "command-spec"),
        (evidence / "AUTHORING_REVIEW.md", "authoring-review"),
        (evidence / "VALIDATION_DESIGN.json", "design-validation"),
        (evidence / "VALIDATION_SPEC.json", "spec-validation"),
        (evidence / "VALIDATION_BUILD.json", "build-validation"),
    ]
    records = [file_record(root, path, role) for path, role in unique_paths(candidates)]
    skill_dir = root / ".claude" / "skills" / target
    records.append(tree_record(root, skill_dir, "runtime-skill-tree"))
    spec = load(evidence / "COMMAND_SPEC.yaml")
    agent = spec.get("agent_requirement", {})
    if isinstance(agent, dict) and agent.get("decision") == "required" and agent.get("path"):
        records.append(file_record(root, root / str(agent["path"]), "generated-agent"))
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--target", required=True)
    parser.add_argument("--kind", choices=["design", "final"], required=True)
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    evidence = root / ".claude" / "skill-authoring" / args.target
    if not evidence.is_dir():
        print(f"ERROR: missing evidence directory: {evidence}", file=sys.stderr)
        return 2

    if args.kind == "design":
        report = evidence / "DESIGN_AUDIT_REPORT.md"
        output = evidence / "DESIGN_AUDIT_ATTESTATION.yaml"
        role = "skill-design-auditor"
        inputs = design_inputs(root, evidence)
    else:
        report = evidence / "AUDIT_REPORT.md"
        output = evidence / "AUDIT_ATTESTATION.yaml"
        role = "skill-author-auditor"
        inputs = final_inputs(root, evidence, args.target)

    if not report.is_file():
        print(f"ERROR: missing audit report: {report}", file=sys.stderr)
        return 2
    try:
        report_verdict = verdict(report)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if report_verdict != "PASS":
        print(f"ERROR: cannot seal a non-PASS audit report: {report_verdict}", file=sys.stderr)
        return 2

    data = {
        "schema_version": "1.3",
        "target_skill": args.target,
        "audit_kind": args.kind,
        "auditor_role": role,
        "verdict": report_verdict,
        "inputs": inputs,
        "input_fingerprint": canonical_json_sha(inputs),
        "report": file_record(root, report, "audit-report"),
        "attested_at": datetime.now(timezone.utc).isoformat(),
    }
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "output": rel(root, output), "fingerprint": data["input_fingerprint"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
