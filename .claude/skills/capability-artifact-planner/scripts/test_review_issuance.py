"""Exercise issuance with ephemeral test identities only."""
import json
import subprocess
import tempfile
from pathlib import Path
from unittest import TestCase, main

from audit_capability_plan import audit
from check_capability_plan import check
from common import canonical_json_bytes, sha256_bytes, sha256_file, write_json
from derive_contracts import derive
from issue_reviewed_plan import main as issue_cli
from planner_stop_gate import decide
from run_self_tests import valid_plan


class Issuance(TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.files = {k: self.root / k for k in ("draft", "request", "policy", "facts", "machine", "procedural", "independent", "signature", "output")}
        self.files["contracts"] = self.root / "contracts"
        inputs = {k: self.files[k] for k in ("request", "policy")}
        inputs["repo_facts"] = self.files["facts"]
        for k, path in inputs.items():
            path.write_text(k)
        plan = valid_plan({k: sha256_file(p) for k, p in inputs.items()})
        self.save("draft", plan)
        self.save("machine", check(plan, inputs))
        proc = audit(plan)
        self.save("procedural", proc)
        for name, value in derive(plan).items():
            write_json(self.files["contracts"] / name, value)
        self.record = {"status": "PASS", "actual_independent_executor_ran": True, "blocking_disagreements": 0,
                       "raw_file_digest": sha256_file(self.files["draft"]), "subject_digest": proc["subject_digest"],
                       "findings": [], "attestation": {"issuer": "test-reviewer", "read_only": True, "issued_at": "2026-01-01T00:00:00Z"}}
        self.openssl("genrsa", "-out", "private", "2048")
        self.openssl("rsa", "-in", "private", "-pubout", "-out", "test-reviewer.pem")
        self.sign()

    def save(self, key, value):
        write_json(self.files[key], value)

    def openssl(self, *args, data=None):
        subprocess.run(["/usr/bin/openssl", *args], cwd=self.root, input=data, capture_output=True, check=True)

    def sign(self):
        self.save("independent", self.record)
        self.openssl("dgst", "-sha256", "-sign", "private", "-out", "signature", data=canonical_json_bytes(self.record))

    def run_cli(self):
        argv = [s for k, path in self.files.items() for s in ("--" + k, str(path))]
        return issue_cli(argv, self.root)

    def rejected(self):
        self.assertEqual(self.run_cli(), 2)
        self.assertFalse(self.files["output"].exists())

    def test_matching(self):
        self.assertEqual(self.run_cli(), 0)
        issued = json.loads(self.files["output"].read_bytes())
        self.assertEqual(issued["status"], "APPROVED_FOR_DESIGN")
        self.assertEqual(issued["issuance"]["draft_raw_digest"], sha256_file(self.files["draft"]))
        self.assertEqual(check(issued)["status"], "PASS")
        before = self.files["output"].read_bytes()
        self.assertEqual(self.run_cli(), 2)
        self.assertEqual(before, self.files["output"].read_bytes())

    def test_other_plan(self):
        self.record["subject_digest"] = sha256_bytes(b"other")
        self.sign()
        self.rejected()

    def test_wrong_issuer(self):
        self.record["attestation"]["issuer"] = "unregistered"
        self.sign()
        self.rejected()

    def test_wrong_signature(self):
        self.files["signature"].write_bytes(b"invalid")
        self.rejected()

    def test_blocking(self):
        self.record["blocking_disagreements"] = 1
        self.sign()
        self.rejected()

    def test_missing(self):
        for name in ("signature", "procedural", "independent"):
            path = self.files[name]
            original = path.read_bytes()
            path.unlink()
            self.rejected()
            path.write_bytes(original)

    def test_procedural_only(self):
        machine = json.loads(self.files["machine"].read_bytes())
        proc = json.loads(self.files["procedural"].read_bytes())
        self.assertEqual(decide(machine, proc, [])["status"], "PASS_LOCAL_PROCEDURE")
        proc["independence"]["actual_independent_executor_ran"] = True
        self.assertEqual(decide(machine, proc, [])["status"], "PASS_LOCAL_PROCEDURE")

    def test_review_conditions(self):
        for field, value in [("status", "FAIL"), ("actual_independent_executor_ran", False),
                             ("findings", [{"severity": "blocking"}])]:
            old = self.record[field]
            self.record[field] = value
            self.sign()
            self.rejected()
            self.record[field] = old
        self.record["attestation"]["read_only"] = False
        self.sign()
        self.rejected()


if __name__ == "__main__":
    main()
