#!/usr/bin/env python3
"""Audit direct Meeko/ProDy preparation of frozen RCSB mmCIF files."""
from __future__ import annotations
import argparse, csv, hashlib, subprocess
from pathlib import Path

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def classify(log: str) -> str:
    value = log.lower()
    if "alternate location" in value: return "alternate_locations"
    if "no template matched" in value or "template matching failed" in value: return "residue_template_mismatch"
    if "element" in value: return "element_error"
    if "timed out" in value: return "preparation_timeout"
    return "other_preparation_failure"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry_csv", type=Path)
    parser.add_argument("mmcif_dir", type=Path)
    parser.add_argument("work_dir", type=Path)
    parser.add_argument("results_csv", type=Path)
    parser.add_argument("--meeko-command", required=True)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    with args.registry_csv.open(newline="", encoding="utf-8") as handle: records = list(csv.DictReader(handle))
    if len(records) != 102: raise RuntimeError("The frozen registry must contain exactly 102 targets.")
    if args.limit is not None: records = records[:args.limit]
    rows = []
    for record in records:
        target, pdb_id = record["target"].lower(), record["pdb_id"].lower()
        source = args.mmcif_dir / f"{pdb_id}.cif"
        common = {"target": target, "pdb_id": pdb_id, "mmcif_sha256": "", "outcome": "", "return_code": "", "pdbqt_bytes": 0, "error_class": ""}
        if not source.exists():
            rows.append({**common, "outcome": "source_missing", "error_class": "FileNotFoundError"}); continue
        common["mmcif_sha256"] = sha256(source)
        output_dir = args.work_dir / target; output_dir.mkdir(parents=True, exist_ok=True)
        output_base = output_dir / "receptor"; pdbqt = Path(f"{output_base}.pdbqt")
        try:
            run = subprocess.run([args.meeko_command, "--read_with_prody", str(source), "--output_basename", str(output_base), "--write_pdbqt"], capture_output=True, text=True, timeout=args.timeout_seconds, check=False)
            log = run.stdout + run.stderr; (output_dir / "prepare_receptor.log").write_text(log, encoding="utf-8")
            success = run.returncode == 0 and pdbqt.exists() and pdbqt.stat().st_size > 0
            rows.append({**common, "outcome": "direct_success" if success else "direct_failure", "return_code": run.returncode, "pdbqt_bytes": pdbqt.stat().st_size if pdbqt.exists() else 0, "error_class": "" if success else classify(log)})
        except subprocess.TimeoutExpired:
            rows.append({**common, "outcome": "direct_failure", "return_code": "timeout", "error_class": "preparation_timeout"})
    fields = ["target", "pdb_id", "mmcif_sha256", "outcome", "return_code", "pdbqt_bytes", "error_class"]
    args.results_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.results_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
if __name__ == "__main__": main()
