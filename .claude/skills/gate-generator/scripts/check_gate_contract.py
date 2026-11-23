#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from gate_engine import read_json, write_json
from gate_validation import comprehensive_check

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('contract',type=Path); p.add_argument('--output',type=Path); a=p.parse_args()
    result=comprehensive_check(read_json(a.contract),[f'I-{n:03d}' for n in range(1,86)])
    if a.output: write_json(a.output,result)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True)); return 0 if result['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
