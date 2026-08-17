---
title: "DESeq2 (Differential Expression Analysis for RNA-Seq)"
type: entity
created: 2026-08-17
updated: 2026-08-17
tags:
  - software-tools
  - r-bioconductor
  - transcriptomics
aliases:
  - DESeq2
sources:
  - "[[wiki/summaries/bioinformatics-research-journal]]"
---

# DESeq2

**DESeq2** is the premier R/Bioconductor package for differential gene expression analysis of RNA-seq read count data.

## Statistical Framework
- **Dispersion Estimation**: Uses Empirical Bayes shrinkage to stabilize dispersion estimates across expression ranges.
- **Hypothesis Testing**: Wald test for standard contrasts or Likelihood Ratio Test (LRT) for time-series / multi-factor designs.
- **Log2 Fold Change Shrinkage**: Eliminates spurious high fold-change inflation in low-count genes.

## Related Concepts & Syntheses
- [[Differential-Gene-Expression-DESeq2]] — statistical formulation.
- [[High-Dimensional-Machine-Learning-in-Genomics]] — downstream classification.
- [[TP53]] — transcriptomic benchmark targets.
