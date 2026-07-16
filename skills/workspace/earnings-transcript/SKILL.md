---
name: earnings-transcript
description: "Fetch earnings call transcripts for public companies. Use when the user asks for a transcript, when research or analysis requires earnings call content, or when auditing transcript availability for portfolio companies."
user_invocable: true
argument: "<ticker> [--quarter Q3 --year 2025] [--latest N] [--output <dir>]"
---
# Earnings Transcript — Fetch & Save Skill

Fetch earnings call transcripts from free web sources and save them as clean markdown. No paid API keys required.

## Scope

- Covers any public company; best coverage for US-listed with meaningful market cap
- ETFs, bond funds, mutual funds do not have earnings calls — skip them
- If all methods fail, flag it clearly; do not silently skip

## Transcript source lookup

Check `hard-disk/data/01-portfolio/current/company-directory.md` — the "Transcript source" column has the preferred source for each company. Use that before searching.

## Source priority (for new companies)

Try in order; stop at first success:

1. Motley Fool — free, no login, no paywall
2. Company IR site — some micro-caps host transcript PDFs
3. MarketScreener / Investing.com — fallback for international small-caps

Do not use Seeking Alpha (paywalled). If `web_fetch` fails, fall back to the `browser` skill.

## Extraction methods

### Motley Fool

Search: `web_search` with `site:fool.com "earnings call transcript" {TICKER}`. Add `Q{N} {YEAR}` for a specific quarter.

Fetch: `web_fetch` the result URL with `maxChars: 200000`. Renders cleanly — no browser needed.

### Company IR

Navigate to the transcript page from the company directory notes or `ir-registry.json`. Use `web_fetch` for HTML or `pdf` tool for PDFs.

### MarketScreener / Investing.com

Search: `web_search` with `"{COMPANY_NAME}" earnings call transcript site:marketscreener.com` (or `site:investing.com`).

Fetch: `web_fetch` the result URL.

## Output

Filename: `{TICKER}-Q{N}-{YEAR}.md`

Header (prepend to every saved file):
```markdown
# {COMPANY_NAME} ({TICKER}) — Q{N} {YEAR} Earnings Call Transcript

- Source: {source name and URL}
- Date: {call date}
- Fetched: {current date}

---
```

Then the transcript content.

## Source audit for new companies

After `minerva portfolio sync` with new tickers, or when asked to audit:

1. Check company-directory.md first
2. If not listed, search Motley Fool → Company IR → MarketScreener
3. Update company-directory.md with the result (including "Not available" if nothing found)

## Edge cases

- Fiscal year mismatch: some companies label quarters by fiscal year, not calendar; try both
- BEPC / BEP: Brookfield Renewable may appear under either ticker; search both
- Rate limiting: space requests by at least 1 second in batch mode
- Recent calls: transcripts typically appear within 24h of the call; if missing, retry later
