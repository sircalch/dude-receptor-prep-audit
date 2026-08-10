#!/usr/bin/env python3
"""Calculate mapped heavy-atom RMSD of Vina SM5 poses against deposited SM5-A."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import gemmi
import numpy as np


def index_map(path: Path) -> dict[int, int]:
    values: list[int] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("REMARK INDEX MAP"):
            values.extend(int(value) for value in line.split()[3:])
    if len(values) % 2:
        raise ValueError("odd number of INDEX MAP values")
    return {values[i + 1]: values[i] for i in range(0, len(values), 2)}


def output_models(path: Path) -> list[tuple[int, float, dict[int, np.ndarray]]]:
    models: list[tuple[int, float, dict[int, np.ndarray]]] = []
    model, affinity, atoms = 1, float("nan"), {}
    seen_model = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("MODEL"):
            if seen_model:
                models.append((model, affinity, atoms))
            model, affinity, atoms = int(line.split()[1]), float("nan"), {}
            seen_model = True
        elif line.startswith("REMARK VINA RESULT:"):
            affinity = float(line.split()[3])
        elif line.startswith("ATOM"):
            serial = int(line[6:11])
            atoms[serial] = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
        elif line.startswith("ENDMDL"):
            models.append((model, affinity, atoms))
            seen_model = False
    if seen_model:
        models.append((model, affinity, atoms))
    if not models:
        raise ValueError("no Vina pose models found")
    return models


def aligned_rmsd(mobile: np.ndarray, reference: np.ndarray) -> float:
    mobile = mobile - mobile.mean(axis=0)
    reference = reference - reference.mean(axis=0)
    left, _, right_t = np.linalg.svd(mobile.T @ reference)
    rotation = left @ right_t
    if np.linalg.det(rotation) < 0:
        left[:, -1] *= -1
        rotation = left @ right_t
    return float(np.sqrt(np.mean(np.sum((mobile @ rotation - reference) ** 2, axis=1))))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mmcif", type=Path)
    parser.add_argument("component_cif", type=Path)
    parser.add_argument("input_pdbqt", type=Path)
    parser.add_argument("vina_output", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    component = gemmi.cif.read_file(str(args.component_cif)).sole_block()
    component_atoms = component.find_mmcif_category("_chem_comp_atom.")
    atom_by_index = {index + 1: (row[1], row[3]) for index, row in enumerate(component_atoms)}
    structure = gemmi.read_structure(str(args.mmcif))
    residue = next(
        residue for model in structure for chain in model if chain.name == "A"
        for residue in chain if residue.name == "SM5" and residue.seqid.num == 1
    )
    deposited = {atom.name: np.array([atom.pos.x, atom.pos.y, atom.pos.z]) for atom in residue}
    mapping = index_map(args.input_pdbqt)
    rows: list[dict[str, str]] = []
    for model, affinity, pose in output_models(args.vina_output):
        reference, predicted = [], []
        for serial, component_index in mapping.items():
            atom_name, element = atom_by_index[component_index]
            if element == "H" or atom_name not in deposited:
                continue
            if serial not in pose:
                raise ValueError(f"model {model} lacks PDBQT atom serial {serial}")
            reference.append(deposited[atom_name])
            predicted.append(pose[serial])
        if len(reference) != 28:
            raise ValueError(f"model {model} has {len(reference)} mapped heavy atoms, expected 28")
        rows.append({
            "model": str(model),
            "vina_affinity_kcal_per_mol": f"{affinity:.3f}",
            "mapped_heavy_atom_count": str(len(reference)),
            "aligned_heavy_atom_rmsd_angstrom": f"{aligned_rmsd(np.array(predicted), np.array(reference)):.3f}",
        })
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
