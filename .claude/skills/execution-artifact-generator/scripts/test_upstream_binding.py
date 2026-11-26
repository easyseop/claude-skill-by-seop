"""Exercise the two compiler/checker CLIs against independent current inputs."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

EXEC = Path(__file__).resolve().parent
GATE = EXEC.parents[1] / "gate-generator" / "scripts"


class ConnectionTest(unittest.TestCase):
    def call(self, script, *args, success=True):
        result = subprocess.run([sys.executable, script, *args], cwd=self.root,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0 if success else 2, result.stderr or result.stdout)

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.plan = {"plan_id": "connection-case-57", "status": "VERIFIED_LOCAL_CANDIDATE",
                     "architecture": {"control_mode": "bounded_agent",
                                      "selected_components": [{"type": "validator"}, {"type": "tool"}]}}
        self.save("plan", self.plan)
        self.call(GATE / "derive_gate_contract.py", "plan", "--output", "gate")
        self.call(EXEC / "derive_execution_contract.py", "plan", "gate", "--output", "exec")

    def save(self, name, value):
        (self.root / name).write_text(json.dumps(value))

    def read(self, name):
        return json.loads((self.root / name).read_bytes())

    def gate(self, success):
        self.call(GATE / "check_gate_contract.py", "gate", "--planner", "plan", success=success)

    def execution(self, success):
        self.call(EXEC / "check_execution_contract.py", "exec", "--planner", "plan", "--gate", "gate", success=success)

    def test_matching_inputs(self):
        self.gate(True)
        self.execution(True)
        gate, execution = self.read("gate"), self.read("exec")
        self.assertEqual(gate["upstream_binding"]["capability_plan_id"], self.plan["plan_id"])
        self.assertEqual(execution["planner_binding"]["selected_components"], ["validator", "tool"])
        self.assertEqual(execution["planner_binding"]["control_mode"], "bounded_agent")
        for key, name in [("planner_digest", "plan"), ("gate_digest", "gate")]:
            self.assertEqual(execution["snapshot"][key], "sha256:" + hashlib.sha256((self.root / name).read_bytes()).hexdigest())

    def test_changed_planner(self):
        self.save("plan", dict(self.plan, plan_id="different"))
        self.gate(False)
        self.execution(False)
        self.call(EXEC / "derive_execution_contract.py", "plan", "gate", "--output", "other", success=False)

    def test_changed_gate_bytes(self):
        with (self.root / "gate").open("a") as handle:
            handle.write("\n")
        self.gate(True)
        self.execution(False)

    def test_resealed_wrong_identity(self):
        for name, key, field, check in [("gate", "upstream_binding", "capability_plan_id", self.gate),
                                         ("exec", "planner_binding", "plan_id", self.execution)]:
            changed = self.read(name)
            changed[key][field] = "substituted"
            del changed["contract_digest"]
            raw = json.dumps(changed, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode()
            changed["contract_digest"] = "sha256:" + hashlib.sha256(raw).hexdigest()
            self.save(name, changed)
            check(False)
            if name == "gate":
                self.call(GATE / "derive_gate_contract.py", "plan", "--output", "gate")

    def test_draft_is_ineligible(self):
        self.save("plan", dict(self.plan, status="DRAFT"))
        self.call(GATE / "derive_gate_contract.py", "plan", "--output", "gate")
        self.gate(False)
        self.call(EXEC / "derive_execution_contract.py", "plan", "gate", "--output", "other", success=False)


if __name__ == "__main__":
    unittest.main()
