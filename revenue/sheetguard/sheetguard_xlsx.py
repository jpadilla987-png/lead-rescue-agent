#!/usr/bin/env python3
"""SheetGuard XLSX pre-flight checker.

Reads the first worksheet from a standard .xlsx file using only Python's
standard library. It reports duplicate identifier values, exact duplicate rows,
and likely duplicate submissions whose non-identifier fields are identical.

This is a screening tool, not an automatic deletion tool. Every flag should be
reviewed by a human before an order is changed or removed.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "p": "http://schemas.openxmlformats.org/package/2006/relationships"}

ID_HEADER_PATTERNS = (
    r"^po$", r"^po\s*(number|no|#)$", r"purchase\s*order", r"order\s*(id|number|no|#)",
    r"^order$", r"invoice\s*(id|number|no|#)", r"reference\s*(id|number|no|#)",
)


def _norm(v: object) -> str:
    if v is None:
        return ""
    s = str(v).strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def _col_index(cell_ref: str) -> int:
    letters = re.match(r"([A-Z]+)", cell_ref.upper())
    if not letters:
        return 0
    n = 0
    for ch in letters.group(1):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def _shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall("m:si", NS):
        parts = [t.text or "" for t in si.findall(".//m:t", NS)]
        out.append("".join(parts))
    return out


def _first_sheet_path(zf: zipfile.ZipFile) -> str:
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    sheet = wb.find("m:sheets/m:sheet", NS)
    if sheet is None:
        raise ValueError("Workbook has no worksheets")
    rid = sheet.attrib.get(f"{{{NS['r']}}}id")
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    target = None
    for rel in rels.findall("p:Relationship", NS):
        if rel.attrib.get("Id") == rid:
            target = rel.attrib.get("Target")
            break
    if not target:
        raise ValueError("Could not resolve first worksheet")
    if target.startswith("/"):
        target = target.lstrip("/")
    elif not target.startswith("xl/"):
        target = "xl/" + target
    return target


def read_first_sheet(path: str | Path) -> list[list[str]]:
    with zipfile.ZipFile(path) as zf:
        shared = _shared_strings(zf)
        sheet_path = _first_sheet_path(zf)
        root = ET.fromstring(zf.read(sheet_path))
        rows: list[list[str]] = []
        for row in root.findall(".//m:sheetData/m:row", NS):
            cells: dict[int, str] = {}
            max_idx = -1
            for c in row.findall("m:c", NS):
                idx = _col_index(c.attrib.get("r", "A1"))
                max_idx = max(max_idx, idx)
                typ = c.attrib.get("t")
                value = ""
                if typ == "inlineStr":
                    value = "".join(t.text or "" for t in c.findall(".//m:t", NS))
                else:
                    v = c.find("m:v", NS)
                    raw = v.text if v is not None and v.text is not None else ""
                    if typ == "s" and raw:
                        try:
                            value = shared[int(raw)]
                        except (ValueError, IndexError):
                            value = raw
                    elif typ == "b":
                        value = "TRUE" if raw == "1" else "FALSE"
                    else:
                        value = raw
                cells[idx] = value
            if max_idx >= 0:
                rows.append([cells.get(i, "") for i in range(max_idx + 1)])
        return rows


def _header_row_index(rows: list[list[str]]) -> int:
    for i, row in enumerate(rows[:25]):
        nonempty = [x for x in row if _norm(x)]
        if len(nonempty) >= 2:
            return i
    raise ValueError("Could not find a usable header row")


def _id_columns(headers: list[str]) -> list[int]:
    cols = []
    for i, h in enumerate(headers):
        n = _norm(h)
        if any(re.search(p, n) for p in ID_HEADER_PATTERNS):
            cols.append(i)
    return cols


def analyze(rows: list[list[str]]) -> dict:
    hidx = _header_row_index(rows)
    headers = rows[hidx]
    width = len(headers)
    data = []
    for source_row_num, row in enumerate(rows[hidx + 1:], start=hidx + 2):
        padded = row + [""] * (width - len(row))
        padded = padded[:width]
        if any(_norm(v) for v in padded):
            data.append((source_row_num, padded))

    id_cols = _id_columns(headers)
    id_groups: list[dict] = []
    for col in id_cols:
        groups: dict[str, list[int]] = defaultdict(list)
        for row_num, row in data:
            key = _norm(row[col])
            if key:
                groups[key].append(row_num)
        for key, nums in groups.items():
            if len(nums) > 1:
                id_groups.append({"column": headers[col], "value": key, "rows": nums})

    exact: dict[tuple[str, ...], list[int]] = defaultdict(list)
    for row_num, row in data:
        sig = tuple(_norm(v) for v in row)
        exact[sig].append(row_num)
    exact_groups = [{"rows": nums} for nums in exact.values() if len(nums) > 1]

    non_id_cols = [i for i in range(width) if i not in id_cols]
    likely: dict[tuple[str, ...], list[tuple[int, list[str]]]] = defaultdict(list)
    if len(non_id_cols) >= 2:
        for row_num, row in data:
            sig = tuple(_norm(row[i]) for i in non_id_cols)
            nonempty_count = sum(bool(x) for x in sig)
            if nonempty_count >= min(3, len(non_id_cols)):
                likely[sig].append((row_num, row))
    likely_groups = []
    exact_sets = {tuple(g["rows"]) for g in exact_groups}
    for members in likely.values():
        if len(members) > 1:
            nums = [m[0] for m in members]
            if tuple(nums) in exact_sets:
                continue
            id_values = []
            for _, row in members:
                id_values.append([row[i] for i in id_cols])
            likely_groups.append({"rows": nums, "identifier_values": id_values})

    return {
        "header_row": hidx + 1,
        "headers": headers,
        "data_rows": len(data),
        "identifier_columns": [headers[i] for i in id_cols],
        "duplicate_identifier_groups": id_groups,
        "exact_duplicate_row_groups": exact_groups,
        "likely_duplicate_submission_groups": likely_groups,
        "summary": {
            "duplicate_identifier_groups": len(id_groups),
            "exact_duplicate_row_groups": len(exact_groups),
            "likely_duplicate_submission_groups": len(likely_groups),
        },
        "caution": "Screening only: review every flag before changing or removing an order.",
    }


def write_report(result: dict, output: str | Path) -> None:
    output = Path(output)
    if output.suffix.lower() == ".json":
        output.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return
    with output.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["flag_type", "column", "value", "rows", "identifier_values"])
        for g in result["duplicate_identifier_groups"]:
            w.writerow(["duplicate_identifier", g["column"], g["value"], ";".join(map(str, g["rows"])), ""])
        for g in result["exact_duplicate_row_groups"]:
            w.writerow(["exact_duplicate_row", "", "", ";".join(map(str, g["rows"])), ""])
        for g in result["likely_duplicate_submission_groups"]:
            w.writerow(["likely_duplicate_submission", "", "", ";".join(map(str, g["rows"])), json.dumps(g["identifier_values"])])


def main() -> int:
    p = argparse.ArgumentParser(description="Screen an XLSX order sheet for likely duplicates.")
    p.add_argument("xlsx")
    p.add_argument("-o", "--output", default=None, help="Optional .json or .csv report path")
    args = p.parse_args()
    try:
        rows = read_first_sheet(args.xlsx)
        result = analyze(rows)
    except Exception as exc:
        print(f"SheetGuard error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    if args.output:
        write_report(result, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())