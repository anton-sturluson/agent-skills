# Agent Skills

Private source repository for Charlie Buffet's custom agent skills.

## Layout

- `skills/workspace/` — investment and research skills from `~/.openclaw/workspace/skills/`
- `skills/shared/` — shared operational skills from `~/.openclaw/skills/`
- `skills/agents/` — agent-specific skills from `~/.agents/skills/`

Shared aliases for `grill-me` and `write-a-skill` point to their canonical copies in `skills/agents/`.

System and plugin skills installed under `/opt/homebrew/` or managed by Codex are intentionally excluded.

## Current workflow

This initial commit is a baseline snapshot of the live skill directories. Changes should be developed and reviewed in this repository before being synchronized to the live locations.

The repository does not yet replace the live directories or change OpenClaw configuration.
