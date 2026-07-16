---
name: update-openclaw-config
description: >-
  MUST be used for ANY activity that changes OpenClaw configuration or
  restarts the gateway — adding/removing model providers or models, editing
  agents, channels, bindings, plugins, skills config, secrets, or
  troubleshooting gateway behavior. Always use `openclaw config set/unset`
  (never hand-edit openclaw.json), dry-run first, and get Anton's explicit
  approval before any restart.
---

# update-openclaw-config

## Rules

- `~/.openclaw/openclaw.json` is sensitive — never hand-edit or whole-file rewrite. Use `openclaw config set` / `openclaw config unset` exclusively. The `gateway config.patch` tool **rejects protected paths** (e.g. `models.providers.*`); the CLI with `--replace` is the sanctioned route
- Every config change needs Anton's explicit ask; every gateway restart needs explicit approval each time — never restart as part of a change, troubleshoot, or smoke test without it
- Run `--dry-run` before any real write; run `openclaw config validate` after

## Procedure

1. **Plan** — state exact dot paths and expected reload-vs-restart effect (most config hot-reloads; provider/secret changes need restart)
2. **Inspect first** — `openclaw config get <path>` or read current state so you merge/preserve, never clobber
3. **Dry-run** — same command with `--dry-run`; fix errors before writing
4. **Apply** — `openclaw config set/unset` (see Patterns)
5. **Validate** — `openclaw config validate`
6. **Restart only if approved**, then **smoke-test live** — a successful write ≠ a working path

## Patterns (`openclaw config set`)

- **Scalar:** `openclaw config set gateway.port 19001 --strict-json`
- **Object/array value:** pass JSON; write to a temp file to dodge shell-quoting:
  `openclaw config set models.providers.X "$(cat /tmp/x.json)" --strict-json --replace`
- **Protected paths** (model providers/models, etc.): add `--replace`
- **Merge into a map** (e.g. add aliases without wiping siblings): `--merge` — **mutually exclusive with `--replace`**; map-merge targets aren't protected so `--merge` alone works
- **Secrets as SecretRef** (preferred over inline `${VAR}`):
  `openclaw config set models.providers.X.apiKey --ref-provider default --ref-source env --ref-id MY_ENV_VAR --replace`
  Serializes to `{source,provider,id}`; the env var must be visible to the **daemon** (set in `~/.openclaw/.env`, not just an interactive shell)
- **Remove a map key:** `openclaw config unset 'a.b.c/with/slashes'` (quote paths containing `/`)
- **Remove one array element:** don't unset by index (leaves a hole) — rewrite the whole array via `config set ... --replace` with the element omitted

## Verify

- `openclaw models list --provider X` — confirm models load; `Auth: yes` means the key resolved
- `openclaw models status --json` → `auth.unusableProfiles` flags missing/broken credentials
- For behavior changes, run a minimal end-to-end test (e.g. spawn a subagent on a new model)

## Slack output rendering

Three layers control Slack send/render; set them on **top-level config AND every account** (`default` + each agent), not just one:

- `channels.slack.*.markdown.tables: code` + `visibleReplies: automatic` — fixes garbled bold/italic/links
- `streaming.mode` / `streaming.preview.toolProgress` — controls whether `🔧` tool-progress chatter leaks into messages
- `commandText` controls *how* progress renders, not *whether* it shows

Symptom → layer: broken markup → `tables`/`visibleReplies`; stray `🔧` lines → `streaming`. Verify live after restart; defaults drift.

## Gotchas

- **Stale config = phantom failures:** a model/provider added but not yet restarted can fail fast (sub-second, no transcript). Re-test after restart before diagnosing the model itself
- **Bundled-plugin catalogs aren't yours to remove:** some providers ship built-in models (untagged in `models list`). Removing your `configured` entry won't delete them
- **Plugin policies override config:** e.g. Fireworks force-clamps Kimi `thinking: off` regardless of `reasoning: true` — verify the live `thinkingLevel`, don't assume config wins
- **Per-agent blocks:** when adding a per-agent block (e.g. `heartbeat`) for one agent, add it for every agent that should keep that behavior — agents without an explicit block can lose implicit defaults
- **Always back up** `openclaw.json` and `.env` before edits, even via CLI
