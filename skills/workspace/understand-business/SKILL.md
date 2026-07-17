---
name: "understand-business"
description: "Build a comparable, evidence-backed five-year structural understanding of any business."
user_invocable: true
argument: "<ticker> [--years 5]"
---

# understand-business

Build a durable structural understanding of a business over up to five years. Produce a business-understanding report with a light expectations-based valuation, not a buy/sell/hold call.

## References

- Report specification and completion check: `references/checklist.md`
- Evidence-subagent contract: `references/extraction-brief.md`
- Main-agent audit procedure: `references/audit.md`
- Munger's psychology checklist: `references/bias-definitions.md`

## Workflow

### 1. Resolve the company and source set

Read `hard-disk/data/01-portfolio/current/company-directory.md`. If no company folder exists, use `initialize-company`. Reuse existing evidence.

Collect up to five years of annual filings or local equivalents, the latest governance or compensation filing, financial history, and relevant full-year transcripts. Add investor materials, regulatory data, or industry sources only where they answer a material question. Include an offering document for a young company when available.

### 2. Tailor the report scope

Read `references/checklist.md`. Decide which metrics and questions are economically applicable before extraction. Do not force industrial-company measures onto banks, insurers, REITs, early-stage companies, or other businesses where they mislead. Mark an item inapplicable only with a short reason and substitute the economically correct question where possible.

Analyze the business before looking at the market price. This sequencing reduces anchoring: price should not influence the assessment of demand, economics, management, durability, or risk. Introduce price only when the structural analysis reaches Valuation.

### 3. Build the metrics spine

Delegate `data/structured/longterm-metrics.md`. This is the complete, reusable financial dataset—not a report-ready table. Split tables by category for readability. Use reported or directly derivable figures and state formulas. Cover:

- scale and mix: revenue or sector equivalent, growth, segments, geography
- profitability: reported earnings and margins or sector equivalents
- cash economics: CFO, capex, and FCF where meaningful
- returns: ROIC, ROE, ROTCE, or the measure that matches the capital model
- ownership and resilience: diluted shares, cash and debt or sector solvency, and material obligations
- a small number of sector-specific operating metrics

Treat acquisitions, buybacks, R&D capitalization, SBC, pensions, leases, and other adjustments as conditional modules only when material. Mark unavailable or inapplicable figures explicitly; do not invent comparability.

### 4. Extract evidence in parallel

Assign narrow, non-overlapping topics from the applicable checklist sections. Give every evidence subagent `references/extraction-brief.md` unchanged plus its topic, scope questions, source paths, lookback, and output path.

Typical topics include business and demand, revenue and profit anatomy, returns and capital allocation, competitive position, value chain and dependencies, management and incentives, balance-sheet resilience, and downside mechanisms. Combine or omit topics when immaterial; do not spawn a fixed set merely because it is listed here.

Save briefs to `research/understand-business/{date}/{topic}.md`.

### 5. Write the report

Read the metrics spine and evidence briefs. Follow `references/checklist.md` section by section. The main agent owns interpretation and checks primary sources where evidence is thin, contradictory, or load-bearing.

Treat the Opening Financial Snapshot as a compact view into the metrics spine: select only the decision-relevant endpoints and trends, cross-reference the full spine, and do not reproduce it. Put each fact in the home section assigned by the checklist and cross-reference rather than restate it.

Save to `analysis/{company}-understanding.md`.

### 6. Complete the checklist

Reread `references/checklist.md` against the draft. Mark each item complete, inapplicable with a reason, or an unresolved evidence gap. Fix material failures only when evidence supports the change; do not manufacture completeness.

### 7. Audit and revise

Read and follow `references/audit.md`.

### 8. Format, render, and inspect

Apply the shared `format-report` skill and render the PDF alongside the Markdown. Its structural, table, rendering, and visual-inspection rules are authoritative. Preserve this skill's report-specific acceptance test below.

## Outputs

- Report: `{company}/analysis/{company}-understanding.md`
- Metrics spine: `{company}/data/structured/longterm-metrics.md`
- Evidence briefs: `{company}/research/understand-business/{date}/{topic}.md`
- Audit and dispositions: `{company}/audits/understanding-audit.md`

Acceptance test: a regular investor can explain how the business earns money, compare its financial profile with another company, identify what sustains the economics, name the conditions that would impair it, and state what growth and operating performance the current price implies.
