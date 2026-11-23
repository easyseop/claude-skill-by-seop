#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from gate_engine import sha256_file, valid_contract, write_json

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('capability_plan', type=Path); p.add_argument('--output', type=Path, required=True); a=p.parse_args()
    contract=valid_contract([f'I-{n:03d}' for n in range(1,86)])
    contract['upstream_binding']['capability_plan_digest']=sha256_file(a.capability_plan)
    contract['snapshot']['upstream_digest']=contract['upstream_binding']['capability_plan_digest']
    write_json(a.output, contract); return 0
if __name__=='__main__': raise SystemExit(main())
