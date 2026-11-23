#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from gate_engine import posttool_gate
payload=json.load(sys.stdin); print(json.dumps(posttool_gate(payload),ensure_ascii=False))
