# Pre-registered validation protocol for the JMM manuscript

## Purpose

This protocol defines the validation work required before the repository is
presented as a *Journal of Molecular Modeling* Software Report. It does not
replace the already frozen v0.2.0 evidence and does not authorize modification
of raw source structures or selective deletion of failed runs.

## Primary question

Can the repository's provenance-aware workflow reproduce its reported strict
DUD-E and RCSB mmCIF preparation outcomes from the versioned inputs, and can a
declared comparator workflow be evaluated under equally explicit conditions?

## Locked baseline

- DUD-E registry: `data/dude_targets.csv`.
- Direct DUD-E route: original `receptor.pdb`, one Meeko direct-reader attempt,
  no repair or bypass options.
- RCSB route: official PDBx/mmCIF coordinate source, one declared
  `--read_with_prody` attempt, no repair or bypass options.
- Reference-pose cases: BRAF 3D4Q/SM5 and KIF11 3CJO/K30 as already documented
  in their individual protocols.
- Result interpretation: software-compatibility and reference-pose observations
  only; no affinity, activity, safety, selectivity, or therapeutic inference.

## Reproduction gate

1. Use a new clean environment and record OS, Python, Meeko, RDKit, Gemmi,
   ProDy, and Vina versions.
2. Retrieve only the sources stated by the baseline protocol and record source
   URLs, retrieval date, byte count, SHA-256, and command logs locally.
3. Run the baseline scripts without editing their inputs.
4. Run `python scripts/verify_frozen_evidence.py` against the versioned result
   directory before and after regeneration.
5. Compare regenerated machine-readable tables with the frozen tables. Any
   difference is a result, not a reason to overwrite the old table.
6. Record the exact commit SHA and independent reviewer in the validation log.

## Comparator selection rules

The comparator must be selected before execution and must satisfy all of the
following conditions:

- It is documented, versioned, and publicly obtainable.
- It accepts the same specified source representation or the source difference
  is explicitly treated as a separate condition.
- Its configuration is recorded completely, including defaults that affect
  structure interpretation.
- It is applied to every eligible target; targets may not be excluded after
  viewing outcomes.
- It does not silently repair, delete, select alternative locations, or add
  templates. If a step does any of these, it becomes a named intervention and
  is evaluated separately.

The manuscript must never frame a comparator as an error-free gold standard.

## Selected comparator: RCSB legacy-PDB direct route

This comparator is selected before execution. It evaluates source-format and
reader compatibility, not the superiority of one preparation suite.

- Population: all 102 entries in `data/dude_targets.csv`; no eligibility
  exclusion is permitted after outcome inspection.
- Source: the official uncompressed RCSB legacy-PDB endpoint
  `https://files.rcsb.org/download/{PDB_ID}.pdb`.
- Retrieval record: for every attempted source, retain URL, UTC retrieval time,
  HTTP status, byte count, and SHA-256. Downloaded coordinates remain ignored
  external data and are not committed to this repository.
- Preparation: one Meeko direct PDB-reader attempt using `--read_pdb`, with
  the same Meeko environment and direct-success definition as the baseline.
- Prohibited interventions: atom/element repair, coordinate editing,
  alternate-location selection, residue-template addition, deletion, and
  manual retry after viewing an individual result.
- Output: retain every target-level row and command log. A missing/failed
  download is reported as `not_evaluated`, never converted to success.

This condition differs from both the original DUD-E PDB files and RCSB mmCIF
files. Results must be presented as a separate source-and-reader condition.

## Outcome definitions

### Receptor preparation

- **Direct success:** process return code is zero and the expected PDBQT output
  exists and is nonempty.
- **Direct failure:** any other outcome, with retained command log and a
  normalized error class.
- **Not evaluated:** source cannot be retrieved or its checksum cannot be
  recorded. This category is reported separately and is not recoded as failure.

### Reference-pose recovery

- All generated poses are retained.
- The top-scoring pose is determined only by the recorded Vina score.
- The lowest-RMSD pose is determined separately from identity-mapped,
  aligned heavy-atom RMSD.
- No RMSD threshold is introduced after inspecting results.
- Cofactor, metal, solvent, and ligand policies are established before each run.

## Reporting requirements

Report denominators, exclusions, versions, commands, all errors, all pose
counts, checksum manifests, and any divergence from the frozen baseline. A
negative or inconclusive result remains reportable evidence.

## Stop conditions

Stop the comparison and document the event if a required tool is unavailable,
license terms prevent reproducible use, the source is altered unexpectedly,
or a protocol change would be needed after results are observed. No substitute
workflow may be introduced retrospectively without a new protocol version.
