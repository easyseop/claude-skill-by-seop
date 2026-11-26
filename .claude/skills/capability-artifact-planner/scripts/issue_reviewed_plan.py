"""Issue a separate design plan after verifying two distinct reviews."""
import argparse
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from audit_capability_plan import audit
from check_capability_plan import check
from common import canonical_json_bytes, sha256_bytes
from derive_contracts import derive

# Installed independently of the checkout by the authority that identifies reviewers.
TRUST = Path("/etc/factory/planner-reviewers")


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_bytes())


def verify_origin(record, signature, trusted_keys):
    attestation = record["attestation"]
    issuer = attestation["issuer"]
    require(isinstance(issuer, str) and re.fullmatch(r"[a-zA-Z0-9_-]{1,128}", issuer), "INVALID_ISSUER")
    key = trusted_keys / (issuer + ".pem")
    require(key.is_file(), "ISSUER_KEY_UNAVAILABLE")
    require(signature and signature.is_file(), "SOURCE_SIGNATURE_MISSING")
    verified = subprocess.run(
        ["/usr/bin/openssl", "dgst", "-sha256", "-verify", str(key), "-signature", str(signature)],
        input=canonical_json_bytes(record), capture_output=True, timeout=10)
    require(verified.returncode == 0, "SOURCE_SIGNATURE_INVALID")
    issued_at = datetime.fromisoformat(attestation["issued_at"].replace("Z", "+00:00"))
    require(issued_at.utcoffset() == timedelta(0) and attestation["read_only"] is True, "INVALID_ATTESTATION")
    return {"issuer": issuer, "key_digest": sha256_bytes(key.read_bytes()),
            "signature_digest": sha256_bytes(signature.read_bytes())}


def issue(args, trusted_keys):
    original = args.draft.read_bytes()
    plan = json.loads(original)
    require(plan["status"] == "DRAFT", "EXPECTED_DRAFT")
    digest = sha256_bytes(canonical_json_bytes(plan))
    machine = check(plan, {"request": args.request, "policy": args.policy, "repo_facts": args.facts})
    require(machine["status"] == "PASS" and read(args.machine) == machine, "MACHINE_CHECK_MISMATCH")
    procedure = read(args.procedural)
    require(procedure == audit(plan) and procedure["status"] == "PASS_LOCAL_PROCEDURE", "PROCEDURAL_AUDIT_MISMATCH")
    for name, expected in derive(plan).items():
        require(read(args.contracts / name) == expected, "STALE_CONTRACT: " + name)

    record = read(args.independent)
    require(record["subject_digest"] == digest and record["raw_file_digest"] == sha256_bytes(original), "SUBJECT_MISMATCH")
    origin = verify_origin(record, args.signature, trusted_keys)
    require(record["actual_independent_executor_ran"] is True and record["status"] == "PASS", "REVIEW_NOT_PASSED")
    require(type(record["blocking_disagreements"]) is int and record["blocking_disagreements"] == 0, "BLOCKING_DISAGREEMENT")
    require(isinstance(record["findings"], list) and all(f["severity"] == "non_blocking" for f in record["findings"]), "UNRESOLVED_FINDING")

    plan["checks_and_evals"].update(machine_check=machine, independent_audit=record)
    plan["issuance"] = dict(origin, draft_subject_digest=digest, draft_raw_digest=sha256_bytes(original),
                            procedural_digest=sha256_bytes(canonical_json_bytes(procedure)),
                            independent_digest=sha256_bytes(canonical_json_bytes(record)),
                            operational_permission=False)
    plan["status"] = "APPROVED_FOR_DESIGN"
    require(check(plan)["status"] == "PASS", "ISSUED_PLAN_INVALID")
    # Publish complete bytes without replacing the draft or any existing output.
    with tempfile.NamedTemporaryFile(dir=args.output.parent) as staging:
        staging.write(canonical_json_bytes(plan) + b"\n")
        staging.flush()
        os.link(staging.name, args.output)


def main(argv, trusted_keys=TRUST):
    parser = argparse.ArgumentParser(description=__doc__)
    for field in ("draft", "request", "policy", "facts", "machine", "procedural", "contracts", "independent", "output"):
        parser.add_argument("--" + field, required=True, type=Path)
    parser.add_argument("--signature", type=Path)
    args = parser.parse_args(argv)
    try:
        issue(args, trusted_keys)
    except (ValueError, KeyError, TypeError, AttributeError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}))
        return 2
    print(json.dumps({"status": "APPROVED_FOR_DESIGN", "output": str(args.output)}))
    return 0
