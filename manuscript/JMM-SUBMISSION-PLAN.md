# Journal of Molecular Modeling submission plan

## Target and article type

**Target journal:** *Journal of Molecular Modeling* (Springer Nature).

**Planned article type:** Software Report, with an alternative classification as
an Original Paper only if the expanded validation supports a methodological
claim beyond the software implementation.

**Working title:** *A reproducible audit workflow for receptor preparation and
reference-pose recovery in molecular docking*.

This plan is an internal editorial and validation record. It is not a
submission manuscript and must not be uploaded to a journal system.

## Evidence already available

| Evidence item | Current factual result | Repository location |
|---|---:|---|
| Strict direct DUD-E receptor attempts | 102 of 102 fail because the input PDB files contain blank element fields | `results/dude_receptor_audit.csv` |
| RCSB mmCIF alternative, strict direct preparation | 26 of 102 direct successes | `results/` and audit outputs |
| BRAF reference-pose recovery | 3D4Q/SM5; 9 Vina poses; top-score RMSD 1.134 A; lowest RMSD 1.083 A | `results/reference_pose_recovery_panel.csv` |
| KIF11 reference-pose recovery | 3CJO/K30; 9 Vina poses; top-score RMSD 1.477 A; lowest RMSD 1.316 A | `results/reference_pose_recovery_panel.csv` |
| Frozen release | v0.2.0, DOI 10.5281/zenodo.21866318 | Zenodo and GitHub release |
| Independent direct DUD-E reproduction | 102 rows; byte-identical to the frozen audit CSV | `reports/INDEPENDENT-DUDE-REPRODUCTION-2026-08-09.md` |
| Independent mmCIF reproduction | 101 of 102 rows agree; 2I78 changed from a 300-second timeout to a direct success | `reports/INDEPENDENT-MMCIF-REPRODUCTION-2026-08-09.md` |
| 2I78 timing follow-up | Three predeclared attempts all succeeded in 147.002–160.443 s and yielded byte-identical PDBQT files | `reports/DPP4-2I78-TIMING-SENSITIVITY-2026-08-09.md` |

All reported values are computational observations. They do not establish
binding affinity, biological activity, safety, or therapeutic effect.

## Required validation before drafting the final paper

1. Completed: investigate the observed timing/resource sensitivity of 2I78
   with a predeclared runtime-measurement protocol. Preserve the frozen v0.2.0
   table; a non-identical rerun is a reported result, not a reason to
   overwrite it.
2. Completed: define and execute the RCSB legacy-PDB direct-reader comparator
   with recorded source manifests, commands, inputs, output criteria, and all
   outcomes; see `reports/RCSB-LEGACY-PDB-COMPARATOR-2026-08-09.md`.
3. Completed for the selected comparator: predefine success/failure criteria
   and retain failures. No comparison was introduced to improve a result.
4. Repeat the BRAF and KIF11 reference-pose campaigns under the declared
   configuration, preserving all output poses and seeds.
5. Add a target-stratified summary of the 102-attempt audit, including the
   observed blank-element failure mechanism and the limits of the mmCIF route.
6. Independently review the code, tables, and interpretation against raw
   outputs. Record reviewer name, date, commit SHA, and any changes.
7. Audit all references from primary or official sources. The final manuscript
   must not claim that a tool or data source has a capability not documented by
   its original source.

## Final manuscript architecture

The authors must write and approve the scientific narrative after the evidence
review. This section fixes the order and factual content to be covered.

### Title page

- Title, running title, all author names, ORCIDs, institutional affiliations,
  corresponding-author email, and author-contribution statement.
- Funding: no external funding; available local computing resources.
- Competing interests: none declared.

### Structured abstract

JMM requires the exact headings **Context** and **Methods**. The abstract must
state the 102/102 result, 26/102 result, both reference-pose examples, the
software versions, and the restriction that no biological or clinical claim is
made. It must not cite references.

