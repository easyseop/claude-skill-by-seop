#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('summary',type=Path);a=p.parse_args();s=json.loads(a.summary.read_text());ok=s.get('status')=='PASS' and s.get('operational_permission') is False;print(json.dumps({'status':'PASS_LOCAL_PROCEDURE' if ok else 'BLOCK','operational_permission':False,'independent_identity':'UNVERIFIED'}));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
