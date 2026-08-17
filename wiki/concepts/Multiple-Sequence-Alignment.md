---
title: "Multiple Sequence Alignment (MSA)"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - bioinformatics
  - algorithms
  - sequence-alignment
aliases:
  - MSA
  - Multiple Alignment
sources:
  - "[[wiki/summaries/biopython-curriculum-30-modules]]"
---

# Multiple Sequence Alignment (MSA)

**Multiple Sequence Alignment (MSA)** is the alignment of three or more biological sequences (protein or nucleic acid), introducing gaps ($\text{--}$) to maximize positional conservation and homology.

## Algorithmic Paradigms

1. **Progressive Alignment**: Builds an initial pairwise distance matrix, generates a guide tree (UPGMA or Neighbor-Joining), and aligns sequences along the tree hierarchy (e.g. ClustalW, Clustal Omega).
2. **Iterative & Consistency Methods**: Refines initial alignments through stochastic or consistency scoring to resolve early misalignments (e.g. MAFFT, MUSCLE, T-Coffee).
3. **Hidden Markov Models (Profile HMMs)**: Probabilistic profile modeling of conserved consensus positions and insertion/deletion states (e.g. HMMER).

## Scoring Functions
- **Sum-of-Pairs (SP) Score**:
  $$S(\text{MSA}) = \sum_{1 \le i < j \le k} \text{Score}(s_i, s_j)$$
  where $\text{Score}(s_i, s_j)$ is computed via standard substitution matrices (BLOSUM62 for proteins, transition/transversion matrices for DNA) and affine gap penalties.

## Downstream Applications
- Identifying catalytic residues and conserved motifs.
- Input data for [[Phylogenetic-Tree-Reconstruction]].
- MSA input for AlphaFold deep learning co-evolution analysis.

## Related Tools & Modules
- [[Bio-AlignIO]]
- [[Bio-Phylo]]
- [[AlphaFold-DB]]
