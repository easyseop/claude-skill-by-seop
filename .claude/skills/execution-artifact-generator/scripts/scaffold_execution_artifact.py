#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from execution_engine import scaffold_python_local
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--path',required=True);p.add_argument('--contract-status',required=True);a=p.parse_args();r=scaffold_python_local(a.root,a.path,a.contract_status);print(json.dumps(r));return 0 if r['status']=='STATIC_CHECKED' else 2
if __name__=='__main__':raise SystemExit(main())
