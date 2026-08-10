#!/usr/bin/env python3
"""Prepare the frozen neutral SM5 baseline for the declared reference run."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import subprocess
from pathlib import Path

from rdkit import Chem


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ideal_sdf", type=Path)
    parser.add_argument("component_cif", type=Path)
    parser.add_argument("output_pdbqt", type=Path)
    parser.add_argument("summary", type=Path)
    parser.add_argument("--meeko-command", required=True)
    parser.add_argument("--meeko-version", required=True)
    args = parser.parse_args()

    molecule = Chem.SDMolSupplier(str(args.ideal_sdf), removeHs=False)[0]
    if molecule is None or molecule.GetProp("_Name") != "SM5":
        raise ValueError("expected one readable SM5 molecule")
    if molecule.GetNumAtoms() != 51 or molecule.GetNumHeavyAtoms() != 28 or molecule.GetNumBonds() != 55:
        raise ValueError("SM5 ideal SDF does not match frozen component counts")
    if sum(atom.GetFormalCharge() for atom in molecule.GetAtoms()) != 0:
        raise ValueError("SM5 ideal SDF does not have the frozen neutral charge")

    args.output_pdbqt.parent.mkdir(parents=True, exist_ok=True)
    command = [
        args.meeko_command, "-i", str(args.ideal_sdf), "-o", str(args.output_pdbqt),
        "--charge_model", "gasteiger", "--add_index_map",
    ]
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    log_path = args.output_pdbqt.with_suffix(".meeko.log")
    normalized_stderr = re.sub(r"\[\d{2}:\d{2}:\d{2}\]", "[time]", completed.stderr)
    log_path.write_text(
        "COMMAND: " + " ".join(command) + "\n\nSTDOUT:\n" + completed.stdout
        + "\n\nSTDERR:\n" + normalized_stderr,
        encoding="utf-8",
    )
    success = completed.returncode == 0 and args.output_pdbqt.is_file() and args.output_pdbqt.stat().st_size > 0
    pdbqt_atom_count = (
        sum(line.startswith("ATOM") for line in args.output_pdbqt.read_text(encoding="utf-8").splitlines())
        if success else 0
    )
    row = {
        "ligand_id": "SM5",
        "ideal_sdf_sha256": sha256(args.ideal_sdf),
        "component_sha256": sha256(args.component_cif),
        "input_atom_count": str(molecule.GetNumAtoms()),
        "input_heavy_atom_count": str(molecule.GetNumHeavyAtoms()),
        "input_bond_count": str(molecule.GetNumBonds()),
        "input_formal_charge": str(sum(atom.GetFormalCharge() for atom in molecule.GetAtoms())),
        "meeko_version": args.meeko_version,
        "command": " ".join(command),
        "return_code": str(completed.returncode),
        "pdbqt_sha256": sha256(args.output_pdbqt) if success else "",
        "pdbqt_bytes": str(args.output_pdbqt.stat().st_size) if success else "0",
        "pdbqt_atom_record_count": str(pdbqt_atom_count),
        "outcome": "direct_success" if success else "direct_failure",
        "log_sha256": sha256(log_path),
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    with args.summary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    if not success:
        raise SystemExit(f"Meeko ligand preparation failed; inspect {log_path}")


if __name__ == "__main__":
    main()
