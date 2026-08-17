---
title: "Protein-Protein Interaction (PPI) Networks & Hub Gene Centrality"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - systems-biology
  - networks
  - ppi
  - graph-theory
aliases:
  - PPI Networks
  - Hub Genes
  - Network Centrality
sources:
  - "[[wiki/summaries/integrated-bioinformatics-analysis-roadmap]]"
---

# Protein-Protein Interaction (PPI) Networks & Hub Gene Centrality

**Protein-Protein Interaction (PPI) Networks** model cellular interactomes as mathematical graphs $G = (V, E)$, where vertices $V$ represent proteins and edges $E$ denote physical binding, functional associations, or co-expression evidence.

## Topological Metrics for Hub Gene Discovery

1. **Degree Centrality ($k_i$)**: Total number of direct interaction partners:
   $$k_i = \sum_{j \in V} A_{ij}$$
2. **Betweenness Centrality ($C_B(v)$)**: Frequency with which node $v$ lies on the shortest path between all pairs of nodes:
   $$C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$
3. **Closeness Centrality ($C_C(v)$)**: Reciprocal of the sum of shortest path distances to all other reachable nodes.
4. **MCODE (Molecular Complex Detection)**: Graph-theoretic clustering algorithm identifying dense interconnected functional sub-networks/protein complexes.

## Downstream Validation
- Identified top hub proteins (e.g. `CDC20`, `AKT1`, `TP53`) represent core regulatory bottlenecks and prime therapeutic drug targets.

## Related Entities & Concepts
- [[STRING-Database]] — PPI evidence repository.
- [[Cytoscape]] — network visualization engine.
- [[Kaplan-Meier-Survival-Analysis]] — prognostic testing of hub genes.
