#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from execution_engine import read_json,write_json
def main():
 p=argparse.ArgumentParser();p.add_argument('contract',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();c=read_json(a.contract);t=c.get('traceability',{});f=t.get('forward',[]);r=t.get('reverse',[]);known=set(t.get('known_entrypoints',[]));rev={x.get('entrypoint') for x in r};bad=[x for x in known if x not in rev];result={'status':'FAIL' if bad else 'PASS','forward':len(f),'reverse':len(r),'orphan_entrypoints':bad};
 if a.output:write_json(a.output,result)
 print(json.dumps(result));return 0 if not bad else 2
if __name__=='__main__':raise SystemExit(main())
