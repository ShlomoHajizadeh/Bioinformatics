---
title: "Solvent Accessible Surface Area (SASA)"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - structural-biology
  - biophysics
  - algorithms
aliases:
  - SASA
  - Solvent Accessibility
sources:
  - "[[wiki/summaries/starter-kit-protein-computational-analysis]]"
---

# Solvent Accessible Surface Area (SASA)

**Solvent Accessible Surface Area (SASA)** is the surface area of a biomolecule that is accessible to a solvent probe (typically a water sphere of radius $r = 1.4\text{ \AA}$). It is a critical parameter in determining hydrophobic free energy, protein folding stability, and binding interfaces.

## Computational Formulations

1. **Lee-Richards & Shrake-Rupley Algorithms**: Exact surface integration using rolling probe spheres.
2. **Local Packing Density Approximation**:
   For rapid statistical screening without mesh triangulation, fractional solvent accessibility can be approximated from local atomic coordination numbers:
   $$\text{SASA}_{\text{fraction}} \approx \max\left(0, 1 - \frac{N_{\text{neighbors}}(R_{\text{sphere}})}{N_{\text{max\_packing}}}\right)$$
   where $N_{\text{neighbors}}$ is the count of $\text{C}_\alpha$ atoms within a $10.0\text{ \AA}$ sphere (with $N_{\text{max\_packing}} \approx 22\text{--}24$ residues).

## Related Entities & Concepts
- [[Protein-Computational-Analysis]] — local density-based SASA estimator.
- [[Kyte-Doolittle-Hydropathy]] — correlation between high hydropathy and buried residues ($\text{SASA} \to 0$).
- [[B-Factor-Thermal-Displacement]] — exposed residues typically exhibit higher thermal displacement.
