---
name: format-report
description: "Format, render, and visually inspect Markdown reports before delivery, especially reports with financial or comparison tables."
---

# Format Report

Apply this workflow after the report is substantively complete and before delivery. Preserve the analysis; change wording only when needed to repair structure, readability, or rendering.

## Prepare the source

1. Keep exactly one H1 containing the document title.
2. Use unique, hierarchical headings without skipped levels or orphaned headings.
3. Remove duplicated titles, build instructions, placeholders, raw extraction notes, and repeated boilerplate.
4. Check Markdown-sensitive characters, fenced blocks, lists, links, images, and local citations.
5. Resolve every relative link from the report's directory.
6. If the report contains tables, read and apply [references/table-formatting.md](references/table-formatting.md).

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

## Inspect, correct, and deliver

1. Confirm the output opens and contains the complete report.
2. Use `pdfinfo` and `pdftotext` for PDF sanity checks when available.
3. Render representative PDF pages to images and inspect title pages, dense tables, charts, and final pages.
4. Check visual quality: clipped content, overflow, tiny text, awkward page breaks, split rows, and orphaned headings.
5. Correct defects in the source and render once more.
6. Deliver only when the output is legible and complete. Disclose any remaining defect.
