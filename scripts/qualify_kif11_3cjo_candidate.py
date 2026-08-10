#!/usr/bin/env python3
"""Generate the traceable KIF11 3CJO candidate preflight record."""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
from pathlib import Path

import gemmi


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def heavy_atoms(residue: gemmi.Residue) -> list[gemmi.Atom]:
    return [atom for atom in residue if atom.element.name != "H"]


def minimum_distance(first: gemmi.Residue, second: gemmi.Residue) -> float:
    return min(
        math.dist((a.pos.x, a.pos.y, a.pos.z), (b.pos.x, b.pos.y, b.pos.z))
        for a in heavy_atoms(first) for b in heavy_atoms(second)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mmcif", type=Path)
    parser.add_argument("audit_table", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    structure = gemmi.read_structure(str(args.mmcif))
    chain = structure[0]["A"]
    by_name = {residue.name: residue for residue in chain if residue.name in {"K30", "ADP", "MG"}}
    if set(by_name) != {"K30", "ADP", "MG"}:
        raise ValueError("expected chain-A K30, ADP, and MG")
    with args.audit_table.open(newline="", encoding="utf-8") as handle:
        audit = next(row for row in csv.DictReader(handle) if row["target"] == "kif11")
    if audit["outcome"] != "direct_success":
        raise ValueError("KIF11 no longer has strict direct-success audit status")
    row = {
        "target": "KIF11", "pdb_id": "3CJO", "source_mmcif_sha256": sha256(args.mmcif),
        "organism": "Homo sapiens", "mutation_status": "no", "resolution_angstrom": "2.28",
        "strict_mmcif_preparation_outcome": audit["outcome"], "reference_ligand": "K30",
        "reference_chain": "A", "reference_heavy_atom_count": str(len(heavy_atoms(by_name["K30"]))),
        "adp_present": "yes", "magnesium_present": "yes",
        "k30_to_adp_min_heavy_atom_distance_angstrom": f"{minimum_distance(by_name['K30'], by_name['ADP']):.3f}",
        "k30_to_magnesium_min_heavy_atom_distance_angstrom": f"{minimum_distance(by_name['K30'], by_name['MG']):.3f}",
        "candidate_status": "stopped_pending_cofactor_policy",
    }
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    main()
