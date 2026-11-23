#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from bootstrap_execution_package import materialize
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo-root',type=Path,default=Path.cwd());a=p.parse_args();materialize(a.repo_root.resolve());return 0
if __name__=='__main__':raise SystemExit(main())
