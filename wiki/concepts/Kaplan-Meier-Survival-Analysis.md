---
title: "Kaplan-Meier Survival Analysis & Log-Rank Testing"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - biostatistics
  - clinical-genomics
  - oncology
aliases:
  - Kaplan-Meier
  - Survival Analysis
  - Log-Rank Test
sources:
  - "[[wiki/summaries/integrated-bioinformatics-analysis-roadmap]]"
---

# Kaplan-Meier Survival Analysis & Log-Rank Testing

**Kaplan-Meier Survival Analysis** is a non-parametric statistic used to estimate the survival function $S(t) = P(T > t)$ from time-to-event clinical cohort data subject to right-censoring.

## Mathematical Formulation

The product-limit estimator is given by:

$$\hat{S}(t) = \prod_{i: t_i \le t} \left(1 - \frac{d_i}{n_i}\right)$$

where:
- $t_i$ represents distinct event times.
- $d_i$ is the number of deceased/relapsed events occurring at time $t_i$.
- $n_i$ is the number of individuals at risk immediately prior to $t_i$.

## Log-Rank Test & Hazard Ratios
- Compares the survival distributions of two expression cohorts (e.g. high vs. low hub gene expression stratified by median cutoff).
- **Cox Proportional Hazards Model**: $h(t \mid X) = h_0(t) \exp(\boldsymbol{\beta}^T \mathbf{X})$ to derive multi-variable Hazard Ratios (HR) adjusted for age, stage, and treatment.

## Related Concepts & Tools
- [[Protein-Protein-Interaction-Networks]] — provides target hub genes for stratification.
- [[GEO-TCGA]] — clinical datasets.
