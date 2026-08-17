---
title: "B-Factor (Thermal Displacement Parameter)"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - structural-biology
  - crystallography
  - biophysics
aliases:
  - Temperature Factor
  - Debye-Waller Factor
  - B-Factor
sources:
  - "[[wiki/summaries/starter-kit-protein-computational-analysis]]"
---

# B-Factor (Thermal Displacement Parameter)

The **B-factor** (also known as the Debye-Waller factor or temperature factor) in X-ray crystallography indicates the isotropic thermal vibration and positional uncertainty of individual atoms around their mean coordinates:

$$B_i = 8\pi^2 \langle u_i^2 \rangle$$

where $\langle u_i^2 \rangle$ is the mean-square displacement ($\text{\AA}^2$) of atom $i$.

## Biophysical Significance & Rigidity Correlation

- **Buried Hydrophobic Core**: Rigid residues encased inside the structural core experience restricted movement and display lower B-factors.
- **Surface Loops & Termini**: Unconstrained flexible loops possess high solvent accessibility and elevated B-factors.
- **Validation Metric**: A statistically significant negative Pearson correlation ($r < -0.3$) between atomic B-factors and local packing density confirms crystallographic model stability.

## Related Concepts & Tools
- [[Protein-Computational-Analysis]] — computes Pearson correlation between packing density and B-factors.
- [[Solvent-Accessible-Surface-Area]] — exposed surface residues correlate with high B-factors.
- [[AlphaFold-DB]] — pLDDT scores in AlphaFold PDB outputs are stored in the B-factor column ($0\text{--}100$).
