# Validation artefacts

This directory contains non-coordinate, machine-readable outputs from the
predeclared RCSB legacy-PDB comparator. Downloaded coordinate files and full
tool logs remain outside version control in `external-data/` and
`audit-output/`, respectively.

| File | Content | SHA-256 |
|---|---|---|
| `rcsb_legacy_pdb_download_manifest_20260809.csv` | One official RCSB legacy-PDB download record for each of 102 registry entries: URL, retrieval time, HTTP status, bytes, and source checksum. | `478315f21667f6c31b4752b4e93c81def5a676abea3fbbea5808256539eea175` |
| `rcsb_legacy_pdb_preparation_audit_20260809.csv` | One strict direct Meeko preparation result for each target, including source checksum, outcome, return code, output bytes, and normalized failure class. | `384b2eb96721605bf6336ee1d1d0e1d1c44a06b3d690c30045b7c57ee1f6404b` |

The preparation table is rendered by
`scripts/render_preparation_comparator_figure.py` into
`reports/figures/figure-6-preparation-comparator.svg`, alongside the frozen
DUD-E and RCSB mmCIF result tables. It supports source-and-reader compatibility
comparison only and must not be used to infer docking or biological outcomes.
