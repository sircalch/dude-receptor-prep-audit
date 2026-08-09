#!/usr/bin/env python3
"""Record coordinate metadata for the deposited BRAF 3D4Q reference ligand.

This script intentionally does not prepare a ligand, alter coordinates, or run
docking.  It extracts small, reviewable metadata from a local RCSB mmCIF file.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

import gemmi


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mmcif", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--padding", type=float, default=5.0)
    args = parser.parse_args()

    structure = gemmi.read_structure(str(args.mmcif))
    rows: list[dict[str, str]] = []
    for model in structure:
        for chain in model:
            for residue in chain:
                if residue.name != "SM5":
                    continue
                atoms = [atom for atom in residue if atom.element.name != "H"]
                if not atoms:
                    raise ValueError("SM5 instance has no heavy atoms")
                axes = {
                    axis: [getattr(atom.pos, axis) for atom in atoms]
                    for axis in ("x", "y", "z")
                }
                lower = {axis: min(values) for axis, values in axes.items()}
                upper = {axis: max(values) for axis, values in axes.items()}
                midpoint = {axis: (lower[axis] + upper[axis]) / 2 for axis in axes}
                size = {
                    axis: (upper[axis] - lower[axis]) + 2 * args.padding
                    for axis in axes
                }
                rows.append(
                    {
                        "pdb_id": "3D4Q",
                        "source_sha256": sha256(args.mmcif),
                        "ligand_id": residue.name,
                        "auth_chain": chain.name,
                        "auth_seq_id": str(residue.seqid.num),
                        "heavy_atom_count": str(len(atoms)),
                        "x_min": f"{lower['x']:.3f}",
                        "x_max": f"{upper['x']:.3f}",
                        "y_min": f"{lower['y']:.3f}",
                        "y_max": f"{upper['y']:.3f}",
                        "z_min": f"{lower['z']:.3f}",
                        "z_max": f"{upper['z']:.3f}",
                        "box_center_x": f"{midpoint['x']:.3f}",
                        "box_center_y": f"{midpoint['y']:.3f}",
                        "box_center_z": f"{midpoint['z']:.3f}",
                        "box_size_x": f"{size['x']:.3f}",
                        "box_size_y": f"{size['y']:.3f}",
                        "box_size_z": f"{size['z']:.3f}",
                        "padding_angstrom": f"{args.padding:.3f}",
                    }
                )
    if len(rows) != 2:
        raise ValueError(f"expected two SM5 instances in 3D4Q, found {len(rows)}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
