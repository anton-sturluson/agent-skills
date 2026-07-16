---
name: research-evidence
description: Build, plan, collect, and audit durable company evidence bases before business analysis. Use when initializing or reusing a company evidence tree, collecting SEC and external sources, planning evidence work from relevant research dimensions, saving or registering evidence, running brainstorm with subagents to challenge the evidence base, building source-grounded datasets, or filling research gaps before synthesis.
---

# research-evidence

Build the evidence base for serious company analysis.

The job is durable, verifiable evidence: saved sources, clear provenance, useful structured data when needed, and an honest audit of what is strong, thin, missing, low-quality, or blocked.

## Principles

### 1. Work backward from the analysis question

Evidence collection serves the analysis that follows. Use the bundled research-dimensions reference as a lens for deciding what evidence matters, not as a checklist to march through.

### 2. Source quality beats source count

A pile of weak sources is not a strong evidence base. Prefer primary sources, official statistics, regulator data, company filings, counterparty materials, reputable industry sources, and clearly sourced expert analysis. Be especially strict on industry and market data: unsourced TAM claims, SEO pages, content farms, generic market-size snippets, and circularly cited consultant summaries are weak evidence.

### 3. Test management narrative against outside reality

Company materials are a baseline, not a conclusion. Test claims that matter against competitors, customers, suppliers, counterparties, regulators, industry structure, and independent external views.

### 4. Investigate the whole system, not just the company

A company's economics live inside a system. Map competitors by segment, ecosystem actors, customer concentration, supplier dependence, channel structure, bargaining power, and regulatory exposure where they materially affect the analysis.

### 5. Triangulate the claims that drive judgment

Single-source claims are fragile. For claims that move the conclusion, seek at least one independent corroborating or disconfirming source before relying on them.

### 6. Absence of evidence is itself evidence

What management does not disclose, what peers do not match, what no third party can verify — these are signals. Record them rather than skipping past them.

### 7. Evidence must survive the session

Important evidence should be saved as individual local files, registered, and made durable. Another agent should be able to verify important claims without relying on chat history. Register each source in the company evidence ledger (use `minerva evidence add-source --root <company-root> --title ... --category ... --status downloaded --path ...`).

### 8. Weak evidence stays visibly weak

If a dimension is thin, missing, blocked, or supported only by low-quality sources, say so plainly. Do not launder weak evidence into confidence because the folder looks busy.

## Primitives

The skill exists to encourage three core moves. Use them deliberately, not as ritual.

### 1. Plan from research dimensions

Before serious collection, check `hard-disk/data/01-portfolio/current/company-directory.md` for filing jurisdiction, transcript sources, IR pages, and any supplemental IR materials listed for the company. If supplemental materials exist (shareholder letters, owners' manuals, etc.), include them in the collection plan. Then read `{baseDir}/references/research-dimensions.md` and decide:

- which dimensions matter most for this company
- what evidence would actually change the analysis
- which competitors, customers, suppliers, and ecosystem actors must be mapped
- which high-quality source types are likely to close the biggest gaps
- where management framing or low-quality market data is the main risk
- what should be split across subagents

For deep dives, write the plan into the company tree before collecting. Naming the plan is half the work.

### 2. Brainstorm with subagents

Once there is enough evidence to be challenged, deploy `brainstorm` subagents to attack the evidence base, not the thesis. Save brainstorm output files under the company's `analysis/` folder. Subagents should read the actual evidence base, not a summary, and surface:

- missing dimensions and missing actors
- weak grounding and single-source claims
- overreliance on management framing
- untested customer, competitor, supplier, or counterparty claims
- disconfirming evidence the agent has not yet looked for
- where the evidence quietly assumes the conclusion

Treat their critique as input to the next plan, not decoration on the current one.

### 3. Iterate

The first plan is a hypothesis. The expected rhythm is:

```text
plan → collect → brainstorm → revise plan → collect again
```

Stop when remaining gaps are immaterial, repetitive, genuinely blocked, or clearly disclosed in the handoff. Do not stop because the folder looks busy. New evidence, weak grounding, or brainstorm critique should reshape the plan rather than be filed as trivia.

## Handoff

End with a compact handoff that makes the next analysis pass easier:

- active company root
- important sources or datasets added
- strongest evidence areas
- thin, missing, low-quality, or blocked areas
- brainstorm findings that changed the plan, if brainstorm was used
- weakly grounded claims that should not be overstated
- recommended next collection step, if any
- readiness judgment for serious analysis

Do not hide uncertainty behind activity. If evidence quality is weak, say so plainly.
