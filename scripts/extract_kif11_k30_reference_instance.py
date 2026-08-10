#!/usr/bin/env python3
"""Extract and reconcile deposited K30 chain-A coordinates without modification."""
from __future__ import annotations
import argparse,csv,hashlib
from pathlib import Path
import gemmi
def sha256(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def main()->None:
 p=argparse.ArgumentParser();p.add_argument('mmcif',type=Path);p.add_argument('component_cif',type=Path);p.add_argument('coordinates',type=Path);p.add_argument('summary',type=Path);a=p.parse_args()
 b=gemmi.cif.read_file(str(a.component_cif)).sole_block(); component=b.find_mmcif_category('_chem_comp_atom.'); expected={r[1]:r[3] for r in component}
 s=gemmi.read_structure(str(a.mmcif)); r=next(r for m in s for c in m if c.name=='A' for r in c if r.name=='K30' and r.seqid.num==1); atoms=list(r)
 a.coordinates.parent.mkdir(parents=True,exist_ok=True)
 with a.coordinates.open('w',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=['atom_id','element','x','y','z']);w.writeheader()
  for x in atoms:w.writerow({'atom_id':x.name,'element':x.element.name,'x':f'{x.pos.x:.3f}','y':f'{x.pos.y:.3f}','z':f'{x.pos.z:.3f}'})
 ids={x.name for x in atoms}; row={'pdb_id':'3CJO','ligand_id':'K30','auth_chain':'A','auth_seq_id':'1','source_mmcif_sha256':sha256(a.mmcif),'component_sha256':sha256(a.component_cif),'extracted_coordinate_sha256':sha256(a.coordinates),'deposited_atom_count':str(len(atoms)),'deposited_heavy_atom_count':str(sum(x.element.name!='H' for x in atoms)),'component_atom_count':str(len(component)),'component_heavy_atom_count':str(sum(x[3]!='H' for x in component)),'component_atom_ids_missing_from_deposit':str(len(set(expected)-ids)),'deposited_atom_ids_missing_from_component':str(len(ids-set(expected))),'element_mismatch_count':str(sum(expected.get(x.name)!=x.element.name for x in atoms))}
 with a.summary.open('w',newline='',encoding='utf-8') as h:w=csv.DictWriter(h,fieldnames=list(row));w.writeheader();w.writerow(row)
if __name__=='__main__':main()
