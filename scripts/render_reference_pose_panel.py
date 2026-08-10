#!/usr/bin/env python3
"""Render a deterministic two-case reference-pose summary from frozen CSVs."""
from __future__ import annotations

import csv
from pathlib import Path


def load(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 9:
        raise ValueError(f"Expected nine poses in {path.name}.")
    return rows


def values(rows: list[dict[str, str]]) -> tuple[str, str, str]:
    top = min(rows, key=lambda row: float(row["vina_affinity_kcal_per_mol"]))
    lowest = min(rows, key=lambda row: float(row["aligned_heavy_atom_rmsd_angstrom"]))
    return (
        top["vina_affinity_kcal_per_mol"],
        top["aligned_heavy_atom_rmsd_angstrom"],
        lowest["aligned_heavy_atom_rmsd_angstrom"],
    )


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    braf = values(load(root / "results" / "braf_sm5_reference_pose_recovery.csv"))
    kif11 = values(load(root / "results" / "kif11_k30_reference_pose_recovery.csv"))
    cards = [(70, "BRAF 3D4Q / SM5", braf), (595, "KIF11 3CJO / K30", kif11)]
    elements = [
    ]
    for x, title, (score, top_rmsd, low_rmsd) in cards:
        elements.extend([
            f'<rect x="{x}" y="55" width="435" height="300" rx="12" fill="#f8fafc" stroke="#334155" stroke-width="2"/>',
            f'<text x="{x + 24}" y="100" style="font:700 23px Arial;fill:#172033">{title}</text>',
            f'<text x="{x + 24}" y="150" style="font:16px Arial;fill:#334155">Top-score value</text>',
            f'<text x="{x + 24}" y="190" style="font:700 30px Arial;fill:#172033">{score} kcal/mol</text>',
            f'<text x="{x + 24}" y="245" style="font:16px Arial;fill:#334155">RMSD of top-score pose</text>',
            f'<text x="{x + 24}" y="280" style="font:700 28px Arial;fill:#172033">{top_rmsd} Å</text>',
            f'<text x="{x + 242}" y="245" style="font:16px Arial;fill:#334155">Lowest RMSD</text>',
            f'<text x="{x + 242}" y="280" style="font:700 28px Arial;fill:#172033">{low_rmsd} Å</text>',
        ])
    target = root / "reports" / "figures" / "figure-7-reference-pose-panel.svg"
    target.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="410" viewBox="0 0 1100 410"><rect width="100%" height="100%" fill="#fff"/>' + "".join(elements) + "</svg>\n", encoding="utf-8")


if __name__ == "__main__":
    main()
