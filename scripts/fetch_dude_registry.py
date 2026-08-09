#!/usr/bin/env python3
"""Freeze the DUD-E target-name/PDB-ID registry as a CSV snapshot."""

from __future__ import annotations

import argparse
import csv
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import urlopen


REGISTRY_URL = "https://dude.docking.org/targets"


class TargetTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self._row = []
        elif tag == "td" and self._row is not None:
            self._cell = []

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "td" and self._row is not None and self._cell is not None:
            self._row.append("".join(self._cell).strip())
            self._cell = None
        elif tag == "tr" and self._row is not None:
            if len(self._row) >= 3 and self._row[0].isdigit():
                self.rows.append(self._row)
            self._row = None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--url", default=REGISTRY_URL)
    arguments = parser.parse_args()

    with urlopen(arguments.url, timeout=60) as response:
        html = response.read().decode("utf-8", errors="replace")
    table = TargetTableParser()
    table.feed(html)
    records = [(row[1], row[2].lower()) for row in table.rows if len(row[2]) == 4]
    if len(records) != 102 or len({target for target, _ in records}) != 102:
        raise RuntimeError(f"Expected exactly 102 unique DUD-E targets, obtained {len(records)}.")

    arguments.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with arguments.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["target", "pdb_id"])
        writer.writerows(records)


if __name__ == "__main__":
    main()
