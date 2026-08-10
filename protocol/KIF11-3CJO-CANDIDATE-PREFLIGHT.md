# KIF11 3CJO candidate preflight

## Scope

This document records candidate selection only. It is **not** a docking
campaign and contains no KIF11 docking calculation, score, RMSD, or biological
claim.

KIF11 entry 3CJO is a plausible independent follow-up to the completed BRAF
reference campaign because it is a human, non-mutated, X-ray structure with a
co-crystallized small molecule and had a direct-success outcome in this
repository's strict mmCIF preparation audit. The RCSB entry reports 2.28 Å
resolution and no mutations. Its public source page is
[RCSB 3CJO](https://www.rcsb.org/structure/3CJO).

## Frozen observations

- Local 3CJO mmCIF SHA-256:
  `94f8d6c475d6533d39cc2cd7241cc557af2eb058cd3da0495eb98abd77d9e705`.
- Co-crystallized reference ligand: K30, chain A, 33 heavy atoms.
- Chain A also contains ADP and Mg²⁺.
- The smallest deposited heavy-atom distances from K30 are 8.632 Å to ADP and
  10.607 Å to Mg²⁺.

All values are in
[`results/kif11_3cjo_candidate_preflight.csv`](../results/kif11_3cjo_candidate_preflight.csv).

## Stop condition

This candidate is intentionally stopped before receptor extraction. Unlike the
BRAF case, non-polymer cofactors are present. Deleting them by default would be
a methodological choice, while retaining them requires an independently
validated treatment in the receptor-preparation pathway. A future KIF11
protocol must pre-specify one of those policies, explain it, and then apply the
same complete provenance, ligand reconciliation, frozen configuration, and
all-pose reporting used for BRAF. It must not retroactively alter the BRAF
record.
