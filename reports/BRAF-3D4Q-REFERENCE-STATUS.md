# BRAF 3D4Q reference campaign: current status

## What is established

The strict source-alternative audit previously recorded direct Meeko receptor
preparation success for BRAF entry 3D4Q.  That is a software-compatibility
observation, not a docking validation.

The deposited 3D4Q mmCIF contains two SM5 ligand instances, each with 28
non-hydrogen atoms: author chain A, residue 1, and author chain B, residue 1.
Their coordinates and candidate padded boxes are reproducibly summarized in
[`results/braf_3d4q_reference_metadata.csv`](../results/braf_3d4q_reference_metadata.csv).
The frozen RCSB chemical-component definition agrees on 28 heavy atoms and
documents the deposited neutral baseline; its auditable summary is
[`results/braf_sm5_component_qualification.csv`](../results/braf_sm5_component_qualification.csv).
The deposited chain-A coordinate record has also been extracted locally without
modification: its 28 atom identities and elements reconcile exactly with the
component definition, while the 23 definition hydrogens are correctly absent
from the deposited X-ray instance. The checksums and counts are in
[`results/braf_sm5_chain_a_extraction.csv`](../results/braf_sm5_chain_a_extraction.csv).
The matching BRAF chain-A receptor was prepared successfully under the strict
Meeko pathway; the selection rule, exclusions, command, version, outputs, and
checksums are in
[`results/braf_chain_a_receptor_preparation.csv`](../results/braf_chain_a_receptor_preparation.csv).
The engine, binary hash, seed, search parameters, and fixed box have been
predeclared in
[`protocol/braf_3d4q_vina_reference.conf`](../protocol/braf_3d4q_vina_reference.conf)
and summarized in
[`results/braf_3d4q_vina_reference_configuration.csv`](../results/braf_3d4q_vina_reference_configuration.csv).

## What is deliberately not yet claimed

The single, predeclared SM5 reference run is complete. Its pose-recovery table
contains all nine Vina poses and identity-mapped, aligned heavy-atom RMSD
values. The top-scoring pose was −10.929 kcal/mol with RMSD 1.134 Å; the lowest
RMSD observed was 1.083 Å for model 3. No pass/fail threshold was declared in
advance, so these are numerical observations rather than a binary validation
claim.

There are no library screens, ranking results beyond this reference ligand,
experimental affinity estimates, or cancer-related efficacy claims.

## Next auditable action

The defined reference-pose campaign is complete. Any extension (an independent
repeat, protonation sensitivity analysis, additional targets, or a screened
compound set) requires a separate pre-specified protocol rather than altering
this record.
