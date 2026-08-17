---
title: "Boosting Theory & Additive Models (AdaBoost & Gradient Boosting)"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - machine-learning
  - algorithms
  - boosting
aliases:
  - AdaBoost
  - Gradient Boosting
sources:
  - "[[wiki/summaries/cambridge-ml-mathematics-lectures]]"
---

# Boosting Theory & Additive Models

**Boosting** is an ensemble methodology in statistical machine learning that sequentially combines a collection of weak base learners $h_m(x)$ into a highly accurate composite predictor $F(x) = \sum_{m=1}^M \alpha_m h_m(x)$.

## Discrete AdaBoost (Adaptive Boosting)

Iteratively minimizes the empirical exponential loss function $L(y, F(x)) = \exp(-y F(x))$ for binary targets $y \in \{-1, +1\}$:

1. **Initialize Sample Weights**: $w_i^{(1)} = \frac{1}{n}$.
2. **Train Weak Learner**: Fit $h_m(x)$ to minimize weighted classification error $\epsilon_m = \sum_{i=1}^n w_i^{(m)} \mathbb{I}[y_i \neq h_m(x_i)]$.
3. **Compute Learner Weight**:
   $$\alpha_m = \frac{1}{2} \ln \left( \frac{1 - \epsilon_m}{\epsilon_m} \right)$$
4. **Update Sample Weights**:
   $$w_i^{(m+1)} = \frac{w_i^{(m)} \exp(-\alpha_m y_i h_m(x_i))}{Z_m}$$
   where $Z_m$ is a normalization constant ensuring $\sum w_i^{(m+1)} = 1$.

## Gradient Boosting & Genomic Applications
- Generalizes boosting to arbitrary differentiable loss functions (e.g. binomial deviance, Poisson loss) by fitting base trees to pseudo-residuals $-\left[\frac{\partial L(y_i, F(x_i))}{\partial F(x_i)}\right]$.
- Standard in functional genomics for variant effect prediction (VEP), pathogenicity scoring, and promoter/enhancer activity classification.

## Related Concepts & Tools
- [[Bias-Variance-Tradeoff]] — boosting primarily targets bias reduction.
- [[Cambridge-ML-Math]]
