#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from execution_engine import validate_generated_source
def main():
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--path',required=True);a=p.parse_args();r=validate_generated_source(a.source.read_text(),a.path);print(json.dumps(r));return 0 if r['status']=='STATIC_CHECKED' else 2
if __name__=='__main__':raise SystemExit(main())
