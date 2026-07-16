# Structure Note Template

Use this format for structure notes (wiki pages) in `pages/`.

```markdown
---
title: "Topic Title"
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# [Title]

[Coherent narrative that reads like a Wikipedia article. Inline links to zettels that back each claim: "Apple's services revenue [exceeded hardware](../../zettels/202604160930.md) in Q2 2025, marking a structural shift."

The page organizes and narrates — zettels are the evidence underneath. Every factual claim links to the supporting zettel or raw source.]

## Related

- [Related Structure Note](path/to/page.md) — [Why this note is related — not just "see also" but the specific connection.]
```

## Rules

- **Semantic filename:** lowercase kebab-case.
- **Reads like a Wikipedia article.** Coherent narrative, not bullet lists. Organize by logical sections, not by source.
- **Inline zettel links.** Every factual claim links to the zettel that backs it.
- **Related section.** Links to other structure notes with context explaining the relationship.
- **Updated field.** Bump `updated` when content changes.
- **Fluidity.** Structure notes are living documents — reorganized, split, merged as the wiki evolves.
- **Multi-level growth.** When a page covers distinct sub-topics, evolve it into a wiki folder. The original file becomes the hub page inside the folder. Sub-pages and nested folders are allowed. Every folder gets an INDEX.md.
- **Depth varies naturally.** No word count constraints.
