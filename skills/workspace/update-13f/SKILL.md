---
name: update-13f
description: "Download and compare quarterly 13-F filings for all tracked fund managers. Use when a new quarter's filings are due, when asked to update 13-F data, or at the start of a new filing season."
---

# Update 13-F Filings

## Overview

Batch-download 13-F filings and generate QoQ comparison diffs for all fund managers listed in the portfolio directory.

## Paths

- Directory: `{baseDir}/hard-disk/data/03-13f-portfolios/directory.md`
- Quarter folders: `{baseDir}/hard-disk/data/03-13f-portfolios/{quarter}/` (e.g. `Q1-2026`)
- Base dir: `/Users/charlie-buffet/Documents/project-minerva`

## Filing calendar

| Quarter ending | Folder name | Filing deadline |
|---|---|---|
| Mar 31 | Q1-YYYY | May 15 |
| Jun 30 | Q2-YYYY | Aug 14 |
| Sep 30 | Q3-YYYY | Nov 14 |
| Dec 31 | Q4-YYYY | Feb 14 |

## Workflow

### Step 1 — Determine the current quarter

Compute the quarter label from today's date:
- Jan 1 – Mar 31 → previous year's Q4 filings are due (folder: `Q4-{prev_year}`)
- Apr 1 – Jun 30 → Q1 filings are due (folder: `Q1-{year}`)
- Jul 1 – Sep 30 → Q2 filings are due (folder: `Q2-{year}`)
- Oct 1 – Dec 31 → Q3 filings are due (folder: `Q3-{year}`)

If the user specifies a quarter, use that instead.

### Step 2 — Create the quarter folder if it doesn't exist

Check if `{baseDir}/hard-disk/data/03-13f-portfolios/{quarter}/` exists. If not, create it.

### Step 3 — Parse the directory for CIKs

Read `directory.md` and extract all CIKs from the "Active Filers" table. Parse the markdown table rows — CIK is the third column. Also extract the investor name and fund entity for slug generation.

Generate slug from fund entity: lowercase, replace spaces with hyphens, strip punctuation (e.g. "Pershing Square Capital Management, L.P." → "pershing-square").

### Step 4 — Download HTML filings

For each CIK, download the filing HTML:

```bash
minerva sec download {CIK} --form 13F-HR --format html --output {quarter}/{slug}.html
```

Skip if the file already exists.

> **Known limitation:** `minerva sec download --format html` currently only captures the cover page, not the holdings table. The holdings table is a separate XML document in the filing. This is a known gap — the cover page is still useful for metadata (filing date, manager info, total value). The actual holdings data lives in the `-diff.md` comparison files from Step 5.

### Step 5 — Generate QoQ comparison diffs

For each CIK, run the comparison:

```bash
minerva sec 13f {CIK} --output {quarter}/{slug}-diff.md
```

Overwrite existing diffs (they may be stale from a previous run).

### Step 6 — Report results

Post a summary to the channel:
- How many managers processed
- Any failures (with CIK and error)
- Notable findings: managers who haven't filed yet for this quarter (check filing date in the cover page)

