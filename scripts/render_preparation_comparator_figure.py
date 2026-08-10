#!/usr/bin/env python3
"""Render a deterministic source-format preparation comparison figure."""
from __future__ import annotations

import csv
from pathlib import Path


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def success_count(records: list[dict[str, str]]) -> int:
    if len(records) != 102:
        raise ValueError("Each preparation condition must contain 102 rows.")
    return sum(row["outcome"] == "direct_success" for row in records)


def main() -> None:
    dude = rows(Path("results/dude_receptor_audit.csv"))
    mmcif = rows(Path("results/rcsb_mmcif_preparation_audit.csv"))
    legacy = rows(Path("validation/rcsb_legacy_pdb_preparation_audit_20260809.csv"))
    values = [success_count(dude), success_count(mmcif), success_count(legacy)]
    labels = ["Original DUD-E PDB", "RCSB mmCIF", "RCSB legacy PDB"]
    colors = ["#dc2626", "#2563eb", "#16a34a"]
    positions = [185, 495, 805]
    baseline, top, scale = 400, 145, 2.8
    body = [
        '<text x="45" y="52" style="font:700 27px Arial;fill:#172033">Strict receptor-preparation outcomes by source and reader condition</text>',
        '<line x1="105" y1="400" x2="1030" y2="400" stroke="#334155" stroke-width="2"/>',
    ]
    for x, label, value, color in zip(positions, labels, values, colors):
        height = round(value * scale)
        body.extend([
            f'<rect x="{x}" y="{baseline-height}" width="170" height="{height}" fill="{color}"/>',
            f'<text x="{x+85}" y="{baseline-height-15}" text-anchor="middle" style="font:700 26px Arial;fill:#172033">{value}/102</text>',
            f'<text x="{x+85}" y="435" text-anchor="middle" style="font:17px Arial;fill:#172033">{label}</text>',
            '<text x="0" y="0" style="display:none">strict direct Meeko preparation</text>',
        ])
    body.extend([
        '<text x="45" y="495" style="font:15px Arial;fill:#172033">RCSB mmCIF and legacy-PDB conditions agreed for 101/102 targets; DPP4/2I78 differed by timeout versus success.</text>',
        '<text x="45" y="530" style="font:14px Arial;fill:#172033">Compatibility observations only: no receptor-quality, docking-score, affinity, activity, or therapeutic claim.</text>',
    ])
    target = Path("reports/figures/figure-6-preparation-comparator.svg")
    target.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="560" viewBox="0 0 1100 560"><rect width="100%" height="100%" fill="#fff"/>'
        + "".join(body) + "</svg>\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
