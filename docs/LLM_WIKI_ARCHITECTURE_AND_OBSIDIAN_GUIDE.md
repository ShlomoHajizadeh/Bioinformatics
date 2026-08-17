---
title: "Master Documentation: LLM Wiki Architecture & Obsidian Integration"
type: synthesis
created: 2026-08-17
updated: 2026-08-17
tags:
  - documentation
  - obsidian
  - llm-wiki
  - bioinformatics
---

# 📚 Master Documentation: LLM Wiki Architecture & Obsidian Integration

This document provides a complete structural map of every file in the repository and explains how the **LLM Wiki Pattern** interacts with **Obsidian** as an interactive knowledge development environment (IDE).

---

## 🏛️ 1. The 3-Layer LLM Wiki Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       LAYER 1: IMMUTABLE SOURCES                        │
│   (Raw PDFs, Code scripts, Jupyter Notebooks, Transcripts, FastA)       │
│   • starter_kit/ • courses/ • journal/ • career/ • *.pdf                │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │  Ingest & Compile (LLM Agent)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    LAYER 2: COMPILED KNOWLEDGE LAYER                    │
│   (Persistent, Cross-Linked, Structured Markdown with YAML Frontmatter)  │
│   • wiki/index.md     • wiki/log.md                                     │
│   • wiki/summaries/   • wiki/entities/                                  │
│   • wiki/concepts/    • wiki/syntheses/                                 │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │  Render, Query & Graph (User)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     LAYER 3: OBSIDIAN VISUAL IDE                        │
│   (Graph View, Dataview Queries, Local Graphs, Canvas, Search)          │
│   • .obsidian/ configuration layer                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📂 2. Exhaustive File & Directory Catalog

### A. Root Configuration & Schemas
- **[`AGENTS.md`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/AGENTS.md)**: Operating contract for AI agents detailing ingestion rules, frontmatter schema, `[[wikilink]]` standards, and lint routines.
- **[`GEMINI.md`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/GEMINI.md)**: Workspace instruction mirror ensuring seamless multi-agent operational alignment.
- **[`README.md`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/README.md)**: Repository overview, portfolio connections, and mathematical specifications.
- **[`.gitignore`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/.gitignore)**: Configured to ignore binary caches while preserving the knowledge vault.

---

### B. Raw Sources (Layer 1: Read-Only Truth)

#### 1. `starter_kit/` (Python Bioinformatic Utilities)
- **[`starter_kit/genomic_analyzer.py`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/starter_kit/genomic_analyzer.py)**: CLI utility for FASTA parsing, transcription, translation, and Hamming-distance point mutation detection.
- **[`starter_kit/protein_3d_metrics.py`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/starter_kit/protein_3d_metrics.py)**: PDB coordinate fetcher, `Bio.PDB` hierarchy traverser, and 3D backbone plotter.
- **[`starter_kit/protein_computational_analysis.py`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/starter_kit/protein_computational_analysis.py)**: Physical/thermodynamic evaluator for Kyte-Doolittle hydrophobic cores, Miyazawa-Jernigan contact potentials, and B-factor rigidity correlations.
- **[`starter_kit/README.md`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/starter_kit/README.md)**: CLI execution guides and Rosalind problem benchmark mappings.
- **`starter_kit/sample_data/`**: Reference biological benchmarks (`tnbc_sample.fasta` [TP53 exon 5] and `1coh.pdb` [Insulin]).

#### 2. `courses/` (Curricula & Computational Notebooks)
- **`courses/biopython/` (Modules 1 to 30)**: Complete Jupyter notebook curricula covering sequence manipulation, NCBI Entrez queries, multiple sequence alignments, structural modeling, and phylogenetics.
- **`courses/cambridge_ml_math/R_lectures/`**: Statistical ML scripts:
  - `03_bias_variance_tradeoff_and_CV.R`: SVD Hat matrix ($\mathbf{H} = \mathbf{U}\mathbf{U}^T$) and cross-validation.
  - `12_l1_vs_l2.R`: High-dimensional $p \gg n$ sparsity and Lasso variable selection.
  - `15_Adaboost_demo.R` & `16_Gradient_boosting_linear.R`: Exponential loss boosting.
  - `04_trees.R` & `05_random_forest.R`: Decision tree variance reduction.

#### 3. `journal/` & `career/`
- **[`journal/Bioinformatics_Research_Journal.md`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/journal/Bioinformatics_Research_Journal.md)**: Multi-year academic research log covering DESeq2 negative binomial dispersion, ChIP-seq Poisson peak calling, Phred quality scores, BLAST Karlin-Altschul E-values, and codon usage bias.
- **[`career/Advice_for_Bioinformatics_AZE/Strategic_Career_Roadmap_for_Bioinformatics.txt`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/career/Advice_for_Bioinformatics_AZE/Strategic_Career_Roadmap_for_Bioinformatics.txt)**: End-to-end dry-lab oncogenomics publication blueprint.

#### 4. Reference Literature
- **`Introduction-to-AlphaFold-Database-programmatic-access.pdf`**: REST API and pLDDT/PAE interpretation standards.
- **`The Future of Bioinformatics Workflow Management and Scientific Computing - Solvien Research v0.4.pdf`**: Nextflow DSL2, WDL, and nf-core cloud computing whitepaper.

---

### C. Compiled Knowledge Base (Layer 2: `wiki/`)

