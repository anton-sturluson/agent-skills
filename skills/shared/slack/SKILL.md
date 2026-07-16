---
name: slack
description: Use this skill before your first Slack interaction in a session, then any time you send, edit, react, read, manage pins, or move files in Slack — Slack uses mrkdwn, not standard Markdown.
---

# Slack

## Formatting — READ FIRST

Slack uses **mrkdwn**, NOT standard Markdown. Writing standard Markdown produces visibly broken output (literal `**`, raw `| --- |` table rows). The OpenClaw auto-converter is unreliable for this — always author native mrkdwn yourself.

| Want | Correct (mrkdwn) | WRONG (do not use) |
| --- | --- | --- |
| Bold | `*one asterisk*` | `**two asterisks**` |
| Italic | `_underscores_` | `*asterisks*` |
| Strikethrough | `~tildes~` | — |
| Inline code | `` `backticks` `` | — |
| Link | `<https://url|label>` | `[label](https://url)` |
| Pseudo-heading | `*Bold line*` on its own line | `# Heading` |

Hard rules:

- **No tables.** Slack has no table support; pipe tables render as literal `| --- |` junk. Put tabular data in a fenced code block with space-padded columns so it aligns:
  ```
  Setting              Value today    Change to
  -------------------  -------------  ---------
  visibleReplies       message_tool   automatic
  streaming.mode       partial        partial
  ```
- **No markdown headings** (`#`, `##`). Use a `*bold line*` instead.
- **No nested bullet indentation** — Slack strips it. Two levels only: `•` top-level, `–` (en-dash) sub-items. Deeper nesting must be flattened or restructured with bold pseudo-headers.
- For file trees or path hierarchies, use a fenced code block with `├──` / `└──`.
- Mention users with the stable `<@USER_ID>` token (not plain `@name`) so Slack links and notifies them.

## The `message` tool

All Slack actions go through the `message` tool. Pass `channel: "slack"` when acting outside the current source channel.

| `action` | Use for | Key inputs |
| --- | --- | --- |
| `send` | Send to a channel or DM | `target`, `message` |
| `edit` | Edit a sent message | `target`, `messageId`, `message` |
| `delete` | Delete a sent message | `target`, `messageId` |
| `react` | Add a reaction | `target`, `messageId`, `emoji` |
| `reactions` | List reactions on a message | `target`, `messageId` |
| `read` | Read channel or thread history | `target`, `threadId` (for a thread), `limit` |
| `pin` / `unpin` | Pin / unpin a message | `target`, `messageId` |
| `list-pins` | List pinned items | `target` |
| `member-info` | Look up a member | `userId` |
| `emoji-list` | List custom emoji | none |
| `upload-file` / `download-file` | Move files | `filePath` (up) / `fileId` (down) |

Pull these from the inbound message context instead of guessing:

- channel id → `target` as `channel:<id>` or `user:<id>`
- message timestamp/id → `messageId` (e.g. `1712023032.123456`)
- thread parent ts → `threadId`
- file id for downloads → `fileId` from `event.files[].id` (starts with `F`)

## Thread discipline

If a conversation starts in a thread, keep all replies in that thread by passing `threadId`. For background/subagent results, set `threadId` explicitly — don't rely on reply-to-current, since thread context can be lost across sessions. Recover the parent `ts` from channel history if needed.

## Minimal examples

Send a message:

```json
{"action":"send","target":"channel:C123","message":"*Done* — see <https://docs.openclaw.ai|the docs>."}
```

Read thread replies:

```json
{"action":"read","target":"C123","threadId":"1712023032.123456","limit":20}
```

React to a message:

```json
{"action":"react","target":"C123","messageId":"1712023032.123456","emoji":"white_check_mark"}
```

If the current session does not expose a needed Slack capability, say so plainly instead of guessing.
