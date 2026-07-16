---
name: business-one-pager
description: "Produce a concise screening brief for a business. Use as the fast pre-step before understand-business or analyze-earnings, to decide whether a company earns a deeper look."
user_invocable: true
argument: "<ticker>"
---

# business-one-pager

Build a screening brief for a business from its latest annual report and matching earnings call. It sits in front of `understand-business` (long-term structural work) and `analyze-earnings` (quarterly), giving Anton the facts to decide whether a company earns a deeper look.

## What this brief is

- **Sources:** the latest annual report (10-K, or 20-F for foreign private issuers) and the earnings transcript for that same fiscal year.
- **Stance:** facts, not judgment. Report what the company does, what the numbers are, and what the filings say — no rating, no buy/sell/hold. Anton draws the conclusions.
- **Center of gravity:** the two business sections carry the brief. If we cannot explain plainly how the company makes money, who pays, and how it competes, that gap is the finding.
- **Reader test:** "one-pager" is a concept, not a page count. It succeeds if Anton reads it comfortably in one sitting and comes away understanding the business. Readability first.

## Checklist vs. this file

The checklist (`references/one-pager-checklist.md`) sets **what content** each section must cover. This file sets **how it is written**. The checklist is an input spec — never reproduce its structure or wording in the output.

## Writing rules

- **Instructions are not content.** Nothing in the checklist or this file should appear on the page as text. Never echo build notes as captions (no "columns oldest → newest", no "\$M unless noted" — put units in the column header). Never reuse a prescribed-sounding sentence verbatim across briefs; phrase every judgment-free observation freshly for the company.
- **Prose, not bullets.** Write sections 1–2 as a few short paragraphs, each opening with a bold topic phrase, then plain sentences. One idea per paragraph, white space between them.
- **Depth is clarity, not accumulation.** Explain how the business is structured and competes — the few facts that matter and what they mean. Choose the facts that carry the structure; leave the rest.
- **No judgment.** Report level, direction, and disclosed facts; do not editorialize into good/bad, cheap/expensive, strong/weak.
- **Plain language**, understandable to a non-specialist.
- **Citations at sentence-end**, one clean reference — not the same source repeated mid-clause.
- **GAAP** unless a figure is explicitly otherwise.
- **Appendix holds the peripheral** — calculation methods, adjustments, assumptions, sources. Sections 1–4 stay clean.
- **Time-series ordered oldest → newest.**

## Workflow

### 1. Resolve company and gather sources

Look up the company in `hard-disk/data/01-portfolio/current/company-directory.md` for evidence root, jurisdiction, and transcript source. No folder? Use `initialize-company` first. Collect into the company's `data/` folder:

| Material | How |
|:---|:---|
| Latest annual report (markdown) | `minerva sec download {TICKER} --form 10-K --format markdown` (`--form 20-F` for foreign private issuers) |
| Matching full-year transcript | `earnings-transcript` skill (the Q4 / full-year call for that fiscal year) |
| 5-year financials | `minerva sec financials {TICKER} --type income --periods 5`, `--type balance`, `--type cash` |

If the matching transcript is unavailable, note it and proceed.

### 2. Read the checklist

Read `{baseDir}/references/one-pager-checklist.md` for the required content of each section.

### 3. Extract with `minerva extract`

The annual report is heavy — do not read it raw into context. Use `minerva extract` (or a `--questions-file` pack) to pull what the checklist requires, leaning hardest on the two business sections where the depth lives. Draw matching color from the transcript where it adds signal.

### 4. Financials, valuation, implied growth

From `minerva sec financials`, build the spine. Compute simple ROIC (NOPAT / invested capital), method in the Appendix; net debt signed (negative when net cash).

Valuation is Current / 5-yr avg / Forward for P/E, EV/Sales, and EV/FCF; forward = next-fiscal-year consensus from an external source (e.g. stockanalysis.com), cited in the Appendix. Compute each cell from its own numerator and denominator; the forward multiple divides EV by the forward metric.

For implied growth, solve the perpetual FCF growth rate implied by current price and a 10% discount rate. State it in one fresh sentence per the checklist; keep the formula, inputs, and assumptions in the Appendix.

### 5. Write

Write the sections in order per the checklist and this file's writing rules. Save to `analysis/{company}-one-pager.md`.

### 6. Audit before rendering

Spawn an audit subagent (`gpt-5.5`, high reasoning) with the prompt at `{baseDir}/references/audit-prompt.md`. Give it read access to the one-pager and the company's `data/` sources. Fix every defect it returns; re-audit if numbers changed.

### 7. Render

`md2pdf <one-pager.md> -o <one-pager.pdf>`. Eyeball it against the reader test.

## Output paths

| File | Location |
|:---|:---|
| One-pager | `{company}/analysis/{company}-one-pager.md` |
| PDF | `{company}/analysis/{company}-one-pager.pdf` |
| Sources | `{company}/data/...` |
