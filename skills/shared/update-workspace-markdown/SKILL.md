---
name: update-workspace-markdown
description: Maintain OpenClaw workspace markdown files and shared bootstrap docs. Use when creating, editing, restructuring, syncing, or deleting workspace markdown or bootstrap files, or when workspace conventions need updating.
---

# update-workspace-markdown

## Workspace hygiene

- Agent workspaces hold only operational files (markdown, memory, skills, subagents, shared copies, runtime state) — no working files, no backup/garbage files, no `INDEX.md` unless explicitly asked
- When archiving in a workspace, use one `archive/` folder with dated subfolders

## Workflow

1. Read `references/markdown-files.md` for file roles, conventions, and sync rules.
2. Make the requested changes.
3. If shared files changed (`workspace/shared/`), mirror as regular file copies to all full-agent workspaces (not symlinks).
4. Summarize what changed and what was mirrored.

## Resources

- `references/markdown-files.md` — file roles, sync rules, edge cases
