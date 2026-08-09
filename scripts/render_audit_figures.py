#!/usr/bin/env python3
"""Validate the versioned audit table and render deterministic SVG summaries."""

from __future__ import annotations

import csv
import html
import sys
from collections import Counter
from pathlib import Path


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "target", "pdb_id", "source_url", "source_bytes", "source_sha256", "atom_records",
        "hetatm_records", "blank_element_fields", "alternate_location_records", "chain_ids",
        "outcome", "return_code", "pdbqt_bytes", "error_class",
    }
    if len(rows) != 102 or set(rows[0]) != required or len({row["target"] for row in rows}) != 102:
        raise ValueError("Audit results must contain exactly one complete row for each of 102 targets.")
    if any(not row["source_sha256"] or len(row["source_sha256"]) != 64 for row in rows):
        raise ValueError("Every target requires a SHA-256 source checksum.")
    if len({row["source_sha256"] for row in rows}) != 102:
        raise ValueError("Source checksums must be unique across targets.")
    for numeric in ("source_bytes", "atom_records", "hetatm_records", "blank_element_fields", "alternate_location_records", "pdbqt_bytes"):
        if any(int(row[numeric]) < 0 for row in rows):
            raise ValueError(f"Negative value in {numeric}.")
    return rows


def write_svg(path: Path, body: str, width: int = 1100, height: int = 560) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        '<rect width="100%" height="100%" fill="#ffffff"/>'
        '<style>text{font-family:Arial,sans-serif;fill:#172033}.title{font-size:28px;font-weight:700}.label{font-size:18px}.small{font-size:14px}</style>'
        + body + "</svg>\n",
        encoding="utf-8",
    )


def main() -> None:
    arguments = sys.argv[1:]
    if len(arguments) > 2:
        raise SystemExit("Usage: python scripts/render_audit_figures.py [results-csv] [output-dir]")
    result_path = Path(arguments[0]) if arguments else Path("results/dude_receptor_audit.csv")
    output_dir = Path(arguments[1]) if len(arguments) == 2 else Path("reports/figures")
    rows = load_rows(result_path)
    total = len(rows)
    downloads = sum(bool(row["source_sha256"]) for row in rows)
    blank = sum(int(row["blank_element_fields"]) > 0 for row in rows)
    direct_failures = sum(row["outcome"] == "direct_failure" for row in rows)
    pdbqt = sum(int(row["pdbqt_bytes"]) > 0 for row in rows)
    atom_total = sum(int(row["atom_records"]) for row in rows)
    blank_total = sum(int(row["blank_element_fields"]) for row in rows)
    error_counts = Counter(row["error_class"] or "none" for row in rows)

    boxes = [(45, "Registry", total, "frozen targets"), (300, "Downloaded", downloads, "source checksums"), (555, "Blank elements", blank, "source files"), (810, "Direct PDBQT", pdbqt, "nonempty outputs")]
    elements = ['<text x="45" y="55" class="title">Strict DUD-E receptor-preparation audit</text>']
    for index, (x, label, value, subtitle) in enumerate(boxes):
        fill = "#dbeafe" if index < 2 else ("#fee2e2" if index == 2 else "#f1f5f9")
        elements.append(f'<rect x="{x}" y="160" width="210" height="175" rx="12" fill="{fill}" stroke="#334155" stroke-width="2"/>')
        elements.append(f'<text x="{x + 105}" y="208" text-anchor="middle" class="label">{html.escape(label)}</text>')
        elements.append(f'<text x="{x + 105}" y="270" text-anchor="middle" style="font:700 54px Arial;fill:#0f172a">{value}</text>')
        elements.append(f'<text x="{x + 105}" y="305" text-anchor="middle" class="small">{html.escape(subtitle)}</text>')
        if index < len(boxes) - 1:
            elements.append(f'<path d="M {x + 215} 247 L {x + 248} 247" stroke="#475569" stroke-width="3" marker-end="url(#arrow)"/>')
    elements.insert(1, '<defs><marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#475569"/></marker></defs>')
    elements.append(f'<text x="45" y="415" class="label">Direct failures: {direct_failures}/{total}; all raw coordinate records preserved without repair.</text>')
    elements.append('<text x="45" y="455" class="small">This figure reports software-compatibility observations only; it contains no docking outcomes.</text>')
    write_svg(output_dir / "figure-1-audit-flow.svg", "".join(elements))

    bar_width = 720
    max_value = max(atom_total, blank_total, 1)
    atom_height = round(280 * atom_total / max_value)
    blank_height = round(280 * blank_total / max_value)
    error_label = ", ".join(f"{key}: {value}" for key, value in sorted(error_counts.items()))
    body = [
        '<text x="55" y="55" class="title">Observed element-field status in original DUD-E receptors</text>',
        '<line x1="180" y1="395" x2="950" y2="395" stroke="#334155" stroke-width="2"/>',
        f'<rect x="270" y="{395 - atom_height}" width="180" height="{atom_height}" fill="#2563eb"/>',
        f'<rect x="650" y="{395 - blank_height}" width="180" height="{blank_height}" fill="#dc2626"/>',
        '<text x="360" y="430" text-anchor="middle" class="label">ATOM records</text>',
        '<text x="740" y="430" text-anchor="middle" class="label">Blank element fields</text>',
        f'<text x="360" y="{380 - atom_height}" text-anchor="middle" class="label">{atom_total:,}</text>',
        f'<text x="740" y="{380 - blank_height}" text-anchor="middle" class="label">{blank_total:,}</text>',
        f'<text x="55" y="495" class="small">Error classification: {html.escape(error_label)}. No HETATM records occurred in the downloaded receptor files.</text>',
    ]
    write_svg(output_dir / "figure-2-element-fields.svg", "".join(body))


if __name__ == "__main__":
    main()
