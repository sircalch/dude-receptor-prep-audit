#!/usr/bin/env python3
"""Mapped heavy-atom RMSD for frozen KIF11/K30 Vina poses."""
from __future__ import annotations
import argparse,csv
from pathlib import Path
import gemmi,numpy as np
def idxmap(p):
 v=[]
 for line in p.read_text().splitlines():
  if line.startswith('REMARK INDEX MAP'):v.extend(map(int,line.split()[3:]))
 return {v[i+1]:v[i] for i in range(0,len(v),2)}
def rmsd(a,b):
 a=a-a.mean(0);b=b-b.mean(0);u,_,vt=np.linalg.svd(a.T@b);r=u@vt
 if np.linalg.det(r)<0:u[:,-1]*=-1;r=u@vt
 return float(np.sqrt(np.mean(np.sum((a@r-b)**2,axis=1))))
def main():
 p=argparse.ArgumentParser();p.add_argument('mmcif',type=Path);p.add_argument('component',type=Path);p.add_argument('input_pdbqt',type=Path);p.add_argument('vina_output',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
 b=gemmi.cif.read_file(str(a.component)).sole_block(); comp={i+1:(r[1],r[3]) for i,r in enumerate(b.find_mmcif_category('_chem_comp_atom.'))};s=gemmi.read_structure(str(a.mmcif));r=next(r for m in s for c in m if c.name=='A' for r in c if r.name=='K30');ref={x.name:np.array([x.pos.x,x.pos.y,x.pos.z]) for x in r}; mapping=idxmap(a.input_pdbqt); models=[]; n=0;aff=None;atoms={}
 for line in a.vina_output.read_text().splitlines():
  if line.startswith('MODEL'):n=int(line.split()[1]);aff=None;atoms={}
  elif line.startswith('REMARK VINA RESULT:'):aff=float(line.split()[3])
  elif line.startswith('ATOM'):atoms[int(line[6:11])]=np.array([float(line[30:38]),float(line[38:46]),float(line[46:54])])
  elif line.startswith('ENDMDL'):
   q=[(comp[i][0],serial) for serial,i in mapping.items() if comp[i][1]!='H'];
   if len(q)!=33 or any(name not in ref or serial not in atoms for name,serial in q):raise ValueError('incomplete K30 atom mapping')
   models.append({'model':str(n),'vina_affinity_kcal_per_mol':f'{aff:.3f}','mapped_heavy_atom_count':'33','aligned_heavy_atom_rmsd_angstrom':f'{rmsd(np.array([atoms[serial] for _,serial in q]),np.array([ref[name] for name,_ in q])):.3f}'})
 with a.output.open('w',newline='',encoding='utf-8') as h:w=csv.DictWriter(h,fieldnames=list(models[0]));w.writeheader();w.writerows(models)
if __name__=='__main__':main()
