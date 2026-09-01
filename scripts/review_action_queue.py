#!/usr/bin/env python3
"""Inspect and acknowledge durable LifeOS review actions."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


DEFAULT_LOCAL_QUEUE = Path(".runtime/review-actions.ndjson")
DEFAULT_APP_QUEUE = Path(
    "/Users/wuyanyu/Library/Application Support/LifeOS-AI/review-actions.ndjson"
)
DEFAULT_CURSOR = Path(".runtime/review-actions-cursor.json")


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def read_actions(path: Path) -> list[dict]:
    if not path.exists():
        return []
    actions = []
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not raw_line.strip():
            continue
        try:
            payload = json.loads(raw_line)
        except json.JSONDecodeError as error:
            raise ValueError(f"invalid JSON at {path}:{line_number}: {error}") from error
        actions.append(
            {"source": str(path.resolve()), "line": line_number, "payload": payload}
        )
    return actions


def pending_actions(
    sources: list[Path], cursor_path: Path, limit: int | None = None
) -> list[dict]:
    cursor = load_json(cursor_path, {"sources": {}})
    pending = []
    for source in sources:
        resolved = str(source.resolve())
        consumed = int(cursor.get("sources", {}).get(resolved, 0))
        pending.extend(
            action for action in read_actions(source) if action["line"] > consumed
        )
    pending.sort(key=lambda item: (item["payload"].get("created_at", ""), item["source"]))
    return pending[:limit] if limit else pending


def acknowledge_action(cursor_path: Path, source: Path, line: int) -> dict:
    source = source.resolve()
    actions = read_actions(source)
    by_line = {action["line"]: action for action in actions}
    if line not in by_line:
        raise ValueError(f"action line does not exist: {source}:{line}")

    cursor = load_json(cursor_path, {"sources": {}})
    sources = cursor.setdefault("sources", {})
    current = int(sources.get(str(source), 0))
    if line <= current:
        return {"changed": False, "reason": "already_acknowledged", "cursor": current}
    if line != current + 1:
        raise ValueError(
            f"cannot skip actions for {source}: current cursor is {current}, requested {line}"
        )

    action = by_line[line]["payload"]
    sources[str(source)] = line
    cursor["last_consumed_message_id"] = action.get("message_id")
    cursor["last_consumed_action"] = action.get("action")
    cursor["last_consumed_entry_key"] = action.get("entry_key")
    atomic_write_json(cursor_path, cursor)
    return {"changed": True, "cursor": line, "action": action}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cursor", type=Path, default=DEFAULT_CURSOR)
    parser.add_argument(
        "--source", type=Path, action="append", dest="sources", default=[]
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    pending = subparsers.add_parser("pending")
    pending.add_argument("--limit", type=int)
    acknowledge = subparsers.add_parser("ack")
    acknowledge.add_argument("--queue", type=Path, required=True)
    acknowledge.add_argument("--line", type=int, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    sources = args.sources or [DEFAULT_LOCAL_QUEUE, DEFAULT_APP_QUEUE]
    try:
        if args.command == "pending":
            for action in pending_actions(sources, args.cursor, args.limit):
                print(json.dumps(action, ensure_ascii=False))
        else:
            print(
                json.dumps(
                    acknowledge_action(args.cursor, args.queue, args.line),
                    ensure_ascii=False,
                )
            )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
