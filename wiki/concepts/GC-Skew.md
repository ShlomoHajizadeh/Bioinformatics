---
title: "Genomic GC-Skew"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - bioinformatics
  - genomics
  - algorithms
aliases:
  - GC Skew
  - Replication Origin Skew
---

# Genomic GC-Skew

**Genomic GC-Skew** is a windowed comparative metric used to detect asymmetric nucleotide substitution patterns between the leading and lagging strands of DNA replication, primarily in circular bacterial and viral genomes.

## Mathematical Formulation

Over a designated sliding window $W$ across the genome:

$$S_{GC} = \frac{C - G}{C + G}$$

where:
- $C$ is the count/frequency of Cytosine residues within the window.
- $G$ is the count/frequency of Guanine residues within the window.

## Biological Significance

- **Origin of Replication ($oriC$)**: Marked by a global minimum in cumulative GC-skew where replication transitions from lagging to leading synthesis.
- **Terminus of Replication ($ter$)**: Marked by the global maximum in cumulative GC-skew.

## Related Concepts & Tools
- [[Biopython]] — used to implement sliding-window sequence analyzers (`SeqIO`).
- [[Kyte-Doolittle-Hydropathy]] — complementary sliding-window technique for amino acid sequences.
