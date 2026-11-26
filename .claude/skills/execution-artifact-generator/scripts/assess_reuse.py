#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from execution_engine import decide_execution,read_json,write_json
def main():
 p=argparse.ArgumentParser();p.add_argument('request',type=Path);p.add_argument('facts',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=decide_execution(read_json(a.request),read_json(a.facts));write_json(a.output,r);print(json.dumps(r));return 0
if __name__=='__main__':raise SystemExit(main())
