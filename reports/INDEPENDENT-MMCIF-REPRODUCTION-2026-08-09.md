# Independent mmCIF preparation reproduction — 2026-08-09

## Scope

This report records an independent, full rerun of the strict RCSB mmCIF
preparation audit. It is deliberately reported as a non-identical reproduction:
the generated CSV must not replace, amend, or be combined with the frozen
v0.2.0 result.

## Reproduction conditions

- Input set: the same 102 target/PDB records as the frozen audit.
- Input identity: the mmCIF SHA-256 for every compared row was unchanged.
- Preparation route: `scripts/audit_rcsb_mmcif_preparation.py`, strict direct
  preparation, Meeko 0.7.1, and the declared 300-second per-structure timeout.
- Checkpointed output: an ignored local audit-output directory, retained for
  the local verification run and not published as a release artefact.

## Comparison result

| CSV | SHA-256 | Direct successes | Direct failures |
|---|---|---:|---:|
| Frozen `results/rcsb_mmcif_preparation_audit.csv` | `42f24d02fa4ab5d8881b15216d3f420466a0172adfb122a21bf91e8d4ef4544f` | 26 | 76 |
| Independent reproduction | `39a678433ed6e2e380fe1b633672d71c50870721d6201b3d56581b8e25156e45` | 27 | 75 |

`scripts/verify_frozen_evidence.py --compare-mmcif-reproduction` correctly
failed because the two tables are not byte-identical.

## Single discordant record

| Target | PDB ID | mmCIF SHA-256 | Frozen outcome | Independent outcome |
|---|---|---|---|---|
| dpp4 | 2i78 | `4c01c0b72f18b43d9525c31356ec0e3a6da8f6431de717144c23d87fef80cd2f` | `preparation_timeout` after 300 s | `direct_success`, 2,504,115-byte PDBQT |

All other 101 records agreed in the comparison. The frozen outcome should be
retained because it is the released observation under its original runtime
conditions. This independent rerun shows that the outcome for this large
structure is sensitive to execution time or runtime conditions despite using
the same source file and nominal timeout; it does not demonstrate an error in
the source-file checksum nor license a general conclusion about mmCIF
preparation.

## Consequence for the manuscript

The manuscript must report the frozen 26/102 result as the versioned audit
result and disclose this one-record non-identical rerun in reproducibility
materials if the mmCIF route is discussed. It must not claim a fully
byte-identical independent reproduction for the mmCIF audit. A future
validation study may investigate timing/resource sensitivity using a
predeclared runtime measurement protocol; no such comparator result exists
yet.
