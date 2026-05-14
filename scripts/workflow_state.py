#!/usr/bin/env python3
"""Maintain resumable workflow state for literature download tasks."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


STATE_FILE = "workflow_state.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def state_path(task_dir: str | Path) -> Path:
    return Path(task_dir).expanduser() / STATE_FILE


def load_state(task_dir: str | Path) -> dict:
    path = state_path(task_dir)
    if not path.exists():
        raise SystemExit(f"Missing state file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(task_dir: str | Path, state: dict) -> Path:
    path = state_path(task_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = now()
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def cmd_init(args: argparse.Namespace) -> int:
    databases = [item.strip() for item in args.databases.split(",") if item.strip()]
    state = {
        "schema": "literature-zotero-download.workflow_state.v1",
        "status": "planned",
        "topic": args.topic,
        "target_count": args.target_count,
        "year_range": args.year_range,
        "language_plan": args.language_plan,
        "databases": databases,
        "current_database": databases[0] if databases else "",
        "zotero_collection": args.zotero_collection,
        "human_gates": [],
        "completed_steps": [],
        "next_action": "build_search_plan",
        "created_at": now(),
    }
    path = save_state(args.task_dir, state)
    print(path)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    print(json.dumps(load_state(args.task_dir), ensure_ascii=False, indent=2))
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    state = load_state(args.task_dir)
    if args.status:
        state["status"] = args.status
    if args.current_database:
        state["current_database"] = args.current_database
    if args.next_action:
        state["next_action"] = args.next_action
    if args.completed_step:
        state.setdefault("completed_steps", []).append({"step": args.completed_step, "completed_at": now()})
    print(save_state(args.task_dir, state))
    return 0


def cmd_gate(args: argparse.Namespace) -> int:
    state = load_state(args.task_dir)
    state["status"] = "human_gate"
    gate = {
        "database": args.database or state.get("current_database", ""),
        "gate_type": args.gate_type,
        "url": args.url,
        "message": args.message,
        "next_action": args.next_action,
        "blocked_at": now(),
        "resolved_at": None,
    }
    state.setdefault("human_gates", []).append(gate)
    state["next_action"] = args.next_action
    print(save_state(args.task_dir, state))
    return 0


def cmd_resolve_gate(args: argparse.Namespace) -> int:
    state = load_state(args.task_dir)
    gates = state.setdefault("human_gates", [])
    unresolved = [gate for gate in gates if not gate.get("resolved_at")]
    if not unresolved:
        raise SystemExit("No unresolved human gate found")
    unresolved[-1]["resolved_at"] = now()
    state["status"] = args.status
    if args.next_action:
        state["next_action"] = args.next_action
    print(save_state(args.task_dir, state))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maintain literature workflow state.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create workflow_state.json")
    init.add_argument("--task-dir", required=True)
    init.add_argument("--topic", required=True)
    init.add_argument("--target-count", type=int, default=20)
    init.add_argument("--year-range", default="")
    init.add_argument("--language-plan", default="")
    init.add_argument("--databases", default="")
    init.add_argument("--zotero-collection", default="")
    init.set_defaults(func=cmd_init)

    status = sub.add_parser("status", help="Print workflow state")
    status.add_argument("--task-dir", required=True)
    status.set_defaults(func=cmd_status)

    set_cmd = sub.add_parser("set", help="Update status/current database/next action")
    set_cmd.add_argument("--task-dir", required=True)
    set_cmd.add_argument("--status")
    set_cmd.add_argument("--current-database")
    set_cmd.add_argument("--next-action")
    set_cmd.add_argument("--completed-step")
    set_cmd.set_defaults(func=cmd_set)

    gate = sub.add_parser("gate", help="Record a human verification gate")
    gate.add_argument("--task-dir", required=True)
    gate.add_argument("--database")
    gate.add_argument("--gate-type", required=True)
    gate.add_argument("--url", default="")
    gate.add_argument("--message", default="")
    gate.add_argument("--next-action", required=True)
    gate.set_defaults(func=cmd_gate)

    resolve = sub.add_parser("resolve-gate", help="Mark the latest human gate resolved")
    resolve.add_argument("--task-dir", required=True)
    resolve.add_argument("--status", default="searching")
    resolve.add_argument("--next-action")
    resolve.set_defaults(func=cmd_resolve_gate)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
