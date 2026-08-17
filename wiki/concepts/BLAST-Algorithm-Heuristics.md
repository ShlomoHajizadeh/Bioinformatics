---
title: "BLAST Algorithm Heuristics & Statistical Significance"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - bioinformatics
  - sequence-alignment
  - algorithms
aliases:
  - BLAST Heuristics
  - E-Value
sources:
  - "[[wiki/summaries/bioinformatics-research-journal]]"
---

# BLAST Algorithm Heuristics & Statistical Significance

**BLAST (Basic Local Alignment Search Tool)** is a heuristic local sequence alignment algorithm designed to rapidly query biological databases (GenBank, UniProt) by identifying exact word seeds and extending them into High-scoring Segment Pairs (HSPs).

## Algorithmic Workflow

1. **Word Seeding**: Generates a list of all $k$-mers of length $W$ (default $W=3$ for proteins, $W=11\text{--}28$ for nucleotides) that match the query with score $\ge T$ under a substitution matrix (e.g. BLOSUM62).
2. **Database Scanning**: Scans the target database for exact matches to the neighborhood words.
3. **HSP Extension**: Extends matches in both directions without gaps until the running alignment score drops by more than threshold $X$ below the maximum score seen so far.
4. **Gapped Extension**: Triggers dynamic programming banded Smith-Waterman around surviving seed pairs.

## Karlin-Altschul Statistical E-Value

The statistical significance of an alignment score $S$ in a database of total length $N$ queried with a sequence of length $M$ is given by the **Expectation Value ($E$-value)**:

$$E = K M N \exp(-\lambda S)$$

where $K$ and $\lambda$ are Karlin-Altschul parameters determined by the background residue frequencies and the scoring matrix.

## Related Entities & Concepts
- [[BLAST]] — tool entity.
- [[Biopython]] — `Bio.Blast` and `NCBIXML` parsing module.
- [[Multiple-Sequence-Alignment]] — full progressive alignment counterpart.
