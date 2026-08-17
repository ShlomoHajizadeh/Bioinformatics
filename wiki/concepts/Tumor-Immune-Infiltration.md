---
title: "Tumor Immune Microenvironment Deconvolution"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - immunology
  - transcriptomics
  - oncology
  - deconvolution
aliases:
  - Immune Infiltration
  - CIBERSORT
  - Microenvironment Deconvolution
sources:
  - "[[wiki/summaries/integrated-bioinformatics-analysis-roadmap]]"
---

# Tumor Immune Microenvironment Deconvolution

**Tumor Immune Microenvironment Deconvolution** estimates the relative fractions or absolute abundances of diverse cell types (e.g. CD8+ cytotoxic T cells, M1/M2 macrophages, regulatory T cells, NK cells) from bulk RNA-seq gene expression mixtures.

## Computational Approaches

1. **Support Vector Regression (CIBERSORT / CIBERSORTx)**:
   Solves $\mathbf{m} = \mathbf{B}\mathbf{f}$ using $\nu$-support vector regression with a reference signature matrix $\mathbf{B}$ (e.g. LM22 leukocyte signature).
2. **Gene Set Enrichment (ssGSEA / xCell)**: Single-sample ranking tests evaluating pre-curated cell-type marker signatures.
3. **Statistical Regression (TIMER)**: Constrained least-squares regression optimized for primary cancer types in TCGA.

## Clinical Relevance
- High CD8+ T-cell infiltration correlates with favorable immune checkpoint inhibitor (anti-PD-1 / anti-CTLA-4) response.
- Dense M2 macrophage infiltration indicates immunosuppression and poor prognosis in Triple-Negative Breast Cancer.

## Related Concepts & Tools
- [[Differential-Gene-Expression-DESeq2]] — prerequisite expression profiling.
- [[GEO-TCGA]] — public source cohorts.
- [[End-to-End-Integrated-Oncogenomics-Framework]]
