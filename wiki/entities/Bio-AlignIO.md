---
title: "Bio.AlignIO (Biopython Alignment I/O Module)"
type: entity
created: 2026-08-17
updated: 2026-08-17
tags:
  - biopython
  - sequence-alignment
  - software-tools
aliases:
  - Bio.AlignIO
  - AlignIO
sources:
  - "[[wiki/summaries/biopython-curriculum-30-modules]]"
---

# Bio.AlignIO

**`Bio.AlignIO`** is Biopython's standard module for reading, writing, and manipulating Multiple Sequence Alignment (MSA) data objects (`MultipleSeqAlignment`).

## Key Operations
- `AlignIO.read(handle, format)`: Loads a single alignment containing multiple aligned sequences of identical length.
- `AlignIO.parse(handle, format)`: Iterates over multiple alignments from a file.
- `AlignIO.write(alignments, handle, format)`: Serializes alignments into target formats.
- `AlignIO.convert(in_file, in_fmt, out_file, out_fmt)`: Stream conversion across formats.

## Supported Formats
Clustal, FASTA (aligned), PHYLIP, Stockholm, Nexus, MAF (Multiple Alignment Format), Mauve.

## Related Concepts & Tools
- [[Multiple-Sequence-Alignment]] — analytical concepts.
- [[Bio-SeqIO]] — unaligned sequence counterpart.
- [[Bio-Phylo]] — downstream tree reconstruction from alignments.
