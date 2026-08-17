---
title: "STRING Database (Search Tool for the Retrieval of Interacting Genes/Proteins)"
type: entity
created: 2026-08-17
updated: 2026-08-17
tags:
  - databases
  - ppi-networks
  - systems-biology
aliases:
  - STRING
  - string-db.org
sources:
  - "[[wiki/summaries/integrated-bioinformatics-analysis-roadmap]]"
---

# STRING Database

**STRING** ([string-db.org](https://string-db.org)) is an open database of known and predicted protein-protein interactions covering physical bindings and functional associations.

## Evidence Channels & Scoring
- **Automated Textmining**: Natural language processing across PubMed abstracts.
- **Experimental Data**: Co-immunoprecipitation, yeast two-hybrid, and crystallographic complexes from BioGRID/IntAct.
- **Computational Predictions**: Genomic context methods (neighborhood, gene fusion, phylogenetic co-occurrence).
- **Curated Databases**: KEGG, Reactome, BioCyc.
- **Combined Confidence Score ($0\text{--}1000$)**:
  - High confidence: Score $\ge 0.700$.
  - Highest confidence: Score $\ge 0.900$.

## Related Concepts & Tools
- [[Protein-Protein-Interaction-Networks]] — underlying topological graph.
- [[Cytoscape]] — downstream network visualization.
- [[End-to-End-Integrated-Oncogenomics-Framework]]
