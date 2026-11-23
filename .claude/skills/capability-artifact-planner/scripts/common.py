#!/usr/bin/env python3
"""Shared deterministic utilities for Capability & Artifact Planner."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable


class PlannerError(RuntimeError):
    """Raised for a blocking planner validation error."""


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".claude").exists() or (candidate / ".git").exists():
            return candidate
    raise PlannerError(f"repository root not found from {current}")


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_json_text(value: Any) -> str:
    return canonical_json_bytes(value).decode("utf-8") + "\n"


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PlannerError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PlannerError(f"invalid canonical JSON in {path}: {exc}") from exc


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(canonical_json_text(value), encoding="utf-8")
    os.replace(temp, path)


def require_exact_ids(items: Iterable[dict[str, Any]], prefix: str, start: int, end: int) -> list[str]:
    ids = [str(item.get("id", "")) for item in items]
    width = max(2, len(str(end)))
    expected = [f"{prefix}-{number:0{width}d}" for number in range(start, end + 1)]
    if ids != expected:
        missing = [item for item in expected if item not in ids]
        extra = [item for item in ids if item not in expected]
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        raise PlannerError(
            f"{prefix} catalog mismatch: count={len(ids)} expected={len(expected)} "
            f"missing={missing} extra={extra} duplicates={duplicates}"
        )
    return ids


def catalog_dir(repo_root: Path) -> Path:
    return repo_root / "docs/agent-authoring/workstreams/upstream-recovery/inputs"


def planner_dir(repo_root: Path) -> Path:
    return repo_root / ".claude/skills/capability-artifact-planner"


def stable_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()
