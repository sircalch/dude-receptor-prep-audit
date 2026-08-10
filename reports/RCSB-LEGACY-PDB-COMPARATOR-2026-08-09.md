# RCSB legacy-PDB direct-preparation comparator — 2026-08-09

## Predeclared condition

This comparison follows the selected condition in
`protocol/JMM-VALIDATION-PROTOCOL.md`: the 102 entries in the frozen registry
were retrieved from the official RCSB legacy-PDB endpoint and each downloaded
file received one strict Meeko direct PDB-reader attempt. No source repair,
element correction, alternate-location selection, template addition, deletion,
or post-outcome exclusion was used.

Downloaded coordinates and logs remain ignored local external data. The
download manifest and preparation table are retained locally with these
SHA-256 values:

| Local artefact | SHA-256 |
|---|---|
| 102-record RCSB legacy-PDB download manifest | `478315f21667f6c31b4752b4e93c81def5a676abea3fbbea5808256539eea175` |
| 102-record preparation table | `384b2eb96721605bf6336ee1d1d0e1d1c44a06b3d690c30045b7c57ee1f6404b` |

## Observed results

All 102 legacy-PDB files were downloaded. Strict direct preparation produced
27 nonempty PDBQT outputs and 75 failures:

| Outcome or recorded failure class | Count |
|---|---:|
| Direct success | 27 |
| Alternate locations | 28 |
| Residue template mismatch | 29 |
| Other preparation failure | 15 |
| Element error | 3 |
| Preparation timeout | 0 |

## Comparison with frozen RCSB mmCIF condition

The frozen strict mmCIF result contains 26 successes and 76 failures. At the
target level, 101 of 102 outcomes matched the legacy-PDB direct-reader
condition:

| Pair of outcomes (legacy PDB, frozen mmCIF) | Count |
|---|---:|
| Direct success, direct success | 26 |
| Direct failure, direct failure | 75 |
| Direct success, direct failure | 1 |

For the 75 jointly failed records, every normalized error class matched:
28 alternate-location cases, 29 residue-template mismatches, 15 other
preparation failures, and three element errors. The only discordant record was
DPP4/2I78: the frozen mmCIF audit recorded a 300-second timeout, while the
legacy-PDB attempt completed successfully. The separate three-attempt follow-up
also completed successfully; see `DPP4-2I78-TIMING-SENSITIVITY-2026-08-09.md`.

## Interpretation limit

This is a source-and-reader compatibility comparison for the declared
versions and inputs. It neither demonstrates that legacy PDB and mmCIF are
generally interchangeable nor validates receptor selection, docking scores,
binding affinity, activity, safety, selectivity, or therapeutic effects. The
frozen v0.2.0 mmCIF table remains the versioned release observation.
