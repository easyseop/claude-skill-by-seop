#!/usr/bin/env python3
"""Bounded, read-only repository discovery for planner inputs."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from common import find_repo_root, sha256_file, stable_relative, write_json


DEFAULT_ROOTS = [
    ".claude/skills",
    ".claude/agents",
    ".claude/commands",
    ".claude/rules",
    ".github/workflows",
    "scripts",
    "tests",
    "docs",
]
MAX_FILES = 5000
MAX_HASH_BYTES = 2 * 1024 * 1024


def classify(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".py", ".js", ".ts", ".java", ".sh", ".sql"}:
        return "source"
    if suffix in {".json", ".yaml", ".yml", ".toml", ".ini"}:
        return "config"
    if suffix in {".md", ".rst", ".txt"}:
        return "document"
    return "other"


def discover(repo_root: Path) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    truncated = False
    for relative_root in DEFAULT_ROOTS:
        root = repo_root / relative_root
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(
                item for item in dirnames if item not in {".git", "node_modules", ".venv", "__pycache__"}
            )
            for filename in sorted(filenames):
                path = Path(dirpath) / filename
                if path.is_symlink():
                    link_target = os.readlink(path)
                    files.append(
                        {
                            "path": stable_relative(path, repo_root),
                            "kind": "symlink",
                            "target": link_target,
                        }
                    )
                    continue
                try:
                    stat = path.stat()
                except OSError:
                    continue
                entry: dict[str, Any] = {
                    "path": stable_relative(path, repo_root),
                    "kind": classify(path),
                    "size": stat.st_size,
                }
                if stat.st_size <= MAX_HASH_BYTES:
                    try:
                        entry["digest"] = sha256_file(path)
                    except OSError:
                        entry["digest_status"] = "UNREADABLE"
                else:
                    entry["digest_status"] = "SKIPPED_OVERSIZE"
                files.append(entry)
                if len(files) >= MAX_FILES:
                    truncated = True
                    break
            if truncated:
                break
        if truncated:
            break

    return {
        "schema_version": "1.0",
        "repository_root": repo_root.as_posix(),
        "scan_policy": {
            "roots": DEFAULT_ROOTS,
            "max_files": MAX_FILES,
            "max_hash_bytes": MAX_HASH_BYTES,
            "read_only": True,
        },
        "truncated": truncated,
        "file_count": len(files),
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo_root = (args.repo_root or find_repo_root()).resolve()
    write_json(args.output, discover(repo_root))
    print(f"PASS wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
