# KIF11 3CJO reference-ligand qualification protocol

## Scope

This is a new, independent reference-pose campaign. It does not modify the
completed BRAF record. Its only permitted calculation is recovery of deposited
K30 against KIF11 3CJO; it does not screen compounds or make claims of affinity,
activity, efficacy, safety, or cancer treatment.

## Cofactor policy

The receptor will retain deposited ADP and Mg²⁺ from author chain A while
excluding K30, the reference ligand being redocked, and all waters. This is the
explicitly selected policy because ADP and Mg²⁺ are crystallographic non-polymer
components of the same chain, whereas retaining K30 in the receptor would make
the reference calculation invalid. No other non-polymer residue will be added,
deleted, repaired, or substituted.

During strict preparation, Meeko 0.7.1 reported that ADP was not in its native
residue-template set and constructed a chemical template automatically. This
behavior is explicitly accepted for this KIF11 reference campaign. It is a
model limitation: the campaign will report it, retain its logs and checksums,
and make no claim that the cofactor parameterization is experimentally
validated.

## Completed Gate 1: cofactor-retaining receptor

Chain A polymer atoms plus one ADP and one Mg²⁺ were retained; one K30 and 178
waters were excluded. The selection contained 2,622 atoms and no selected
alternate locations. Meeko 0.7.1 completed strict preparation successfully.
The exact command, warning-bearing log checksum, and source/output checksums
are in [`results/kif11_chain_a_cofactor_receptor_preparation.csv`](../results/kif11_chain_a_cofactor_receptor_preparation.csv).

## Completed component freeze

The authoritative K30 definition has SHA-256
`ffce02cf297fc7378ef997bee8ad390860e4e02cc7cc98d49915c3aafe51f7c1` and
records 61 atoms, 33 heavy atoms, 64 bonds, and formal charge 0. The neutral
deposited component is the reference baseline; it is not asserted to be the
only state in every environment. See
[`results/kif11_k30_component_qualification.csv`](../results/kif11_k30_component_qualification.csv).

## Planned gates

1. Extract chain-A polymer atoms plus ADP and Mg²⁺; record every retained and
   excluded component, checksums, and strict Meeko preparation result.
2. Freeze the RCSB K30 component definition and reconcile its deposited chain-A
   instance without altering coordinates.
3. Freeze Vina version, binary checksum, ligand-derived box, seed, search
   settings, and an identity-mapped heavy-atom RMSD rule.
4. Run K30 once, retain all poses, and report numerical observations without a
   retrospective binary acceptance claim.
