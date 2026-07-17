# Agent Skills

Source repository for Charlie Buffet's custom agent skills.

## Layout

- `skills/workspace/` — investment and research skills from `~/.openclaw/workspace/skills/`
- `skills/shared/` — shared operational skills from `~/.openclaw/skills/`

System and plugin skills installed under `/opt/homebrew/` or managed by Codex are intentionally excluded.

## Install

Install or update all repository-managed skills:

```bash
curl -fsSL https://raw.githubusercontent.com/anton-sturluson/agent-skills/main/install.sh | bash
```

The installer maps `skills/workspace/` to `~/.openclaw/workspace/skills/` and
`skills/shared/` to `~/.openclaw/skills/`. It updates only skills present in
this repository and does not delete unrelated skills.

Set `OPENCLAW_HOME`, `OPENCLAW_WORKSPACE`, or `AGENT_SKILLS_REF` to override
the default locations or install a pinned branch, tag, or commit. Contributors
can set `AGENT_SKILLS_SOURCE` to test a local checkout without downloading it.

## Current workflow

This initial commit is a baseline snapshot of the live skill directories. Changes should be developed and reviewed in this repository before being synchronized to the live locations.

The repository does not change OpenClaw configuration.
