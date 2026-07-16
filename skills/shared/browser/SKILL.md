---
name: browser
description: "Drive a persistent browser via CLI commands through a Chrome extension bridge. Visible commands: open, tabs, focus, close, click, type, fill, upload, wait, snapshot, diff, inspect, describe, ask, extract, eval, dialog, status, stop. Supports multi-tab management with aliases (t0, t1, ...) and per-agent window isolation. The browser session persists across calls. Auto-starts on first command."
---

# Browser CLI (v2)

Controls the user's real Chrome through a local server plus extension bridge. State persists across calls: cookies, logins, navigation, and DOM context stay live.

Run `browser help` for the full command list. Run `browser <command> --help` for detailed usage, options, examples, and next steps.

## Bridge Disconnected: Hard Stop

If any command returns `Chrome extension bridge is not connected`, **stop immediately**. Do not retry. Tell the user Chrome must be open with the extension loaded. This is not recoverable from the agent side.

## Per-Agent Windows

Always open your own isolated window. Never share the default active tab.

```bash
browser open "https://example.com" --new --window   # creates a dedicated Chrome window
# note the tab alias from the output (e.g. t3)
browser inspect --tab t3                             # all commands pinned to your tab
browser close t3                                     # window auto-closes when empty
```

## Workflow

1. **Open:** `browser open "<url>" --new --window`
2. **Orient:** `describe` for visual overview, `snapshot` for structure, `inspect` for clickable refs
3. **Act:** `click`, `fill`, `type`, `upload` using refs (e1, e2) or selectors
4. **Verify:** `ask "did it work?"` or `diff` to see what changed
5. **Close:** `browser close <alias>` when done

## Observation Commands

| Command    | Use when                                              |
|------------|-------------------------------------------------------|
| `describe` | Page orientation — "what is on this page?"            |
| `ask`      | Targeted check — "is the error banner visible?"       |
| `snapshot` | Raw accessibility tree for structure/debugging        |
| `diff`     | What changed since last snapshot                      |
| `inspect`  | Find clickable elements and get ref IDs               |
| `extract`  | Pull visible text or structured link/text items       |
| `eval`     | Run JS for precise DOM checks                         |

## Pacing

Write commands (`open`, `click`, `type`, `fill`, `upload`) have built-in 300–800ms randomized delays.

For aggressive sites (TikTok, LinkedIn, Amazon), add explicit waits:

```bash
browser wait --ms 2000-4000
```

Back off on failure: 5s → 15s → 30s → stop and report.

## Locations

Repo: `/Users/charlie-buffet/Documents/heartbeat-browser-agent/src/browser-cli-v2`
Extension: `/Users/charlie-buffet/Documents/heartbeat-browser-agent/src/browser-cli-v2/extension`
