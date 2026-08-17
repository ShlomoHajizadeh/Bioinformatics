---
title: "Sequence Motif Discovery & Matrix Models"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - bioinformatics
  - genomics
  - algorithms
aliases:
  - PWM
  - PFM
  - Motif Discovery
sources:
  - "[[wiki/summaries/biopython-curriculum-30-modules]]"
---

# Sequence Motif Discovery & Matrix Models

**Sequence Motif Discovery** identifies conserved short, recurring sequence patterns in biological polymers that have functional biological significance (e.g. Transcription Factor Binding Sites [TFBS], splice junctions, phosphorylation motifs).

## Quantitative Matrix Representations

1. **Position Frequency Matrix (PFM)**: Direct counts $C(b, j)$ of base/amino acid $b$ at column position $j$.
2. **Position Probability Matrix (PPM)**: Normalization of frequencies into empirical probabilities:
   $$P(b, j) = \frac{C(b, j) + s(b)}{N + \sum s(b)}$$
   where $s(b)$ represents pseudocounts to avoid zero-probability artifacts.
3. **Position Weight Matrix (PWM) / Log-Odds Matrix**:
   $$W(b, j) = \log_2 \left( \frac{P(b, j)}{Q(b)} \right)$$
   where $Q(b)$ is the background nucleotide frequency (typically 0.25 each or GC-adjusted).

## Information Content & Sequence Logos
The total sequence conservation at position $j$ is measured using Shannon information entropy ($R_{\text{seq}}$ in bits):

$$R_{\text{seq}}(j) = 2 - \left( -\sum_{b \in \{A,C,G,T\}} P(b, j) \log_2 P(b, j) \right)$$

## Related Tools & Modules
- [[Biopython]] — `Bio.motifs` module.
- [[Genomic-Analyzer]] — pattern matching.
