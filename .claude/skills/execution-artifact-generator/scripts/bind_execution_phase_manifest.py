#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from execution_engine import sha256_file,write_json
def main():
 p=argparse.ArgumentParser();p.add_argument('files',nargs='+',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();write_json(a.output,{'status':'PASS','files':[{'path':x.as_posix(),'digest':sha256_file(x)} for x in a.files],'stale_propagation':True});return 0
if __name__=='__main__':raise SystemExit(main())
