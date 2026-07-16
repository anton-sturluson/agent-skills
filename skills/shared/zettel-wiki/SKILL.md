---
name: zettel-wiki
description: >
  Build and maintain an agent-driven knowledge base using the Zettel-Wiki pattern — a fusion of Karpathy's LLM Wiki and the Zettelkasten method. The wiki is a persistent, compounding hypertext of interlinked markdown files: structure notes (wiki pages) for navigable topic articles, and Zettels (atomic notes) for individual thoughts and claims.
---

# Zettel-Wiki

Agent-maintained knowledge base. Two content types, seven principles.

Wiki root: `/Users/charlie-buffet/Documents/project-minerva/hard-disk/wiki/`

## Principles

### Zettels first, structure emerges

Zettels are extracted from raw evidence without reference to a pre-defined topic list. Structure notes are written after extraction, organizing the natural clusters that emerged. If the evidence warrants a structure that surprises you, that's the method working.

### Zettels are fixed, structure is fluid

A zettel, once written, is a durable record — one thought grounded in one source. Structure notes are living documents that reorganize as new zettels arrive. During ingest, existing structure notes are reviewed to understand the current landscape and identify what new structures should emerge. Structure notes can be split, merged, reorganized, promoted into folders, or retired.

### Raw evidence is primary

Build zettels from raw evidence. The test for whether something is a valid zettel source: does it contain knowledge that cannot be found in any single existing source? Raw filings, transcripts, and third-party data pass trivially. Original analytical work that produces new facts from raw inputs (calculations, models, structured datasets) also passes. Summaries and memos that restate what is already in the evidence base do not.

### Every connection explains why

Links without context are noise. Every connection between zettels, or between a zettel and a structure note, includes inline prose explaining the relationship. "See also" is never sufficient. Connections are bidirectional — update both sides.

### Audit is a gate, not a suggestion

After every ingest, verify coverage, evidence grounding, and link soundness. Fix issues found. Ingest is not complete until audit passes. This includes structural evolution: fixing orphans, proposing page splits, creating new structure notes from emergent zettel clusters.

### Failed work is retried, not deferred

When a batch fails, retry immediately — smaller batches, different chunking, adjusted approach. Known gaps are not acceptable in a completion report.

### Depth varies naturally

Zettels and structure notes have no word count constraints. A zettel can be three sentences or a full page. A structure note can link to 3 zettels or 30. Split when unwieldy.

## Content types

### Zettel (atomic note)

One thought per file. The smallest unit of knowledge.

| Property | Detail |
|---|---|
| Location | `zettels/` (flat) |
| ID | Timestamp: `YYYYMMDDHHmm` |
| Grounding | Every zettel traces back to a raw source |
| Connections | Bidirectional links to related zettels with explicit context |
| Tags | 2–5 `#kebab-case` tags; entry points, not taxonomy |
| Durability | Fixed once written; may be marked stale, not rewritten |

A zettel is not an excerpt. It is processed knowledge — what the source says and why it matters.

Template: `references/zettel-template.md`

### Structure note (wiki page)

A navigable topic article that organizes a cluster of zettels. Coherent prose with inline zettel links, not bullet lists.

| Property | Detail |
|---|---|
| Location | `pages/` (nested folders) |
| ID | Semantic filename: `apple.md`, `gpu-supply-chain.md` |
| Emergence | Created when 3+ zettels cluster around a topic |
| Fluidity | Living document — reorganized as knowledge shifts |
| Cross-references | Structure notes can link to each other with context |

Template: `references/page-template.md`

#### Multi-level growth

When a structure note covers distinct sub-topics, it evolves into a wiki folder. The hub page keeps the original filename inside the folder. Sub-pages and nested folders are allowed. Every folder gets an `INDEX.md`.

## How the wiki grows

### Ingest — `references/ingest.md`

Process new sources into wiki knowledge. Creates zettels from raw evidence, cross-links them, reviews and updates structure notes.

### Audit — `references/audit.md`

Verify quality and evolve structure. Runs after every ingest (mandatory) and periodically for wiki-wide health.

### Query — `references/query.md`

Answer questions from wiki knowledge. Synthesizes answers with citations, files new zettels when the answer produces insight.

## Infrastructure

- `INDEX.md` — master catalog in every folder. Auto-maintained.
- `LEDGER.md` — append-only activity log.

Formats: `references/schema.md`
