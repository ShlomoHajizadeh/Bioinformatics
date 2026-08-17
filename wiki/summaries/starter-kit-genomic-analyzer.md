---
title: "Source Summary: Genomic Analyzer & Mutation Detector"
type: summary
created: 2026-08-17
updated: 2026-08-17
tags:
  - bioinformatics
  - genomics
  - code-summary
sources:
  - "[[starter_kit/genomic_analyzer.py]]"
---

# Source Summary: `genomic_analyzer.py`

- **File Path**: `starter_kit/genomic_analyzer.py`
- **Author**: Süleyman Hacızadə
- **Purpose**: Production-grade FASTA sequence parsing, transcription/translation engine, GC content calculation, and Hamming-distance point mutation (SNP) detection with live terminal ANSI alignment.

## Key Capabilities & Algorithms

1. **FASTA Parsing (`parse_fasta`)**: Reads single/multi-record FASTA files without external dependencies.
2. **Transcription (`transcribe_dna_to_rna`)**: Biochemical simulation replacing Thymine (`T`) with Uracil (`U`).
3. **Translation (`translate_rna_to_protein`)**: Open Reading Frame (ORF) translation from `AUG` to Stop codons (`UAA`, `UAG`, `UGA`) using the Standard Genetic Code dictionary.
4. **GC Content (`calculate_gc_content`)**: Exact $(G+C)/Total \times 100$ percentage calculation.
5. **Hamming Distance & Visual Alignment (`calculate_hamming_distance`, `visualize_mutation_alignment`)**:
   - $D_H(s_1, s_2) = \sum_{i=1}^{n} \mathbf{1}[s_1[i] \neq s_2[i]]$
   - Colorized terminal alignment highlighting SNPs (e.g., TP53 codon 175 R175H hotspot).

## Cross-Linked Entities & Concepts
- **Concepts**: [[Hamming-Distance-Genomics]], [[GC-Skew]]
- **Entities**: [[Genomic-Analyzer]], [[TP53]], [[Rosalind-Platform]]
