# Earnings Analysis Checklist

This checklist defines the output structure. Each section below maps 1:1 to a section in the final analysis. Every item must be addressed — directly answered, compressed as minor, marked immaterial with reason, or flagged as evidence gap.

## Writing rules

**Completeness:** Every metric the company reports in its earnings release, presentation, or supplement must appear in the analysis. If the company reports it, include it.

**Analytical density:** Each table or data block must be followed by interpretive prose — not restating the numbers, but explaining what they mean, what patterns they reveal, and what questions they raise. If a table shows margin compression, the prose should explain the mechanism, assess whether it's structural or temporary, and connect it to the business thesis. Data without interpretation belongs in the Appendix. Guard against redundancy/unnecessarily repeating the same content across sections.

**Table placement:** Tables that directly illuminate the quarter's core narrative stay in the main body alongside their interpretation. Supporting tables needed only for completeness — full geographic splits at every granularity, detailed reconciliations, minor segment breakdowns — go to the Appendix with inline cross-references (e.g., "see Appendix Table X"). The test: if removing a table from the main body would leave a gap in the analytical argument, it stays. If the argument reads just as well citing a few key numbers in prose, move the table to the Appendix. Place the most recent information to the left and the least recent information to the right.

**Coherence:** Write a coherent analysis, not a mechanical checklist dump. Guard against verbosity and redundancy — say it once, clearly. No judgment creep (thesis verdicts, action recommendations).

**Q&A format:** Every analyst question as a numbered heading (format in Section 3a). Do not use tables for Q&A — they render poorly in PDF.

---

## Header & Quarter in Brief

Open the analysis with:

```
# {COMPANY} ({TICKER}) — Q{N} {YEAR} Earnings Analysis

- Call date: {date}
- Analysis date: {current date}
- Prior quarter comparison: {Q(N-1) Y{YYYY} or "Not available"}
```

Then a Quarter in Brief paragraph. Write this at the very end and place it on the top after finishing the rest of the note. It must cover:
- [ ] Headline financial result with key numbers
- [ ] Most important operational, competitive, or strategic signal
- [ ] Key open question or unresolved tension the quarter leaves behind

No bullet structure in the output — write as a short paragraph. No thesis verdicts or action language.

---

## Section 1: Business Results & KPIs

### 1a. Financial Summary

Table immediately after the header. Columns: current quarter, YoY change, LTM, LTM YoY change (where the trailing view adds signal — revenue, earnings, FCF, key operating metrics). Not all rows need LTM.

Required rows (adapt to the business):
- [ ] Revenue (total + by segment/geography) — absolute and growth rates
- [ ] Revenue growth: USD and FX-neutral where reported
- [ ] Gross profit and gross margin
- [ ] Operating income and operating margin
- [ ] Net income and net income margin
- [ ] EPS (diluted)
- [ ] Adjusted EBITDA or non-GAAP operating income (if reported)
- [ ] FCF or adjusted FCF
- [ ] SBC as % of revenue
- [ ] GAAP vs non-GAAP gap: what's excluded, is the gap growing? (Detail the specific adjustments in the Appendix)

Source priority: investor presentation (multi-quarter trends) + earnings release (current + prior year).

### 1b. Segment & Business-Line Deep Dives

Identify the 2–5 material segments. For each:
- [ ] Every KPI from earnings release, presentation, and supplement — current quarter + multi-quarter trend
- [ ] Growth rates: reported (USD) and FX-neutral/constant-currency where applicable
- [ ] Unit economics: revenue per unit, cost per unit, contribution margin, payback — whatever is disclosed or derivable
- [ ] Management commentary from prepared remarks — strategic emphasis, new initiatives, problems acknowledged
- [ ] Competitive dynamics relevant to this segment (fold in; no standalone competition section)

<details>
<summary>Business-type KPI reference (non-exhaustive)</summary>

| Type | Key metrics to look for |
|:---|:---|
| E-commerce / marketplace | GMV by geo, items sold, unique buyers, take rate, ASP, fulfillment penetration, shipping unit costs, 1P/3P mix, ads revenue, membership metrics |
| Fintech / banking | MAU/DAU, AUM, credit portfolio by product, NPL by vintage/bucket, NIMAL/NIM, provisions & coverage, TPV by channel, cost to serve, ARPAC by cohort |
| SaaS / subscription | ARR/MRR, NRR, gross churn, RPO/cRPO, cloud migration %, seat expansion, AI/copilot attach rates, customer count by tier |
| Advertising / media | DAU/MAU, ad impressions, ARPU, engagement (time spent, content volume), advertiser count/mix |
| Hardware / semiconductor | Revenue by end market, ASP trends, unit shipments, design wins, inventory (channel + own), book-to-bill |

</details>

### 1c. Margin Bridge & Cost Structure

- [ ] Each major line item's contribution to margin change YoY and QoQ
- [ ] Which cost lines are scaling (improving as % of revenue) vs. expanding
- [ ] Operating leverage dynamics — what happens to the cost structure as revenue scales?

### 1d. Capital Allocation

