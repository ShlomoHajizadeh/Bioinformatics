---
title: "Genomic Analyzer (starter_kit)"
type: entity
created: 2026-08-17
updated: 2026-08-17
tags:
  - software-tools
  - genomics
  - python
aliases:
  - genomic_analyzer.py
sources:
  - "[[wiki/summaries/starter-kit-genomic-analyzer]]"
---

# Genomic Analyzer (`genomic_analyzer.py`)

The **Genomic Analyzer** is a standalone Python bioinformatics tool in `starter_kit/` designed for high-performance sequence operations, transcription/translation simulations, and Hamming-distance point mutation profiling.

## Command-Line Interface (CLI)

```bash
# Run transcription, translation, and GC analysis
python starter_kit/genomic_analyzer.py --file starter_kit/sample_data/tnbc_sample.fasta --transcribe --translate --gc

# Compare normal and tumor sequences using Hamming distance
python starter_kit/genomic_analyzer.py --file starter_kit/sample_data/tnbc_sample.fasta --compare
```

## Internal Architecture
- `parse_fasta(file_path)`: Custom multi-line fasta parser.
- `transcribe_dna_to_rna(dna_sequence)`: DNA $\to$ RNA converter.
- `translate_rna_to_protein(rna_sequence)`: ORF scanner identifying `AUG` to Stop codon transitions.
- `calculate_gc_content(sequence)`: Base frequency calculator.
- `calculate_hamming_distance(seq1, seq2)`: Point mutation detector.
- `visualize_mutation_alignment(seq1, seq2)`: ANSI terminal colorized comparator.

## Related Entities & Concepts
- [[Hamming-Distance-Genomics]] — underlying mathematical metric.
- [[TP53]] — benchmark sequence used in sample dataset.
- [[Rosalind-Platform]] — addresses Rosalind problems `DNA`, `RNA`, `PROT`, `GC`, `HAMM`.
