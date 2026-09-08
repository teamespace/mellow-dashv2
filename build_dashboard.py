#!/usr/bin/env python3
"""Inject an inquiries CSV export into dashboard.template.html -> mellow-dashv2.html.

Usage:
    python3 build_dashboard.py                      # uses ./inquiries.csv
    python3 build_dashboard.py path/to/export.csv
    python3 build_dashboard.py export.csv out.html
"""
import csv, json, pathlib, sys

HERE = pathlib.Path(__file__).parent
TEMPLATE = HERE / "dashboard.template.html"
DEFAULT_CSV = HERE / "inquiries.csv"
DEFAULT_OUT = HERE / "mellow-dashv2.html"


def main(argv) -> int:
    csv_path = pathlib.Path(argv[1]) if len(argv) > 1 else DEFAULT_CSV
    out_path = pathlib.Path(argv[2]) if len(argv) > 2 else DEFAULT_OUT

    if not csv_path.exists():
        print(f"error: no CSV at {csv_path}\n"
              f"       pass one explicitly: python3 {pathlib.Path(argv[0]).name} <export.csv>",
              file=sys.stderr)
        return 1

    with csv_path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        cols = next(reader)
        rows = [r + [""] * (len(cols) - len(r)) for r in reader]

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__COLS__", json.dumps(cols, ensure_ascii=False))
    html = html.replace("__ROWS__", json.dumps(rows, ensure_ascii=False, separators=(",", ":")))
    out_path.write_text(html, encoding="utf-8")

    print(f"{out_path.name}: {len(rows)} rows x {len(cols)} cols, {out_path.stat().st_size/1024:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
