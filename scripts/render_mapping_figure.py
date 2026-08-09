#!/usr/bin/env python3
"""Validate Phase 2 mapping results and render a deterministic SVG figure."""

from __future__ import annotations

import csv
from pathlib import Path


def main() -> None:
    source = Path("results/dude_rcsb_element_mapping.csv")
    with source.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 102 or len({row["target"] for row in rows}) != 102:
        raise ValueError("Mapping results must contain 102 unique targets.")
    if any(row["outcome"] == "rcsb_download_failure" for row in rows):
        raise ValueError("Mapping results contain an unresolved RCSB download failure.")
    mapped = sum(int(row["mapped_records"]) for row in rows)
    unmatched = sum(int(row["unmatched_records"]) for row in rows)
    conflicting = sum(int(row["conflicting_element_records"]) for row in rows)
    complete = sum(row["outcome"] == "complete_unambiguous_mapping" for row in rows)
    total = mapped + unmatched + conflicting
    if total <= 0:
        raise ValueError("Mapping results contain no atom records.")

    scale = 280 / total
    mapped_height, unmatched_height, conflicting_height = round(mapped * scale), round(unmatched * scale), round(conflicting * scale)
    labels = [(240, mapped_height, "Mapped exactly", mapped, "#2563eb"), (510, unmatched_height, "Unmatched", unmatched, "#dc2626"), (780, conflicting_height, "Conflicting", conflicting, "#f59e0b")]
    body = [
        '<text x="55" y="55" style="font:700 28px Arial;fill:#172033">Authoritative mmCIF mapping qualification</text>',
        '<line x1="150" y1="410" x2="975" y2="410" stroke="#334155" stroke-width="2"/>',
    ]
    for x, height, label, value, color in labels:
        body.append(f'<rect x="{x}" y="{410 - height}" width="150" height="{height}" fill="{color}"/>')
        body.append(f'<text x="{x + 75}" y="445" text-anchor="middle" style="font:18px Arial;fill:#172033">{label}</text>')
        body.append(f'<text x="{x + 75}" y="{395 - height}" text-anchor="middle" style="font:700 20px Arial;fill:#172033">{value:,}</text>')
    body.append(f'<text x="55" y="505" style="font:18px Arial;fill:#172033">Complete, unambiguous targets: {complete}/102. No receptor derivative was written.</text>')
    body.append('<text x="55" y="535" style="font:14px Arial;fill:#172033">Exact coordinate/residue/atom correspondence is assessed without editing either source.</text>')
    target = Path("reports/figures/figure-3-authoritative-mapping.svg")
    target.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="560" viewBox="0 0 1100 560">'
        '<rect width="100%" height="100%" fill="#ffffff"/>' + "".join(body) + "</svg>\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
