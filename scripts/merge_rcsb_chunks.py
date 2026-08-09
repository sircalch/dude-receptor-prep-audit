#!/usr/bin/env python3
"""Merge validated resumable RCSB mmCIF audit chunks into one result table."""
import csv
from pathlib import Path

chunks = [Path("results") / f"rcsb_mmcif_chunk_{index:02d}.csv" for index in (0, 20, 40, 60, 80, 100)]
rows = []
for chunk in chunks:
    with chunk.open(newline="", encoding="utf-8") as handle:
        rows.extend(csv.DictReader(handle))
if len(rows) != 102 or len({row["target"] for row in rows}) != 102:
    raise ValueError("Chunks must contain exactly 102 unique targets.")
rows.sort(key=lambda row: row["target"])
with Path("results/rcsb_mmcif_preparation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
    writer.writeheader(); writer.writerows(rows)
