---
name: manage-agents-and-skills
description: Create, delete, or reconfigure agents and skills. Use when adding/removing full agents, specialist agents, or shared/agent-specific skills.
---

# manage-agents-and-skills

## Agent types

- Full agents — own workspace, channel bindings, heartbeat (Charlie, Steve)
- Specialist agents — registered in `agents.list`, own workspace with custom persona, spawned via `agentId` (think-like-*)
- Subagents — ephemeral workers spawned during sessions, inherit parent's workspace

## Creating agents

- New full agents: copy shared bootstrap from `shared/`, create fresh `SOUL.md` and `IDENTITY.md`
- Specialist agents only need `AGENTS.md` and `TOOLS.md` in their workspace — those are the only files OpenClaw injects for subagent sessions

## Deleting agents

- Requires Anton's approval
- Clean up references, symlinks, registry entries, and `agents.list` config
- Archive specialist agent workspace files unless told to permanently remove

## Skills

- Shared skills live in `~/.openclaw/skills/` (loaded for all agents)
- Workspace `skills/` folders are agent-specific overrides
- When updating a shared skill, update `~/.openclaw/skills/` and clean up stale per-workspace duplicates
- Do not maintain a skill catalog in bootstrap markdown — OpenClaw injects skill names/descriptions automatically
