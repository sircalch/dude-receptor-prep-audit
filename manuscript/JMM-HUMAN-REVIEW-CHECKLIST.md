# Human review checklist for the JMM manuscript

This is a review aid, not evidence that review has occurred. Each reviewer
should inspect the referenced artefact directly, record any discrepancy, and
complete the log at the end in their own words.

## Methods and provenance

- [ ] Confirm that the DUD-E direct audit denominator is 102 and that its
  reported blank-element result is supported by `results/dude_receptor_audit.csv`.
- [ ] Confirm that the frozen RCSB mmCIF condition reports 26 direct successes
  and 76 retained failures in `results/rcsb_mmcif_preparation_audit.csv`.
- [ ] Confirm that the RCSB legacy-PDB comparator reports 27 direct successes
  and 75 failures in `validation/rcsb_legacy_pdb_preparation_audit_20260809.csv`.
- [ ] Confirm that the comparison report says 101/102 outcomes agree and
  identifies only DPP4/2I78 as discordant.
- [ ] Confirm that DPP4/2I78 is described as execution-sensitive, not as proof
  that an older frozen observation is erroneous.
- [ ] Check that no method statement implies coordinate repair, hidden retry,
  alternate-location selection, or silent template addition.

## Docking cases and limits

- [ ] Recompute or inspect the BRAF and KIF11 CSV results and ensure the text
  distinguishes top-score RMSD from lowest-RMSD pose.
- [ ] Confirm that all retained poses, Vina settings, seeds, and cofactor policy
  match their protocols and reports.
- [ ] Remove or revise any wording that infers affinity, activity, selectivity,
  safety, therapeutic utility, or cancer relevance from preparation or docking
  observations.

## Figures, tables, and reproducibility

- [ ] Run `python scripts/verify_frozen_evidence.py --results-dir results` and
  retain the terminal output with date and commit SHA.
- [ ] Re-render `scripts/render_preparation_comparator_figure.py` and check
  that the SVG communicates denominators and limitations legibly.
- [ ] Check every number in the manuscript tables against its named CSV or
  report, including units and target/PDB IDs.
- [ ] Verify that source coordinates are not redistributed in supplementary
  material; only identifiers, URLs, checksums, scripts, and derived tables
  should be included unless permissions are independently checked.

## Editorial, authorship, and integrity

- [ ] Verify each reference against its cited sentence and remove any unused
  item; consult `JMM-REFERENCES-VERIFIED.md` and
  `JMM-REFERENCE-ADDITIONS-VERIFIED.md` as evidence lists rather than copying
  them blindly.
- [ ] Each author checks author order, affiliations, ORCID, CRediT roles,
  funding statement, competing-interest statement, and corresponding author.
- [ ] The authors write or substantially revise the scientific narrative,
  interpretation, and final English text, and approve the final version.
- [ ] State any computational assistance accurately in the journal's requested
  disclosure field; authors remain responsible for the complete article.
- [ ] Confirm the target journal's current article type, formatting rules, and
  publication route on the day of submission.

## Review log (complete manually)

- Reviewer name and role:
- Date (UTC or local time zone):
- Repository commit reviewed:
- Artefacts inspected:
- Discrepancies or requested changes:
- Outcome (approve / approve with changes / request changes):
- Reviewer signature or institutional review record, if applicable:
