# INDEX

| Name | Notes |
|---|---|
| `browser` | Shared browser automation skill; canonical copy now uses the newer browser-v2 wording. |
| `coding-agent` | Shared coding-agent skill for Codex & Gemini CLI delegation. Moved from node_modules 2026-04-09. |
| `earnings-transcript` | Fetch earnings call transcripts from free web sources (Motley Fool, company IR, MarketScreener). Added 2026-04-18. |
| `clawhub` | Bundled skill override kept installed but hidden from the model prompt. |
| `gemini` | Bundled skill override kept installed but hidden from the model prompt. |
| `git-worktree` | Shared git worktree workflow skill. |
| `grill-me` | Shared plan and design stress-testing skill. |
| `healthcheck` | Bundled skill override kept installed but hidden from the model prompt. |
| `learn` | Shared knowledge-ingestion skill; re-enabled as model-visible on 2026-04-07. |
| `openai-whisper` | Bundled skill override kept installed but hidden from the model prompt. |
| `push-git-remote` | Shared push/PR/merge workflow skill. |
| `slack` | Shared Slack operation skill. |
| `update-workspace-markdown` | Shared markdown-maintenance skill; model-visible. |
| `use-printer` | Shared local printing workflow for CUPS/Brother, duplex checks, and HTML-to-PDF printing. |
| `video-frames` | Bundled skill override kept installed but hidden from the model prompt. |
| `write-a-skill` | Shared workflow for creating reusable agent skills. |
| `xlsx` | Shared spreadsheet skill; kept installed but hidden from the model prompt. |

## Notes

- `~/.openclaw/skills/` is the native machine-wide shared skill location for OpenClaw.
- Workspace `skills/` folders remain the per-agent override layer for agent-specific skills only.
- During this 2026-04-07 sweep, shared skills were promoted here and redundant per-workspace shared copies were archived under `~/.openclaw/archive/skills-sweep-2026-04-07/`.
- The custom `pdf` and `image-generation` skills were removed from the live tree.
