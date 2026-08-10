# JMM evidence matrix

This internal matrix separates reproducible observations from statements that
would require interpretation. It is not submission prose. Every row marked
**ready** links to a frozen or independently reproduced artefact; rows marked
**pending** must not be presented as completed results.

| Proposed manuscript element | Evidence that may be reported | Primary artefact | Independent status | Editorial limit |
|---|---|---|---|---|
| Direct-input audit | All 102 strict direct DUD-E receptor attempts failed; the recorded mechanism was blank PDB element fields. | `results/dude_receptor_audit.csv` | Ready: byte-identical independent reproduction recorded in `reports/INDEPENDENT-DUDE-REPRODUCTION-2026-08-09.md`. | Applies to this frozen input set and declared preparation route only. |
| Alternative source route | Strict direct preparation from RCSB mmCIF produced 26 successes in 102 attempts; all remaining outcomes and reasons must be reported. | `results/rcsb_mmcif_preparation_audit.csv` | Pending completion of the running independent full-set reproduction. | Not a claim that mmCIF universally resolves receptor preparation. |
| BRAF reference-pose case | For 3D4Q/SM5, nine Vina poses were generated; top-score RMSD was 1.134 Å and lowest RMSD was 1.083 Å. | `results/braf_sm5_reference_pose_recovery.csv` | Ready: byte-identical independent campaign recorded in `reports/INDEPENDENT-REFERENCE-POSE-REPRODUCTION-2026-08-09.md`. | A pose-recovery observation, not affinity, potency, or therapeutic evidence. |
| KIF11 reference-pose case | For 3CJO/K30, nine Vina poses were generated; top-score RMSD was 1.477 Å and lowest RMSD was 1.316 Å. | `results/kif11_k30_reference_pose_recovery.csv` | Ready: byte-identical independent campaign recorded in `reports/INDEPENDENT-REFERENCE-POSE-REPRODUCTION-2026-08-09.md`. | Preserve the retained ADP/Mg policy and the recorded Meeko limitation. |
| Execution environment | The historical mmCIF run used Windows, Python 3.13.5, Meeko 0.7.1, RDKit 2026.3.5, and ProDy 2.6.1. | `protocol/JMM-ENVIRONMENT-MANIFEST.md` | Ready as an environment record. | This records provenance; it does not establish portability across all platforms. |
| Reproducibility controls | Frozen checksums, deterministic figure renderers, fixed Vina configurations, and verification scripts are available. | `scripts/verify_frozen_evidence.py`, `protocol/`, `reports/` | Ready for the direct audit and both pose cases. | A clean-environment full rerun and comparator study remain separate gates. |
| Comparator preparation workflow | No comparison result exists yet. | `protocol/JMM-VALIDATION-PROTOCOL.md` | Pending. | Do not describe a comparator as performed until its protocol and outputs are frozen and independently checked. |

## Sources-to-claim map

Use the verified reference seed only where it supports the corresponding
methodological context, never as evidence for this repository's numerical
results.

| Contextual statement | Appropriate source(s) from `JMM-REFERENCES-VERIFIED.md` |
|---|---|
| DUD-E dataset provenance and benchmarking context | 1 |
| RCSB structure source and format provenance | 2 |
| Docking engine and configuration context | 3–4 |
| Coordinate parsing and structural analysis software | 5–7, 12 |
| FAIR/reproducibility framing | 8–9 |
| Identity of the two reference-ligand case studies | 10–11 |

## Author-review gate

Before any manuscript draft is submitted, all authors must check each numeric
row against the stated artefact, decide which contextual claims are warranted,
and write or substantially revise the scientific narrative in their own words.
The contribution of software-assisted formatting or language editing should be
described accurately in the journal's requested disclosure field, while the
authors retain responsibility for the methods, results, interpretation, and
final text.
