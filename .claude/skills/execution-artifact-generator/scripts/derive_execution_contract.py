#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from execution_engine import sha256_file,valid_contract,write_json
def main():
 p=argparse.ArgumentParser();p.add_argument('planner',type=Path);p.add_argument('gate',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();c=valid_contract([f'EXI-{n:03d}' for n in range(1,46)]);c['snapshot']['planner_digest']=sha256_file(a.planner);c['snapshot']['gate_digest']=sha256_file(a.gate);write_json(a.output,c);return 0
if __name__=='__main__':raise SystemExit(main())
