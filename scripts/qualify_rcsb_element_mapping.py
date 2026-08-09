#!/usr/bin/env python3
"""Assess authoritative element mapping without writing modified receptors."""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import defaultdict
from pathlib import Path
from urllib.request import urlopen

import gemmi


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def coordinate_key(residue: str, number: int, atom: str, x: float, y: float, z: float) -> tuple[object, ...]:
    return residue, number, atom, round(x, 3), round(y, 3), round(z, 3)


def download(url: str, destination: Path) -> None:
    if destination.exists() and destination.stat().st_size > 0:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(url, timeout=120) as response, destination.open("wb") as handle:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            handle.write(block)


def rcsb_index(path: Path) -> dict[tuple[object, ...], set[str]]:
    structure = gemmi.read_structure(str(path))
    index: dict[tuple[object, ...], set[str]] = defaultdict(set)
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    key = coordinate_key(residue.name.strip(), residue.seqid.num, atom.name.strip(), atom.pos.x, atom.pos.y, atom.pos.z)
                    index[key].add(atom.element.name)
    return index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry_csv", type=Path)
    parser.add_argument("dude_raw_dir", type=Path)
    parser.add_argument("rcsb_dir", type=Path)
    parser.add_argument("results_csv", type=Path)
    parser.add_argument("--limit", type=int)
    arguments = parser.parse_args()

    with arguments.registry_csv.open(newline="", encoding="utf-8") as handle:
        registry = list(csv.DictReader(handle))
    if len(registry) != 102:
        raise RuntimeError("The frozen registry must contain exactly 102 targets.")
    if arguments.limit is not None:
        registry = registry[:arguments.limit]

    rows: list[dict[str, object]] = []
    for record in registry:
        target, pdb_id = record["target"].lower(), record["pdb_id"].lower()
        dude_pdb = arguments.dude_raw_dir / target / "receptor.pdb"
        cif = arguments.rcsb_dir / f"{pdb_id}.cif"
        source_url = f"https://files.rcsb.org/download/{pdb_id.upper()}.cif"
        common: dict[str, object] = {"target": target, "pdb_id": pdb_id, "rcsb_url": source_url}
        try:
            if not dude_pdb.exists():
                raise FileNotFoundError(dude_pdb)
            download(source_url, cif)
            index = rcsb_index(cif)
            source_rows = [line for line in dude_pdb.read_text(encoding="utf-8", errors="replace").splitlines() if line.startswith("ATOM")]
            mapped = unmatched = conflicting = 0
            for line in source_rows:
                key = coordinate_key(line[17:20].strip(), int(line[22:26]), line[12:16].strip(), float(line[30:38]), float(line[38:46]), float(line[46:54]))
                elements = index.get(key, set())
                if not elements:
                    unmatched += 1
                elif len(elements) == 1:
                    mapped += 1
                else:
                    conflicting += 1
            outcome = "complete_unambiguous_mapping" if unmatched == 0 and conflicting == 0 else "incomplete_or_conflicting_mapping"
            rows.append({
                **common, "dude_atom_records": len(source_rows), "mapped_records": mapped,
                "unmatched_records": unmatched, "conflicting_element_records": conflicting,
                "rcsb_sha256": sha256(cif), "outcome": outcome, "error_class": "",
            })
        except Exception as error:
            rows.append({
                **common, "dude_atom_records": "", "mapped_records": "", "unmatched_records": "",
                "conflicting_element_records": "", "rcsb_sha256": "", "outcome": "rcsb_download_failure", "error_class": type(error).__name__,
            })

    fields = ["target", "pdb_id", "rcsb_url", "dude_atom_records", "mapped_records", "unmatched_records", "conflicting_element_records", "rcsb_sha256", "outcome", "error_class"]
    arguments.results_csv.parent.mkdir(parents=True, exist_ok=True)
    with arguments.results_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
