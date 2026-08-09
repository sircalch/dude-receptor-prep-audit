# Phase 2 protocol: authoritative element-mapping qualification

## Purpose

This phase does **not** repair a DUD-E receptor or run Meeko. It tests whether
each atom record in a DUD-E receptor can be mapped, without coordinate editing,
to an atom record in the authoritative wwPDB PDBx/mmCIF file for the PDB ID
already frozen in the DUD-E registry. PDBx/mmCIF includes the formal
`_atom_site.type_symbol` element item.

## Why a mapping qualification is required

The strict audit observed blank legacy-PDB element fields. The DUD-E receptor
files also use `ATOM` for some modified residues, cofactors, ions and waters.
Inferring an element from an atom name alone would be unsafe and is forbidden.

## Frozen workflow

For every registry row:

1. Download the official RCSB PDBx/mmCIF coordinate file for the frozen PDB ID
   and record its SHA-256.
2. Read DUD-E `ATOM` records and PDBx/mmCIF atom sites without modifying either
   source.
3. Attempt atom correspondence using residue name, author residue number, atom
   name and coordinates rounded to the three decimal places represented in the
   DUD-E PDB source. Chain identity is not used because it is absent from the
   audited DUD-E receptor files.
4. Record mapped, unmapped and conflicting-element rows. A coordinate key with
   several RCSB atoms is acceptable only when every candidate has the same
   official element symbol.

## Outcome definitions

- **complete_unambiguous_mapping**: every DUD-E `ATOM` record maps and no key
  has conflicting official element symbols.
- **incomplete_or_conflicting_mapping**: one or more rows are unmatched or
  have conflicting official element symbols.
- **rcsb_download_failure**: official mmCIF acquisition did not complete.

No recovered PDB is written in this phase. Only a future, separately reviewed
protocol may consider an element-only derivative, and only for targets passing
the complete-unambiguous gate.

## Interpretation boundary

Mapping success would establish coordinate-level concordance for an element
annotation source. It would not validate the receptor, Meeko preparation,
docking, poses, scores, affinity, biological activity or therapeutic effect.

## Sources

- wwPDB PDB-to-PDBx/mmCIF correspondence for the element symbol:
  <https://mmcif.wwpdb.org/docs/pdb_to_pdbx_correspondences.html>
- `_atom_site.type_symbol` definition:
  <https://mmcif.wwpdb.org/dictionaries/mmcif_std.dic/Items/_atom_type.symbol.html>
