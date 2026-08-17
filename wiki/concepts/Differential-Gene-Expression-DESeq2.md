---
title: "Differential Gene Expression Analysis (Negative Binomial Model)"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - transcriptomics
  - statistics
  - rna-seq
aliases:
  - DGE
  - Negative Binomial RNA-Seq
sources:
  - "[[wiki/summaries/bioinformatics-research-journal]]"
---

# Differential Gene Expression Analysis (Negative Binomial Model)

**Differential Gene Expression (DGE)** analysis quantifies statistically significant changes in transcript abundance across experimental conditions (e.g. tumor vs. normal adjacent tissue in Triple-Negative Breast Cancer).

## Statistical Model

Because RNA-seq raw read counts $K_{ij}$ exhibit biological variance that exceeds the mean (overdispersion), counts are modeled using a **Negative Binomial (NB) distribution**:

$$K_{ij} \sim \text{NB}(\mu_{ij}, \alpha_i)$$

where:
- $\mu_{ij} = q_{ij} s_{j}$ is the mean expression scaled by size factor $s_j$.
- $\alpha_i$ is the gene-specific dispersion parameter.
- The variance is quadratic: $\text{Var}(K_{ij}) = \mu_{ij} + \alpha_i \mu_{ij}^2$.

## Shrinkage Estimation
- **Dispersion Shrinkage**: Shares information across all genes with similar mean expression using empirical Bayes to shrink noisy gene-wise dispersion estimates toward a smooth trend curve.
- **Log2 Fold Change (LFC) Shrinkage**: Shrinks high-variance LFC estimates of lowly expressed genes (e.g. `apeglm` or `ashr` algorithms).

## Related Entities & Concepts
- [[DESeq2]] — standard R/Bioconductor package.
- [[L1-vs-L2-High-Dimensional-Genomics]] — downstream classification on normalized expression matrices.
