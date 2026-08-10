#!/usr/bin/env python3
"""Verify internal consistency of the versioned audit evidence.

This check is deliberately narrow.  It verifies only the observable facts
reported by the repository's frozen result tables; it does not rerun Meeko,
download structures, or infer docking or biological performance.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from collections import Counter
from pathlib import Path


EXPECTED_DUDE_ROWS = 102
EXPECTED_MMCIF_ROWS = 102
EXPECTED_REFERENCE_TARGETS = {"BRAF", "KIF11"}
EXPECTED_POSES_PER_TARGET = 9


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_dude(rows: list[dict[str, str]]) -> str:
    require(len(rows) == EXPECTED_DUDE_ROWS, "DUD-E table must contain 102 rows")
    require(
        {row["target"] for row in rows}.__len__() == EXPECTED_DUDE_ROWS,
        "DUD-E target names must be unique",
    )
    require(
        all(row["outcome"] == "direct_failure" for row in rows),
        "DUD-E table contains an unexpected preparation outcome",
    )
    require(
        all(row["error_class"] == "blank_element_fields" for row in rows),
        "DUD-E table contains an unexpected error class",
    )
    require(
        all(int(row["pdbqt_bytes"]) == 0 for row in rows),
        "A direct DUD-E failure unexpectedly includes PDBQT output",
    )
    require(
        all(
            int(row["atom_records"]) == int(row["blank_element_fields"])
            for row in rows
        ),
        "Not every DUD-E ATOM record has the reported blank element field",
    )
    return (
        f"DUD-E: {len(rows)}/{EXPECTED_DUDE_ROWS} direct failures with "
        "blank element fields"
    )


def validate_mmcif(rows: list[dict[str, str]]) -> str:
    require(len(rows) == EXPECTED_MMCIF_ROWS, "mmCIF table must contain 102 rows")
    outcomes = Counter(row["outcome"] for row in rows)
    require(
        outcomes == Counter({"direct_success": 26, "direct_failure": 76}),
        f"Unexpected mmCIF outcome counts: {dict(outcomes)}",
    )
    require(
        all(
            (row["outcome"] == "direct_success") == (int(row["pdbqt_bytes"]) > 0)
            for row in rows
        ),
        "mmCIF success status and PDBQT byte count disagree",
    )
    failures = Counter(
        row["error_class"] for row in rows if row["outcome"] == "direct_failure"
    )
    expected_failures = Counter(
        {
            "residue_template_mismatch": 29,
            "alternate_locations": 28,
            "other_preparation_failure": 15,
            "element_error": 3,
            "preparation_timeout": 1,
        }
    )
    require(
        failures == expected_failures,
        f"Unexpected mmCIF failure classes: {dict(failures)}",
    )
    return "mmCIF: 26/102 direct successes and 76 retained failures"


def validate_poses(path: Path, target: str) -> tuple[int, float, int, float]:
    rows = read_csv(path)
    require(
        len(rows) == EXPECTED_POSES_PER_TARGET,
        f"{target} must retain exactly nine Vina poses",
    )
    models = [int(row["model"]) for row in rows]
    require(models == list(range(1, EXPECTED_POSES_PER_TARGET + 1)), f"{target} pose IDs")
    affinities = [float(row["vina_affinity_kcal_per_mol"]) for row in rows]
    rmsds = [float(row["aligned_heavy_atom_rmsd_angstrom"]) for row in rows]
    best_index = min(range(len(rows)), key=lambda index: affinities[index])
    lowest_index = min(range(len(rows)), key=lambda index: rmsds[index])
    return models[best_index], affinities[best_index], models[lowest_index], rmsds[lowest_index]


def validate_reference_panel(results_dir: Path) -> str:
    panel = read_csv(results_dir / "reference_pose_recovery_panel.csv")
    require(
        {row["target"] for row in panel} == EXPECTED_REFERENCE_TARGETS,
        "Reference panel must contain BRAF and KIF11 only",
    )
    observed = {
        "BRAF": validate_poses(results_dir / "braf_sm5_reference_pose_recovery.csv", "BRAF"),
        "KIF11": validate_poses(results_dir / "kif11_k30_reference_pose_recovery.csv", "KIF11"),
    }
    for row in panel:
        target = row["target"]
        best_model, best_affinity, low_model, low_rmsd = observed[target]
        require(int(row["vina_pose_count"]) == EXPECTED_POSES_PER_TARGET, f"{target} pose count")
        require(int(row["best_scoring_model"]) == best_model, f"{target} best model")
        require(float(row["best_scoring_affinity_kcal_per_mol"]) == best_affinity, f"{target} affinity")
        require(float(row["best_scoring_model_rmsd_angstrom"]) == low_or_best_rmsd(results_dir, target, best_model), f"{target} best RMSD")
        require(int(row["lowest_rmsd_model"]) == low_model, f"{target} lowest-RMSD model")
        require(float(row["lowest_rmsd_angstrom"]) == low_rmsd, f"{target} lowest RMSD")
    return "Reference panel: two targets with nine retained poses each"


def low_or_best_rmsd(results_dir: Path, target: str, model: int) -> float:
    filename = {
        "BRAF": "braf_sm5_reference_pose_recovery.csv",
        "KIF11": "kif11_k30_reference_pose_recovery.csv",
    }[target]
    for row in read_csv(results_dir / filename):
        if int(row["model"]) == model:
            return float(row["aligned_heavy_atom_rmsd_angstrom"])
    raise ValueError(f"{target} model {model} is absent")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results",
        help="directory holding the versioned CSV evidence",
    )
    parser.add_argument(
        "--compare-mmcif-reproduction",
        type=Path,
        help="optional independently reproduced mmCIF CSV that must match exactly",
    )
    args = parser.parse_args()
    results_dir = args.results_dir.resolve()
    try:
        dude = results_dir / "dude_receptor_audit.csv"
        mmcif = results_dir / "rcsb_mmcif_preparation_audit.csv"
        messages = [
            validate_dude(read_csv(dude)),
            validate_mmcif(read_csv(mmcif)),
            validate_reference_panel(results_dir),
        ]
        if args.compare_mmcif_reproduction is not None:
            reproduced = args.compare_mmcif_reproduction.resolve()
            require(reproduced.read_bytes() == mmcif.read_bytes(), "mmCIF reproduction differs from the frozen CSV")
            messages.append("mmCIF reproduction: byte-identical to the frozen audit CSV")
    except (OSError, KeyError, ValueError) as error:
        print(f"Evidence verification failed: {error}", file=sys.stderr)
        return 1

    for message in messages:
        print(message)
    print("SHA-256 manifest:")
    for path in sorted(results_dir.glob("*.csv")):
        print(f"{sha256(path)}  {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
