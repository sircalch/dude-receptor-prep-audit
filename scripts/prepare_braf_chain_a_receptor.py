#!/usr/bin/env python3
"""Make a chain-A BRAF receptor PDBQT through a declared strict pathway.

Only polymer ATOM records from deposited 3D4Q chain A are retained. The script
does not repair residues, choose alternate locations, add hydrogens manually,
or remove polymer atoms. It then invokes Meeko without bypass flags.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
from pathlib import Path

import gemmi


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atom_line(serial: int, residue: gemmi.Residue, chain: gemmi.Chain, atom: gemmi.Atom) -> str:
    altloc = atom.altloc if atom.altloc and atom.altloc != "\x00" else " "
    icode = residue.seqid.icode if residue.seqid.icode and residue.seqid.icode != "\x00" else " "
    return (
        f"ATOM  {serial:5d} {atom.name:>4}{altloc:1}{residue.name:>3} {chain.name:1}"
        f"{residue.seqid.num:4d}{icode:1}   {atom.pos.x:8.3f}{atom.pos.y:8.3f}{atom.pos.z:8.3f}"
        f"{atom.occ:6.2f}{atom.b_iso:6.2f}          {atom.element.name:>2}\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mmcif", type=Path)
    parser.add_argument("prepared_pdb", type=Path)
    parser.add_argument("prepared_pdbqt", type=Path)
    parser.add_argument("summary", type=Path)
    parser.add_argument("--meeko-command", required=True)
    parser.add_argument("--meeko-version", required=True)
    args = parser.parse_args()

    structure = gemmi.read_structure(str(args.mmcif))
    if len(structure) != 1 or structure[0].find_chain("A") is None:
        raise ValueError("expected model 1 chain A in 3D4Q")
    chain = structure[0]["A"]
    all_residues = list(chain)
    residues = [residue for residue in chain if residue.het_flag == "A"]
    excluded_residues = [residue for residue in chain if residue.het_flag != "A"]
    atoms = [(residue, atom) for residue in residues for atom in residue]
    if not residues or not atoms:
        raise ValueError("chain A contained no polymer atoms")
    args.prepared_pdb.parent.mkdir(parents=True, exist_ok=True)
    with args.prepared_pdb.open("w", newline="\n", encoding="ascii") as handle:
        for serial, (residue, atom) in enumerate(atoms, start=1):
            handle.write(atom_line(serial, residue, chain, atom))
        handle.write("END\n")

    command = [
        args.meeko_command,
        "--read_pdb",
        str(args.prepared_pdb),
        "--write_pdbqt",
        str(args.prepared_pdbqt),
    ]
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    log_path = args.prepared_pdbqt.with_suffix(".meeko.log")
    log_path.write_text(
        "COMMAND: " + " ".join(command) + "\n\nSTDOUT:\n" + completed.stdout
        + "\n\nSTDERR:\n" + completed.stderr,
        encoding="utf-8",
    )
    success = completed.returncode == 0 and args.prepared_pdbqt.is_file() and args.prepared_pdbqt.stat().st_size > 0
    row = {
        "pdb_id": "3D4Q",
        "selected_auth_chain": "A",
        "source_mmcif_sha256": sha256(args.mmcif),
        "selection_rule": "polymer ATOM records from author chain A only",
        "source_chain_residue_count": str(len(all_residues)),
        "selected_residue_count": str(len(residues)),
        "selected_atom_count": str(len(atoms)),
        "excluded_nonpoly_residue_count": str(len(excluded_residues)),
        "excluded_nonpoly_atom_count": str(sum(len(residue) for residue in excluded_residues)),
        "alternate_location_atom_count": str(sum(atom.altloc not in ("", " ", "\x00") for _, atom in atoms)),
        "selected_pdb_sha256": sha256(args.prepared_pdb),
        "meeko_version": args.meeko_version,
        "command": " ".join(command),
        "return_code": str(completed.returncode),
        "pdbqt_sha256": sha256(args.prepared_pdbqt) if success else "",
        "pdbqt_bytes": str(args.prepared_pdbqt.stat().st_size) if success else "0",
        "outcome": "direct_success" if success else "direct_failure",
        "log_sha256": sha256(log_path),
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    with args.summary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    if not success:
        raise SystemExit(f"strict Meeko preparation failed; inspect {log_path}")


if __name__ == "__main__":
    main()