### 1. Introduction

- Reproducibility problem in docking receptor preparation.
- Why preserving source identity, preparation choices, and all output poses is
  necessary for an auditable workflow.
- Specific gap addressed by the software.
- Explicit objective and testable scope.

### 2. Materials and methods

#### 2.1 Source registry and provenance
Describe the DUD-E registry, RCSB retrieval route, checksums, and the rule that
source coordinates are not redistributed.

#### 2.2 Strict preparation audit
Define the no-repair/no-bypass Meeko pathway, allowed input route, failure
capture, result schema, and reproducibility controls.

#### 2.3 mmCIF alternative and comparator protocol
Describe the predeclared alternative and any comparator only after it has been
implemented and independently reproduced.

#### 2.4 Reference-pose recovery protocol
State target PDB IDs, ligand component IDs, cofactor policy, receptor and
ligand preparation, Vina version and fixed configuration, identity mapping,
alignment, and heavy-atom RMSD calculation.

#### 2.5 Software availability and execution
State release tag, Zenodo DOI, MIT license, environment requirements, and the
commands required to reproduce the audit.

### 3. Results

#### 3.1 Audit outcomes across the DUD-E set
Report the strict direct 102/102 failures and the observed blank-element
mechanism without generalizing beyond the evaluated files and versions.

#### 3.2 Alternative-source qualification
Report the 26/102 mmCIF successes together with exclusions and unresolved
cases. Include a target-stratified table after independent validation.

#### 3.3 Reference-pose recovery cases
Report all nine poses for BRAF and KIF11; distinguish top-score from
lowest-RMSD values; describe retained ADP/Mg and the recorded Meeko limitation
for KIF11.

#### 3.4 Comparator results
Include only predeclared, reproducible comparisons produced during the planned
validation. Keep negative and inconclusive results.

### 4. Discussion

- Explain the practical value of an audit trail rather than claiming a universal
  best preparation workflow.
- Separate reproducibility evidence from docking-performance claims.
- Discuss scope limits: two reference-pose cases, software/version dependence,
  source-file limitations, and no experimental validation.

### 5. Conclusions

State only the evidence-supported contribution: a reusable, provenance-aware
audit and reference-pose recovery workflow.

### Declarations and supplementary material

- CRediT roles, funding, competing interests, data/code availability, and
  software citation.
- Supplementary files: target registry; result tables; exact commands; versions;
  full BRAF/KIF11 pose panels; and validation checklist.

## Figures and tables

1. **Figure 1:** Workflow diagram from source registry to strict audit,
   alternative-source check, and reference-pose analysis.
2. **Figure 2:** Outcome summary for 102 DUD-E direct attempts and the mmCIF
   alternative, with denominators shown.
3. **Figure 3:** BRAF and KIF11 reference-pose recovery panel, displaying all
   poses or an accessible summary linked to the full table.
4. **Figure 4:** Strict preparation comparison across original DUD-E PDB,
   RCSB mmCIF, and RCSB legacy-PDB conditions, with all denominators shown.
5. **Table 1:** Reproducibility manifest: software, versions, configurations,
   seeds, input IDs, result files, and checksums.
6. **Table 2:** Target-level audit outcomes and exclusions, including the
   separate legacy-PDB comparator condition.
7. **Table 3:** Reference-pose results, including top-score and lowest-RMSD
   values without conflating the selection rules.

## Editorial and integrity gates

- English must receive final human scientific editing before submission.
- Every author must approve the final wording, author order, affiliation, and
  CRediT statement.
- A transparent declaration must describe any AI assistance used for code or
  manuscript organization, while authors retain responsibility for the final
  article.
- All manuscript claims must be traceable to a release, script, raw output, or
  cited primary source.
- Select the traditional publication route unless funding for Open Choice is
  expressly obtained; do not assume an APC waiver.
- Do not submit simultaneously to another journal.
