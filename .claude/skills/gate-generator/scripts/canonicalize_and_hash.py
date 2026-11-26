#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from gate_engine import read_json, sha256_value, write_json

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('input',type=Path); p.add_argument('--output',type=Path); a=p.parse_args()
    result={'schema_version':'1.0','status':'PASS','digest':sha256_value(read_json(a.input))}
    if a.output: write_json(a.output,result)
    print(json.dumps(result,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
