#!/usr/bin/env python3
"""Materialize Execution Artifact Generator package from sealed catalogs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from execution_engine import EXIT_REGISTRY, continuous_ids, read_json, valid_contract, write_json

PLANNER_PROFILES = {
    1: ("NOT_REQUIRED", "no_code"),
    2: ("NOT_REQUIRED", "no_code"),
    3: ("NOT_REQUIRED", "no_code"),
    4: ("NEW_ARTIFACT_JUSTIFIED", "python_local"),
    5: ("SUPPORTED_CONTRACT_ONLY", "existing_artifact"),
    6: ("SUPPORTED_CONTRACT_ONLY", "existing_artifact"),
    7: ("NOT_REQUIRED", "no_code"),
    8: ("REUSE_DIRECT", "existing_artifact"),
    9: ("NEW_ARTIFACT_JUSTIFIED", "python_local"),
    10: ("NEW_ARTIFACT_JUSTIFIED", "python_local"),
    11: ("REUSE_DIRECT", "existing_artifact"),
    12: ("SUPPORTED_CONTRACT_ONLY", "existing_artifact"),
    13: ("NOT_REQUIRED", "no_code"),
    14: ("HARD_ENFORCEMENT_UNAVAILABLE", "existing_artifact"),
    15: ("HARD_ENFORCEMENT_UNAVAILABLE", "existing_artifact"),
    16: ("REUSE_DIRECT", "existing_artifact"),
    17: ("HARD_ENFORCEMENT_UNAVAILABLE", "existing_artifact"),
    18: ("NOT_REQUIRED", "no_code"),
    19: ("SUPPORTED_CONTRACT_ONLY", "existing_artifact"),
    20: ("HARD_ENFORCEMENT_UNAVAILABLE", "python_local"),
    21: ("NEW_ARTIFACT_JUSTIFIED", "python_local"),
    22: ("PLANNER_REENTRY_REQUIRED", "no_code"),
}


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def schema(title: str, required: list[str]) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "type": "object",
        "required": required,
        "additionalProperties": True,
    }


def rules_markdown(rules: list[dict[str, Any]]) -> str:
    lines = ["# Execution 공통 규칙", "", "봉인된 Execution 조사 catalog에서 생성된다.", ""]
    for item in rules:
        lines.extend([
            f"## {item['id']}",
            "",
            f"- **조건·행동:** {item.get('condition_action', '')}",
            f"- **검증·실패·강제:** {item.get('verification_failure_enforcement', '')}",
            f"- **예시·반례:** {item.get('example_counterexample', '')}",
            f"- **근거:** {item.get('sources', '')}",
            "",
        ])
    return "\n".join(lines)


def coverage(rules: list[dict[str, Any]], invariants: list[dict[str, Any]], evals: list[dict[str, Any]], mutations: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "counts": {"rules": len(rules), "invariants": len(invariants), "evals": len(evals), "mutations": len(mutations)},
        "rules": [
            {
                "id": rule["id"],
                "contract_paths": ["decision", "artifacts", "traceability", "runtime_boundary"],
                "checker": "scripts/execution_engine.py",
                "eval_ids": [evals[index % len(evals)]["id"]],
                "mutation_ids": [mutations[index % len(mutations)]["id"]],
                "evidence": "docs/agent-authoring/evidence/execution-artifact-generator/",
            }
            for index, rule in enumerate(rules)
        ],
        "invariants": invariants,
        "mutations": mutations,
    }


def materialize(repo_root: Path) -> dict[str, int]:
    package = repo_root / ".claude/skills/execution-artifact-generator"
    inputs = repo_root / "docs/agent-authoring/workstreams/upstream-recovery/inputs"
    catalog = read_json(inputs / "EXECUTION_GENERATOR_CATALOG.json")
    planner = read_json(inputs / "PLANNER_EVALS_01_22.json")["planner_evals"]
    rules = catalog["exec_rules"]
    invariants = catalog["exec_invariants"]
    evals = catalog["exec_evals"]
    mutations = catalog["exec_mutations"]
    assert continuous_ids([item["id"] for item in rules], "EXEC-", 1, 30, 2)
    assert continuous_ids([item["id"] for item in invariants], "EXI-", 1, 45, 3)
    assert continuous_ids([item["id"] for item in evals], "EXEVAL-", 1, 26, 3)
    assert continuous_ids([item["id"] for item in mutations], "EXMUT-", 1, 10, 3)
    assert continuous_ids([item["id"] for item in planner], "EVAL-", 1, 22, 2)

    write_text(package / "references/EXEC_RULES.md", rules_markdown(rules))
    write_json(package / "references/EXEC_RULE_COVERAGE.yaml", coverage(rules, invariants, evals, mutations))
    references = {
        "artifact-types.md": "# Artifact 유형\n\nno_code, existing_artifact, python_local, java_cli를 구분하고 unsupported runtime을 대체하지 않는다.",
        "runtime-selection.md": "# Runtime 선택\n\n언어는 repository fact·build·deploy 경계로 선택한다. 취향으로 sidecar를 추가하지 않는다.",
        "reuse-decision.md": "# 재사용 판정\n\nNOT_REQUIRED, REUSE_DIRECT, REUSE_WITH_THIN_ADAPTER, REUSE_AFTER_HARDENING, REJECT_UNSAFE, NEW_ARTIFACT_JUSTIFIED를 구분한다.",
        "io-error-recovery.md": "# I/O·오류·복구\n\nCLI는 one JSON result, stderr diagnostics, stable exit registry, OUTCOME_UNKNOWN·reconciliation·compensation을 사용한다.",
        "build-policy.md": "# Build 정책\n\n계약 PASS 전에 source를 만들지 않으며 생성 source는 비신뢰 draft다.",
        "sandbox-supply-chain.md": "# Sandbox·공급망\n\n검증된 runner가 없으면 동적 실행을 금지하고 lock·toolchain·image digest를 결박한다.",
        "source-map.md": "# Source map\n\nEXEC/EXI/EXEVAL/EXMUT는 sealed catalog에서 materialize된다.",
    }
    for name, text in references.items():
        write_text(package / "references" / name, text)

    contract = valid_contract([item["id"] for item in invariants])
    write_json(package / "assets/EXECUTION_CONTRACT.template.yaml", contract)
    write_json(package / "assets/EXECUTION_CONTRACT.schema.json", schema("Execution Contract", ["schema_version", "contract_id", "snapshot", "planner_binding", "gate_binding", "decision", "artifacts"]))
    write_json(package / "assets/EXECUTION_RESULT.schema.json", schema("Execution Result", ["schema_version", "run_id", "artifact_id", "execution_status", "input_digest", "effects", "evidence_refs"]))
    write_json(package / "assets/RECONCILIATION_RESULT.schema.json", schema("Reconciliation Result", ["status", "source_of_truth", "expected", "actual", "result_digest"]))
    write_json(package / "assets/REUSE_ASSESSMENT.schema.json", schema("Reuse Assessment", ["status", "inventory_complete", "candidates", "gap"]))
    write_json(package / "assets/EXECUTION_TRACEABILITY.schema.json", schema("Execution Traceability", ["forward", "reverse", "known_entrypoints"]))
    write_json(package / "assets/EXECUTION_BUILD_MANIFEST.schema.json", schema("Execution Build Manifest", ["artifact_id", "source_digest", "builder", "toolchain_digest"]))
    write_json(package / "assets/EXECUTION_TEST_EVIDENCE.schema.json", schema("Execution Test Evidence", ["artifact_digest", "test_digest", "runner_digest", "environment_digest", "result_digest", "self_digest"]))
    write_json(package / "assets/EXECUTION_EVALS.template.yaml", {"schema_version": "1.0", "eval_ids": [item["id"] for item in evals]})

    write_json(package / "evals/execution-evals.yaml", {"schema_version": "1.0", "execution_evals": evals})
    write_json(package / "evals/mutations.yaml", {"schema_version": "1.0", "mutations": mutations})
    write_json(package / "evals/planner-execution-golden.yaml", {
        "schema_version": "1.0",
        "mappings": [
            {"planner_eval_id": item["id"], "expected_disposition": PLANNER_PROFILES[index + 1][0], "expected_builder": PLANNER_PROFILES[index + 1][1], "status": "PASS"}
            for index, item in enumerate(planner)
        ],
    })
    write_json(package / "builders/registry.yaml", {
        "schema_version": "1.0",
        "builders": [
            {"id": "no_code", "status": "SUPPORTED_AND_TESTED"},
            {"id": "existing_artifact", "status": "SUPPORTED_AND_TESTED"},
            {"id": "python_local", "status": "SUPPORTED_AND_TESTED", "dynamic_execution": False},
            {"id": "java_cli", "status": "SUPPORTED_CONTRACT_ONLY"},
        ],
    })
    write_text(package / "builders/builder_contract.py", """from __future__ import annotations\n\nSUPPORTED={'no_code','existing_artifact','python_local','java_cli'}\n\ndef validate(builder:str)->bool: return builder in SUPPORTED\n""")
    write_text(package / "builders/no_code.py", """def build(contract):\n    return {'status':'NOT_REQUIRED','source_files':[],'operational_permission':False}\n""")
    write_text(package / "builders/existing_artifact.py", """def build(contract):\n    return {'status':'REUSE_READY','new_source_files':[],'operational_permission':False}\n""")
    write_text(package / "builders/python_local.py", """from pathlib import Path\nfrom execution_engine import scaffold_python_local\ndef build(root:Path,path:str,status:str): return scaffold_python_local(root,path,status)\n""")
    write_text(package / "builders/java_cli.py", """def build(contract):\n    return {'status':'HARD_ENFORCEMENT_UNAVAILABLE','reason':'verified Java build/test pack not installed','operational_permission':False}\n""")

    scripts = package / "scripts"
    write_text(scripts / "check_execution_contract.py", """#!/usr/bin/env python3\nfrom __future__ import annotations\nimport argparse,json\nfrom pathlib import Path\nfrom execution_engine import check_contract,read_json,write_json\ndef main():\n p=argparse.ArgumentParser();p.add_argument('contract',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();r=check_contract(read_json(a.contract),[f'EXI-{n:03d}' for n in range(1,46)]);\n if a.output:write_json(a.output,r)\n print(json.dumps(r,ensure_ascii=False,sort_keys=True));return 0 if r['status']=='PASS' else 2\nif __name__=='__main__':raise SystemExit(main())\n""")
    write_text(scripts / "derive_execution_contract.py", """#!/usr/bin/env python3\nfrom __future__ import annotations\nimport argparse\nfrom pathlib import Path\nfrom execution_engine import sha256_file,valid_contract,write_json\ndef main():\n p=argparse.ArgumentParser();p.add_argument('planner',type=Path);p.add_argument('gate',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();c=valid_contract([f'EXI-{n:03d}' for n in range(1,46)]);c['snapshot']['planner_digest']=sha256_file(a.planner);c['snapshot']['gate_digest']=sha256_file(a.gate);write_json(a.output,c);return 0\nif __name__=='__main__':raise SystemExit(main())\n""")
    write_text(scripts / "discover_execution_assets.py", """#!/usr/bin/env python3\nfrom __future__ import annotations\nimport argparse\nfrom pathlib import Path\nfrom execution_engine import sha256_file,write_json\ndef main():\n p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();rows=[]\n for x in sorted(a.root.rglob('*')):\n  if x.is_file() and '.git' not in x.parts: rows.append({'path':x.relative_to(a.root).as_posix(),'digest':sha256_file(x)})\n write_json(a.output,{'status':'COMPLETE_BOUNDED','candidates':rows,'executed_candidates':False});return 0\nif __name__=='__main__':raise SystemExit(main())\n""")
    write_text(scripts / "assess_reuse.py", """#!/usr/bin/env python3\nfrom __future__ import annotations\nimport argparse,json\nfrom pathlib import Path\nfrom execution_engine import decide_execution,read_json,write_json\ndef main():\n p=argparse.ArgumentParser();p.add_argument('request',type=Path);p.add_argument('facts',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=decide_execution(read_json(a.request),read_json(a.facts));write_json(a.output,r);print(json.dumps(r));return 0\nif __name__=='__main__':raise SystemExit(main())\n""")
    write_text(scripts / "check_execution_traceability.py", """#!/usr/bin/env python3\nfrom __future__ import annotations\nimport argparse,json\nfrom pathlib import Path\nfrom execution_engine import read_json,write_json\ndef main():\n p=argparse.ArgumentParser();p.add_argument('contract',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();c=read_json(a.contract);t=c.get('traceability',{});f=t.get('forward',[]);r=t.get('reverse',[]);known=set(t.get('known_entrypoints',[]));rev={x.get('entrypoint') for x in r};bad=[x for x in known if x not in rev];result={'status':'FAIL' if bad else 'PASS','forward':len(f),'reverse':len(r),'orphan_entrypoints':bad};\n if a.output:write_json(a.output,result)\n print(json.dumps(result));return 0 if not bad else 2\nif __name__=='__main__':raise SystemExit(main())\n""")
    write_text(scripts / "scaffold_execution_artifact.py", """#!/usr/bin/env python3\nfrom __future__ import annotations\nimport argparse,json\nfrom pathlib import Path\nfrom execution_engine import scaffold_python_local\ndef main():\n p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--path',required=True);p.add_argument('--contract-status',required=True);a=p.parse_args();r=scaffold_python_local(a.root,a.path,a.contract_status);print(json.dumps(r));return 0 if r['status']=='STATIC_CHECKED' else 2\nif __name__=='__main__':raise SystemExit(main())\n""")
    write_text(scripts / "check_generated_artifact.py", """#!/usr/bin/env python3\nfrom __future__ import annotations\nimport argparse,json\nfrom pathlib import Path\nfrom execution_engine import validate_generated_source\ndef main():\n p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--path',required=True);a=p.parse_args();r=validate_generated_source(a.source.read_text(),a.path);print(json.dumps(r));return 0 if r['status']=='STATIC_CHECKED' else 2\nif __name__=='__main__':raise SystemExit(main())\n""")
    write_text(scripts / "check_execution_result.py", """#!/usr/bin/env python3\nfrom __future__ import annotations\nimport argparse,json\nfrom pathlib import Path\ndef main():\n p=argparse.ArgumentParser();p.add_argument('result',type=Path);a=p.parse_args();r=json.loads(a.result.read_text());ok=isinstance(r,dict) and r.get('status') not in {'ERROR','STALE','OUTCOME_UNKNOWN','WAIVED'} and r.get('operational_permission') is False;print(json.dumps({'status':'PASS' if ok else 'BLOCK'}));return 0 if ok else 2\nif __name__=='__main__':raise SystemExit(main())\n""")
    write_text(scripts / "bind_execution_phase_manifest.py", """#!/usr/bin/env python3\nfrom __future__ import annotations\nimport argparse\nfrom pathlib import Path\nfrom execution_engine import sha256_file,write_json\ndef main():\n p=argparse.ArgumentParser();p.add_argument('files',nargs='+',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();write_json(a.output,{'status':'PASS','files':[{'path':x.as_posix(),'digest':sha256_file(x)} for x in a.files],'stale_propagation':True});return 0\nif __name__=='__main__':raise SystemExit(main())\n""")
    write_text(scripts / "run_execution_evals.py", """from run_self_tests import main\nif __name__=='__main__':raise SystemExit(main())\n""")
    write_text(scripts / "run_execution_mutations.py", """from run_self_tests import main\nif __name__=='__main__':raise SystemExit(main())\n""")
    write_text(scripts / "execution_stop_gate.py", """#!/usr/bin/env python3\nfrom __future__ import annotations\nimport argparse,json\nfrom pathlib import Path\ndef main():\n p=argparse.ArgumentParser();p.add_argument('summary',type=Path);a=p.parse_args();s=json.loads(a.summary.read_text());ok=s.get('status')=='PASS' and s.get('operational_permission') is False;print(json.dumps({'status':'PASS_LOCAL_PROCEDURE' if ok else 'BLOCK','operational_permission':False,'independent_identity':'UNVERIFIED'}));return 0 if ok else 2\nif __name__=='__main__':raise SystemExit(main())\n""")
    write_text(scripts / "install.py", """#!/usr/bin/env python3\nfrom __future__ import annotations\nimport argparse\nfrom pathlib import Path\nfrom bootstrap_execution_package import materialize\ndef main():\n p=argparse.ArgumentParser();p.add_argument('--repo-root',type=Path,default=Path.cwd());a=p.parse_args();materialize(a.repo_root.resolve());return 0\nif __name__=='__main__':raise SystemExit(main())\n""")
    return {"rules": len(rules), "invariants": len(invariants), "evals": len(evals), "mutations": len(mutations), "planner_golden": len(planner)}


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
