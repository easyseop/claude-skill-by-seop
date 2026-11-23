#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from bootstrap_gate_package import materialize
from normalize_gate_package import normalize

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('--repo-root',type=Path,default=Path.cwd()); a=p.parse_args(); root=a.repo_root.resolve(); materialize(root); normalize(root); return 0
if __name__=='__main__': raise SystemExit(main())
