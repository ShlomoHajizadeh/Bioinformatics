---
title: "Bias-Variance Tradeoff & Mathematical Model Selection"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - machine-learning
  - statistics
  - mathematics
aliases:
  - Bias Variance Tradeoff
  - Model Selection
sources:
  - "[[wiki/summaries/cambridge-ml-mathematics-lectures]]"
---

# Bias-Variance Tradeoff & Mathematical Model Selection

The **Bias-Variance Tradeoff** is the fundamental theoretical tension in supervised statistical learning between the approximation error of a model family (bias) and the sensitivity of the fitted estimator to random fluctuations in the training dataset (variance).

## Mathematical Formulation

For an unknown target function $Y = f(X) + \epsilon$ with zero-mean irreducible noise $\mathbb{E}[\epsilon] = 0$ and $\text{Var}(\epsilon) = \sigma^2$:

$$\mathbb{E}\left[(Y - \hat{f}(X))^2\right] = \underbrace{\left(\mathbb{E}[\hat{f}(X)] - f(X)\right)^2}_{\text{Bias}^2(\hat{f}(X))} + \underbrace{\mathbb{E}\left[(\hat{f}(X) - \mathbb{E}[\hat{f}(X)])^2\right]}_{\text{Variance}(\hat{f}(X))} + \underbrace{\sigma^2}_{\text{Irreducible Noise}}$$

## Linear Smoother & Hat Matrix

For linear estimators $\hat{\mathbf{y}} = \mathbf{H}\mathbf{y}$, where $\mathbf{H} = \mathbf{\Phi}(\mathbf{\Phi}^T\mathbf{\Phi})^{-1}\mathbf{\Phi}^T$:
- Model degrees of freedom is given by $\text{tr}(\mathbf{H})$.
- Total variance scales with $\sigma^2 \text{tr}(\mathbf{H}\mathbf{H}^T) = \sigma^2 \text{tr}(\mathbf{H}) = \sigma^2 p$.
- Model selection via K-fold cross-validation and permutation tests optimizes the model complexity parameter (e.g. polynomial degree or regularization parameter $\lambda$) to minimize total expected test error.

## Related Concepts & Tools
- [[L1-vs-L2-High-Dimensional-Genomics]] — regularization to control variance.
- [[Boosting-Theory-AdaBoost]] — bias-reduction via iterative additive modeling.
- [[Cambridge-ML-Math]] — mathematical curriculum source.
