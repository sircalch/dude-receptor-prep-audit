#!/usr/bin/env python3
"""Extract the deposited 3D4Q SM5 chain-A coordinate record without preparation."""

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
    parser.add_argument("component_cif", type=Path)
    parser.add_argument("coordinates_output", type=Path)
    parser.add_argument("summary_output", type=Path)
    args = parser.parse_args()

    block = gemmi.cif.read_file(str(args.component_cif)).sole_block()
    component_atoms = block.find_mmcif_category("_chem_comp_atom.")
    expected_elements = {row[1]: row[3] for row in component_atoms}
    structure = gemmi.read_structure(str(args.mmcif))
    matches = [
        residue
        for model in structure
        for chain in model
        if chain.name == "A"
        for residue in chain
        if residue.name == "SM5" and residue.seqid.num == 1
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one chain-A SM5 residue, found {len(matches)}")
    residue = matches[0]
    atoms = list(residue)
    args.coordinates_output.parent.mkdir(parents=True, exist_ok=True)
    with args.coordinates_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["atom_id", "element", "x", "y", "z"])
        writer.writeheader()
        for atom in atoms:
            writer.writerow(
                {
                    "atom_id": atom.name,
                    "element": atom.element.name,
                    "x": f"{atom.pos.x:.3f}",
                    "y": f"{atom.pos.y:.3f}",
                    "z": f"{atom.pos.z:.3f}",
                }
            )
    atom_ids = {atom.name for atom in atoms}
    mismatches = [
        atom for atom in atoms if expected_elements.get(atom.name) != atom.element.name
    ]
    summary = {
        "pdb_id": "3D4Q",
        "ligand_id": "SM5",
        "auth_chain": "A",
        "auth_seq_id": "1",
        "source_mmcif_sha256": sha256(args.mmcif),
        "component_sha256": sha256(args.component_cif),
        "extracted_coordinate_sha256": sha256(args.coordinates_output),
        "deposited_atom_count": str(len(atoms)),
        "deposited_heavy_atom_count": str(sum(atom.element.name != "H" for atom in atoms)),
        "component_atom_count": str(len(component_atoms)),
        "component_heavy_atom_count": str(sum(row[3] != "H" for row in component_atoms)),
        "component_atom_ids_missing_from_deposit": str(len(set(expected_elements) - atom_ids)),
        "deposited_atom_ids_missing_from_component": str(len(atom_ids - set(expected_elements))),
        "element_mismatch_count": str(len(mismatches)),
    }
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    with args.summary_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary))
        writer.writeheader()
        writer.writerow(summary)


if __name__ == "__main__":
    main()
