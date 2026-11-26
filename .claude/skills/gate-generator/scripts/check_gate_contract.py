#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from derive_gate_contract import check_current, load_plan
from gate_engine import read_json, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    parser.add_argument("--planner", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = check_current(read_json(args.contract), *load_plan(args.planner))
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
        result = {"status": "FAIL", "failures": {"I-005": str(exc)}}
    if args.output:
        write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
