# Audit protocol: strict DUD-E receptor preparation

## Study type

This is a descriptive reproducibility and software-compatibility audit. Its
unit of analysis is one DUD-E target receptor file from the target registry
snapshot stored in `data/dude_targets.csv`.

## Frozen workflow

For each target, download only its original DUD-E `receptor.pdb`, compute a
SHA-256 checksum, inspect fixed-width PDB fields, and invoke the declared Meeko
executable exactly once with `--read_pdb`, `--output_basename`, and
`--write_pdbqt`.

The audit records source URL, download status, file size, checksum, ATOM and
HETATM record counts, blank PDB-element fields, alternate-location records,
chain identifiers, process exit status, PDBQT existence/size, and a concise
error classification. Full logs remain local and ignored.

## Forbidden actions

No `--allow_bad_res`, `--default_altloc`, `--wanted_altloc`, deletion, repair,
minimization, protonation policy, ligand preparation, grid generation, Vina
execution, score calculation or target substitution is permitted.

## Outcome definitions

- **direct_success**: Meeko exits with code zero and produces a nonempty PDBQT.
- **direct_failure**: the direct process exits nonzero or no nonempty PDBQT is
  produced.
- **download_failure**: source acquisition did not complete; no preparation is
  attempted.

The observed outcome is limited to this exact software configuration and does
not establish structural quality or docking performance.

## Reporting

Report every registry entry, including download failures. Do not pool results
with docking outcomes and do not omit failures. The result table and registry
are versioned; raw receptor files, PDBQT files and logs are not redistributed.

## Sources

- DUD-E target registry: <https://dude.docking.org/targets>
- Meeko receptor-preparation documentation:
  <https://github.com/forlilab/Meeko/blob/develop/docs/source/cli_rec_prep.rst>
