# Workspace markdown files

Use this reference when updating workspace markdown files.

## Full-agent workspaces vs prompt-pack subagents

There are two different patterns in this environment:

1. **Full-agent workspaces**
   - Example: `workspace` (Charlie), `workspace-steve` (Steve)
   - These are real workspaces with bootstrap files loaded by OpenClaw.
   - Shared bootstrap markdown files should be sourced from `workspace/shared/` and copied into separate full-agent workspaces.

2. **Prompt-pack subagents**
   - Example: `workspace/subagents/think-like-*`
   - These folders are reusable prompt packs.
   - Their local markdown files are part of the prompt bundle and should not be overwritten by the shared sync step unless Anton explicitly asks.

## Important OpenClaw behavior

OpenClaw can ignore bootstrap-file symlinks that resolve outside the source workspace.

Practical implication:
- a cross-workspace symlink such as `workspace-steve/AGENTS.md -> ../workspace/shared/AGENTS.md` may exist on disk but still be treated as missing by bootstrap loading
- for separate workspaces, shared markdown files must be copied as regular files

## Shared skills vs shared markdown

These are different patterns:
- shared bootstrap markdown files live under `workspace/shared/` and should be copied into separate full-agent workspaces as regular files
- reusable shared skills should live under `~/.openclaw/skills/` so every full agent can load them natively
- do not rely on `workspace/shared/skills/` or cross-workspace skill symlinks as the runtime loading mechanism
- keep agent-specific skills local to the workspace unless Anton explicitly wants them centralized
- prompt-pack subagents should keep their own local files unless Anton explicitly asks for a shared setup

## File roles

### AGENTS.md
Use for shared operational rules:
- approvals
- deletion rules
- storage conventions
- when to use Notion vs hard-disk
- workflow conventions

Do not put personality or worldview here.

### SOUL.md
Use for:
- personality
- worldview
- writing style
- specialist reasoning stance

### IDENTITY.md
Use for:
- name
- role
- vibe

### USER.md
Use for:
- Anton-specific preferences
- stable user context shared across full agents if appropriate

### TOOLS.md
Use for:
- environment-specific notes
- local tool quirks
- path conventions that are operationally useful

Do not use it for identity or worldview.

### HEARTBEAT.md
Use only for explicit heartbeat tasks. If empty, heartbeat should be skipped.

### BOOTSTRAP.md
Optional bootstrap helper file when the environment expects it.

### memory/YYYY-MM-DD.md
Use for short dated operational memory notes.
- append to the canonical day file
- do not create ad hoc timestamped variants

## Updating guidance

When editing workspace markdown files:
- keep rules in the right file
- avoid duplicating the same instruction across multiple files unless the duplication is intentional
- prefer concise wording and examples over repeated prose
- after editing shared markdown files, mirror the same change manually into the corresponding shared copies for the other full-agent workspaces

## Shared markdown sync

Source of truth:
- `workspace/shared/*.md`

Current sync target pattern:
- copy the changed shared markdown files manually into the corresponding shared copies for separate full-agent workspaces such as `workspace-steve/shared/`
- do not sync them into prompt-pack subagents
- do not rely on an external helper script; verify the destination path explicitly each time
