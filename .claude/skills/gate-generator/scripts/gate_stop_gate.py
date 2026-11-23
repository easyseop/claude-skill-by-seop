#!/usr/bin/env python3
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
