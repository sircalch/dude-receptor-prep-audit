# DUD-E receptor-preparation compatibility audit: a reproducible workflow for strict preparation and reference-pose recovery

Andrés Monreal Hernández¹*, Sara Lizbeth Franco Amaya¹, Carlos Ivanhoe Martínez Osorio²

¹ Doctorado en Nanotecnología, Universidad de Sonora, México

² Doctorado en Ciencia de Materiales, Universidad de Sonora, México

* Corresponding author: andres.monreal@ues.mx

## Abstract

**Background:** Receptor preparation choices are often difficult to inspect or
reproduce in molecular-docking workflows. We developed an open workflow that
records strict receptor-preparation outcomes, source checksums, component
selection, and bounded reference-pose recovery results.

**Methods:** The workflow audits original DUD-E receptor PDB files using a
declared Meeko pathway without repair or bypass options. It then qualifies an
RCSB mmCIF alternative and records all observable outcomes. Two independent
reference-pose campaigns use frozen source structures, reconciled ligand
components, explicit receptor/cofactor policies, and one fixed AutoDock Vina
configuration per target. Pose recovery is measured by identity-mapped,
aligned heavy-atom RMSD.

**Results:** The repository provides 102 strict DUD-E receptor attempts,
authoritative mapping and mmCIF-preparation tables, and two completed reference
campaigns. For BRAF 3D4Q/SM5, the top-scoring pose had RMSD 1.134 Å. For KIF11
3CJO/K30, the top-scoring pose had RMSD 1.477 Å; this model retained ADP and
Mg²⁺ and records Meeko's automatically constructed ADP template as a
limitation. All nine poses from each run are retained.

**Conclusions:** The software provides an auditable framework for documenting
strict preparation and reference-pose recovery. Its outputs are computational
observations only and do not establish experimental affinity, biological
activity, safety, or therapeutic effect.

## Keywords

Molecular docking; reproducibility; receptor preparation; Meeko; AutoDock Vina;
DUD-E; research software.

## Introduction

The workflow addresses a practical reproducibility problem: a reported docking
result is difficult to interpret when its structural source, preparation
choices, and output-selection rules are not retained. The tool stores compact,
reviewable evidence rather than redistributing source coordinates.

## Methods

### Implementation

The project comprises Python scripts, versioned CSV result tables, Markdown
protocols, and deterministic SVG figures. It uses Gemmi for structural parsing,
Meeko for receptor and ligand preparation, and AutoDock Vina for the two
predeclared reference calculations. The GitHub workflow compiles scripts,
regenerates deterministic evidence, and rejects unexpected differences.

### Operation

Users provide a frozen target registry, local directories for source structures
and tool outputs, and the path to `mk_prepare_receptor`. The baseline audit can
be started with:

```sh
python scripts/fetch_dude_registry.py data/dude_targets.csv
python scripts/audit_dude_receptors.py data/dude_targets.csv external-data audit-output results/dude_receptor_audit.csv --meeko-command /path/to/mk_prepare_receptor
```

Reference-pose campaigns are intentionally separate protocols, not defaults for
arbitrary targets. They require a declared cofactor policy and fixed inputs
before execution.

## Use cases and outputs

The baseline use case reports whether each DUD-E receptor passes a direct,
no-bypass Meeko preparation attempt. The BRAF and KIF11 use cases demonstrate
how a deposited ligand can be reconciled with its component definition,
prepared under stated choices, and compared to all Vina output poses. The
two-target panel is in `results/reference_pose_recovery_panel.csv`.

## Availability

Source code is MIT licensed at
https://github.com/sircalch/dude-receptor-prep-audit. A permanent Zenodo archive
and DOI must be inserted here after the authors approve release version 0.2.0.
Raw coordinates, prepared PDBQT files, and tool logs are kept local; versioned
checksums and non-coordinate summaries describe their provenance.

## Author contributions

To be finalized and approved by all authors before submission using CRediT
roles. The final submission must reflect actual contributions.

## Competing interests

The authors declare no competing interests.

## Grant information

No external funding supported this work; the authors used available local
computing resources.

## References to verify and format before submission

1. DUD-E resource.
2. RCSB Protein Data Bank resource.
3. Meeko documentation and citation.
4. AutoDock Vina citations.
5. Primary structure papers for 3D4Q and 3CJO.
