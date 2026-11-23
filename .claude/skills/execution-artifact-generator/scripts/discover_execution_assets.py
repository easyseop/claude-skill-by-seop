#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from execution_engine import sha256_file,write_json
def main():
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();rows=[]
 for x in sorted(a.root.rglob('*')):
  if x.is_file() and '.git' not in x.parts: rows.append({'path':x.relative_to(a.root).as_posix(),'digest':sha256_file(x)})
 write_json(a.output,{'status':'COMPLETE_BOUNDED','candidates':rows,'executed_candidates':False});return 0
if __name__=='__main__':raise SystemExit(main())
