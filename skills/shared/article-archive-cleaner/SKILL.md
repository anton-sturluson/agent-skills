---
name: article-archive-cleaner
description: Archive, extract, clean, and convert article-like web pages or local HTML files into readable markdown or text with predictable filenames and folder indexes. Use when the task involves downloading, repairing, or organizing articles, newsletters, blog posts, essays, reports, or other content-heavy pages, especially when raw HTML is noisy, source files are missing, or a folder contains manifests without usable article files.
---

# Article Archive Cleaner

## Overview

Turn article-like web pages or saved HTML into durable, readable markdown or text.

Preserve the content, not the full page shell. Keep the title, headings, paragraphs, lists, links, tables, and useful captions. Remove navigation, buttons, ads, scripts, embeds, and other junk unless the user explicitly wants them.

## Bundled script

Use `scripts/clean_article_html.py` for the actual extraction, cleanup, conversion, and file-writing work.

The script accepts URL(s) or local HTML file(s), writes cleaned markdown or text to an output directory, and can also update `INDEX.md` and `download-manifest.md`.

Typical usage:

```text
scripts/clean_article_html.py --out-dir <folder> <url-or-html-file> [more inputs...]
scripts/clean_article_html.py --out-dir <folder> --update-index --update-manifest <inputs...>
```

Prefer the script over ad hoc one-off cleanup. If the output is poor, inspect the source shape and improve the extraction heuristics instead of manually fixing one file at a time.

## Workflow

### 1. Choose the target output

Determine whether the user wants markdown, plain text, or both. Default to markdown.

### 2. Run the script

Use `scripts/clean_article_html.py` with the target folder and inputs.

The script should:

- Fetch URLs or read local HTML files
- Prefer a source-specific fast path when a clear article body is exposed
- Otherwise extract the main content block from the full HTML
- Decode escaped HTML and entities before conversion
- Remove wrappers, prompts, viewer chrome, and empty tags
- Omit images and embeds by default, but keep informative captions when practical
- Write stable output filenames with a short metadata header
- Update `INDEX.md` and `download-manifest.md` when requested

### 3. Verify before reporting success

Open at least one saved file, search for obvious leftover raw HTML, confirm the expected file count exists, and ensure the manifest and index reflect reality.

## Quality bar

Prefer clean markdown over raw HTML. Keep filenames short and stable. Call out partial paywalls, omitted media, or other material limitations explicitly. Do not claim the archive is complete if only manifests or summaries were written.
