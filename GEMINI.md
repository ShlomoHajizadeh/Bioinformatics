# LLM Wiki Schema & Operational Guidelines

See [AGENTS.md](file:///Users/macbookairm2/Documents/GitHub/Bioinformatics/AGENTS.md) for full architecture specifications.

## Operating Principles
- **Read-Only Raw Sources**: Never alter files in `raw/` or incoming reference papers.
- **Persistent Compounding**: When processing inquiries or ingesting materials, always build and maintain the `wiki/` directory.
- **Always Keep Index & Log Updated**: Every ingest, synthesis, or lint pass updates `wiki/index.md` and appends to `wiki/log.md`.
- **Obsidian Compatibility**: Use YAML frontmatter and `[[wikilinks]]`.
