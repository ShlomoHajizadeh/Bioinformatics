---
title: "Bio.SeqIO (Biopython Sequence Input/Output Module)"
type: entity
created: 2026-08-17
updated: 2026-08-17
tags:
  - biopython
  - software-tools
  - sequence-analysis
aliases:
  - SeqIO
  - Bio.SeqIO
sources:
  - "[[wiki/summaries/biopython-curriculum-30-modules]]"
---

# Bio.SeqIO

**`Bio.SeqIO`** is Biopython's standard unified sequence input/output interface for reading, parsing, converting, and indexing biological sequence file formats.

## Key Methods
- `SeqIO.parse(handle, format)`: Generator returning `SeqRecord` objects one by one (memory-efficient for multi-gigabyte FASTA/FASTQ files).
- `SeqIO.read(handle, format)`: Returns a single `SeqRecord` for single-entry files (errors if multiple records exist).
- `SeqIO.write(records, handle, format)`: Serializes `SeqRecord` objects into the specified file format.
- `SeqIO.convert(in_file, in_fmt, out_file, out_fmt)`: High-performance stream converter between formats (e.g. GenBank $\to$ FASTA).
- `SeqIO.index(filename, format)`: Builds an on-disk dictionary mapping record IDs to seek offsets for random access.

## Supported Formats
FASTA, GenBank, EMBL, FASTQ (Illumina/Sanger), ABI trace, Clustal, PHYLIP, SwissProt, Tab-delimited.

## Related Entities & Concepts
- [[Biopython]] — parent library.
- [[Bio-AlignIO]] — alignment counterpart.
- [[Genomic-Analyzer]] — custom FASTA parser implementation.
