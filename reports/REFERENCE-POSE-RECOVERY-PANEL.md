# Reference pose-recovery panel

## Scope

This panel consolidates the two completed, independently pre-specified
reference-pose campaigns in this repository. It is not a virtual screen, does
not rank new compounds, and does not infer experimental binding affinity or
biological activity.

| Target | Reference | Top-score pose | RMSD of top-score pose | Lowest observed RMSD | Key limitation |
|---|---:|---:|---:|---:|---|
| BRAF 3D4Q | SM5 | −10.929 kcal/mol | 1.134 Å | 1.083 Å (mode 3) | No binary RMSD criterion was predeclared. |
| KIF11 3CJO | K30 | −10.994 kcal/mol | 1.477 Å | 1.316 Å (mode 4) | ADP was retained using an automatically constructed Meeko template. |

The machine-readable version is
[`results/reference_pose_recovery_panel.csv`](../results/reference_pose_recovery_panel.csv).

## Interpretation boundary

Each campaign ran one frozen Vina configuration for its deposited reference
ligand and retained all nine output poses. The values are identity-mapped,
aligned heavy-atom RMSD observations. They show how these two explicitly
defined workflows behaved for their own crystallographic references; they do
not establish general docking performance, prospective hit discovery, affinity,
selectivity, efficacy, safety, or cancer-related effect.

The underlying records remain separate:

- [BRAF 3D4Q / SM5](BRAF-3D4Q-REFERENCE-STATUS.md)
- [KIF11 3CJO / K30 protocol](../protocol/KIF11-3CJO-REFERENCE-LIGAND-QUALIFICATION.md)
