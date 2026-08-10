# DUD-E receptor-preparation compatibility audit: a reproducible workflow for strict preparation and reference-pose recovery

> Submission status: journal-neutral manuscript. It must not be submitted to
> F1000Research because its current generative-AI policy is incompatible with
> the documented use of AI assistance in this software project. A journal whose
> policy permits transparent AI disclosure must be selected before submission.

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
choices, and output-selection rules are not retained. DUD-E is a widely used
benchmarking resource for docking workflows [1]. The tool stores compact,
reviewable evidence rather than redistributing source coordinates obtained from
DUD-E and the RCSB Protein Data Bank (RCSB PDB) [1,2].

## Methods

### Implementation

The project comprises Python scripts, versioned CSV result tables, Markdown
protocols, and deterministic SVG figures. It uses Gemmi for structural parsing,
Meeko for receptor and ligand preparation [3], and AutoDock Vina 1.2.7 for the
two predeclared reference calculations [4,5]. The GitHub workflow compiles
scripts, regenerates deterministic evidence, and rejects unexpected differences.

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
no-bypass Meeko preparation attempt. The BRAF and KIF11 use cases use the
deposited 3D4Q/SM5 and 3CJO/K30 structures, respectively [6,7], to demonstrate
how a deposited ligand can be reconciled with its component definition,
prepared under stated choices, and compared to all Vina output poses. The
two-target panel is in `results/reference_pose_recovery_panel.csv`.

## Availability

Source code is MIT licensed at
https://github.com/sircalch/dude-receptor-prep-audit. The frozen v0.2.0
software-and-evidence archive is available from Zenodo at
https://doi.org/10.5281/zenodo.21866318. Raw coordinate inputs remain available
from their original DUD-E and RCSB PDB sources; they are not redistributed in
the archive. Versioned source URLs, checksums, derived result tables, protocols,
and deterministic figures are included in the repository and Zenodo archive.

## Author contributions (CRediT)

Sara Lizbeth Franco Amaya: Conceptualization; Writing – review & editing.

Carlos Ivanhoe MartÃ­nez Osorio: Methodology.

AndrÃ©s Monreal HernÃ¡ndez: Data curation; Formal analysis; Investigation;
Software; Visualization; Writing – original draft.

All authors reviewed the manuscript, approved the author order, and accept
responsibility for the final submitted version.

## Competing interests

The authors declare no competing interests.

## Grant information

No external funding supported this work; the authors used available local
computing resources.

## Declaration of generative AI and AI-assisted technologies

During development of this work and preparation of the manuscript, the authors
used OpenAI Codex (GPT-5) as assistance for software and document organization.
The authors reviewed and edited the resulting material and take full
responsibility for the scientific decisions, computational work, references,
figures, and final content.

## References

1. Mysinger MM, Carchia M, Irwin JJ, Shoichet BK. Directory of Useful Decoys,
Enhanced (DUD-E): Better Ligands and Decoys for Better Benchmarking. *Journal
of Medicinal Chemistry*. 2012;55(14):6582-6594.
https://doi.org/10.1021/jm300687e

2. Burley SK, Bhikadiya C, Bi C, et al. RCSB Protein Data Bank (RCSB.org):
delivery of experimentally-determined PDB structures alongside one million
computed structure models of proteins from artificial intelligence/machine
learning. *Nucleic Acids Research*. 2023;51(D1):D488-D508.
https://doi.org/10.1093/nar/gkac1077

3. Forli Lab. Meeko version 0.7.1 [software]. Python Package Index; 2025.
https://pypi.org/project/meeko/0.7.1/

4. Trott O, Olson AJ. AutoDock Vina: improving the speed and accuracy of docking
with a new scoring function, efficient optimization, and multithreading.
*Journal of Computational Chemistry*. 2010;31(2):455-461.
https://doi.org/10.1002/jcc.21334

5. Eberhardt J, Santos-Martins D, Tillack AF, Forli S. AutoDock Vina 1.2.0: New
Docking Methods, Expanded Force Field, and Python Bindings. *Journal of Chemical
Information and Modeling*. 2021;61(8):3891-3898.
https://doi.org/10.1021/acs.jcim.1c00203

6. Hansen JD, Grina J, Newhouse B, et al. Potent and selective pyrazole-based
inhibitors of B-Raf kinase. *Bioorganic & Medicinal Chemistry Letters*.
2008;18:4692-4695. https://doi.org/10.1016/j.bmcl.2008.07.002

7. Cox CD, Coleman PJ, Breslin MJ, et al. Kinesin spindle protein (KSP)
inhibitors. 9. Discovery of MK-0731 for the treatment of taxane-refractory
cancer. *Journal of Medicinal Chemistry*. 2008;51:4239-4252.
https://doi.org/10.1021/jm800386y