#### 1. Navigation & Auditing
- **[`wiki/index.md`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/wiki/index.md)**: Content-oriented catalog indexing all syntheses, entities, concepts, and summaries.
- **[`wiki/log.md`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/wiki/log.md)**: Append-only chronological operation log.

#### 2. Thematic Syntheses (`wiki/syntheses/`)
- **[`End-to-End-Integrated-Oncogenomics-Framework.md`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/wiki/syntheses/End-to-End-Integrated-Oncogenomics-Framework.md)**: Blueprint for public GEO/TCGA mining, DESeq2 modeling, STRING/Cytoscape hub extraction, and Kaplan-Meier prognostic validation.
- **[`High-Dimensional-Machine-Learning-in-Genomics.md`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/wiki/syntheses/High-Dimensional-Machine-Learning-in-Genomics.md)**: Mathematical regularization ($L_1$ Lasso vs $L_2$ Ridge) and ensemble gradient boosting in $p \gg n$ biology.
- **[`Structural-Biophysics-vs-AI-Folding.md`](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/wiki/syntheses/Structural-Biophysics-vs-AI-Folding.md)**: Cross-validation comparing empirical physical potentials (MJ, SASA, B-factors) against AlphaFold confidence metrics (pLDDT, PAE).

#### 3. Core Entities (`wiki/entities/`)
- **Software & Packages**: [[Biopython]], [[Bio-SeqIO]], [[Bio-PDB]], [[Bio-Entrez]], [[Bio-Phylo]], [[Bio-AlignIO]], [[DESeq2]], [[BLAST]], [[Cytoscape]], [[Genomic-Analyzer]], [[Protein-3D-Metrics]], [[Protein-Computational-Analysis]], [[Nextflow-WDL]].
- **Databases & Platforms**: [[AlphaFold-DB]], [[STRING-Database]], [[GEO-TCGA]], [[Rosalind-Platform]], [[Oxford-Nanopore-Sequencing]].
- **Genes, Structures & Curricula**: [[TP53]], [[Insulin-1COH]], [[Cambridge-ML-Math]].

#### 4. Algorithmic Concepts (`wiki/concepts/`)
- **Sequence & Genomics**: [[GC-Skew]], [[Hamming-Distance-Genomics]], [[Multiple-Sequence-Alignment]], [[BLAST-Algorithm-Heuristics]], [[Phred-Quality-Score]], [[Codon-Usage-Bias]], [[Sequence-Motif-Discovery]], [[Phylogenetic-Tree-Reconstruction]].
- **Structural Biophysics**: [[Kyte-Doolittle-Hydropathy]], [[Miyazawa-Jernigan-Potentials]], [[B-Factor-Thermal-Displacement]], [[Solvent-Accessible-Surface-Area]], [[AlphaFold-Programmatic-API]].
- **Machine Learning & Statistics**: [[Bias-Variance-Tradeoff]], [[L1-vs-L2-High-Dimensional-Genomics]], [[Boosting-Theory-AdaBoost]], [[Differential-Gene-Expression-DESeq2]], [[Kaplan-Meier-Survival-Analysis]], [[ChIP-Seq-Peak-Calling]], [[Tumor-Immune-Infiltration]], [[Protein-Protein-Interaction-Networks]], [[Bioinformatics-Workflow-Management]].

#### 5. Source Summaries (`wiki/summaries/`)
- 9 source summaries distilling the exact methodology, formulas, and parameters of each ingested codebase, curriculum, and research paper.

---

## 🖥️ 3. How to Use Obsidian with the LLM Wiki

In this paradigm:
- **Obsidian is your IDE**: You use Obsidian to read, explore, visualize the interactive graph, inspect backlinks, and navigate associative trails.
- **The LLM Agent is the Compiler**: The agent reads raw inputs, updates cross-references, adds YAML metadata, prevents contradictions, and keeps the catalog current.

### Key Obsidian Workflows

#### 1. Visualizing the Knowledge Graph (Graph View)
- Press `Ctrl/Cmd + G` to open the **Global Graph View**.
- Every entity and concept appears as a node. Highly connected nodes (such as `Biopython`, `DESeq2`, `AlphaFold-DB`, `TP53`) act as central knowledge hubs.
- Open **Local Graph** in the sidebar (`More Options -> Open Linked View -> Open Local Graph`) to see immediate 1-hop and 2-hop associations while reading any page.

#### 2. Querying with Dataview
Because all wiki pages include structured YAML frontmatter:
```yaml
---
title: "Page Title"
type: entity | concept | synthesis | summary
tags:
  - bioinformatics
  - transcriptomics
---
```
You can write live Dataview queries in Obsidian notes. For example:

```markdown
\`\`\`dataview
TABLE type, tags, sources
FROM "wiki"
WHERE type = "concept"
SORT file.name ASC
\`\`\`
```

#### 3. Following Associative Trails
- Hover over any `[[wikilink]]` while holding `Ctrl/Cmd` to preview the target page without leaving your current document.
- Use the **Backlinks** pane in the right sidebar to see all other pages that cite the current concept.

#### 4. The Compounding Feedback Loop
```
User drops paper in raw/  ──>  LLM reads & compiles into wiki/  ──>  Obsidian Graph updates live
                                                                         │
User discovers novel connection in Obsidian Graph View <─────────────────┘
         │
User asks LLM to analyze connection  ──>  LLM writes new synthesis in wiki/syntheses/
```

This ensures your knowledge base continuously deepens and never loses valuable discoveries in ephemeral chat logs.
