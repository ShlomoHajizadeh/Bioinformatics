---
title: "AlphaFold Database Programmatic Access & REST Architecture"
type: concept
created: 2026-08-17
updated: 2026-08-17
tags:
  - structural-biology
  - alphafold
  - api
  - rest
aliases:
  - AlphaFold API
  - AFDB API
sources:
  - "[[wiki/summaries/alphafold-db-programmatic-access]]"
---

# AlphaFold Database Programmatic Access & REST Architecture

The **AlphaFold Database (AFDB) REST API** enables automated, programmatic extraction of atomic coordinates, confidence metrics, and domain-alignment uncertainty matrices for over 200+ million proteins.

## Endpoint Architecture

| Resource | HTTP Method | URL Template | Response Format |
|---|---|---|---|
| **Prediction Summary** | `GET` | `/api/prediction/{uniprot_accession}` | JSON (Metadata, pLDDT ranges, file URLs) |
| **PDB Coordinates** | `GET` | Direct URL from summary (`.pdb`) | Crystallographic PDB (pLDDT in B-factor col) |
| **mmCIF Coordinates** | `GET` | Direct URL from summary (`.cif`) | Standard mmCIF format |
| **PAE Matrix** | `GET` | Direct URL from summary (`.json`) | $N \times N$ matrix of expected aligned error in Å |

## Python Automation Pattern

```python
import requests
import json

def fetch_alphafold_metadata(uniprot_id):
    url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[0] # Returns prediction entry dict
    return None
```

## Related Entities & Concepts
- [[AlphaFold-DB]] — database entity.
- [[Bio-PDB]] — downstream coordinate parsing.
- [[B-Factor-Thermal-Displacement]] — storage mechanism for pLDDT.
- [[Structural-Biophysics-vs-AI-Folding]] — structural comparison.
