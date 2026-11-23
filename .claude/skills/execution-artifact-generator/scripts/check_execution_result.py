#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('result',type=Path);a=p.parse_args();r=json.loads(a.result.read_text());ok=isinstance(r,dict) and r.get('status') not in {'ERROR','STALE','OUTCOME_UNKNOWN','WAIVED'} and r.get('operational_permission') is False;print(json.dumps({'status':'PASS' if ok else 'BLOCK'}));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
