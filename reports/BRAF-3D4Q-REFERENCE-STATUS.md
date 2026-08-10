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

## What is deliberately not yet claimed

There are no ligand-preparation outputs, docking runs, recovered poses, RMSD
values, docking scores, ranking results, affinity estimates, or cancer-related
efficacy claims.  Consequently, no validation result exists yet.

## Next auditable action

The next action is Gate 4 in the
[qualification protocol](../protocol/BRAF-3D4Q-REFERENCE-LIGAND-QUALIFICATION.md):
freeze the docking engine and all calculation settings before a single run. Only
after the listed gates are complete may a reference-pose calculation be run.
