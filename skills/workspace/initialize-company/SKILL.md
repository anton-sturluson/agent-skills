---
name: initialize-company
description: One-time setup for a new company in the evidence tree. Creates the folder structure, collects initial filings (SEC for US, IR-site investigation for non-US), discovers transcript sources, and updates the central company directory. Use when adding a company to the research universe for the first time.
---

# initialize-company

One-time initialization when a company enters the research universe. Run once per company, before any evidence collection or analysis.

## Central directory

All company metadata lives in one place: `hard-disk/data/01-portfolio/current/company-directory.md`

This is the single source of truth for filing jurisdiction, IR pages, transcript sources, and fiscal calendar. Always read it before investigating a company and update it as the last step.

## Inputs

- Ticker, company name, slug
- Company root path: `hard-disk/reports/00-companies/{NN}-{slug}`
  - Pick the next available number prefix by checking existing folders

## Steps

### 1. Create evidence tree

```
minerva evidence init --root {root} --ticker {TICKER} --name "{Company Name}" --slug {slug}
```

### 2. Determine filing jurisdiction

Web search: `"{company name}" SEC EDGAR CIK` and check the exchange from universe.json

| Signal | Path |
|---|---|
| Listed on NYSE/NASDAQ/NYSE MKT, or has CIK on EDGAR | US filer → step 3A |
| Foreign private issuer filing 20-F on EDGAR | Hybrid → step 3A (20-F only) + 3B |
| No EDGAR presence | Non-US → step 3B |

### 3A. US/SEC filer — collect filings

```
minerva sec bulk-download {TICKER} --output {root}/data/sources --annual 5 --quarters 4 --earnings 4
minerva sec financials {TICKER} --type all --periods 5
```

Save financials output to `{root}/data/structured/`

### 3B. Non-US filer — investigate IR site

1. Find the official IR page (web search `"{company name}" investor relations`)
2. Identify where annual reports, quarterly reports, and results presentations are hosted
3. Check for these filing types and note availability:
   - Annual report / annual results
   - Interim / half-year / quarterly results
   - Investor presentations
   - Results webcasts or transcripts
4. If the company has an ADR or cross-listing, check EDGAR for 20-F/6-K filings

### 4. Discover transcript source

Search for earnings call transcripts using the `earnings-transcript` skill's source priority:
1. Motley Fool (`site:fool.com "{TICKER}" OR "{company name}" earnings call transcript`)
2. Company IR site (check for hosted transcripts or webcast pages)
3. Alpha Spread, Quartr, MarketScreener, Investing.com

### 5. Update company directory

Add or update the company's row in `hard-disk/data/01-portfolio/current/company-directory.md` with all discovered metadata: exchange, fiscal year end, filing jurisdiction, SEC filer status, IR page, transcript source, evidence root (folder name under `00-companies/`), and any notes.

If management publishes supplemental materials beyond standard filings and transcripts (shareholder letters, investor presentations, owners' manuals, etc.), add an entry to the `## Supplemental IR materials` section with the material type and source URL.

Also update `ir-registry.json` if a new IR page or feed was discovered.

### 6. Verify and report

Confirm all expected files exist. Report:
- Root path created
- Filing jurisdiction and collection status
- Transcript source (or not available)
- Company directory updated
- Any gaps or follow-ups needed
