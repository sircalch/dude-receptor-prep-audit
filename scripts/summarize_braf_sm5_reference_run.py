#!/usr/bin/env python3
"""Summarize the one frozen BRAF-SM5 Vina reference calculation."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("vina_output", type=Path)
    parser.add_argument("pose_results", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with args.pose_results.open(newline="", encoding="utf-8") as handle:
        poses = list(csv.DictReader(handle))
    if len(poses) != 9 or any(row["mapped_heavy_atom_count"] != "28" for row in poses):
        raise ValueError("expected nine poses with 28 mapped heavy atoms each")
    best_score = min(poses, key=lambda row: float(row["vina_affinity_kcal_per_mol"]))
    best_rmsd = min(poses, key=lambda row: float(row["aligned_heavy_atom_rmsd_angstrom"]))
    row = {
        "engine": "AutoDock Vina",
        "engine_version": "1.2.7",
        "configuration_sha256": sha256(args.config),
        "vina_output_sha256": sha256(args.vina_output),
        "pose_result_table_sha256": sha256(args.pose_results),
        "pose_count": str(len(poses)),
        "best_scoring_model": best_score["model"],
        "best_scoring_affinity_kcal_per_mol": best_score["vina_affinity_kcal_per_mol"],
        "best_scoring_model_aligned_heavy_atom_rmsd_angstrom": best_score["aligned_heavy_atom_rmsd_angstrom"],
        "lowest_rmsd_model": best_rmsd["model"],
        "lowest_aligned_heavy_atom_rmsd_angstrom": best_rmsd["aligned_heavy_atom_rmsd_angstrom"],
    }
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    main()
