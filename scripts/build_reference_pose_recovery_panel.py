#!/usr/bin/env python3
"""Build the two-target panel from the versioned pose-recovery tables."""
from __future__ import annotations
import csv
from pathlib import Path
def read(path):
 with path.open(newline='',encoding='utf-8') as h:return list(csv.DictReader(h))
def main():
 root=Path(__file__).resolve().parents[1]; b=read(root/'results'/'braf_sm5_reference_pose_recovery.csv'); k=read(root/'results'/'kif11_k30_reference_pose_recovery.csv')
 rows=[]
 for target,pdb,ligand,poses,policy,limit in [('BRAF','3D4Q','SM5',b,'polymer chain A only; non-polymers excluded','no binary RMSD criterion predeclared'),('KIF11','3CJO','K30',k,'polymer chain A plus ADP and Mg; K30 and waters excluded','ADP template constructed automatically by Meeko and accepted explicitly')]:
  top=min(poses,key=lambda r:float(r['vina_affinity_kcal_per_mol'])); low=min(poses,key=lambda r:float(r['aligned_heavy_atom_rmsd_angstrom']))
  rows.append({'target':target,'pdb_id':pdb,'reference_ligand':ligand,'cofactor_policy':policy,'meeko_receptor_outcome':'direct_success','meeko_ligand_outcome':'direct_success','vina_pose_count':str(len(poses)),'best_scoring_model':top['model'],'best_scoring_affinity_kcal_per_mol':top['vina_affinity_kcal_per_mol'],'best_scoring_model_rmsd_angstrom':top['aligned_heavy_atom_rmsd_angstrom'],'lowest_rmsd_model':low['model'],'lowest_rmsd_angstrom':low['aligned_heavy_atom_rmsd_angstrom'],'material_limitation':limit})
 with (root/'results'/'reference_pose_recovery_panel.csv').open('w',newline='',encoding='utf-8') as h:w=csv.DictWriter(h,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
if __name__=='__main__':main()
