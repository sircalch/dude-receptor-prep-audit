#!/usr/bin/env python3
"""Validate Phase 3 results and render a deterministic SVG summary."""
import csv
from collections import Counter
from pathlib import Path

rows = list(csv.DictReader(open("results/rcsb_mmcif_preparation_audit.csv", encoding="utf-8")))
if len(rows) != 102 or len({row["target"] for row in rows}) != 102:
    raise ValueError("Expected 102 unique RCSB mmCIF audit rows.")
outcomes = Counter(row["outcome"] for row in rows)
if outcomes["direct_success"] + outcomes["direct_failure"] != 102:
    raise ValueError("Unexpected Phase 3 outcome values.")
errors = Counter(row["error_class"] for row in rows if row["error_class"])
success, failure = outcomes["direct_success"], outcomes["direct_failure"]
scale = 280 / 102
bars = [(260, success, "Direct success", "#16a34a"), (650, failure, "Direct failure", "#dc2626")]
body = ['<text x="50" y="55" style="font:700 28px Arial;fill:#172033">Strict Meeko preparation of official RCSB mmCIF sources</text>', '<line x1="150" y1="410" x2="960" y2="410" stroke="#334155" stroke-width="2"/>']
for x, value, label, color in bars:
    height = round(value * scale)
    body += [f'<rect x="{x}" y="{410-height}" width="190" height="{height}" fill="{color}"/>', f'<text x="{x+95}" y="445" text-anchor="middle" style="font:18px Arial;fill:#172033">{label}</text>', f'<text x="{x+95}" y="{395-height}" text-anchor="middle" style="font:700 24px Arial;fill:#172033">{value}/102</text>']
summary = "; ".join(f"{key}: {value}" for key, value in sorted(errors.items()))
body += [f'<text x="50" y="505" style="font:15px Arial;fill:#172033">Failure classifications: {summary}</text>', '<text x="50" y="535" style="font:14px Arial;fill:#172033">Compatibility only: no ligands, docking, poses, scores or biological claims.</text>']
Path("reports/figures/figure-4-mmcif-compatibility.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="560" viewBox="0 0 1100 560"><rect width="100%" height="100%" fill="#fff"/>' + "".join(body) + "</svg>\n", encoding="utf-8")
