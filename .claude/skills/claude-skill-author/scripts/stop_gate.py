#!/usr/bin/env python3
"""Optional Stop hook gate for an active claude-skill-author run.

Install via the provided settings.stop-hook.example.json only after reviewing it.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        hook_input = {}
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()
    active_path = project / ".claude" / "skill-authoring" / ".active.json"
    if not active_path.exists():
        return 0
    try:
        active = json.loads(active_path.read_text(encoding="utf-8"))
    except Exception:
        return 0
    mode = str(active.get("mode", "full")).lower()
    phase_upper = str(active.get("phase", "SPEC")).upper()
    status = str(active.get("status", "IN_PROGRESS")).upper()
    required_final_phase = {"spec": "SPEC", "build": "BUILD", "audit": "AUDIT", "full": "AUDIT"}.get(mode, "AUDIT")
    if status == "PASS" and phase_upper == required_final_phase:
        return 0
    target = active.get("target")
    phase = phase_upper.lower()
    if phase not in {"spec", "build", "audit"}:
        phase = "spec"
    validator = project / ".claude" / "skills" / "claude-skill-author" / "scripts" / "validate_authoring.py"
    if not target or not validator.exists():
        return 0
    proc = subprocess.run(
        [sys.executable, str(validator), "--project-root", str(project), "--target", str(target), "--phase", phase],
        text=True,
        capture_output=True,
    )
    if proc.returncode == 0:
        if phase_upper != required_final_phase:
            reason = (
                f"{mode} 모드는 {required_final_phase} 단계 PASS까지 완료해야 합니다. "
                f"현재 {phase_upper} 검증만 통과했습니다. 다음 단계를 계속 수행하십시오."
            )
            print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
            return 0
        return 0
    reason = proc.stdout[-5000:] or proc.stderr[-5000:] or "authoring validation failed"
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
