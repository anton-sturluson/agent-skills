---
name: brainstorm
description: Triangulate a question through four specialist agents. Use to surface angles, disagreements, and blind spots.
---

# Brainstorm

Spawn all four specialists in parallel on the same question. The value is in the disagreements, not the consensus.

## Agents

| Agent | agentId | Model |
|---|---|---|
| Charlie | `think-like-charlie-buffet` | `anthropic/claude-opus-4-6` |
| Mauboussin | `think-like-mauboussin` | `openai/gpt-5.5` |
| Taleb | `think-like-taleb` | `openai/gpt-5.5` |
| Christensen | `think-like-christensen` | `google/gemini-3.1-pro-preview` |

## Spawning

Use `sessions_spawn` for each agent with `agentId` from the table, `mode="run"`, `cleanup="delete"`, `thinking="high"`, and the per-agent model.

Give every agent the same core task:
- The question or thesis
- Relevant context (company, industry, situation)
- Where to write output (file path), when applicable

Do not prime agents with their own framework concepts (e.g. telling Taleb to look for fragility, or Mauboussin to think about base rates). Each agent's AGENTS.md is auto-injected — trust it to supply the lens. Priming produces echoes of your own framing instead of independent perspectives.

Don't paste wiki content into the task — the agents read wiki files themselves.

Spawn all four, then `sessions_yield` and wait for all completions. If a subagent fails, retry it once before moving on.

## After completions

Synthesize: where do they agree, where do they disagree, what questions surfaced that weren't in the original framing?

## Output

For company deep dives, write to the company's `analysis/brainstorm-{TOPIC}/` folder — one file per agent, one synthesis file. Chat reply: short synthesis, bottom line, next step. The written files are the primary artifact.
