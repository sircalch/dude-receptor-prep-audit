#!/usr/bin/env python3
"""Run the prespecified strict direct-preparation audit for DUD-E receptors."""

from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
from pathlib import Path
from urllib.request import urlopen


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def error_classification(log: str, blank_elements: int) -> str:
    lower = log.lower()
    if blank_elements:
        return "blank_element_fields"
    if "alternate location" in lower:
        return "alternate_locations"
    if "no template matched" in lower or "template matching failed" in lower:
        return "residue_template_mismatch"
    if "timed out" in lower:
        return "preparation_timeout"
    return "other_preparation_failure"


def inspect_pdb(path: Path) -> dict[str, object]:
    rows = path.read_text(encoding="utf-8", errors="replace").splitlines()
    atom_rows = [row for row in rows if row.startswith("ATOM")]
    hetatm_rows = [row for row in rows if row.startswith("HETATM")]
    coordinate_rows = atom_rows + hetatm_rows
    return {
        "atom_records": len(atom_rows),
        "hetatm_records": len(hetatm_rows),
        "blank_element_fields": sum(not row[76:78].strip() for row in coordinate_rows),
        "alternate_location_records": sum(bool(row[16:17].strip()) for row in coordinate_rows),
        "chain_ids": ";".join(sorted({row[21:22].strip() or "_" for row in atom_rows})),
    }


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry_csv", type=Path)
    parser.add_argument("raw_dir", type=Path)
    parser.add_argument("work_dir", type=Path)
    parser.add_argument("results_csv", type=Path)
    parser.add_argument("--meeko-command", required=True)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    arguments = parser.parse_args()

    with arguments.registry_csv.open(newline="", encoding="utf-8") as handle:
        records = list(csv.DictReader(handle))
    if len(records) != 102:
        raise RuntimeError("The frozen registry must contain exactly 102 targets.")
    if arguments.limit is not None:
        records = records[: arguments.limit]

    result_rows: list[dict[str, object]] = []
    for record in records:
        target = record["target"].lower()
        source_url = f"https://dude.docking.org/targets/{target}/receptor.pdb"
        receptor = arguments.raw_dir / target / "receptor.pdb"
        common: dict[str, object] = {"target": target, "pdb_id": record["pdb_id"], "source_url": source_url}
        try:
            download(source_url, receptor)
            observations = inspect_pdb(receptor)
            common.update(observations)
            common["source_bytes"] = receptor.stat().st_size
            common["source_sha256"] = sha256(receptor)
        except Exception as error:  # logged as an audit observation
            result_rows.append({**common, "outcome": "download_failure", "return_code": "", "pdbqt_bytes": 0, "error_class": type(error).__name__})
            continue

        target_work = arguments.work_dir / target
        target_work.mkdir(parents=True, exist_ok=True)
        output_base = target_work / "receptor"
        pdbqt = Path(f"{output_base}.pdbqt")
        command = [arguments.meeko_command, "--read_pdb", str(receptor), "--output_basename", str(output_base), "--write_pdbqt"]
        try:
            completed = subprocess.run(command, capture_output=True, text=True, timeout=arguments.timeout_seconds, check=False)
            log = completed.stdout + completed.stderr
            (target_work / "prepare_receptor.log").write_text(log, encoding="utf-8")
            success = completed.returncode == 0 and pdbqt.exists() and pdbqt.stat().st_size > 0
            result_rows.append({
                **common,
                "outcome": "direct_success" if success else "direct_failure",
                "return_code": completed.returncode,
                "pdbqt_bytes": pdbqt.stat().st_size if pdbqt.exists() else 0,
                "error_class": "" if success else error_classification(log, int(common["blank_element_fields"])),
            })
        except subprocess.TimeoutExpired as error:
            log = (error.stdout or "") + (error.stderr or "")
            (target_work / "prepare_receptor.log").write_text(log, encoding="utf-8")
            result_rows.append({**common, "outcome": "direct_failure", "return_code": "timeout", "pdbqt_bytes": 0, "error_class": "preparation_timeout"})

    fields = [
        "target", "pdb_id", "source_url", "source_bytes", "source_sha256", "atom_records", "hetatm_records",
        "blank_element_fields", "alternate_location_records", "chain_ids", "outcome", "return_code", "pdbqt_bytes", "error_class",
    ]
    arguments.results_csv.parent.mkdir(parents=True, exist_ok=True)
    with arguments.results_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result_rows)


if __name__ == "__main__":
    main()
