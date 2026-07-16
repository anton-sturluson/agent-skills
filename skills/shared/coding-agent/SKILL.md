---
name: coding-agent
description: 'Delegate complex coding tasks to a coding agent via background
process. Use for: multi-file implementation, refactoring, feature builds, PR
reviews, or any iterative coding that benefits from autonomous file
exploration.
metadata:
  { "openclaw": { "emoji": "🧩", "requires": { "anyBins": ["pi", "claude", "codex", "gemini"] } } }
---

# Coding Agent

## Priority Order

1. **Pi** (default) — `pi`
2. **Claude Code** — `claude`
3. **Codex** — `codex`
4. **Gemini CLI** — `gemini` (last resort)

Use the highest-priority agent available. Fall back only if the chosen agent fails or is explicitly overridden by Anton.

## PTY Required

All agents are interactive terminal apps. Always use `pty:true`.

## Invocation

### Pi (default)

Pi uses `~/.pi/agent/settings.json` for model/thinking defaults — no extra flags needed.

```bash
# One-shot
exec pty:true workdir:~/project command:"pi -p 'Your task'"

# Background
exec pty:true workdir:~/project background:true command:"pi -p 'Your task'"

# Read-only review
exec pty:true workdir:~/project command:"pi --tools read,grep,find,ls -p 'Review the code'"
```

### Claude Code (fallback)

```bash
exec pty:true workdir:~/project command:"claude --model opus --effort high --dangerously-skip-permissions -p 'Your task'"
```

### Codex (fallback)

Requires a git repo.

```bash
exec pty:true workdir:~/project command:"codex -c model_reasoning_effort=\"high\" exec --full-auto 'Your task'"
```

For no-sandbox mode: replace `--full-auto` with `--yolo`.

### Gemini CLI (last resort)

```bash
exec pty:true workdir:~/project command:"gemini -m gemini-3.1-pro-preview --approval-mode=yolo -p 'Your task'"
```

## Parallel Work with Worktrees

```bash
git worktree add -b fix/issue-78 /tmp/issue-78 main
exec pty:true workdir:/tmp/issue-78 background:true command:"pi -p 'Fix issue #78. Commit when done.'"
```

## Rules

1. **PTY required** — always `pty:true`.
2. **Respect tool choice** — use what Anton asked for. Don't silently switch agents.
3. **Be patient** — don't kill sessions for being slow.
4. **Auto-approve for building** — Pi has no permission system. Claude Code: `--dangerously-skip-permissions`. Codex: `--full-auto` or `--yolo`. Gemini: `--approval-mode=yolo`. Use vanilla mode for reviewing.
5. **Minimum timeout** — never set `timeout` below 1200 (20 min). For complex work, omit timeout entirely.
6. **NEVER start agents in `~/.openclaw/`** or checkout branches in `~/Projects/openclaw/`.

## Progress Updates

- 1 short message when you start (what + where).
- Update only on material changes: milestone, error, or completion.
- On completion, report what changed and where.

## Auto-Notify on Completion

Append a wake trigger so OpenClaw gets pinged:

```bash
exec pty:true workdir:~/project background:true command:"pi -p 'Build a REST API.

When completely finished, run: openclaw system event --text \"Done: Built REST API\" --mode now'"
```
