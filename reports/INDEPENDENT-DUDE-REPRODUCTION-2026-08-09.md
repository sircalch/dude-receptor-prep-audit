# Independent strict DUD-E reproduction, 2026-08-09

## Scope

This record reports a local re-execution of the frozen direct DUD-E
receptor-preparation audit. It is a reproduction check, not a new scientific
experiment and not an assessment of docking performance.

## Environment and inputs

- Input registry: `data/dude_targets.csv` (102 targets).
- Raw sources: the locally retained original DUD-E `receptor.pdb` files under
  the ignored `external-data/` directory; no download, repair, or editing step
  was performed during this reproduction.
- Command pathway: one direct `--read_pdb` Meeko receptor-preparation attempt
  per source file, with no bypass options.
- Meeko: 0.7.1.
- RDKit: 2024.9.6.

## Observed result

The reproduction produced 102 rows, 102 direct failures, 102
`blank_element_fields` classifications, and 102 unique source checksums. The
independent CSV was byte-identical to the committed frozen table:

| File | SHA-256 |
|---|---|
| `results/dude_receptor_audit.csv` | `121150212a47a34fbe751490433d2386d6729c65c12eb987c46af38801e0b924` |
| independent reproduction CSV | `121150212a47a34fbe751490433d2386d6729c65c12eb987c46af38801e0b924` |

## Boundary

This check reproduces only the strict DUD-E direct-reader result. It does not
by itself reproduce the separate RCSB mmCIF audit or the reference-pose runs;
those require their own documented environment and execution record. It does
not support an inference about receptor quality, docking scores, affinity,
biological activity, safety, or therapeutic effect.
