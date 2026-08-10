# Strict receptor preparation and reference-pose recovery: a reproducible two-target docking audit

Andrés Monreal Hernández¹*, Sara Lizbeth Franco Amaya¹, Carlos Ivanhoe Martínez Osorio²

¹ Doctorado en Nanotecnología, Universidad de Sonora, México

² Doctorado en Ciencia de Materiales, Universidad de Sonora, México
* Corresponding author: andres.monreal@ues.mx

## Abstract

Reproducible molecular-docking studies require that receptor and ligand
preparation choices are stated and verifiable. We first conducted a strict
software-compatibility audit of 102 DUD-E receptor files and then developed two
independent, frozen reference-pose recovery campaigns using human BRAF (3D4Q,
SM5) and KIF11 (3CJO, K30). Each campaign retained source checksums, explicit
component-selection rules, Meeko preparation records, a frozen AutoDock Vina
configuration, and all output poses. The BRAF top-scoring pose had a mapped
heavy-atom RMSD of 1.134 Å and the lowest observed RMSD was 1.083 Å. The KIF11
top-scoring pose had RMSD 1.477 Å and the lowest observed RMSD was 1.316 Å;
this model retained ADP and Mg²⁺, with ADP handled through an automatically
constructed Meeko template. These are reproducible computational observations,
not experimental affinity, efficacy, or cancer-treatment claims. The repository
provides an auditable basis for extending the work through separately
pre-specified campaigns.

## 1. Introduction

Docking workflows often depend on unstated choices in structural source,
receptor preparation, ligand state, cofactors, search settings, and pose
comparison. These choices can make a workflow difficult to reproduce even
before prospective compounds are considered. This work asks a deliberately
narrow question: can strictly documented source structures be prepared and used
for deposited-reference pose recovery under a frozen workflow?

## 2. Methods

### 2.1 Receptor compatibility audit

The repository-wide audit downloaded original DUD-E receptor PDB files and
attempted direct Meeko preparation without repairs, deletion bypasses,
alternate-location selection, template overrides, ligand preparation, or
docking. A follow-up used official RCSB mmCIF structures as a source
alternative. Raw coordinates and tool output remain local; checksums and
non-coordinate result tables are versioned.

### 2.2 Reference-pose campaigns

BRAF 3D4Q and KIF11 3CJO were selected from the strict mmCIF direct-success
subset. For each target, the RCSB chemical-component definition and one
deposited ligand instance were reconciled before ligand preparation. Vina 1.2.7
was run once per frozen configuration with CPU=1, seed=20260809,
exhaustiveness=16, num_modes=9, min_rmsd=1.0 Å, and energy_range=3.0 kcal/mol.
Pose recovery used identity-mapped, aligned heavy-atom RMSD against the
deposited ligand instance.

For BRAF, the receptor was author chain A polymer only. For KIF11, author chain
A polymer plus deposited ADP and Mg²⁺ were retained; K30 and waters were
excluded. Meeko automatically constructed an ADP template, which is retained
as an explicit limitation.

## 3. Results

| Target | Reference ligand | Top-score pose | RMSD of top-score pose | Lowest RMSD | Principal limitation |
|---|---|---:|---:|---:|---|
| BRAF 3D4Q | SM5 | −10.929 kcal/mol | 1.134 Å | 1.083 Å | No binary RMSD threshold was predeclared. |
| KIF11 3CJO | K30 | −10.994 kcal/mol | 1.477 Å | 1.316 Å | ADP template was constructed automatically by Meeko. |

The complete two-target table is generated from versioned pose tables in
`results/reference_pose_recovery_panel.csv`. The BRAF campaign includes a
versioned all-pose figure. All nine output poses for each target were retained
in their respective result tables.

## 4. Discussion

The two workflows produced numerical reference-pose recovery observations under
fully stated settings. Their values should not be generalized as a benchmark of
all docking systems, because the sample contains two target-ligand cases and
only one run per configuration. The KIF11 result further demonstrates why
cofactor treatment must be a declared methodological choice rather than an
implicit preprocessing step.

The study does not measure binding affinity, selectivity, cell response,
toxicity, pharmacokinetics, or therapeutic effect. It therefore cannot support
claims about anticancer activity. Its contribution is an auditable workflow and
evidence boundary suitable for future, independently pre-specified extensions.

## 5. Conclusions

Strict source tracking, explicit structural selections, frozen docking settings,
and all-pose reporting make a modest docking study inspectable and reproducible.
The BRAF and KIF11 reference campaigns provide two documented examples; any
prospective screen or additional target should be treated as a new protocol.

## Data and code availability

Code, tracked result tables, protocols, and deterministic figures are available
in this repository. Source coordinate files, locally prepared PDBQT files, and
tool logs are excluded from version control but represented by checksums.

## Declarations

Funding: This work used the authors' available local computing resources.

Conflicts of interest: The authors declare no conflicts of interest.
Author contributions: To be finalized and confirmed by all authors before submission.

## References to complete before submission

1. DUD-E resource reference.
2. RCSB Protein Data Bank reference.
3. Meeko reference and versioned documentation.
4. AutoDock Vina references.
5. Primary structural references for 3D4Q and 3CJO.
