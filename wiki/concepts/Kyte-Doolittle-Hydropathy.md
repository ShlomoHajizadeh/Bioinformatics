---
title: "Kyte-Doolittle Hydrophobic Hydropathy Profile"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - bioinformatics
  - structural-biology
  - algorithms
aliases:
  - Kyte-Doolittle Scale
  - Hydropathy Analysis
---

# Kyte-Doolittle Hydrophobic Hydropathy Profile

The **Kyte-Doolittle scale** is an empirical hydropathy indexing method used to predict transmembrane regions, interior hydrophobic cores, and surface-exposed hydrophilic loops in proteins.

## Mathematical Formulation

For a polypeptide of length $L$ and sliding window size $w$ (typically $w = 9$ for surface regions or $w = 19$ for transmembrane spanning helices):

$$H_i = \frac{1}{2w + 1} \sum_{j=-w}^{w} h_{i+j}$$

where $h_k$ is the assigned Kyte-Doolittle hydropathy value for residue at position $k$.

## Interpretive Thresholds
- **$H_i > 1.6$ (over 19-aa window)**: High probability of a transmembrane $\alpha$-helix.
- **$H_i < -0.5$**: High likelihood of water-exposed, hydrophilic loops.

## Related Concepts & Tools
- [[Biopython]] — used to parse sequences and compute hydropathy matrices.
- [[Miyazawa-Jernigan-Potentials]] — thermodynamic interaction potentials between contact pairs.
