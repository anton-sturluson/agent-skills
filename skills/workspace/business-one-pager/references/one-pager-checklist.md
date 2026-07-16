# One-Pager Content Checklist

Defines **what content each section must cover**. How the brief reads — prose form, density, style — is governed by SKILL.md. The items below are coverage requirements, not an output template or wording to reproduce.

Section headers are used verbatim and in order. Figures are GAAP unless a row says otherwise. Footnotes, methodology, adjustments, and assumptions live in the Appendix.

## Header

```
# {COMPANY} ({TICKER}) — Business One-Pager

- Source: {annual report form} FY{YYYY} + FY{YYYY} earnings call
- Date: {current date}
```

`{annual report form}`: 10-K (US filers), 20-F (foreign private issuers).

## 1. The business

- [ ] What the company does and how it makes money
- [ ] Customers — who buys and why they pay
- [ ] Concentration — customer (top customer / top-10 % if disclosed) and revenue by segment, product, geography
- [ ] Recurring vs. transactional revenue mix, if derivable
- [ ] Value chain / ecosystem — position from input → end customer; key suppliers and sole-source dependencies; channel/partner reliance

## 2. Competitive landscape & moat

Report facts bearing on competitive position; do not rate the moat.

- [ ] Market structure — size and the company's share if disclosed; how fragmented or concentrated
- [ ] Named competitors and their relative scale; the company's stated position
- [ ] Competitive intensity / pricing — price-taker vs. price-setter; pricing history where disclosed
- [ ] Moat evidence — stated advantage(s) (brand, switching costs, network effects, cost/scale, regulatory, intangibles, efficient scale) and the specific evidence for each
- [ ] Stickiness — retention/churn, net revenue retention, switching-cost evidence, R&D or capex intensity where disclosed

## 3. Financial spine

One table, these rows in order, five fiscal years:

| Row | Notes |
|:---|:---|
| Revenue ($M) | segment split only if it stays compact |
| Revenue growth | |
| Gross margin | |
| Operating margin | |
| Net margin | |
| ROIC (simple) | |
| FCF ($M) | |
| FCF margin | |
| Diluted shares (M) | |
| SBC % of revenue | |
| Net debt ($M) | negative when net cash (e.g. −1,800 = $1.8B net cash) |

Add the business's key operating metrics as rows here — the few management leads with and investors track (e.g. ARPU, net/gross revenue retention, renewal rate, same-store sales, RPO/backlog, take rate, subscribers, occupancy, load factor). Where disclosed only for recent years, mark earlier years `n/d`.

Below the table, 2–4 sentences on what the numbers show — growth, margins, returns, cash generation, dilution, balance sheet.

## 4. Valuation & implied expectations

| Multiple | Current | 5-yr avg | Forward |
|:---|---:|---:|---:|
| P/E | | | |
| EV / Sales | | | |
| EV / FCF | | | |

Forward = next-fiscal-year consensus. Use `n/m` where losses make a multiple meaningless.

Then one line stating the implied growth: the perpetual FCF growth rate today's price and a 10% discount rate imply, framed as expectations to weigh against a base rate for a company of this type and size — not against management guidance. Phrase it freshly for the company; do not reuse a stock sentence.

## Appendix

- [ ] ROIC method (NOPAT and invested-capital definition)
- [ ] Implied-growth inputs (FCF base year, 10% discount rate, cash-return proxy, edge cases)
- [ ] Normalization/adjustments (one-time tax items, stock splits, capitalized intangibles, EV bridge)
- [ ] Forward-metric source
- [ ] Company-specific terms/acronyms only