- [ ] Capex: level, % of revenue, maintenance vs growth
- [ ] R&D: level, % of revenue, core vs new markets
- [ ] Buybacks and dividends: actual cash returned
- [ ] Acquisitions: M&A activity, integration costs
- [ ] Stated priorities vs actual cash flows — do they match?
- [ ] FCF conversion: OCF → FCF, and FCF/net income ratio
- [ ] Working capital trends: DSO, DIO, DPO — any growing divergence?

### 1e. Management Strategy & Emphasis (This Quarter)

- [ ] What metric or narrative did the CEO lead with? What does the ordering signal?
- [ ] New topics introduced this quarter — why now?
- [ ] Framing: language, analogies, confidence signals
- [ ] New initiatives: backed by dollar commitments, or talking points?

### 1f. Guidance

- [ ] Specific targets, ranges, or qualitative language
- [ ] Trajectory vs prior guidance: raised, maintained, or lowered?
- [ ] Coverage and specificity: guiding on all key metrics, or dropped/vaguened some? (Change in guidance coverage is a signal.)
- [ ] Historical accuracy: does this management beat, meet, or miss their guidance? (Track cross-quarter; don't repeat in Section 2.)

---

## Section 2: Cross-Quarter Comparison & Pattern Recognition

Section 1 covered *this quarter*. Section 2 covers how it compares to prior quarters.

### 2a. Promise Tracking

- [ ] Table: prior-quarter commitment → what was delivered → verdict (delivered / partial / missed / quietly dropped)
- [ ] Multi-quarter promises still pending

### 2b. KPI & Narrative Trajectory

- [ ] Which metrics accelerated, decelerated, or inflected?
- [ ] Metrics management stopped or started reporting — disappearance is often a red flag; note in Red Flags (Section 6b) if material
- [ ] Strategic story change across last 2–3 quarters
- [ ] Language escalation/de-escalation (e.g., "strong" → "resilient" → "selective")
- [ ] Is management anchoring on different metrics than before?

---

## Section 3: Analyst Q&A

### 3a. Full Q&A Map

Every analyst question as a numbered heading:

```
### 1. Analyst Name (Firm) — Topic summary
**Topic:** What they asked
**Key details:** Important specifics — numbers, timelines, commitments, notable omissions.
**Read-through:** What can we infer from this exchange?
```

### 3b. Q&A Synthesis

- [ ] Top concerns: what do the first 3 questions reveal? How has this shifted from prior 1–2 quarters?
- [ ] Recurring themes: multiple analysts on the same topic = unresolved concern
- [ ] What was NOT asked: unpriced risks or unexamined assumptions
- [ ] What management volunteered unprompted (signals what they want to get ahead of)
- [ ] Directness: numbers and timelines, or adjectives and deflection?

---

## Section 4: User-Requested Deep Dives (Optional)

Flexible section for topics the user specifically asks for — macro context, competitive landscape, technology assessment, regulatory analysis, etc. Skip if no user request.

---

## Section 5: Fragility Check

Compact.

- [ ] Leverage: debt, net debt, direction, net debt/EBITDA
- [ ] Debt maturity: near-term refinancing walls?
- [ ] Covenant headroom
- [ ] Liquidity: cash, revolver, FCF vs near-term obligations
- [ ] Revenue/customer/geographic concentration
- [ ] Operating leverage in a downturn: what if revenue drops 15–20%?
- [ ] Risks surfaced or intensified this quarter — specific scenarios grounded in evidence
- [ ] Can this business go to zero? What's the path? (2–3 sentences unless the risk is real)

---

## Section 6: Footnotes & Flags

### 6a. Footnotes & Fine Print

Scan 10-Q/10-K footnotes for:
- [ ] Accounting policy changes
- [ ] Contingent liabilities and legal proceedings: new or changed?
- [ ] Related-party transactions: new or expanded?
- [ ] Segment reporting changes
- [ ] Revenue recognition changes
- [ ] Debt covenant compliance, amendments, refinancing
- [ ] Goodwill/intangible impairment indicators

### 6b. Red Flags

- [ ] Narrative diverging from financials
- [ ] New non-GAAP adjustments or changed definitions
- [ ] Recurring "one-time" charges
- [ ] Management blaming entirely external factors
- [ ] Insider selling contradicting bullish narrative
- [ ] Persistent vague answers to repeated analyst probing

### 6c. Green Flags

- [ ] Management acknowledging problems with specific remedial actions
- [ ] Historically conservative guidance
- [ ] Consistent KPI reporting across quarters — same metrics, same definitions
- [ ] CEO answering tough questions with data
- [ ] Voluntarily discussing risks unprompted
- [ ] GAAP/non-GAAP with clear reconciliation

---

## Section 7: Key Questions for Next Quarter

- [ ] 5–8 specific, testable questions
- [ ] Each with a measurable test or observable outcome
- [ ] What would confirm or disconfirm the key patterns from this quarter?

---

## Appendix (Required)

- [ ] *Glossary:* Define company-specific terms and acronyms — proprietary metrics, internal programs, entity names, and non-obvious business terminology. Do not define standard finance terms (EBITDA, EPS, ROE, FCF, M&A, PE, etc.)
- [ ] *Adjustment detail:* For every adjusted/non-GAAP metric in Section 1a, list specific adjustments with dollar amounts (GAAP → Non-GAAP reconciliation)
- [ ] *Supporting data tables:* Any tables moved from the main body for completeness (geographic splits, detailed reconciliations, minor segments)
