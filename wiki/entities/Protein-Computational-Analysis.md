---
title: "Protein Biophysics & Folding Analyzer (starter_kit)"
type: entity
created: 2026-08-17
updated: 2026-08-17
tags:
  - software-tools
  - biophysics
  - python
aliases:
  - protein_computational_analysis.py
sources:
  - "[[wiki/summaries/starter-kit-protein-computational-analysis]]"
---

# Protein Biophysics & Folding Analyzer (`protein_computational_analysis.py`)

A quantitative structural biophysics analyzer in `starter_kit/` that evaluates the physical and thermodynamic stability of protein conformations from crystallographic PDB coordinates.

## Command-Line Interface (CLI)

```bash
python starter_kit/protein_computational_analysis.py --download 1coh --chain A --output_img sample_data/biophysical_profile.png
```

## Key Computations
1. **Hydrophobic Core Scoring**: Integrates local coordination number with Kyte-Doolittle hydropathy values.
2. **Contact Potential Energy**: Aggregates pairwise non-covalent statistical interaction energies using a simplified Miyazawa-Jernigan (MJ) matrix.
3. **Rigidity Analysis**: Computes the Pearson correlation between isotropic B-factors (thermal vibration) and local packing density.
4. **SASA Estimation**: Approximates fractional solvent accessibility based on local residue packing in a $10.0\text{ \AA}$ sphere.

## Related Concepts & Tools
- [[Kyte-Doolittle-Hydropathy]] — amino acid hydrophobicity index.
- [[Miyazawa-Jernigan-Potentials]] — statistical contact matrix.
- [[B-Factor-Thermal-Displacement]] — crystallographic thermal factor.
- [[Solvent-Accessible-Surface-Area]] — solvent boundary estimation.
- [[Insulin-1COH]] — reference crystal structure.
