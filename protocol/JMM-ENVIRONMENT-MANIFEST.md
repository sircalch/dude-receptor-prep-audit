# JMM reproducibility environment manifest

## Historical preparation environment used for the mmCIF audit

The independent mmCIF reproduction is executed with the retained environment
referenced by the original preparation logs.

| Component | Observed version |
|---|---:|
| Operating system | Windows NT 10.0.26200.0, 64-bit |
| Python | 3.13.5 |
| Meeko | 0.7.1 |
| RDKit | 2026.3.5 |
| ProDy | 2.6.1 |

## Execution invariants

- Frozen registry: `data/dude_targets.csv`.
- Original DUD-E PDB route: direct `--read_pdb` input only.
- RCSB source-alternative route: direct `--read_with_prody` mmCIF input only.
- One preparation attempt per source structure.
- No repair, residue deletion, alternate-location selection, template override,
  minimization, ligand preparation, or docking is part of either audit.
- Local raw coordinates and logs are retained under ignored directories; only
  derived checksums and result summaries are versioned.

## Separate reference-pose environment

The BRAF and KIF11 reference-pose campaigns use their committed configuration
files. Their independent rerun must additionally record the exact AutoDock Vina
1.2.7 executable, binary checksum, seed, CPU count, and output pose files.
This record does not claim that such a rerun has been completed.
