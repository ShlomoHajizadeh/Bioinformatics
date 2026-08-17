---
title: "Source Summary: Introduction to AlphaFold Database Programmatic Access"
type: summary
created: 2026-08-17
updated: 2026-08-17
tags:
  - structural-biology
  - alphafold
  - api
  - deep-learning
sources:
  - "[[Introduction-to-AlphaFold-Database-programmatic-access.pdf]]"
---

# Source Summary: Introduction to AlphaFold Database Programmatic Access

- **Source File**: `Introduction-to-AlphaFold-Database-programmatic-access.pdf` (EMBL-EBI / DeepMind Technical Protocol)
- **Scope**: Systematic guide to querying, retrieving, and batch-processing predicted 3D protein structures via the AlphaFold Database (AFDB) REST API and 3D-Beacons network.

## Key Protocols & Technical Specifications

1. **REST API Endpoints**:
   - `GET https://alphafold.ebi.ac.uk/api/prediction/{uniprot_accession}`: Returns full metadata, confidence summaries, and download URLs for `.pdb`, `.cif`, and PAE JSON matrices.
   - 3D-Beacons standard API compatibility for federated structural queries across experimental (PDB) and predicted (AFDB) structural data.
2. **Confidence Metrics Interpretation**:
   - **pLDDT (0–100)**:
     - $>90$: Very high confidence (reliable side-chain rotamers).
     - $70\text{--}90$: High confidence (well-modeled backbone).
     - $50\text{--}70$: Low confidence (potential secondary structure elements).
     - $<50$: Very low confidence (strongly indicative of Intrinsically Disordered Regions [IDRs]).
   - **PAE Matrix ($N \times N$)**: Quantitative inter-residue alignment error matrix in Ångströms, resolving whether domains have fixed relative 3D orientations.
3. **Automated Python Integration**:
   - Programmatic workflows downloading structures in bulk via `requests` and parsing coordinates into `Bio.PDB` or analyzing PAE matrices with `numpy` and `matplotlib`.

## Cross-Linked Entities & Concepts
- **Entities**: [[AlphaFold-DB]], [[Biopython]], [[Bio-PDB]]
- **Concepts**: [[AlphaFold-Programmatic-API]], [[B-Factor-Thermal-Displacement]], [[Solvent-Accessible-Surface-Area]]
- **Syntheses**: [[Structural-Biophysics-vs-AI-Folding]]
