---
title: "Miyazawa-Jernigan Statistical Contact Potentials"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - bioinformatics
  - structural-biology
  - statistical-mechanics
aliases:
  - MJ Potentials
  - Residue Contact Energies
---

# Miyazawa-Jernigan Statistical Contact Potentials

**Miyazawa-Jernigan (MJ) Potentials** provide an empirical contact energy matrix derived from the observed frequencies of spatial residue-residue contacts in high-resolution crystallographic structures (PDB).

## Mathematical Formulation

The pseudo-folding free energy ($E$) of a 3D structural model is evaluated as:

$$E = \sum_{i < j} e(R_i, R_j) \cdot \mathbb{I}\left(d(C_{\alpha,i}, C_{\alpha,j}) \leq d_{\text{cutoff}}\right)$$

where:
- $e(R_i, R_j)$ represents the statistical contact energy between amino acid types $R_i$ and $R_j$.
- $d(C_{\alpha,i}, C_{\alpha,j})$ is the 3D Euclidean distance between the $\text{C}_\alpha$ atoms of residues $i$ and $j$.
- $\mathbb{I}(\cdot)$ is an indicator function returning 1 if the distance is within contact range (typically $d_{\text{cutoff}} = 6.5\text{ \AA}$ or $8.0\text{ \AA}$).

## Related Entities & Concepts
- [[AlphaFold-DB]] — used to validate predicted structure contacts against statistical contact priors.
- [[Kyte-Doolittle-Hydropathy]] — complementary 1D profile vs. 3D contact potential.
