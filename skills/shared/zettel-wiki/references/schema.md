# Zettel-Wiki Schema

Conventions for the wiki at `/Users/charlie-buffet/Documents/project-minerva/hard-disk/wiki/`.

## Naming

- Structure notes: lowercase kebab-case semantic filenames (`apple.md`, `gpu-supply-chain.md`)
- Zettels: timestamp IDs in `YYYYMMDDHHmm` format (`202604160930.md`)
- Folders: lowercase kebab-case (`companies/`, `concepts/`)
- Infrastructure files: ALL CAPS (`INDEX.md`, `LEDGER.md`)

## Wiki folders

When a structure note evolves into a folder, the hub page keeps the same filename inside the folder: `pages/apple.md` → `pages/apple/apple.md`

Sub-pages use semantic filenames. Nested folders are allowed. Every folder gets an `INDEX.md`.

## INDEX.md format

Every folder gets an `INDEX.md` with a markdown table of immediate children:

```markdown
| Name | Notes |
|---|---|
| `apple.md` | Apple — business model, competitive position |
| `nvidia.md` | NVIDIA — GPU supply, AI infra |
```

The root `INDEX.md` is the master entry point.

## LEDGER.md format

Append-only chronological activity log:

```markdown
## [YYYY-MM-DD HH:MM] action | Title

- **Source**: path or URL
- **Created**: list of new files
- **Updated**: list of modified files
```

## Tag conventions

- Tags use `#kebab-case`: `#platform-economics`, `#apple`
- Tags are entry points, not a taxonomy — don't overthink them
- Tags evolve organically
