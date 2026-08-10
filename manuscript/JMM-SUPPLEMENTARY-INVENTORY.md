# Proposed supplementary-material inventory for Journal of Molecular Modeling

This inventory identifies repository artefacts that can support peer review and
reproducibility. Final selection must follow the journal's upload limits and
the authors' final review.

| Proposed item | Contents | Source files | Status |
|---|---|---|---|
| Online Resource 1 | Frozen target registry and source provenance | `data/dude_targets.csv`, `results/dude_receptor_audit.csv` | Available |
| Online Resource 2 | Strict mmCIF audit, including retained failures | `results/rcsb_mmcif_preparation_audit.csv`, `results/dude_rcsb_element_mapping.csv` | Available |
| Online Resource 3 | BRAF pose-recovery records and configuration | `results/braf_*`, `protocol/braf_3d4q_vina_reference.conf` | Available |
| Online Resource 4 | KIF11 pose-recovery records and configuration | `results/kif11_*`, `protocol/kif11_3cjo_vina_reference.conf` | Available |
| Online Resource 5 | Reproducibility checker and SHA-256 manifest | `scripts/verify_frozen_evidence.py` plus its emitted manifest | Available |
| Online Resource 6 | RCSB legacy-PDB comparator manifest and target-level output table | `validation/rcsb_legacy_pdb_*_20260809.csv`, `validation/README.md` | Available |
| Online Resource 7 | Human independent-review record | Signed or dated review log, commit SHA, findings | Pending |

## Repository and archive citation

The manuscript should cite the versioned GitHub release and Zenodo record:

- Software release: `v0.2.0`.
- Archive DOI: `10.5281/zenodo.21866318`.
- Repository: `https://github.com/sircalch/dude-receptor-prep-audit`.

Raw DUD-E and RCSB coordinate files are not redistributed. The supplementary
material should preserve identifiers, source URLs, checksums, protocols, and
derived evidence rather than copying third-party coordinate archives.
