#!/usr/bin/env python3
"""Validate that a downloaded file is a plausible PDF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate_pdf(path: Path, min_bytes: int, expected_title: str | None) -> dict:
    result = {
        "path": str(path),
        "exists": path.exists(),
        "valid_pdf": False,
        "size_bytes": 0,
        "page_markers": 0,
        "warnings": [],
    }
    if not path.exists():
        result["warnings"].append("file_missing")
        return result
    if path.is_dir():
        result["warnings"].append("path_is_directory")
        return result

    data = path.read_bytes()
    result["size_bytes"] = len(data)

    head = data[:2048].lstrip()
    if not head.startswith(b"%PDF-"):
        lower_head = head[:512].lower()
        if b"<html" in lower_head or b"<!doctype html" in lower_head:
            result["warnings"].append("html_instead_of_pdf")
        else:
            result["warnings"].append("missing_pdf_header")
        return result

    if len(data) < min_bytes:
        result["warnings"].append("file_too_small")

    if b"%%EOF" not in data[-4096:]:
        result["warnings"].append("missing_eof_marker")

    result["page_markers"] = data.count(b"/Type /Page")

    if expected_title:
        compact_expected = "".join(expected_title.lower().split())
        decoded = data[: min(len(data), 250_000)].decode("utf-8", errors="ignore").lower()
        compact_decoded = "".join(decoded.split())
        if compact_expected and compact_expected not in compact_decoded:
            result["warnings"].append("expected_title_not_found_in_sample")

    fatal = {"html_instead_of_pdf", "missing_pdf_header", "file_missing", "path_is_directory"}
    result["valid_pdf"] = not fatal.intersection(result["warnings"])
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a downloaded PDF.")
    parser.add_argument("pdf_path")
    parser.add_argument("--expected-title")
    parser.add_argument("--min-bytes", type=int, default=1024)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate_pdf(Path(args.pdf_path).expanduser(), args.min_bytes, args.expected_title)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "valid" if result["valid_pdf"] else "invalid"
        warnings = ", ".join(result["warnings"]) if result["warnings"] else "none"
        print(f"{status}: {result['path']} ({result['size_bytes']} bytes; warnings: {warnings})")
    return 0 if result["valid_pdf"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
