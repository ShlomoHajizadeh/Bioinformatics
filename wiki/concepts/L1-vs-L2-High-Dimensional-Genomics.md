---
title: "L1 (Lasso) vs. L2 (Ridge) Regularization in High-Dimensional Genomics"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - machine-learning
  - statistics
  - genomics
aliases:
  - Lasso vs Ridge
  - Sparse Regularization
sources:
  - "[[wiki/summaries/cambridge-ml-mathematics-lectures]]"
---

# L1 (Lasso) vs. L2 (Ridge) Regularization in High-Dimensional Genomics

In modern omics studies (transcriptomics, whole-genome sequencing), datasets invariably operate in the **high-dimensional $p \gg n$ regime**, where the number of measured features (genes, variants, transcripts $p \approx 20,000\text{--}1,000,000$) vastly exceeds the number of clinical patient samples ($n \approx 50\text{--}1,000$).

## Mathematical Comparison

Given design matrix $\mathbf{X} \in \mathbb{R}^{n \times p}$ and response vector $\mathbf{y} \in \mathbb{R}^n$:

### 1. $L_1$ Regularization (Lasso)
$$\hat{\boldsymbol{\beta}}_{\text{Lasso}} = \arg\min_{\boldsymbol{\beta}} \left\{ \frac{1}{2n}\|\mathbf{y} - \mathbf{X}\boldsymbol{\beta}\|_2^2 + \lambda \|\boldsymbol{\beta}\|_1 \right\}$$
- **Geometry**: The non-differentiable diamond vertices of the $L_1$ ball ($\sum |\beta_j| \le t$) force exact sparsity ($\beta_j = 0$).
- **Genomic Utility**: Solves the variable selection problem by identifying small, interpretable biomarker signatures ($s \ll p$) associated with disease outcomes (e.g. TNBC drug response).

### 2. $L_2$ Regularization (Ridge)
$$\hat{\boldsymbol{\beta}}_{\text{Ridge}} = \arg\min_{\boldsymbol{\beta}} \left\{ \frac{1}{2n}\|\mathbf{y} - \mathbf{X}\boldsymbol{\beta}\|_2^2 + \lambda \|\boldsymbol{\beta}\|_2^2 \right\} = (\mathbf{X}^T\mathbf{X} + \lambda \mathbf{I})^{-1}\mathbf{X}^T\mathbf{y}$$
- **Geometry**: Smooth spherical constraint shrinks coefficients toward zero without setting any exactly to zero.
- **Limitation in Sparse Genomics**: Shrinks all non-causal background genes uniformly, retaining noisy dense models with inferior out-of-sample prediction error when the underlying biology is governed by a sparse set of driver pathways.

## Related Concepts & Syntheses
- [[Bias-Variance-Tradeoff]] — controlling parameter variance in large $p$.
- [[Cambridge-ML-Math]]
- [[High-Dimensional-Machine-Learning-in-Genomics]] — overarching synthesis.
