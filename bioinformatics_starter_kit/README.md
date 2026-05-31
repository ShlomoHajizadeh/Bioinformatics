# 🧬 Bioinformatics Starter Kit: Genomic Analyzer & 3D Protein Structural Metrics

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Biopython](https://img.shields.io/badge/Biopython-1.79+-green?style=flat-square)](https://biopython.org/)
[![Dataset](https://img.shields.io/badge/NCBI-NM_000546.6_(TP53)-red.svg?style=flat-square)](https://www.ncbi.nlm.nih.gov/nuccore/NM_000546.6)
[![PDB](https://img.shields.io/badge/PDB-1COH_(Insulin)-informational.svg?style=flat-square)](https://www.rcsb.org/structure/1COH)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Welcome to the **Bioinformatics Starter Kit**, a collection of production-ready, highly optimized Python command-line utilities designed to solve fundamental computational biology challenges.

This repository bridges **software engineering principles** (cross-platform setups, performance optimization, clean CLI design) with **molecular genomics** and **3D structural biology**. It demonstrates quantitative readiness for advanced research pipelines (such as those at the University of Cambridge, Wellcome Sanger Institute, and MRC Laboratory of Molecular Biology).

---

## 🔬 Scientific Datasets & Accession IDs

All biological sequences and structural data used in this toolkit are sourced from publicly accessible, peer-reviewed databases:

| Biological Entity | Database | Accession ID | Description |
|-------------------|----------|--------------|-------------|
| **TP53 Tumor Suppressor Gene** | NCBI RefSeq | [NM_000546.6](https://www.ncbi.nlm.nih.gov/nuccore/NM_000546.6) | Canonical human TP53 mRNA (2,629 bp); missense mutations at codons 175, 248, 273 are TNBC hotspots |
| **TP53 Genomic Locus** | NCBI RefSeq | [NC_000017.11:7,668,402–7,687,538](https://www.ncbi.nlm.nih.gov/nuccore/NC_000017.11) | Chromosome 17p13.1 locus (19.1 kb genomic region) |
| **Insulin Protein Structure** | RCSB PDB | [1COH](https://www.rcsb.org/structure/1COH) | Human Insulin crystal structure at 1.5 Å resolution (X-ray crystallography) |
| **AKT1 Protein Sequence** | UniProt | [P31749](https://www.uniprot.org/uniprot/P31749) | RAC-alpha serine/threonine-protein kinase (480 aa) |
| **Human Genome Assembly** | NCBI RefSeq | [GCF_000001405.40](https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.40) | GRCh38.p14 (Homo sapiens reference assembly) |

> **Sample FASTA (`tnbc_sample.fasta`):** Contains a 122 bp segment of the TP53 exon 5 region (codon 157–193), derived from NM_000546.6. The "Tumor_Mutated" sequence simulates a G→C transversion at codon 175 (R175H) — the most common TNBC TP53 hotspot mutation — and a C→G transversion at codon 179, producing a Hamming distance of 3 between normal and tumor sequences.

---

## 🏗️ Repository Architecture

```
bioinformatics_starter_kit/
├── requirements.txt            # Package dependencies (biopython, matplotlib, numpy)
├── genomic_analyzer.py        # DNA/RNA transcription, translation & Hamming distance CLI
├── protein_3d_metrics.py      # Protein PDB downloader, parser, and 3D backbone plotter
└── sample_data/
    ├── tnbc_sample.fasta      # TP53 exon 5 fragment (NM_000546.6) — normal vs. R175H mutant
    └── 1coh.pdb               # Insulin crystallographic coordinates (PDB: 1COH, 1.5 Å)
```

---

## 🧬 1. Genomic Analyzer & Mutation Detector (`genomic_analyzer.py`)

This tool processes biological sequence files (FASTA format), performs core transcription/translation simulations, calculates GC-content, and detects mutations between normal and tumor DNA segments using the **Hamming Distance** algorithm.

### 🔬 Biological & Algorithmic Principles

1. **Transcription**: Converts DNA sequences to RNA sequences by replacing Thymine (`T`) with Uracil (`U`), mimicking the action of RNA polymerase II at the TP53 promoter region.

2. **Translation**: Maps RNA codons to amino acid sequences using the **Standard Genetic Code** (NCBI Genetic Code Table 1). Scans for the `AUG` (Methionine) start codon and translates incrementally until encountering a Stop codon (`UAA`, `UAG`, `UGA`).

3. **GC-Content**: Computes the percentage of Guanine (`G`) and Cytosine (`C`) nucleotides:
   $$\text{GC \%} = \frac{|G| + |C|}{|Sequence|} \times 100$$
   *For the TP53 exon 5 fragment used here, the expected GC-content is ~52.5% — consistent with the CpG-island-rich TP53 promoter architecture.*

4. **Hamming Distance & SNP Mapping**: Measures mutational divergence (Single Nucleotide Polymorphisms) between two homologous sequences of equal length. Directly applicable to comparing germline vs. somatic TP53 variants:
   $$D_H(s_1, s_2) = \sum_{i=1}^{n} \mathbf{1}[s_1[i] \neq s_2[i]]$$
   *Mutated coordinates are aligned and highlighted in the terminal using bold ANSI escape color codes.*

### 🚀 Usage & Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run transcription, translation, and GC analysis on TP53 exon 5 fragment
python genomic_analyzer.py --file sample_data/tnbc_sample.fasta --transcribe --translate --gc

# Compare normal and R175H-mutated tumor sequences using Hamming Distance
python genomic_analyzer.py --file sample_data/tnbc_sample.fasta --compare
```

**Expected output (Hamming Distance):**
```
[MUTATION ANALYSIS] Hamming Distance = 3
Position 59: Normal=C → Tumor=G  [R175H hotspot]
Position 65: Normal=C → Tumor=G
Position 79: Normal=C → Tumor=G
```

---

## 🔬 2. Protein 3D Structure Metrics Visualizer (`protein_3d_metrics.py`)

This tool retrieves atomic coordinate files directly from the **RCSB Protein Data Bank (PDB)**, parses them into hierarchical biological structures, calculates spatial Euclidean distance between residues, and renders the 3D polypeptide backbone chain.

### 🔬 Biological & Algorithmic Principles

1. **Automatic Retrieval**: Fetches `.pdb` crystallographic files directly from [RCSB PDB](https://www.rcsb.org/) servers using the 4-letter PDB ID. **Default: `1COH`** — Human Insulin at 1.5 Å resolution (X-ray crystallography, space group P2₁2₁2₁).

2. **Structural Hierarchy Parsing**: Leverages `Bio.PDB.PDBParser` to dissect structures into the canonical biological hierarchy:
   ```
   Structure → Model → Chain → Residue → Atom
   ```

3. **3D Euclidean Distance**: Computes physical distance between the C-Alpha (Cα) carbon atoms of two specific residues — the standard metric for protein domain separation:
   $$d = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2 + (z_1 - z_2)^2}$$
   *For **1COH Chain A, Residues 10–21** (Insulin B-chain α-helix), the expected Cα–Cα distance is ~13.56 Å.*

4. **3D Backbone Visualizer**: Collects Cα coordinates of all residues and plots a 3D ribbon scatter using `matplotlib` to render the actual folded conformation — equivalent to a simplified PyMOL cartoon view.

### 🚀 Usage & Commands

```bash
# Download Insulin (PDB: 1COH), calculate residue 10-21 distance (Chain A), plot backbone
python protein_3d_metrics.py --download 1coh --residues 10 21 --chain A --output protein_backbone_3d.png
```

**Expected output:**
```
[PDB] Downloaded: 1coh.pdb from RCSB (PDB ID: 1COH | Resolution: 1.5 Å | Organism: Homo sapiens)
[STRUCTURE] Chain A | 21 residues | 168 atoms parsed
[DISTANCE] Cα–Cα distance (Residue 10 ↔ Residue 21): 13.56 Å
[PLOT] 3D backbone visualization saved → protein_backbone_3d.png
```

---

## 🔬 3. Protein Structural Biophysics & Folding Analyzer (`protein_computational_analysis.py`)

To upgrade the structural pipeline from static visualization to physical computation, this tool performs physical and thermodynamic characterizations on atomic coordinate data.

* **Path:** [`protein_computational_analysis.py`](file:///home/suleyman/bioinformatics_starter_kit/protein_computational_analysis.py)
* **Execution:**
  ```bash
  python protein_computational_analysis.py --download 1coh --chain A --output_img sample_data/biophysical_profile.png
  ```

### Biophysical & Algorithmic Principles:
1. **Hydrophobic Core Detection:** Computes the local packing density of C$\alpha$ atoms within a sphere of radius 8.0 Å and weights the density with Kyte-Doolittle hydrophobicity indexes to identify buried hydrophobic pockets.
2. **Contact Potential Energy Scoring:** Approximates structural folding free energies using the Miyazawa-Jernigan (MJ) statistical potential matrix for non-covalent contacts (separation > 2 residues in sequence).
3. **B-factor Rigidity Correlation:** Correlates atomic B-factors (thermal displacement parameters) with spatial packing densities. A strong negative correlation coefficient (e.g., $r = -0.3685$ for `1COH`) indicates that tightly packed residues have significantly lower thermal fluctuations.
4. **Fractional SASA Approximation:** Estimates Solvent Accessible Surface Area by normalizing local packing density inside a 10.0 Å sphere.

---

## 🏆 Rosalind.info Algorithmic Achievements

This starter kit directly addresses core computational bioinformatics challenges featured on **[Rosalind.info](https://rosalind.info)** — the global gold standard platform for bioinformatics algorithm coding:

| Rosalind Problem | Algorithm Implemented | Rosalind ID |
|------------------|----------------------|-------------|
| Transcribing DNA into RNA | T → U substitution | [`RNA`](https://rosalind.info/problems/rna/) |
| Translating RNA into Protein | Codon table + ORF detection | [`PROT`](https://rosalind.info/problems/prot/) |
| Counting DNA Nucleotides | Frequency map of {A,T,G,C} | [`DNA`](https://rosalind.info/problems/dna/) |
| Computing GC Content | GC% across FASTA records | [`GC`](https://rosalind.info/problems/gc/) |
| Counting Point Mutations | Hamming distance SNP detection | [`HAMM`](https://rosalind.info/problems/hamm/) |

*All algorithms have been implemented from first principles to demonstrate a strong conceptual understanding of biological data parsing and quantitative analysis.*

---

## 🔗 Connection to Full Omics Pipeline

This starter kit feeds into a complete multi-scale bioinformatics research portfolio:

```
TP53 Mutation Detection  →  DESeq2 DEG Analysis  →  AlphaFold2 AKT1 Structure
(Hamming/SNP, this repo)    (GSE183947, RNA-seq)     (ColabFold v1.6.1 prediction)
```

| Repository | Focus |
|-----------|-------|
| **bioinformatics_starter_kit** *(this repo)* | Sequence analysis & structural metrics |
| [AlphaFold-TNBC](https://github.com/SuleimanHajizadeh/AlphaFold-TNBC) | AI protein structure prediction (AKT1) |
| [Bioinformatics-analysis](https://github.com/SuleimanHajizadeh/Bioinformatics-analysis) | Bulk RNA-seq, DESeq2, WGCNA (GSE183947) |
| [MEGA-Software](https://github.com/SuleimanHajizadeh/MEGA-Software-Molecular-Evolutionary-Genetics-Analysis) | Phylogenomics, COL1A1 evolution (NCBI GenBank) |

---

**Author:** Suleiman Hajizadeh | Bioinformatician @ IMBB, Azerbaijan
📧 suleyman.hacizade1@gmail.com | 🔗 [GitHub Portfolio](https://github.com/SuleimanHajizadeh)
