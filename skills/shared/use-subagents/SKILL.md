---
name: use-subagents
description: Coordinate parallel subagent work for extraction, research, or batch tasks. Use when spawning multiple subagents or planning parallel work.
---

# use-subagents

## Model selection

- Default: Sonnet for extraction, triage, and evidence capture
- Opus for tasks requiring complex judgment, synthesis, or nuanced reasoning

## Platform constraints

| Setting | Value | What it controls |
|---|---|---|
| `maxConcurrent` | 20 | Global concurrency cap |
| `maxChildrenPerAgent` | 10 | Max children per agent session |
| `maxSpawnDepth` | 1 | Nesting depth (2 for orchestrator pattern) |

- Batch subagent waves at 8 to keep headroom for Charlie and Steve
- For orchestrator patterns (main → orchestrator → workers), set `maxSpawnDepth: 2`

## Workflow

- Split work into discrete batches with minimal overlap — usually one subagent per document, filing, transcript, or tightly scoped topic
- Each subagent writes to the appropriate local folder; after completion, verify output files exist before reporting success (subagents may silently write to wrong paths)
- Re-run any failed, errored, timed-out, or empty-output subagent once before consolidating; if it fails again, report which failed and why rather than silently dropping it
- After the parallel pass, consolidate and synthesize in the main session
