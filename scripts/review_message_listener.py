#!/usr/bin/env python3
"""Listen for Feishu review commands and persist deterministic review actions."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


COMMAND_RE = re.compile(
    r"^(通过|修改)\s+(\d{4}-\d{2}-\d{2}(?:-\d+)?)\s+"
    r"(标准解析稿|视频脚本|公众号文章)(?:[：:]\s*(.+))?$"
)
STAGE_KEYS = {
    "标准解析稿": "parsed_note",
    "视频脚本": "video_script",
    "公众号文章": "wechat_article",
}


def parse_review_command(content: str) -> dict[str, str] | None:
    match = COMMAND_RE.match(content.strip())
    if not match:
        return None
    decision, entry_key, label, comment = match.groups()
    if decision == "修改" and not comment:
        return None
    return {
        "decision": "approved" if decision == "通过" else "changes_requested",
        "entry_key": entry_key,
        "stage": STAGE_KEYS[label],
        "comment": (comment or "").strip(),
    }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write_json(path: Path, value: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def find_review_state(entries_dir: Path, entry_key: str) -> Path | None:
    exact = entries_dir / f"{entry_key}-daily-reflection" / "review-state.json"
    return exact if exact.exists() else None


def apply_review_command(
    state_path: Path, command: dict[str, str], reviewer_open_id: str
) -> dict:
    state = load_json(state_path)
    stage = command["stage"]
    stage_state = state[stage]
    decision = command["decision"]

    if stage_state["status"] == decision:
        return {"changed": False, "action": "duplicate_review"}

    if stage_state["status"] not in {"pending_review", "changes_requested"}:
        return {"changed": False, "action": "invalid_transition"}

    stage_state["status"] = decision
    stage_state["reviewer_open_id"] = reviewer_open_id
    stage_state["reviewed_at"] = utc_now()
    stage_state["review_comment"] = command["comment"] or None

    if stage == "parsed_note":
        state["pipeline_status"] = (
            "generating_derivatives"
            if decision == "approved"
            else "parsed_changes_requested"
        )
        action = (
            "generate_derivatives"
            if decision == "approved"
            else "revise_parsed_note"
        )
    else:
        if decision == "changes_requested":
            state["pipeline_status"] = "derivatives_pending_review"
            action = f"revise_{stage}"
        elif (
            state["video_script"]["status"] == "approved"
            and state["wechat_article"]["status"] == "approved"
        ):
            state["pipeline_status"] = "completed"
            action = "complete_entry"
        else:
            state["pipeline_status"] = "derivatives_pending_review"
            action = "wait_for_sibling_review"

    atomic_write_json(state_path, state)
    return {"changed": True, "action": action, "state": state}


def append_action(actions_path: Path, payload: dict) -> None:
    actions_path.parent.mkdir(parents=True, exist_ok=True)
    with actions_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def handle_event(
    event: dict,
    entries_dir: Path,
    actions_path: Path,
    reviewer_open_id: str,
) -> dict | None:
    if event.get("type") != "im.message.receive_v1":
        return None
    if event.get("sender_id") != reviewer_open_id:
        return {"ignored": "unauthorized_sender"}

    command = parse_review_command(str(event.get("content", "")))
    if not command:
        return {"ignored": "not_a_review_command"}

    state_path = find_review_state(entries_dir, command["entry_key"])
    if not state_path:
        return {"ignored": "entry_not_found", "entry_key": command["entry_key"]}

    result = apply_review_command(state_path, command, reviewer_open_id)
    if result.get("changed"):
        append_action(
            actions_path,
            {
                "created_at": utc_now(),
                "entry_key": command["entry_key"],
                "stage": command["stage"],
                "decision": command["decision"],
                "comment": command["comment"],
                "action": result["action"],
                "message_id": event.get("message_id"),
            },
        )
    return result


def run_listener(args: argparse.Namespace) -> int:
    config = load_json(args.config)
    reviewer_open_id = config["reviewer_open_id"]
    command = [
        "lark-cli",
        "event",
        "+subscribe",
        "--profile",
        config.get("profile", "siyangyuan-tiantu"),
        "--as",
        "bot",
        "--event-types",
        "im.message.receive_v1",
        "--compact",
        "--quiet",
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        text=True,
        bufsize=1,
    )
    assert process.stdout is not None
    for line in process.stdout:
        try:
            event = json.loads(line)
            result = handle_event(
                event, args.entries_dir, args.actions_path, reviewer_open_id
            )
            if result:
                print(json.dumps(result, ensure_ascii=False), flush=True)
        except (json.JSONDecodeError, KeyError, OSError) as error:
            print(f"listener_error: {error}", file=sys.stderr, flush=True)
    return process.wait()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", type=Path, default=Path(".runtime/review-listener-config.json")
    )
    parser.add_argument("--entries-dir", type=Path, default=Path("entries"))
    parser.add_argument(
        "--actions-path", type=Path, default=Path(".runtime/review-actions.ndjson")
    )
    return parser


if __name__ == "__main__":
    raise SystemExit(run_listener(build_parser().parse_args()))
