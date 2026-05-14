#!/usr/bin/env python3
"""Append structured literature workflow records to CSV logs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_FIELDS = {
    "search_results": [
        "paper_id",
        "title",
        "authors",
        "year",
        "doi",
        "source_database",
        "url",
        "abstract",
        "citation_count",
        "query_used",
        "retrieved_at",
    ],
    "download_log": [
        "paper_id",
        "title",
        "doi",
        "source_database",
        "download_method_tried",
        "download_status",
        "pdf_path",
        "failure_reason",
        "next_action",
        "requires_user_action",
        "retried_count",
    ],
    "zotero_import_log": [
        "paper_id",
        "title",
        "doi",
        "zotero_status",
        "zotero_item_key",
        "zotero_collection",
        "attachment_status",
        "pdf_attached",
        "duplicate_status",
        "import_error",
    ],
}


def infer_kind(path: Path) -> str:
    stem = path.stem.lower()
    for kind in DEFAULT_FIELDS:
        if kind in stem:
            return kind
    return "download_log"


def append_record(path: Path, record: dict, fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerow({field: record.get(field, "") for field in fields})


def main() -> int:
    parser = argparse.ArgumentParser(description="Append one record to a literature CSV log.")
    parser.add_argument("--log", required=True, help="CSV log path")
    parser.add_argument("--kind", choices=sorted(DEFAULT_FIELDS), help="Log schema")
    parser.add_argument("--record-json", required=True, help="JSON object to append")
    parser.add_argument("--fields", help="Comma-separated custom field order")
    args = parser.parse_args()

    path = Path(args.log).expanduser()
    record = json.loads(args.record_json)
    if not isinstance(record, dict):
        raise SystemExit("--record-json must be a JSON object")

    if args.fields:
        fields = [field.strip() for field in args.fields.split(",") if field.strip()]
    else:
        fields = DEFAULT_FIELDS[args.kind or infer_kind(path)]
    append_record(path, record, fields)
    print(str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
