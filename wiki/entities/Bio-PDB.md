---
title: "Bio.PDB (Biopython Structural Biology Module)"
type: entity
created: 2026-08-17
updated: 2026-08-17
tags:
  - biopython
  - structural-biology
  - software-tools
aliases:
  - Bio.PDB
  - PDBParser
sources:
  - "[[wiki/summaries/biopython-curriculum-30-modules]]"
---

# Bio.PDB

**`Bio.PDB`** is Biopython's structural biology module for parsing, analyzing, superimposing, and transforming macromolecular 3D coordinate files (PDB and mmCIF formats).

## The SMCRA Hierarchy

`Bio.PDB` organizes structural data strictly into the canonical **SMCRA** object architecture:

```
Structure (PDB ID)
└── Model (NMR model or 0 for X-ray)
    └── Chain (Chain ID: 'A', 'B', ...)
        └── Residue (Residue ID: (' ', res_seq_num, insertion_code))
            └── Atom (Atom Name: 'CA', 'N', 'C', 'O', coordinates [x, y, z])
```

## Key Modules & Tools
- **`PDBParser` / `MMCIFParser`**: Robust coordinate file parsers.
- **`Superimposer`**: Least-squares 3D rigid-body superposition algorithm minimizing RMSD (Root Mean Square Deviation) between atom sets.
- **`NeighborSearch`**: KD-tree spatial index for rapid contact identification ($O(\log N)$ spatial queries).
- **`Polypeptide`**: Extracts backbone dihedral angles ($\phi, \psi$) for Ramachandran plot construction.

## Related Tools & Concepts
- [[Protein-3D-Metrics]] — parsing and 3D visualization.
- [[Protein-Computational-Analysis]] — thermodynamic scoring and rigidity analysis.
- [[AlphaFold-DB]] — parsing predicted structures.
