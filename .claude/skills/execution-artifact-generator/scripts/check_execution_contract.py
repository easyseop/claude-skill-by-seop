#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from execution_engine import check_contract,read_json,write_json
def main():
 p=argparse.ArgumentParser();p.add_argument('contract',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();r=check_contract(read_json(a.contract),[f'EXI-{n:03d}' for n in range(1,46)]);
 if a.output:write_json(a.output,r)
 print(json.dumps(r,ensure_ascii=False,sort_keys=True));return 0 if r['status']=='PASS' else 2
if __name__=='__main__':raise SystemExit(main())
