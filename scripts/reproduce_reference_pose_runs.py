#!/usr/bin/env python3
"""Re-run frozen BRAF and KIF11 Vina cases without overwriting evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_config(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        values[key] = value
    required = {"receptor", "ligand", "out", "center_x", "center_y", "center_z", "size_x", "size_y", "size_z", "scoring", "cpu", "seed", "exhaustiveness", "num_modes", "min_rmsd", "energy_range", "verbosity"}
    missing = required - values.keys()
    if missing:
        raise ValueError(f"{path.name} lacks: {', '.join(sorted(missing))}")
    return values


def run_case(root: Path, vina: Path, output_root: Path, name: str, config_name: str, analyzer: str, mmcif: str, component: str, ligand: str, frozen_csv: str) -> dict[str, str]:
    config_path = root / "protocol" / config_name
    config = parse_config(config_path)
    case_dir = output_root / name
    case_dir.mkdir(parents=True, exist_ok=True)
    output = case_dir / "vina_output.pdbqt"
    analysis = case_dir / "pose_recovery.csv"
    log = case_dir / "vina.log"
    command = [str(vina)]
    for key in ("receptor", "ligand", "center_x", "center_y", "center_z", "size_x", "size_y", "size_z", "scoring", "cpu", "seed", "exhaustiveness", "num_modes", "min_rmsd", "energy_range", "verbosity"):
        command.extend([f"--{key}", config[key]])
    command.extend(["--out", str(output)])
    completed = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
    log.write_text(completed.stdout + completed.stderr, encoding="utf-8")
    if completed.returncode != 0 or not output.exists() or output.stat().st_size == 0:
        raise RuntimeError(f"{name}: Vina failed; see {log}")
    analyze = [sys.executable, str(root / "scripts" / analyzer), str(root / mmcif), str(root / component), str(root / ligand), str(output), str(analysis)]
    subprocess.run(analyze, cwd=root, check=True)
    frozen = root / frozen_csv
    return {
        "case": name,
        "config_sha256": sha256(config_path),
        "vina_output_sha256": sha256(output),
        "analysis_sha256": sha256(analysis),
        "analysis_matches_frozen": str(analysis.read_bytes() == frozen.read_bytes()).lower(),
        "pose_count": str(sum(1 for line in output.read_text(encoding="utf-8").splitlines() if line.startswith("MODEL"))),
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vina", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--case", choices=("all", "braf", "kif11"), default="all")
    args = parser.parse_args()
    vina = args.vina.resolve()
    if not vina.is_file():
        raise FileNotFoundError(vina)
    cases = {
        "braf": ("braf-3d4q", "braf_3d4q_vina_reference.conf", "analyze_braf_sm5_pose_recovery.py", "external-data/rcsb-mmcif/3d4q.cif", "external-data/rcsb-chemcomp/SM5.cif", "audit-output/braf-3d4q/sm5_chain_a_reference.pdbqt", "results/braf_sm5_reference_pose_recovery.csv"),
        "kif11": ("kif11-3cjo", "kif11_3cjo_vina_reference.conf", "analyze_kif11_k30_pose_recovery.py", "external-data/rcsb-mmcif/3cjo.cif", "external-data/rcsb-chemcomp/K30.cif", "audit-output/kif11-3cjo/k30_chain_a_reference.pdbqt", "results/kif11_k30_reference_pose_recovery.csv"),
    }
    selected = cases if args.case == "all" else {args.case: cases[args.case]}
    rows = [run_case(root, vina, args.output_root, *case) for case in selected.values()]
    summary = args.output_root / "reproduction_summary.csv"
    with summary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
