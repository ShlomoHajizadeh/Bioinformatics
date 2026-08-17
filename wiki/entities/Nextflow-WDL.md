---
title: "Nextflow & Scientific Workflow Engines (WDL / Snakemake)"
type: entity
created: 2026-08-17
updated: 2026-08-17
tags:
  - software-tools
  - bioinformatics
  - workflows
aliases:
  - Nextflow
  - nf-core
  - WDL
sources:
  - "[[wiki/summaries/solvien-bioinformatics-workflow-management]]"
---

# Nextflow & Scientific Workflow Engines

**Nextflow** and declarative workflow engines (WDL, Snakemake) provide the standard execution infrastructure for modern computational biology, enabling parallel, reproducible, and portable pipeline execution.

## Architectural Highlights
- **Nextflow DSL2**: Functional reactive syntax connecting computational `processes` via asynchronous `channels`.
- **nf-core**: A community effort to build peer-reviewed, high-quality analysis pipelines using Nextflow.
- **WDL (Workflow Description Language)**: Human-readable task/workflow language maintained by the OpenWDL community and GA4GH.

## Related Concepts
- [[Bioinformatics-Workflow-Management]] — theoretical principles.
- [[Oxford-Nanopore-Sequencing]] — downstream streaming pipelines (`nf-core/nanoseq`).
