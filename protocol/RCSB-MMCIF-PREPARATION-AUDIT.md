# Phase 3 protocol: strict RCSB mmCIF receptor preparation audit

This is a source-alternative compatibility audit, separate from the original
DUD-E receptor audit. For the same frozen 102 PDB IDs, it uses the official
RCSB PDBx/mmCIF coordinate files already checksummed in Phase 2.

For each file, Meeko is invoked once with `--read_with_prody`,
`--output_basename`, and `--write_pdbqt`. No DUD-E coordinate is changed or
used as an input. No `--allow_bad_res`, alternate-location selection, deletion,
repair, minimization, template override, ligand preparation or docking is
permitted.

An outcome is `direct_success` only if the process exits zero and produces a
nonempty PDBQT. This establishes source/software compatibility only; it is not
validation of receptor choice, pose, score, affinity or biological activity.
