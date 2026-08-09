#!/usr/bin/env python3
"""Summarize the authoritative RCSB chemical-component definition for SM5.

The input is a locally frozen component CIF. This program neither changes the
component nor creates a docking-ready ligand.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from pathlib import Path

import gemmi


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("component_cif", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    block = gemmi.cif.read_file(str(args.component_cif)).sole_block()
    component_id = block.find_value("_chem_comp.id")
    if component_id != "SM5":
        raise ValueError(f"expected component SM5, found {component_id!r}")
    atoms = block.find_mmcif_category("_chem_comp_atom.")
    bonds = block.find_mmcif_category("_chem_comp_bond.")
    bond_orders = Counter(row[3] for row in bonds)
    row = {
        "component_id": component_id,
        "component_sha256": sha256(args.component_cif),
        "formula": block.find_value("_chem_comp.formula").strip('"'),
        "formal_charge": block.find_value("_chem_comp.pdbx_formal_charge"),
        "formula_weight": block.find_value("_chem_comp.formula_weight"),
        "atom_count": str(len(atoms)),
        "heavy_atom_count": str(sum(atom[3] != "H" for atom in atoms)),
        "bond_count": str(len(bonds)),
        "single_bond_count": str(bond_orders["SING"]),
        "double_bond_count": str(bond_orders["DOUB"]),
        "aromatic_bond_count": str(sum(bond_orders[key] for key in ("AROM", "AROMATIC"))),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    main()
