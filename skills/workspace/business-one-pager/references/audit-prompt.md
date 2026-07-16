# One-Pager Audit Prompt

Audit a finished business one-pager against its source data. Return a numbered defect list only — no rewrite, no praise, no commentary. If a check passes, say nothing about it. If clean, return `No defects found.`

## Inputs

- One-pager markdown: `{path to analysis/{company}-one-pager.md}`
- Source financials and filings: the company's `data/` folder (`data/structured/`, `data/sources/`)

## Syntax / rendering

- Every table renders: aligned dividers, header separator row present, equal cell count per row, no stray or missing pipes.
- Every `$` inside a table cell **and in prose** is escaped as `\$`. Unescaped `$...$` triggers pandoc math mode and breaks rendering — flag each occurrence.
- Section headers match the checklist verbatim and in order.
- No build-note text, instruction fragments, or repeated boilerplate on the page.
- No stale, duplicate, or leftover sections.

## Numbers

Recompute every derived figure from the source data and stated inputs; flag any that does not reconcile:

- Revenue growth, gross/operating/net margins, FCF margin, SBC % of revenue.
- ROIC (against the Appendix NOPAT and invested-capital definitions).
- Net debt sign (negative = net cash).
- All valuation multiples — current **and** forward — each recomputed from its own numerator and denominator. Confirm forward multiples divide EV by the **forward** metric (forward FCF, forward sales), not a reused current-year value.
- EV bridge (market cap ± net debt).
- Implied-growth solve (formula, FCF base, discount rate, EV).

Also flag any figure in prose that disagrees with the tables.

## Output format

```
1. [SYNTAX] <location> — <defect> → <fix>
2. [NUMBER] <location> — stated <X>, recomputed <Y> from <source> → <fix>
...
```
