---
title: "Bio.Entrez (NCBI E-Utilities Interface)"
type: entity
created: 2026-08-17
updated: 2026-08-17
tags:
  - biopython
  - databases
  - ncbi
aliases:
  - Bio.Entrez
  - Entrez
sources:
  - "[[wiki/summaries/biopython-curriculum-30-modules]]"
---

# Bio.Entrez

**`Bio.Entrez`** is the Python client module in Biopython for querying NCBI's Entrez E-utilities (Entrez Programming Utilities).

## Core E-Utilities Functions
- **`Entrez.esearch`**: Searches any NCBI database (PubMed, Nucleotide, Protein, Gene) and returns UIDs.
- **`Entrez.efetch`**: Downloads full biological records (FASTA, GenBank, XML, Medline) for specific UIDs.
- **`Entrez.esummary`**: Returns document summaries (DocSums) for a list of primary IDs.
- **`Entrez.elink`**: Discovers related items across different NCBI databases (e.g. finding Nucleotide sequences linked to a PubMed article).
- **`Entrez.read`**: Parses NCBI XML responses into Python dictionaries and lists.

## Compliance & Rate Limiting
- Requires setting `Entrez.email = "user@example.com"` and optional `Entrez.api_key`.
- Limits automated requests to standard NCBI API rate ceilings (3 requests/sec without key; 10 requests/sec with API key).

## Related Entities
- [[Biopython]] — parent package.
- [[Bio-SeqIO]] — parses records returned from `efetch`.
