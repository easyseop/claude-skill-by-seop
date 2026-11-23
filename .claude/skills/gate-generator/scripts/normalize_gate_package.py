#!/usr/bin/env python3
"""Normalize generated Gate package entrypoints after materialization."""

from __future__ import annotations

import argparse
from pathlib import Path


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def normalize(repo_root: Path) -> None:
    scripts = repo_root / ".claude/skills/gate-generator/scripts"
    write(scripts / "check_gate_contract.py", '''#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from gate_engine import read_json, write_json
from gate_validation import comprehensive_check

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('contract',type=Path); p.add_argument('--output',type=Path); a=p.parse_args()
    result=comprehensive_check(read_json(a.contract),[f'I-{n:03d}' for n in range(1,86)])
    if a.output: write_json(a.output,result)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True)); return 0 if result['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
''')
    write(scripts / "canonicalize_and_hash.py", '''#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from gate_engine import read_json, sha256_value, write_json

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('input',type=Path); p.add_argument('--output',type=Path); a=p.parse_args()
    result={'schema_version':'1.0','status':'PASS','digest':sha256_value(read_json(a.input))}
    if a.output: write_json(a.output,result)
    print(json.dumps(result,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
''')
    write(scripts / "install.py", '''#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from bootstrap_gate_package import materialize
from normalize_gate_package import normalize

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('--repo-root',type=Path,default=Path.cwd()); a=p.parse_args(); root=a.repo_root.resolve(); materialize(root); normalize(root); return 0
if __name__=='__main__': raise SystemExit(main())
''')


def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('--repo-root',type=Path,default=Path.cwd()); a=p.parse_args(); normalize(a.repo_root.resolve()); return 0


if __name__=='__main__':
    raise SystemExit(main())
