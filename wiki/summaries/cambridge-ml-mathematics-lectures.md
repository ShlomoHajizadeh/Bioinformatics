---
title: "Source Summary: Cambridge Mathematics of Machine Learning Lectures"
type: summary
created: 2026-08-17
updated: 2026-08-17
tags:
  - machine-learning
  - mathematics
  - statistics
  - cambridge
sources:
  - "[[courses/cambridge_ml_math/R_lectures/]]"
---

# Source Summary: Cambridge Mathematics of Machine Learning Lectures

- **Path**: `courses/cambridge_ml_math/R_lectures/`
- **Curriculum**: University of Cambridge, Mathematics of Machine Learning
- **Scope**: Mathematical foundations of statistical estimation, non-parametric classification, high-dimensional regularization, and ensemble learning.

## Key Theoretical Themes & Scripts

1. **Bias-Variance Tradeoff & Model Selection (`03_bias_variance_tradeoff_and_CV.R`)**:
   - Decomposes mean squared error into $\text{MSE} = \text{Bias}^2 + \text{Variance} + \sigma^2$.
   - Evaluates the projection Hat matrix $\mathbf{H} = \mathbf{\Phi}(\mathbf{\Phi}^T\mathbf{\Phi})^{-1}\mathbf{\Phi}^T = \mathbf{U}\mathbf{U}^T$ via Singular Value Decomposition (SVD).
   - Simulates K-fold cross-validation with sample permutation testing to empirically identify the global error minimum.
2. **Nonparametric Function Spaces & Histogram Classifiers (`07_histogram_classifier.R`, `09_vector_space_of_fns.R`)**:
   - Partitioning feature space into hyper-cubes of width $1/m$ to approach the Bayes optimal decision boundary.
   - Polynomial basis expansions $\mathbf{\Phi}(x)$ under $L_2$ shrinkage to avoid combinatorial explosion.
3. **High-Dimensional $L_1$ vs. $L_2$ Sparsity in $p \gg n$ Regimes (`12_l1_vs_l2.R`)**:
   - Tests sparse signals where $s \ll p$ (e.g. $s = 10$, $p = 500$, $n = 1000$).
   - Demonstrates how $L_1$ regularization (Lasso / $\alpha=0.95$) achieves Bayes-optimal classification error by performing exact variable selection, whereas $L_2$ (Ridge / $\alpha=0$) fails in sparse genomic scenarios due to dense coefficient shrinkage.
4. **Ensemble Theory: Bagging, Random Forests & Boosting (`04_trees.R`, `05_random_forest.R`, `15_Adaboost_demo.R`, `16_Gradient_boosting_linear.R`)**:
   - Variance reduction via de-correlated decision tree bootstrap aggregation (Random Forests).
   - Discrete AdaBoost and Gradient Boosting optimizing exponential and differentiable loss functions in additive function space.

## Cross-Linked Entities & Concepts
- **Concepts**: [[Bias-Variance-Tradeoff]], [[L1-vs-L2-High-Dimensional-Genomics]], [[Boosting-Theory-AdaBoost]]
- **Entities**: [[Cambridge-ML-Math]]
- **Syntheses**: [[High-Dimensional-Machine-Learning-in-Genomics]]
