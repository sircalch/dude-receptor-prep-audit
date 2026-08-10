# Independent reference-pose reproduction, 2026-08-09

## Scope

The two frozen reference-pose campaigns were re-executed in new ignored output
directories. The original PDBQT outputs and versioned CSV tables were not
overwritten.

## Execution inputs

- AutoDock Vina: 1.2.7.
- Vina executable SHA-256:
  `e0c4b2715e0c1a74f6e92d0f3be0328ac97542eafbc111e6b1efad897a73cce5`.
- BRAF configuration: `protocol/braf_3d4q_vina_reference.conf`.
- KIF11 configuration: `protocol/kif11_3cjo_vina_reference.conf`.
- Each configuration fixes CPU=1, seed=20260809, exhaustiveness=16, and nine
  output modes.

## Result

| Case | Poses reproduced | RMSD analysis vs. frozen CSV |
|---|---:|---|
| BRAF 3D4Q / SM5 | 9 | Byte-identical |
| KIF11 3CJO / K30 | 9 | Byte-identical |

For BRAF, the reproduced RMSD table has SHA-256
`1b09b7deb0ad06de66900050cd1006c7f6017d673680eea04cf1fdca45da711e`.
For KIF11, it has SHA-256
`dd0df2f7485c1f41a683119afaffa944eb8a5d7a1b9ef5f45716ad22ce3064f7`.

## Interpretation boundary

This verifies deterministic reproduction of these two defined docking runs. It
does not validate a universal receptor-preparation workflow and does not infer
experimental affinity, biological activity, selectivity, safety, or therapeutic
effect.
