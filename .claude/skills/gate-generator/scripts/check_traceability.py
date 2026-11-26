#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from gate_engine import read_json, write_json

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('contract', type=Path); p.add_argument('--output', type=Path); a=p.parse_args(); c=read_json(a.contract)
    failures=[]
    inventory={x.get('gate_id'):x for x in c.get('implementation_inventory',[])}
    for gate in c.get('gates',[]):
        if gate.get('id') not in inventory or not gate.get('test_ids') or not gate.get('evidence_refs'): failures.append(gate.get('id'))
    result={'schema_version':'1.0','status':'FAIL' if failures else 'PASS','forward':len(c.get('gates',[])),'reverse':len(inventory),'failures':failures}
    if a.output: write_json(a.output,result)
    print(json.dumps(result,ensure_ascii=False)); return 0 if not failures else 2
if __name__=='__main__': raise SystemExit(main())
