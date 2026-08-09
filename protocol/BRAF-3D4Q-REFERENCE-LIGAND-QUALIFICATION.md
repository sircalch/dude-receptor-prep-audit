# BRAF 3D4Q reference-ligand qualification protocol

## Status and scope

This is a pre-specified, reference-pose qualification campaign.  It is a
separate follow-up to the repository-wide receptor-preparation audit; it does
not change any of that audit's conclusions.  The campaign begins with the
deposited BRAF entry 3D4Q and its co-crystallized ligand SM5.  It does **not**
screen compounds, estimate activity, or support a claim about cancer treatment.

At this stage the only completed operation is coordinate metadata extraction
from the frozen mmCIF source.  No ligand PDBQT, docking configuration, docking
run, score, pose, molecular-dynamics trajectory, or biological result has been
produced.

## Source identity

- Entry: RCSB PDB 3D4Q, human BRAF, X-ray diffraction, 2.80 Å.
- Ligand: SM5, `(1E)-5-(1-piperidin-4-yl-3-pyridin-4-yl-1H-pyrazol-4-yl)-2,3-dihydro-1H-inden-1-one oxime`.
- Frozen local mmCIF SHA-256:
  `034d6572fda3bb64e13c3b42ef5d55466f3ec4704f47d1357fa23bf802d0d983`.
- The repository does not redistribute the coordinate file.  The provenance
  table is [`results/braf_3d4q_reference_metadata.csv`](../results/braf_3d4q_reference_metadata.csv).

The public source pages are [RCSB 3D4Q](https://www.rcsb.org/structure/3D4Q)
and [RCSB SM5](https://www.rcsb.org/ligand/SM5).

## Completed extraction

`scripts/extract_braf_reference_metadata.py` reads the mmCIF with Gemmi,
selects only residues named `SM5`, and records the deposited heavy-atom bounds.
It performs no coordinate modification.  Two crystallographic instances are
present, on author chains A and B.  Chain A is designated the *primary
reference instance* solely to make downstream tests deterministic; chain B is
retained as an independent deposited-instance check.

The reported prospective boxes are the tight heavy-atom bounding boxes expanded
by 5.0 Å in each direction.  They are candidate configuration values only, not
an established docking protocol.

## Gates before any reference-pose calculation

All of the following must be recorded before running a docking engine:

1. Retrieve the RCSB chemical-component definition for SM5 and record its
   checksum, bond orders, formal charge, and explicitly chosen protonation
   state.
2. Extract one deposited ligand instance without changing its coordinates;
   record the output checksum and atom-identity reconciliation.
3. Recreate the strict RCSB-mmCIF receptor preparation for the selected chain
   and record the exact Meeko version, command, output checksum, and any
   receptor atoms retained or excluded by the tool.
4. Freeze a docking engine/version, seed, exhaustiveness, energy range, number
   of modes, box, and RMSD comparison rule before execution.
5. Run only SM5 against its matched receptor first.  Report pose recovery as
   heavy-atom RMSD after a declared atom mapping, with all poses and failures
   retained.  A successful recovery would validate only this narrow
   computational setup, not affinity or biological activity.

Any failure at a gate stops the campaign for diagnosis; it must not be hidden
by a repair, manual coordinate adjustment, or selective rerun.
