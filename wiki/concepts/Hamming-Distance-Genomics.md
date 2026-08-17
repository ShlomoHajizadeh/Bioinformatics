---
title: "Hamming Distance in Genomics"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - bioinformatics
  - genomics
  - algorithms
aliases:
  - Hamming Distance
  - Point Mutation Counting
sources:
  - "[[wiki/summaries/starter-kit-genomic-analyzer]]"
---

# Hamming Distance in Genomics

**Hamming Distance** ($D_H$) is an information-theoretic distance metric measuring the number of positions at which two biological sequences of equal length differ. In computational genomics, it serves as the foundational algorithm for quantifying single nucleotide polymorphisms (SNPs) and point mutations between homologous sequences (e.g., germline vs. somatic tumor DNA).

## Mathematical Formulation

For two aligned sequences $s_1$ and $s_2$ of length $n$:

$$D_H(s_1, s_2) = \sum_{i=1}^{n} \mathbb{I}[s_1[i] \neq s_2[i]]$$

where $\mathbb{I}[\cdot]$ is the indicator function evaluating to 1 when characters mismatch and 0 when identical.

## Clinical Application Example
- **TP53 Exon 5 Mutation Hotspots**: Distinguishing wild-type `NM_000546.6` from mutated Triple-Negative Breast Cancer (TNBC) oncogenic alleles (e.g., R175H transversion at codon 175).

## Related Entities & Concepts
- [[Genomic-Analyzer]] — CLI implementation with ANSI sequence alignment.
- [[TP53]] — standard biological benchmarking target.
- [[Rosalind-Platform]] — Rosalind problem `HAMM`.
