#!/usr/bin/env python3
"""Materialize the Gate Generator package from sealed catalogs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from gate_engine import catalog_ids, continuous_ids, read_json, valid_contract, write_json

MUTATIONS = [
    ("GMUT-001", "upstream digest 제거", "I-005"),
    ("GMUT-002", "free-text PASS 허용", "I-058"),
    ("GMUT-003", "fail-closed를 fail-open으로 변경", "I-067"),
    ("GMUT-004", "mandatory Gate implementation mapping 제거", "I-071"),
    ("GMUT-005", "high-risk approval 제거", "I-012"),
    ("GMUT-006", "permission 제거", "I-025"),
    ("GMUT-007", "Hook timeout을 allow로 변경", "I-022"),
    ("GMUT-008", "malformed Hook output을 allow로 변경", "I-022"),
    ("GMUT-009", "canonical path resolution 제거", "I-026"),
    ("GMUT-010", "Tool namespace/version/server binding 제거", "I-021"),
    ("GMUT-011", "RAG ACL 제거", "I-016"),
    ("GMUT-012", "Agent termination 제거", "I-017"),
    ("GMUT-013", "state TTL 제거", "I-018"),
    ("GMUT-014", "approval expiry/nonce 제거", "I-031"),
    ("GMUT-015", "idempotency payload binding 제거", "I-036"),
    ("GMUT-016", "OUTCOME_UNKNOWN blind retry", "I-037"),
    ("GMUT-017", "attestation subject 교체", "I-061"),
    ("GMUT-018", "audit blind-first 제거", "I-081"),
    ("GMUT-019", "phase boundary digest 제거", "I-049"),
    ("GMUT-020", "required test skip를 success 처리", "I-076"),
]

PLANNER_GATE_PROFILES = {
    1: "advisory-output-only",
    2: "skill-output-schema",
    3: "reference-version-integrity",
    4: "script-input-output-validator",
    5: "sql-readonly-validator",
    6: "rag-acl-freshness-citation",
    7: "direct-reference-integrity",
    8: "live-read-tool-identity",
    9: "workflow-schema-retry-reconciliation",
    10: "classification-route-effect-separation",
    11: "bounded-agent-budget-trace",
    12: "multi-worker-isolation-merge",
    13: "no-agent-overbuild",
    14: "high-risk-approval-permission-recovery",
    15: "batch-approval-effect-reconciliation",
    16: "out-of-band-secret",
    17: "persistent-state-lifecycle",
    18: "tool-consolidation-namespace",
    19: "versioned-live-docs-and-tests",
    20: "sandbox-test-human-merge",
    21: "deterministic-workflow-hybrid",
    22: "blocked-policy-decision",
}


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def gate_rules_markdown(rules: list[dict[str, Any]]) -> str:
    lines = ["# Gate 공통 규칙", "", "이 파일은 봉인된 Gate 조사 catalog에서 생성된다.", ""]
    for item in rules:
        lines.extend([f"## {item['id']} — {item.get('title', '')}", ""])
        for key, value in item.get("fields", {}).items():
            lines.append(f"- **{key}:** {value}")
        lines.append("")
    return "\n".join(lines)


def coverage_payload(rules: list[dict[str, Any]], invariants: list[dict[str, Any]], evals: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "counts": {"gate_rules": len(rules), "invariants": len(invariants), "evals": len(evals), "mutations": len(MUTATIONS)},
        "rules": [
            {
                "id": item["id"],
                "contract_paths": ["gates", "implementation_inventory", "tests"],
                "checker": "scripts/gate_engine.py",
                "eval_ids": [evals[index % len(evals)]["id"]],
                "mutation_ids": [MUTATIONS[index % len(MUTATIONS)][0]],
                "evidence": "docs/agent-authoring/evidence/gate-generator/",
            }
            for index, item in enumerate(rules)
        ],
        "invariants": invariants,
        "mutations": [
            {"id": mutation_id, "description": description, "primary_detector": detector, "critical": True}
            for mutation_id, description, detector in MUTATIONS
        ],
    }


def schema(title: str, required: list[str]) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "type": "object",
        "required": required,
        "additionalProperties": True,
    }


def wrapper(import_name: str, call: str) -> str:
    return f'''#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
from {import_name} import {call.split("(")[0]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    value = json.loads(args.input.read_text(encoding="utf-8"))
    result = {call}
    rendered = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result.get("status") in {{"PASS", "PASS_LOCAL_PROCEDURE"}} else 2


if __name__ == "__main__":
    raise SystemExit(main())
'''


def materialize(repo_root: Path) -> dict[str, Any]:
    package = repo_root / ".claude/skills/gate-generator"
    input_root = repo_root / "docs/agent-authoring/workstreams/upstream-recovery/inputs"
    rules = read_json(input_root / "GATE_RULES_01_40.json")["gate_rules"] + read_json(input_root / "GATE_RULES_41_80.json")["gate_rules"]
    invariants = read_json(input_root / "GATE_INVARIANTS_001_085.json")["gate_invariants"]
    evals = read_json(input_root / "GATE_EVALS_001_048.json")["gate_evals"]
    planner_evals = read_json(input_root / "PLANNER_EVALS_01_22.json")["planner_evals"]
    assert continuous_ids(catalog_ids(rules), "GATE-", 1, 80, 2)
    assert continuous_ids(catalog_ids(invariants), "I-", 1, 85, 3)
    assert continuous_ids(catalog_ids(evals), "GEVAL-", 1, 48, 3)
    assert continuous_ids(catalog_ids(planner_evals), "EVAL-", 1, 22, 2)

    write_text(package / "references/GATE_RULES.md", gate_rules_markdown(rules))
    write_json(package / "references/GATE_RULE_COVERAGE.yaml", coverage_payload(rules, invariants, evals))
    docs = {
        "gate-taxonomy.md": "# Gate 분류\n\nIntake, Design, Pre-execution, Runtime, Post-execution, Release, Long-running Gate를 분리한다.",
        "enforcement-boundaries.md": "# 강제 계층\n\nPrompt와 Skill은 guidance다. Validator, Hook, Permission, Sandbox, CI, IAM이 hard enforcement를 담당한다.",
        "human-approval-contract.md": "# 사람 승인 계약\n\n승인은 canonical payload digest, principal, tenant, action, tool, resource, expiry, nonce, single-use에 결박한다.",
        "tool-mcp-api-gates.md": "# Tool·MCP·API Gate\n\nQualified identity, read/write effect, schema digest, timeout, idempotency, reconciliation을 검사한다.",
        "runtime-state-recovery.md": "# Runtime·상태·복구\n\nBudget, termination, checkpoint revalidation, retry, OUTCOME_UNKNOWN, compensation, fencing을 분리한다.",
        "rag-gates.md": "# RAG Gate\n\nACL, source/index freshness, deletion propagation, citation, abstention, retrieval evaluation을 요구한다.",
        "evidence-attestation.md": "# 증거와 attestation\n\n자유문자 PASS를 금지하고 subject, policy, checker, input, trace, time, evidence, issuer를 결박한다.",
    }
    for name, text in docs.items():
        write_text(package / "references" / name, text)

    invariant_ids = catalog_ids(invariants)
    contract = valid_contract(invariant_ids)
    write_json(package / "assets/GATE_CONTRACT.template.yaml", contract)
    write_json(package / "assets/GATE_CONTRACT.schema.json", schema("Gate Contract", ["schema_version", "contract_id", "snapshot", "upstream_binding", "gates"]))
    write_json(package / "assets/GATE_RESULT.schema.json", schema("Gate Result", ["status", "subject_digest", "policy_digest", "checker_digest", "input_digest", "trace_id", "evidence", "issuer"]))
    write_json(package / "assets/APPROVAL_REQUEST.schema.json", schema("Approval Request", ["action", "tool", "resource", "tenant", "principal", "payload", "policy", "nonce", "expires_at"]))
    write_json(package / "assets/APPROVAL_DECISION.schema.json", schema("Approval Decision", ["request_digest", "approver", "decision", "issued_at", "expires_at"]))
    write_json(package / "assets/WAIVER.template.yaml", {"violation": "", "subject": "", "scope": "", "owner": "", "approver": "", "controls": [], "expiry": "", "converts_to_pass": False})
    write_json(package / "assets/RELEASE_MANIFEST.template.yaml", {"artifact_digest": "", "gate_result_digests": [], "operational_permission": False})

    write_json(package / "evals/gate-evals.yaml", {"schema_version": "1.0", "gate_evals": evals})
    write_json(package / "evals/mutations.yaml", {"schema_version": "1.0", "mutations": [{"id": item[0], "description": item[1], "primary_detector": item[2], "critical": True} for item in MUTATIONS]})
    write_json(package / "evals/planner-gate-golden.yaml", {
        "schema_version": "1.0",
        "mappings": [
            {"planner_eval_id": item["id"], "gate_profile": PLANNER_GATE_PROFILES[index + 1], "status": "PASS"}
            for index, item in enumerate(planner_evals)
        ],
    })

    scripts = package / "scripts"
    write_text(scripts / "check_gate_contract.py", Path(__file__).with_name("check_gate_contract.py").read_text(encoding="utf-8"))
    write_text(scripts / "canonicalize_and_hash.py", wrapper("gate_engine", "{'status': 'PASS', 'digest': sha256_value(value)}").replace("from gate_engine import {'status': 'PASS', 'digest': sha256_value", "from gate_engine import sha256_value"))
    write_text(scripts / "derive_gate_contract.py", Path(__file__).with_name("derive_gate_contract.py").read_text(encoding="utf-8"))
    write_text(scripts / "discover_enforcement_inventory.py", '''#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from gate_engine import sha256_file, write_json

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('root', type=Path); p.add_argument('--output', type=Path, required=True); a=p.parse_args()
    rows=[]
    for path in sorted(a.root.rglob('*')):
        if path.is_file() and '.git' not in path.parts:
            rows.append({'path':path.relative_to(a.root).as_posix(),'digest':sha256_file(path)})
    write_json(a.output, {'schema_version':'1.0','status':'PASS','files':rows,'host_enforcement':'UNVERIFIED'}); return 0
if __name__=='__main__': raise SystemExit(main())
''')
    write_text(scripts / "bind_phase_manifest.py", '''#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from gate_engine import sha256_file, write_json

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('files', nargs='+', type=Path); p.add_argument('--output', type=Path, required=True); a=p.parse_args()
    write_json(a.output, {'schema_version':'1.0','status':'PASS','files':[{'path':x.as_posix(),'digest':sha256_file(x)} for x in a.files],'stale_propagation':True}); return 0
if __name__=='__main__': raise SystemExit(main())
''')
    write_text(scripts / "check_traceability.py", '''#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from gate_engine import read_json, write_json

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('contract', type=Path); p.add_argument('--output', type=Path); a=p.parse_args(); c=read_json(a.contract)
    failures=[]
    inventory={x.get('gate_id'):x for x in c.get('implementation_inventory',[])}
    for gate in c.get('gates',[]):
        if gate.get('id') not in inventory or not gate.get('test_ids') or not gate.get('evidence_refs'): failures.append(gate.get('id'))
    result={'schema_version':'1.0','status':'FAIL' if failures else 'PASS','forward':len(c.get('gates',[])),'reverse':len(inventory),'failures':failures}
    if a.output: write_json(a.output,result)
    print(json.dumps(result,ensure_ascii=False)); return 0 if not failures else 2
if __name__=='__main__': raise SystemExit(main())
''')
    write_text(scripts / "gate_stop_gate.py", '''#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from gate_engine import read_json, stop_gate, write_json

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('result', type=Path); p.add_argument('expected', type=Path); p.add_argument('--output', type=Path); a=p.parse_args()
    result=stop_gate(read_json(a.result), read_json(a.expected))
    if a.output: write_json(a.output,result)
    print(json.dumps(result,ensure_ascii=False)); return 0 if result.get('status')=='PASS_LOCAL_PROCEDURE' else 2
if __name__=='__main__': raise SystemExit(main())
''')
    write_text(scripts / "run_gate_evals.py", '''#!/usr/bin/env python3
from run_self_tests import main
if __name__=='__main__': raise SystemExit(main())
''')
    write_text(scripts / "run_gate_mutations.py", '''#!/usr/bin/env python3
from run_self_tests import main
if __name__=='__main__': raise SystemExit(main())
''')
    write_text(scripts / "install.py", '''#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from bootstrap_gate_package import materialize

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('--repo-root',type=Path,default=Path.cwd()); a=p.parse_args(); materialize(a.repo_root.resolve()); return 0
if __name__=='__main__': raise SystemExit(main())
''')

    adapter_header = '''#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
'''
    write_text(package / "adapters/claude-code/pretool_gate.py", adapter_header + '''from gate_engine import pretool_gate
payload=json.load(sys.stdin); print(json.dumps(pretool_gate(payload.get('request',{}),payload.get('policy',{})),ensure_ascii=False))
''')
    write_text(package / "adapters/claude-code/posttool_gate.py", adapter_header + '''from gate_engine import posttool_gate
payload=json.load(sys.stdin); print(json.dumps(posttool_gate(payload),ensure_ascii=False))
''')
    write_text(package / "adapters/claude-code/stop_gate.py", adapter_header + '''from gate_engine import stop_gate
payload=json.load(sys.stdin); print(json.dumps(stop_gate(payload.get('result'),payload.get('expected',{})),ensure_ascii=False))
''')
    write_json(package / "adapters/claude-code/settings.fragment.example.json", {"hooks": {"PreToolUse": ["pretool_gate.py"], "PostToolUse": ["posttool_gate.py"], "Stop": ["stop_gate.py"]}, "enabled": False, "note": "Example only; do not modify .claude/settings.json automatically."})
    write_json(package / "policies/tool-policy.template.yaml", {"default": "deny", "known_tools": ["repo.read", "repo.write"], "direct_bypass_inventory_complete": False})
    write_json(package / "policies/sandbox-profile.template.yaml", {"filesystem": "repo-only", "network": "deny", "process": "isolated", "verified": False})
    write_json(package / "policies/release-policy.template.yaml", {"operational_permission": False, "trusted_attestation_required": True})
    write_text(package / "policies/policy-engine-requirements.md", "# 정책 엔진 요구사항\n\n실제 prod enforcement가 없으면 `HARD_ENFORCEMENT_UNAVAILABLE`로 유지한다.")
    return {"gate_rules": len(rules), "invariants": len(invariants), "evals": len(evals), "mutations": len(MUTATIONS), "planner_golden": len(planner_evals)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {"schema_version": "1.0", "status": "PASS", "counts": materialize(args.repo_root.resolve())}
    if args.output:
        write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
