---
title: "BLAST (Basic Local Alignment Search Tool)"
type: entity
created: 2026-08-17
updated: 2026-08-17
tags:
  - software-tools
  - ncbi
  - sequence-alignment
aliases:
  - BLAST
  - BLAST+
  - blastp
  - blastn
sources:
  - "[[wiki/summaries/bioinformatics-research-journal]]"
---

# BLAST (Basic Local Alignment Search Tool)

**BLAST** is the standard NCBI suite of heuristic local sequence alignment search tools.

## Flavors of BLAST
- **`blastn`**: Nucleotide query against nucleotide database.
- **`blastp`**: Protein query against protein database.
- **`blastx`**: Nucleotide query (6-frame translated) against protein database.
- **`tblastn`**: Protein query against translated nucleotide database.
- **`tblastx`**: 6-frame translated query against 6-frame translated database.

## Related Concepts & Tools
- [[BLAST-Algorithm-Heuristics]] — word seeding and Karlin-Altschul E-value statistics.
- [[Biopython]] — programmatic interface via `Bio.Blast`.
