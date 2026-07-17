---
name: format-report
description: Format, render, and visually inspect Markdown reports before delivery, especially reports with financial or comparison tables.
---

# Format Report

Apply this workflow after the report is substantively complete and before delivery. Preserve the analysis; change wording only when needed to repair structure, readability, or rendering.

## Structural preflight

1. Keep exactly one H1 containing the document title.
2. Use unique, hierarchical headings without skipped levels or orphaned headings.
3. Remove duplicated titles, build instructions, placeholders, raw extraction notes, and repeated boilerplate.
4. Check Markdown-sensitive characters, fenced blocks, lists, links, images, and local citations.
5. Resolve every relative link from the report's directory.

## Tables

Read [references/table-formatting.md](references/table-formatting.md) whenever the report contains tables.

- Put units in the table title, caption, or column heading.
- Order time-series columns from oldest on the left to newest on the right.
- Keep labels left-aligned and comparable numeric values consistently aligned.
- Select the least compressed size that renders cleanly.
- Apply a table profile only when its behavior matches the table.
- Follow each decision-relevant table with a short interpretation; do not merely repeat its values.

## Render

Set the shared stylesheet path:

```bash
FORMAT_REPORT_CSS="${OPENCLAW_HOME:-$HOME/.openclaw}/skills/format-report/assets/report-tables.css"
```

Render the requested format:

```bash
md2html <report.md> -o <report.html> --extra-css "$FORMAT_REPORT_CSS"
md2pdf <report.md> -o <report.pdf> --extra-css "$FORMAT_REPORT_CSS"
```

If the report skill requires both formats, render both. Do not substitute a new renderer when the repository already specifies one.

## Inspect and correct

1. Confirm the output opens and contains the complete report.
2. Use `pdfinfo` and `pdftotext` for PDF sanity checks when available.
3. Render representative PDF pages to images and inspect title pages, dense tables, charts, and final pages.
4. Check for clipped content, overflow, tiny text, awkward page breaks, split rows, orphaned headings, broken links, and duplicated titles.
5. Correct defects and render once more.
6. If a defect remains, disclose it rather than silently delivering a compromised document.

## Acceptance

Deliver only when:

- the Markdown has one H1 and a coherent heading hierarchy
- tables state units and use oldest-to-newest chronology where applicable
- links and citations resolve
- no instructions, placeholders, or extraction debris remain
- the rendered output is legible and complete
