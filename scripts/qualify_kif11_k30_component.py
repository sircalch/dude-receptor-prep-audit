#!/usr/bin/env python3
"""Freeze basic authoritative K30 chemical-component provenance."""
from __future__ import annotations
import argparse, csv, hashlib
from pathlib import Path
import gemmi

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("component_cif", type=Path); p.add_argument("output", type=Path); a=p.parse_args()
    b=gemmi.cif.read_file(str(a.component_cif)).sole_block(); atoms=b.find_mmcif_category("_chem_comp_atom."); bonds=b.find_mmcif_category("_chem_comp_bond.")
    if b.find_value("_chem_comp.id") != "K30": raise ValueError("expected K30")
    row={"component_id":"K30","component_sha256":sha256(a.component_cif),"formula":b.find_value("_chem_comp.formula").strip('"'),"formal_charge":b.find_value("_chem_comp.pdbx_formal_charge"),"formula_weight":b.find_value("_chem_comp.formula_weight"),"atom_count":str(len(atoms)),"heavy_atom_count":str(sum(x[3] != "H" for x in atoms)),"bond_count":str(len(bonds))}
    with a.output.open("w",newline="",encoding="utf-8") as h: w=csv.DictWriter(h,fieldnames=list(row));w.writeheader();w.writerow(row)
if __name__ == "__main__": main()
