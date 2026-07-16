# Audit — Zettel-Wiki

Verify wiki quality and evolve wiki structure. See SKILL.md for principles and content type definitions.

Audit runs after every ingest (mandatory) and periodically or on request for wiki-wide health.

## What audit accomplishes

Recent ingest verified for quality. Issues found and fixed. Wiki structure evolved — orphans linked, pages split when unwieldy, new structure notes created from zettel clusters, redundant zettels merged. INDEX files consistent. LEDGER updated.

## Quality verification

### Coverage

Were the right sources processed? Compare the source corpus against what was actually ingested. High-value files (filings, transcripts, product docs) should not be skipped without reason. Metadata files, manifests, and download logs are fine to skip.

### Evidence grounding

Does every zettel trace back to a raw source? Flag zettels citing synthesis documents instead of raw evidence. Spot-check claims against cited sources when something feels uncertain.

### Content-match verification

For every zettel created in this ingest, confirm the `source` frontmatter references this ingest's source — not just that the file exists. This catches namespace collisions where the file on disk belongs to a different ingest entirely.

### Link soundness

Are connections bidirectional? Does every connection include context explaining why? Are there obvious missing connections between related zettels?

## Structural evolution

### Orphan zettels

Zettels with no inbound links — nothing points to them. Read the orphan, understand its content, and add connections from the most relevant structure notes and related zettels. Add the link with explicit context.

### Context-free links

Links that say "see [ID]" or "related to" without explaining why. Read both sides, understand the relationship, add a one-sentence explanation.

### Contradictions

Contradictions are expected — the world has genuine disagreements. Don't resolve unless one claim is clearly wrong (superseded by a newer source).

For legitimate contradictions: link the conflicting zettels to each other, explain what contradicts and how the tension reads, update any structure notes that reference both.

For clear errors: mark the incorrect zettel as superseded, link to the correction, update structure notes that relied on the wrong claim.

### Page splits and folder promotion

When a structure note covers clearly distinct sub-topics, propose evolving it into a wiki folder with sub-pages. The original file becomes the hub page. Multi-level nesting is expected.

Flag significant restructuring to the user. Fix routine issues autonomously.

### Zettel clusters without a structure note

Groups of 3+ related zettels that share connections but have no structure note organizing them. Create a structure note — write coherent narrative linking to the zettels.

### Redundant zettels

Near-duplicates covering the same ground. Merge into the richer version. Add any unique evidence from the weaker one. Update all inbound links to point to the survivor.

### Stale content

Zettels whose claims have been superseded by newer information. Use judgment — time-bound claims need freshness checks more than evergreen definitions. Add a staleness note and link to the newer zettel if one exists.

## Batch operations

For large-scale cross-linking or orphan resolution, spawn subagents. Give each worker a batch of zettels plus the full zettel catalog for reference. Workers add connections; the main agent verifies quality after completion.

## Autonomy vs. flagging

Fix autonomously: orphan links, broken links, missing INDEX entries, context-free connections, INDEX regeneration, small structure note updates.

Flag to user: significant page splits, major folder reorganization, contradictions that require domain judgment, suggestions for sources to seek out.

## Completing audit

Update all affected INDEX.md files. Append a LEDGER entry summarizing what was verified, what was fixed, and what was flagged.

## Pitfalls

- Checking without fixing. Audit both verifies and remediates.
- Silently resolving contradictions instead of linking both sides.
- Skipping audit after ingest because "it looked fine."
- Flagging everything to the user instead of fixing routine issues autonomously.
