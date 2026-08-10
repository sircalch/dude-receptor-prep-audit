# DPP4 / 2I78 timing-sensitivity result — 2026-08-09

## Predeclared question

This focused follow-up used the protocol in
`protocol/DPP4-2I78-TIMING-SENSITIVITY-PROTOCOL.md` to test whether the
strict direct mmCIF preparation result for DPP4/2I78 was repeatable under the
same archived source and a 300-second timeout.

## Conditions

- Source: `external-data/rcsb-mmcif/2i78.cif`.
- Source SHA-256:
  `4c01c0b72f18b43d9525c31356ec0e3a6da8f6431de717144c23d87fef80cd2f`.
- Three sequential attempts, each with strict direct `--read_with_prody`
  preparation, Meeko 0.7.1, and a 300-second timeout.
- No coordinate repair, alternate-location selection, template addition, or
  parameter tuning.

## Results

| Attempt | Wall time (s) | Outcome | PDBQT bytes | PDBQT SHA-256 |
|---:|---:|---|---:|---|
| 1 | 147.002 | direct success | 2,504,115 | `4968b8dbf2ee0146f254040c78e6de48a1b0ed86122e8879bae5eae59b083d4a` |
| 2 | 151.585 | direct success | 2,504,115 | `4968b8dbf2ee0146f254040c78e6de48a1b0ed86122e8879bae5eae59b083d4a` |
| 3 | 160.443 | direct success | 2,504,115 | `4968b8dbf2ee0146f254040c78e6de48a1b0ed86122e8879bae5eae59b083d4a` |

Mean wall time was 153.010 seconds (range 147.002–160.443 seconds). The
local ignored summary CSV has SHA-256
`0ac67abb236393ed91f2794067728676492532ef84c8f8758f1d85de250ab68f`.

## Interpretation

All three predeclared attempts succeeded within the nominal timeout and
produced byte-identical PDBQT outputs. Together with the earlier full rerun,
this shows that the original frozen 300-second timeout for 2I78 was not
reproduced in this environment. It does not invalidate or overwrite the
frozen v0.2.0 table, and it does not establish a general timing rule for
mmCIF preparation. The manuscript may describe it as an execution-sensitive
record and must distinguish the frozen 26/102 audit result from this follow-up.
