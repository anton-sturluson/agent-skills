# Ingest — Zettel-Wiki

Process raw sources into wiki knowledge. See SKILL.md for principles and content type definitions.

## What ingest accomplishes

New sources become wiki knowledge: zettels extracted from raw evidence, cross-linked with explicit context, organized into structure notes, with INDEX and LEDGER updated. Every zettel is grounded and connected before ingest is considered complete.

## Sources

Sources are files on disk (filings, transcripts, product docs, case studies), URLs, or conversation content. Never copy source files into the wiki — reference them via paths or URLs.

Adhere to raw evidence. Filings, transcripts, product docs, and case studies are valid zettel sources. Notes, memos, and deep dives are not — they are outputs of prior analysis. If you catch yourself building a zettel from a synthesis document, stop and find the underlying raw source.

## Extraction

Read sources and identify discrete atomic insights. For each candidate, the key decisions:

- **Knowledge or information?** Knowledge is contextualized, connected, and answers "why does this matter?" Information is a dead fact. Only knowledge becomes a zettel.
- **Can it stand alone?** One thought per zettel. Two distinct ideas = two zettels.
- **Already captured?** Check `zettels/INDEX.md`. Same claim with new evidence → enrich the existing zettel. Same topic, different angle → new zettel linked to the existing one. True duplicate → skip.

For batch extraction at scale, spawn subagents with non-overlapping timestamp namespaces. Each worker gets a batch of source files and the zettel template. After all workers complete, the main agent reviews output and wires cross-batch connections — workers can only link within their own batch. If a worker batch fails, retry immediately with smaller batches.

### Namespace collision guard

Before assigning a namespace, run `ls zettels/YYYYMMDDHH*.md` to check for existing files in the range. If any exist, shift forward until clear. Two ingests writing to the same IDs silently overwrite each other.

## Cross-linking

Every new zettel gets at least one connection with explicit context explaining why the link exists. Connections are bidirectional — when linking A → B, update B → A too.

Cross-linking is not optional. Zettels without connections are orphans and represent incomplete work. All zettels must be linked before ingest is considered complete.

## Structure notes

After extraction, review what emerged:

- **Existing structure notes:** Read them. Understand the current landscape. Update their narratives to incorporate new zettels. Bump the `updated` field.
- **New clusters:** When 3+ new zettels cluster around a topic that has no structure note, create one. Let the topic emerge from the zettels — don't pre-define it.
- **Growth:** When a structure note now covers distinct sub-topics, consider evolving it into a wiki folder with sub-pages.

Structure notes are fluid. Reorganize them as needed — the current structure is not sacred.

## Completing ingest

Update all affected INDEX.md files. Append a LEDGER entry with source, files created, and files updated.

Then flow into audit. Ingest is not done until audit passes.

## Pitfalls

- Pre-planning structure note topics before extraction. Let structure emerge.
- Using notes or deep dives as zettel sources instead of raw evidence.
- Accepting batch failures as "known gaps" instead of retrying.
- Cross-linking only a few zettels and deferring the rest.
- Copying source text verbatim instead of processing it into knowledge.
- Delegating structure notes to extraction-tier models. Structure notes are synthesis; use the main agent or a synthesis-grade model such as Opus-tier or GPT-tier.
