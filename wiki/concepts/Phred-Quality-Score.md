---
title: "Phred Quality Score & Sequencing Error Probabilities"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - genomics
  - sequencing
  - quality-control
aliases:
  - Phred Score
  - Q-Score
sources:
  - "[[wiki/summaries/bioinformatics-research-journal]]"
---

# Phred Quality Score & Sequencing Error Probabilities

The **Phred Quality Score** ($Q$) is a logarithmically scaled metric assigned to each base call in high-throughput sequencing (FASTQ format) quantifying the probability of an erroneous base call:

$$Q = -10 \log_{10}(P)$$

$$P = 10^{-\frac{Q}{10}}$$

where $P$ is the estimated probability that the base call is incorrect.

## Standard Interpretive Benchmarks

| Phred Score ($Q$) | Error Probability ($P$) | Base Call Accuracy | Standard Domain |
|---|---|---|---|
| **$Q10$** | $1 \text{ in } 10$ ($0.1$) | $90.0\%$ | Early long-read raw nanopore |
| **$Q20$** | $1 \text{ in } 100$ ($0.01$) | $99.0\%$ | Standard ONT duplex / R10.4.1 |
| **$Q30$** | $1 \text{ in } 1,000$ ($0.001$) | $99.9\%$ | Illumina short-read clinical benchmark |
| **$Q40$** | $1 \text{ in } 10,000$ ($0.0001$) | $99.99\%$ | High-fidelity PacBio HiFi |

## Related Entities & Concepts
- [[Oxford-Nanopore-Sequencing]] — real-time raw signal basecalling accuracy.
- [[Genomic-Analyzer]] — downstream filtering.
- [[Bio-SeqIO]] — FASTQ parsing (`fastq-sanger`, `fastq-illumina`).
