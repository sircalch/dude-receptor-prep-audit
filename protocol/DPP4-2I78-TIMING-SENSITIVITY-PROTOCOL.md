# Predeclared timing-sensitivity protocol: DPP4 / 2I78

## Question

Can the strict direct mmCIF preparation outcome for DPP4 structure 2I78 change
under repeated executions with the same archived input and nominal 300-second
timeout?

## Motivation

The frozen v0.2.0 audit classified 2I78 as a `preparation_timeout`, whereas a
subsequent independent full-set rerun completed successfully. The source
mmCIF checksum was identical in both records. This focused follow-up measures
execution-time sensitivity; it does not alter the frozen audit table.

## Locked inputs and conditions

- Registry row: index 26 of `data/dude_targets.csv` (`DPP4`, `2I78`).
- Coordinate input: existing archived `external-data/rcsb-mmcif/2i78.cif`;
  record its
  SHA-256 before execution.
- Preparation command: the historical `mk_prepare_receptor.exe` through
  `scripts/audit_rcsb_mmcif_preparation.py` with `--read_with_prody`.
- Timeout: 300 seconds for each attempt.
- Environment: use the same declared Python/Meeko environment as
  `protocol/JMM-ENVIRONMENT-MANIFEST.md`; record the executable path and
  software versions in the run log.
- Attempts: three sequential attempts, each in a new output directory.
- No source repair, alternate-location selection, template addition, parameter
  tuning, or manual intervention is permitted.

## Outcomes to retain

For every attempt retain the emitted CSV row, wall-clock duration, exit code,
PDBQT byte count, log, and source checksum. A timeout is a valid outcome.
Do not repeat selectively after viewing a result.

## Interpretation rule

Report counts and durations only. If attempts differ, describe 2I78 as
time/resource-sensitive under these conditions. Do not generalize to all RCSB
mmCIF structures or claim that one outcome is the definitive preparation
status. The frozen v0.2.0 result remains the versioned release observation.
