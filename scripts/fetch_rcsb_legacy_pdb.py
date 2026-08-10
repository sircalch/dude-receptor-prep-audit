#!/usr/bin/env python3
"""Fetch official RCSB legacy-PDB files with a provenance manifest."""
from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry_csv", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("manifest_csv", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args()

    with args.registry_csv.open(newline="", encoding="utf-8") as handle:
        records = list(csv.DictReader(handle))
    if len(records) != 102:
        raise RuntimeError("The frozen registry must contain exactly 102 targets.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for record in records:
        target, pdb_id = record["target"].lower(), record["pdb_id"].lower()
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        timestamp = datetime.now(timezone.utc).isoformat()
        destination = args.output_dir / f"{pdb_id}.pdb"
        common = {
            "target": target,
            "pdb_id": pdb_id,
            "url": url,
            "retrieved_utc": timestamp,
            "http_status": "",
            "bytes": 0,
            "sha256": "",
            "outcome": "",
            "error_class": "",
        }
        try:
            with urlopen(url, timeout=args.timeout_seconds) as response:
                payload = response.read()
                status = response.status
            destination.write_bytes(payload)
            rows.append({
                **common,
                "http_status": status,
                "bytes": len(payload),
                "sha256": sha256(payload),
                "outcome": "downloaded",
            })
        except HTTPError as error:
            rows.append({**common, "http_status": error.code, "outcome": "not_evaluated", "error_class": type(error).__name__})
        except URLError as error:
            rows.append({**common, "outcome": "not_evaluated", "error_class": type(error).__name__})

    fields = ["target", "pdb_id", "url", "retrieved_utc", "http_status", "bytes", "sha256", "outcome", "error_class"]
    args.manifest_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.manifest_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
