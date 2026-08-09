# DUD-E receptor-preparation compatibility audit

This repository records a strict, reproducible audit of whether the original
receptor PDB files made available by DUD-E can be processed directly by a
declared version of Meeko. It does not repair structures, generate ligands, run
docking, estimate affinities, or make biological claims.

## Question

For the frozen DUD-E target registry, how often does each original receptor
file pass a direct, no-bypass receptor-preparation attempt, and which observable
file characteristics accompany failures?

## Strict method

- Download only `https://dude.docking.org/targets/<target>/receptor.pdb`.
- Preserve raw source files and command logs locally under ignored directories.
- Run Meeko with `--read_pdb` and `--write_pdbqt` only.
- Never use `--allow_bad_res`, alternate-location selection, residue deletion,
  repair, minimization, template override, another converter, ligand
  preparation, or docking.
- Publish source checksums and non-sensitive audit summaries, not receptor
  coordinate files.

The exact protocol is in
[protocol/AUDIT-PROTOCOL.md](protocol/AUDIT-PROTOCOL.md). Results are
descriptive software-compatibility observations only.

## Results

The completed strict audit and its versioned figures are in
[reports/AUDIT-RESULTS.md](reports/AUDIT-RESULTS.md).
The follow-up authoritative element-mapping qualification is documented in
[reports/ELEMENT-MAPPING-RESULTS.md](reports/ELEMENT-MAPPING-RESULTS.md).
The strict source-alternative mmCIF audit is in
[reports/RCSB-MMCIF-PREPARATION-RESULTS.md](reports/RCSB-MMCIF-PREPARATION-RESULTS.md).

## Reproduction

1. Freeze the target registry:

   ```sh
   python scripts/fetch_dude_registry.py data/dude_targets.csv
   ```

2. Run the audit with the installed Meeko executable:

   ```sh
   python scripts/audit_dude_receptors.py data/dude_targets.csv external-data audit-output results/dude_receptor_audit.csv --meeko-command /path/to/mk_prepare_receptor
   ```

The script can be resumed safely. Raw coordinates, PDBQT files and logs remain
local; the results table records checksums and observed statuses.

## Limits

A successful PDBQT conversion is not validation of a binding pose, docking
score, enrichment, affinity, biological activity, efficacy, safety, or clinical
utility. A failure is likewise a compatibility observation under one strict
software configuration, not a statement that a target is unsuitable for all
docking workflows.
