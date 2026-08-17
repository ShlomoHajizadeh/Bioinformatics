# LLM Wiki Schema & Operational Guidelines

This document specifies the architecture, conventions, and operational workflows for maintaining the persistent Bioinformatics & Computational Biology LLM Wiki.

---

## 1. Architecture Overview

- **`raw/` (Immutable Sources)**: Original, unmodified source materials (PDFs, clipped markdown, protocol sheets, data tables, lecture transcripts). The agent reads from this layer but **never edits** raw sources.
- **`wiki/` (Compiled Knowledge Layer)**: Persistent, cross-linked, structured markdown files created and maintained exclusively by the LLM agent.
  - `wiki/index.md`: Content-oriented catalog of all entries with categorization and one-line summaries.
  - `wiki/log.md`: Chronological, append-only operational history (`[YYYY-MM-DD] <operation> | <summary>`).
  - `wiki/entities/`: Concrete entities (proteins, genes, software tools, databases, biological pathways, hardware).
  - `wiki/concepts/`: Theoretical concepts, mathematical algorithms, statistical models, biochemical mechanisms.
  - `wiki/syntheses/`: Evolving thematic syntheses, cross-document analyses, research hypotheses, and meta-reviews.
  - `wiki/summaries/`: Source-level distillations and key takeaways linking directly to entities and concepts.

---

## 2. Page Conventions & Metadata

All wiki pages (except `index.md` and `log.md`) must begin with YAML frontmatter compatible with Obsidian Dataview:

```yaml
---
title: "Page Title"
type: entity | concept | synthesis | summary
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - bioinformatics
  - topic-tag
aliases:
  - Alternative Name
sources:
  - "[[source_summary_or_raw_path]]"
---
```

### Linking Style
- Use standard Obsidian wikilinks: `[[Target Page]]` or `[[Target Page|Display Text]]`.
- Keep link targets matching file basenames without `.md`.
- Every page must contain outbound links to parent concepts and related entities.

---

## 3. Core Operations

### 3.1 Ingest (`Ingest <source_file>`)
1. **Read & Extract**: Thoroughly read the raw file from `raw/` (or repository literature/protocols).
2. **Create Source Summary**: Write `wiki/summaries/<source-basename>.md` capturing key claims, methodology, results, and citations.
3. **Compound Entity & Concept Pages**:
   - Create or update relevant pages in `wiki/entities/` and `wiki/concepts/`.
   - Add new evidence, update descriptions, and record any conflicting viewpoints or superseded paradigms.
4. **Update Syntheses**: If the source impacts an existing topic thesis, update the relevant page in `wiki/syntheses/`.
5. **Update Index**: Add new or updated entries to `wiki/index.md`.
6. **Append Log**: Add a log entry in `wiki/log.md` in the format:
   `## [YYYY-MM-DD] ingest | <Source Title> (touches N pages)`

### 3.2 Query (`Query <question>`)
1. Consult `wiki/index.md` and search relevant `wiki/` pages.
2. Formulate a comprehensive synthesis citing wiki pages and original raw sources.
3. **Filing Back**: If the query produces a substantial comparison, new taxonomy, or analytical framework, save it into `wiki/syntheses/<topic>.md`, link it in `wiki/index.md`, and log it.

### 3.3 Lint (`Lint`)
Perform periodic integrity audits:
- **Orphan Check**: Identify pages with zero inbound links.
- **Dangling Link Check**: Fix broken wikilinks.
- **Contradiction / Stale Claim Audit**: Flag conflicting findings between older and newer ingested literature.
- **Knowledge Gaps**: Highlight referenced concepts or entities that do not yet have their own dedicated page.

---

## 4. Obsidian Optimization
- Vault root is set to the repository root.
- Images and figures extracted or downloaded are saved under `raw/assets/` and linked as `![[asset-name.png]]`.
