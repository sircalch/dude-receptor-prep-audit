#!/usr/bin/env python3
"""Prepare KIF11 chain A retaining only its deposited ADP and Mg cofactor pair."""

from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
from collections import Counter
from pathlib import Path

import gemmi


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pdb_line(record: str, serial: int, residue: gemmi.Residue, chain: gemmi.Chain, atom: gemmi.Atom) -> str:
    altloc = atom.altloc if atom.altloc and atom.altloc != "\x00" else " "
    icode = residue.seqid.icode if residue.seqid.icode and residue.seqid.icode != "\x00" else " "
    return (f"{record:<6}{serial:5d} {atom.name:>4}{altloc:1}{residue.name:>3} {chain.name:1}{residue.seqid.num:4d}{icode:1}   "
            f"{atom.pos.x:8.3f}{atom.pos.y:8.3f}{atom.pos.z:8.3f}{atom.occ:6.2f}{atom.b_iso:6.2f}          {atom.element.name:>2}\n")


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
    chain = structure[0]["A"]
    retained = [residue for residue in chain if residue.het_flag == "A" or residue.name in {"ADP", "MG"}]
    excluded = [residue for residue in chain if residue not in retained]
    retained_names = Counter(residue.name for residue in retained if residue.het_flag != "A")
    if retained_names != Counter({"ADP": 1, "MG": 1}) or any(residue.name == "K30" for residue in retained):
        raise ValueError("cofactor selection did not retain exactly ADP and MG while excluding K30")
    atoms = [(residue, atom) for residue in retained for atom in residue]
    args.prepared_pdb.parent.mkdir(parents=True, exist_ok=True)
    with args.prepared_pdb.open("w", newline="\n", encoding="ascii") as handle:
        for serial, (residue, atom) in enumerate(atoms, start=1):
            handle.write(pdb_line("ATOM" if residue.het_flag == "A" else "HETATM", serial, residue, chain, atom))
        handle.write("END\n")
    command = [args.meeko_command, "--read_pdb", str(args.prepared_pdb), "--write_pdbqt", str(args.prepared_pdbqt)]
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    log_path = args.prepared_pdbqt.with_suffix(".meeko.log")
    log_path.write_text("COMMAND: " + " ".join(command) + "\n\nSTDOUT:\n" + completed.stdout + "\n\nSTDERR:\n" + completed.stderr, encoding="utf-8")
    success = completed.returncode == 0 and args.prepared_pdbqt.is_file() and args.prepared_pdbqt.stat().st_size > 0
    row = {
        "pdb_id": "3CJO", "selected_auth_chain": "A", "source_mmcif_sha256": sha256(args.mmcif),
        "selection_rule": "chain-A polymer plus ADP and MG; exclude K30 and waters",
        "retained_polymer_residue_count": str(sum(residue.het_flag == "A" for residue in retained)),
        "retained_adp_count": str(retained_names["ADP"]), "retained_magnesium_count": str(retained_names["MG"]),
        "retained_atom_count": str(len(atoms)), "excluded_residue_count": str(len(excluded)),
        "excluded_k30_count": str(sum(residue.name == "K30" for residue in excluded)),
        "excluded_water_count": str(sum(residue.name == "HOH" for residue in excluded)),
        "alternate_location_atom_count": str(sum(atom.altloc not in ("", " ", "\x00") for _, atom in atoms)),
        "selected_pdb_sha256": sha256(args.prepared_pdb), "meeko_version": args.meeko_version,
        "command": " ".join(command), "return_code": str(completed.returncode),
        "pdbqt_sha256": sha256(args.prepared_pdbqt) if success else "", "pdbqt_bytes": str(args.prepared_pdbqt.stat().st_size) if success else "0",
        "outcome": "direct_success" if success else "direct_failure", "log_sha256": sha256(log_path),
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    with args.summary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row)); writer.writeheader(); writer.writerow(row)
    if not success:
        raise SystemExit(f"strict Meeko preparation failed; inspect {log_path}")


if __name__ == "__main__":
    main()
