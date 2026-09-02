#!/usr/bin/env python3
"""Optional Stop-hook gate for an active claude-skill-author v1.3 run."""
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
    if hook_input.get("stop_hook_active") is True:
        return 0

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()
    active_path = project / ".claude" / "skill-authoring" / ".active.json"
    if not active_path.exists():
        return 0
    try:
        active = json.loads(active_path.read_text(encoding="utf-8"))
    except Exception:
        return 0

    mode = str(active.get("mode", "full")).lower()
    required_phase = {
        "design": "design", "spec": "spec", "build": "build", "audit": "audit", "full": "audit",
    }.get(mode, "audit")
    target = active.get("target")
    validator = project / ".claude" / "skills" / "claude-skill-author" / "scripts" / "validate_authoring.py"
    if not target or not validator.exists():
        return 0

    # Always rerun the required final phase. This checks stale fingerprints and
    # never trusts a previous PASS marker by itself.
    proc = subprocess.run(
        [sys.executable, str(validator), "--project-root", str(project), "--target", str(target), "--phase", required_phase],
        text=True,
        capture_output=True,
    )
    if proc.returncode == 0:
        return 0
    reason = proc.stdout[-12000:] or proc.stderr[-12000:] or "authoring validation failed"
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
