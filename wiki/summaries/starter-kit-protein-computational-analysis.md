---
title: "Source Summary: Protein Biophysics & Folding Analyzer"
type: summary
created: 2026-08-17
updated: 2026-08-17
tags:
  - structural-biology
  - biophysics
  - code-summary
sources:
  - "[[starter_kit/protein_computational_analysis.py]]"
---

# Source Summary: `protein_computational_analysis.py`

- **File Path**: `starter_kit/protein_computational_analysis.py`
- **Author**: Suleyman Hajizadeh
- **Purpose**: Physical and thermodynamic scoring of 3D protein structures, including hydrophobic core detection, statistical contact potential energy evaluation, thermal B-factor rigidity correlations, and geometric SASA approximations.

## Key Capabilities & Algorithms

1. **Hydrophobic Core Scoring (`run_computational_analysis`)**:
   - Evaluates local spatial packing density inside an 8.0 Å sphere.
   - Weights density with Kyte-Doolittle hydropathy values: $\text{CoreScore}_i = N_{\text{neighbors}} \times h_{\text{KD}}(R_i)$.
2. **Contact Potential Energy Grid (`calculate_mj_energy`)**:
   - Groups residues into Hydrophobic ($H$), Polar ($P$), Positive ($Pos$), and Negative ($Neg$).
   - Calculates Miyazawa-Jernigan statistical potential matrix for sequence separation $\Delta \text{seq} > 2$:
     - $H \leftrightarrow H = -5.0\text{ kcal/mol}$ (Hydrophobic collapse)
     - $Pos \leftrightarrow Neg = -6.0\text{ kcal/mol}$ (Salt bridge)
     - $Pos \leftrightarrow Pos / Neg \leftrightarrow Neg = +3.0\text{ kcal/mol}$ (Repulsion)
3. **Rigidity Analysis & B-Factor Correlation**:
   - Pearson correlation between isotropic B-factors (thermal displacement) and local packing density:
     $$r = \frac{\sum (B_i - \bar{B})(P_i - \bar{P})}{\sqrt{\sum (B_i - \bar{B})^2 \sum (P_i - \bar{P})^2}}$$
   - Significant negative correlation ($r < -0.3$) validates structural stability in crystallographic cores.
4. **Fractional SASA Approximation**:
   - $\text{SASA}_{\text{est}} = \max\left(0, 1 - \frac{N_{\text{neighbors}(10\text{\AA})}}{22.0}\right)$.

## Cross-Linked Entities & Concepts
- **Concepts**: [[Kyte-Doolittle-Hydropathy]], [[Miyazawa-Jernigan-Potentials]], [[B-Factor-Thermal-Displacement]], [[Solvent-Accessible-Surface-Area]]
- **Entities**: [[Protein-Computational-Analysis]], [[Insulin-1COH]], [[Biopython]]
- **Syntheses**: [[Structural-Biophysics-vs-AI-Folding]]
