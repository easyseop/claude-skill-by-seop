#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from gate_engine import stop_gate
payload=json.load(sys.stdin); print(json.dumps(stop_gate(payload.get('result'),payload.get('expected',{})),ensure_ascii=False))
