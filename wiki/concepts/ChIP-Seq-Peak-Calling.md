---
title: "ChIP-Seq & Epigenomic Peak Calling"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - epigenomics
  - sequencing
  - transcription-factors
aliases:
  - ChIP-Seq
  - Peak Calling
sources:
  - "[[wiki/summaries/bioinformatics-research-journal]]"
---

# ChIP-Seq & Epigenomic Peak Calling

**ChIP-Seq (Chromatin Immunoprecipitation Sequencing)** couples selective antibody-based immunoprecipitation of DNA-binding proteins (transcription factors, coregulators, modified histones) with massively parallel high-throughput sequencing to profile physical genome-wide interaction landscapes.

## Peak Calling Methodology (MACS / MACS2/3)

1. **Tag Shift & Fragment Size Estimation**: Cross-correlation between Watson and Crick strand tag densities identifies the average ChIP DNA fragment length ($d$).
2. **Dynamic Background $\lambda_{\text{local}}$**: Computes local Poisson background lambda over multiple genomic windows ($1\text{ kb}, 5\text{ kb}, 10\text{ kb}$):
   $$\lambda_{\text{local}} = \max(\lambda_{\text{BG}}, \lambda_{1\text{k}}, \lambda_{5\text{k}}, \lambda_{10\text{k}})$$
3. **Statistical Significance**: Poisson $p$-value and Benjamini-Hochberg False Discovery Rate (FDR $q$-value) filtering.

## Related Concepts & Tools
- [[Sequence-Motif-Discovery]] — extracting consensus binding matrices from peak intervals.
- [[Nextflow-WDL]] — automated processing via `nf-core/chipseq`.
