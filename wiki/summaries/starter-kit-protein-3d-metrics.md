---
title: "Source Summary: Protein 3D Structure Metrics Visualizer"
type: summary
created: 2026-08-17
updated: 2026-08-17
tags:
  - bioinformatics
  - structural-biology
  - code-summary
sources:
  - "[[starter_kit/protein_3d_metrics.py]]"
---

# Source Summary: `protein_3d_metrics.py`

- **File Path**: `starter_kit/protein_3d_metrics.py`
- **Author**: Süleyman Hacızadə
- **Purpose**: RCSB PDB coordinate retrieval, structural hierarchy parsing (`Structure -> Model -> Chain -> Residue -> Atom`), C$\alpha$ Euclidean distance metrics, and 3D backbone ribbon rendering with dark-mode aesthetic styling.

## Key Capabilities & Algorithms

1. **Automated PDB Ingestion (`download_pdb`)**: Direct HTTP retrieval of `.pdb` crystallographic models from RCSB PDB with local caching (defaulting to Insulin `1COH` at 1.5 Å resolution).
2. **Structural Traversal (`analyze_pdb_structure`)**: Utilizes `Bio.PDB.PDBParser` to resolve amino acid residues and target Carbon-Alpha ($\text{C}_\alpha$) coordinates.
3. **3D Euclidean Distance (`calculate_euclidean_distance`)**:
   $$d = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2 + (z_1 - z_2)^2}$$
4. **3D Ribbon & Vector Visualizer (`visualize_protein_backbone_3d`)**: Matplotlib 3D projection rendering $\text{C}_\alpha$ backbone coordinates with dashed Euclidean distance vectors between target residues.

## Cross-Linked Entities & Concepts
- **Entities**: [[Protein-3D-Metrics]], [[Biopython]], [[Insulin-1COH]], [[AlphaFold-DB]]
- **Concepts**: [[Miyazawa-Jernigan-Potentials]], [[Solvent-Accessible-Surface-Area]]
