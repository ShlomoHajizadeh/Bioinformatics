---
title: "Phylogenetic Tree Reconstruction"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - phylogenetics
  - evolution
  - algorithms
aliases:
  - Phylogeny Reconstruction
  - Tree Building
sources:
  - "[[wiki/summaries/biopython-curriculum-30-modules]]"
---

# Phylogenetic Tree Reconstruction

**Phylogenetic Tree Reconstruction** is the inferential process of estimating evolutionary relationships and branching histories among biological taxa, genes, or species from sequence alignments.

## Mathematical Methods

1. **Distance-Based Methods**:
   - **Neighbor-Joining (NJ)**: Bottom-up star-decomposition clustering algorithm that accounts for unequal evolutionary rates across lineages without assuming an ultrametric molecular clock.
     $$Q(i, j) = (n - 2) d(i, j) - \sum_{k=1}^n d(i, k) - \sum_{k=1}^n d(j, k)$$
   - **UPGMA**: Arithmetic average clustering assuming constant evolutionary rate (ultrametric trees).

2. **Character-Based & Probabilistic Methods**:
   - **Maximum Parsimony (MP)**: Identifies the tree topology requiring the minimum total number of evolutionary substitution events.
   - **Maximum Likelihood (ML)**: Evaluates the likelihood $L(T) = P(D \mid T, \theta)$ under specific nucleotide/amino acid substitution models (e.g. Jukes-Cantor, Kimura 2-parameter, GTR, WAG).
   - **Bayesian Inference**: Samples tree posterior probability distributions using Markov Chain Monte Carlo (MCMC).

## Related Tools & Modules
- [[Bio-Phylo]] — Python tree construction and manipulation engine.
- [[Multiple-Sequence-Alignment]] — essential input alignment matrix.
- [[MEGA-Software-Genetics]] — external desktop phylogenomics pipeline.
