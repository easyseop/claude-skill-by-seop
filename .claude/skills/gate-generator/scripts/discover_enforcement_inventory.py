#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from gate_engine import sha256_file, write_json

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('root', type=Path); p.add_argument('--output', type=Path, required=True); a=p.parse_args()
    rows=[]
    for path in sorted(a.root.rglob('*')):
        if path.is_file() and '.git' not in path.parts:
            rows.append({'path':path.relative_to(a.root).as_posix(),'digest':sha256_file(path)})
    write_json(a.output, {'schema_version':'1.0','status':'PASS','files':rows,'host_enforcement':'UNVERIFIED'}); return 0
if __name__=='__main__': raise SystemExit(main())
