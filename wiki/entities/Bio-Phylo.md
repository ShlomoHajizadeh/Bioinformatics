---
title: "Bio.Phylo (Biopython Phylogenetics Module)"
type: entity
created: 2026-08-17
updated: 2026-08-17
tags:
  - biopython
  - phylogenetics
  - evolution
aliases:
  - Bio.Phylo
  - Phylo
sources:
  - "[[wiki/summaries/biopython-curriculum-30-modules]]"
---

# Bio.Phylo

**`Bio.Phylo`** provides computational phylogenetic analysis, tree construction, tree traversal, format conversion, and visualization within Biopython.

## Supported Formats
Newick, Nexus, phyloXML, NeXML, CDAO.

## Tree Construction Algorithms
- **Neighbor-Joining (NJ)**: Distance-based bottom-up clustering algorithm (`TreeConstruction.DistanceTreeConstructor`).
- **UPGMA (Unweighted Pair Group Method with Arithmetic Mean)**: Assumes a constant molecular clock rate.
- **Parsimony**: `TreeConstruction.ParsimonyTreeConstructor` with tree searching heuristics.

## Tree Manipulation & Traversal
- `tree.get_terminals()`: Access all leaf taxa.
- `tree.get_nonterminals()`: Access all internal ancestral nodes.
- `tree.root_with_outgroup(outgroup_node)`: Re-roots phylogenetic topology.
- `Phylo.draw(tree)` / `Phylo.draw_ascii(tree)`: Visualizes trees graphically via Matplotlib or in the terminal as text.

## Related Concepts
- [[Phylogenetic-Tree-Reconstruction]] — mathematical foundations.
- [[Multiple-Sequence-Alignment]] — input for distance matrix calculation.
