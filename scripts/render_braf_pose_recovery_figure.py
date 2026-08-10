#!/usr/bin/env python3
"""Render a deterministic SVG for the frozen BRAF-SM5 pose-recovery table."""

from __future__ import annotations

import csv
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    with (root / "results" / "braf_sm5_reference_pose_recovery.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    width, height, left, right, top, bottom = 760, 430, 82, 38, 58, 70
    x_min, x_max, y_min, y_max = -11.1, -9.0, 0.9, 1.95
    plot_w, plot_h = width - left - right, height - top - bottom
    x = lambda value: left + (value - x_min) / (x_max - x_min) * plot_w
    y = lambda value: top + (y_max - value) / (y_max - y_min) * plot_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#1f2937}.small{font-size:12px}.label{font-size:14px}.title{font-size:18px;font-weight:600}</style>',
        '<text class="title" x="82" y="30">BRAF 3D4Q / SM5: frozen reference-pose recovery</text>',
        f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#374151"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#374151"/>',
    ]
    for value in (-11.0, -10.5, -10.0, -9.5):
        px = x(value)
        parts.extend([f'<line x1="{px:.1f}" y1="{top}" x2="{px:.1f}" y2="{height-bottom}" stroke="#e5e7eb"/>', f'<text class="small" text-anchor="middle" x="{px:.1f}" y="{height-bottom+22}">{value:.1f}</text>'])
    for value in (1.0, 1.2, 1.4, 1.6, 1.8):
        py = y(value)
        parts.extend([f'<line x1="{left}" y1="{py:.1f}" x2="{width-right}" y2="{py:.1f}" stroke="#e5e7eb"/>', f'<text class="small" text-anchor="end" x="{left-10}" y="{py+4:.1f}">{value:.1f}</text>'])
    for row in rows:
        affinity, rmsd, model = float(row["vina_affinity_kcal_per_mol"]), float(row["aligned_heavy_atom_rmsd_angstrom"]), row["model"]
        color = "#be123c" if model == "1" else ("#047857" if model == "3" else "#2563eb")
        parts.extend([f'<circle cx="{x(affinity):.1f}" cy="{y(rmsd):.1f}" r="7" fill="{color}"/>', f'<text class="small" text-anchor="middle" x="{x(affinity):.1f}" y="{y(rmsd)-12:.1f}">{model}</text>'])
    parts.extend([
        f'<text class="label" text-anchor="middle" x="{left+plot_w/2:.1f}" y="{height-18}">Vina affinity (kcal/mol; lower is better within this run)</text>',
        f'<text class="label" text-anchor="middle" transform="translate(20 {top+plot_h/2:.1f}) rotate(-90)">Aligned heavy-atom RMSD to deposited SM5-A (Å)</text>',
        '<circle cx="465" cy="42" r="6" fill="#be123c"/><text class="small" x="477" y="46">top score (mode 1)</text>',
        '<circle cx="610" cy="42" r="6" fill="#047857"/><text class="small" x="622" y="46">lowest RMSD (mode 3)</text>',
        '</svg>',
    ])
    output = root / "reports" / "figures" / "figure-5-braf-sm5-pose-recovery.svg"
    output.write_text("\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
