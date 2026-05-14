#!/usr/bin/env python3
"""Create a simple XLSX literature matrix from JSON records without dependencies."""

from __future__ import annotations

import argparse
import html
import json
import zipfile
from pathlib import Path


COLUMNS = ["作者年份", "主题", "方法", "样本", "理论", "主要发现", "局限", "对我研究的启发", "下载状态"]

ALIASES = {
    "作者年份": ["作者年份", "author_year", "authorYear"],
    "主题": ["主题", "topic", "theme"],
    "方法": ["方法", "method", "methods"],
    "样本": ["样本", "sample", "samples"],
    "理论": ["理论", "theory", "theories"],
    "主要发现": ["主要发现", "findings", "main_findings", "mainFindings"],
    "局限": ["局限", "limitations", "limitation"],
    "对我研究的启发": ["对我研究的启发", "implications", "research_implications", "inspiration"],
    "下载状态": ["下载状态", "download_status", "downloadStatus", "status"],
}


def cell_ref(col_index: int, row_index: int) -> str:
    letters = ""
    col = col_index
    while col:
        col, rem = divmod(col - 1, 26)
        letters = chr(65 + rem) + letters
    return f"{letters}{row_index}"


def value_for(record: dict, column: str) -> str:
    for key in ALIASES[column]:
        if key in record and record[key] not in (None, ""):
            return str(record[key])
    return "待精读" if column not in ("作者年份", "主题", "下载状态") else ""


def sheet_xml(records: list[dict]) -> str:
    rows = []
    all_rows = [dict(zip(COLUMNS, COLUMNS))]
    for record in records:
        all_rows.append({column: value_for(record, column) for column in COLUMNS})

    for row_index, row in enumerate(all_rows, start=1):
        cells = []
        for col_index, column in enumerate(COLUMNS, start=1):
            value = html.escape(str(row[column]))
            cells.append(f'<c r="{cell_ref(col_index, row_index)}" t="inlineStr"><is><t>{value}</t></is></c>')
        rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    dimension = f"A1:{cell_ref(len(COLUMNS), max(len(all_rows), 1))}"
    col_defs = "".join('<col min="{0}" max="{0}" width="22" customWidth="1"/>'.format(i) for i in range(1, len(COLUMNS) + 1))
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <dimension ref="{dimension}"/>
  <cols>{col_defs}</cols>
  <sheetData>{"".join(rows)}</sheetData>
</worksheet>'''


def write_xlsx(records: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>''')
        zf.writestr("_rels/.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>''')
        zf.writestr("xl/workbook.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets><sheet name="literature_summary" sheetId="1" r:id="rId1"/></sheets>
</workbook>''')
        zf.writestr("xl/_rels/workbook.xml.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>''')
        zf.writestr("xl/worksheets/sheet1.xml", sheet_xml(records))


def main() -> int:
    parser = argparse.ArgumentParser(description="Write literature_summary.xlsx from JSON records.")
    parser.add_argument("--input", required=True, help="JSON file containing an array of records")
    parser.add_argument("--output", required=True, help="Output .xlsx path")
    args = parser.parse_args()

    records = json.loads(Path(args.input).expanduser().read_text(encoding="utf-8"))
    if not isinstance(records, list) or not all(isinstance(item, dict) for item in records):
        raise SystemExit("--input must be a JSON array of objects")
    write_xlsx(records, Path(args.output).expanduser())
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
