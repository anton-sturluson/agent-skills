---
name: analyze-business
description: Use when asked to analyze a company/business and produce a deep-dive report.
---

# analyze-business

Turn collected evidence into an investment deep dive the reader can audit and act on.

## Principles

1. Translate the business into plain language — where does the money come from, who pays, why, and what keeps them paying
2. Find the few variables that actually drive long-term value — three to five things that move outcomes over years; everything else is texture
3. Use the outside view first — start from base rates before accepting the story of why this one is different
4. Take the system seriously, not just the company — competitors, customers, suppliers, regulators, bargaining power, dependencies
5. Anchor load-bearing claims in primary evidence — filings, transcripts, regulator data, independent sources; management materials are inputs, not conclusions; see shared AGENTS.md for citation rules
6. Resist neat narratives — if every fact aligns and every flywheel reinforces, the work hasn't pressed hard enough
7. End with a monitorable judgment — thesis in one paragraph, variables to watch, disconfirming conditions, explicit recommendation

## Workflow

Five phases, plus a final pitch step. Not rigid gates — use judgment to move between them. Runs up to N rounds (default 2, user-configurable). If round N still triggers a loop-back, flag the gap in the report rather than blocking.

### Phase 1 — Orient and plan

Read the company's wiki pages, important zettels, and collected evidence. Compare evidence state against `{baseDir}/references/deep-dive-checklist.md`

Write a plan to `plans/{NN}-plan-{company}-deep-dive.md` inside the company's evidence tree:
- Evidence assessment mapped against checklist sections
- Topic assignments for each specialist, adapted to the company
- Which topics should overlap between specialists for alignment through disagreement
- Evidence gaps flagged

On loop-back rounds, revise the plan based on brainstorm feedback — topics may shift, new dimensions may be added

### Phase 2 — Specialist analysis

Use the `brainstorm` skill to write analysis to `analysis/specialist-{name}/`. Do not prime agents with their own framework concepts. Give them their assigned topics and the company context. If prior brainstorm findings exist, reference them as context

Specialists should read existing analysis documents in the company's evidence tree (prior deep dive versions, structured data files, research artifacts) before producing their own work — build on what exists rather than duplicating it

Specialist output must contain original analysis that extends or deepens what exists — calculations, models, reasoning chains, not summaries of wiki content

#### Topics

The plan assigns topics based on what matters for this business. Overlaps between specialists on the same topic are deliberate — the disagreement is the insight

The following are exemplary topics per specialist. Expand, substitute, or add topics depending on the focus area of the business:

| Specialist | Core topics |
|---|---|
| Charlie Buffet | Business model and economics, moat analysis, management candor assessment and one-dollar test, capital allocation record, pricing power evidence, customer concentration, franchise vs commodity classification, owner earnings vs reported earnings, insider alignment |
| Mauboussin | ROIC decomposition (total, incremental, by segment), reverse-DCF/price-implied expectations, base rate analysis with reference class persistence and fade rates, probability-weighted scenario model, unit economics and cohort analysis, TAM sizing and market share trajectory, threshold margin calculation, lifecycle stage classification, M&A value creation analysis |
| Taleb | Fragility map with ruin path transmission mechanisms, payoff structure analysis, hidden leverage inventory, skin-in-the-game audit of insider behavior and incentive structure, reflexive feedback loops, regulatory/political tail risk, technology obsolescence risk, liquidity and refinancing fragility |
| Christensen | Disruption risk assessment, jobs-to-be-done for the company's customers, organizational capability analysis, value chain integration-modularity dynamics, platform economics and multi-sided market dynamics, competitive response prediction, adjacent market entry risk, regulatory moat vs innovation moat, channel strategy and distribution evolution |

### Phase 3 — Deep dive synthesis

Read all specialist outputs plus wiki structure notes. Specialist work substitutes for raw evidence in their domain

Write the deep dive as `analysis/{company}-deep-dive-v{N}.md` — versioned, increment if prior versions exist. Overwrite if this is the loop-back step. Use the checklist as spine but let the structure serve the argument

Where specialists disagree, surface the disagreement inline within the relevant topic. Make a judgment call with reasoning, or preserve the tension explicitly. Never average, never omit

One coherent document, not stapled specialist sections

### Phase 4 — Brainstorm validation

Run `brainstorm` against the synthesized deep dive. Specialists should also audit the deep dive against the checklist — flag any items that are thin, missing, or inadequately addressed. Validation output at most 10K characters per specialist

Loop-back when brainstorm results show a clear gap in the analysis: wrong question about the business, missing critical dimension, thesis-invalidating evidence, or irreconcilable disagreement papered over. Otherwise move to Phase 5

### Phase 5 — Revision and completion

Incorporate feedback via targeted edits. During revision, guard against unnecessary verbosity. On loop-back, return to Phase 1 with brainstorm findings as context

### Final step — Stock pitch

Once the deep dive is complete, prepend a concise stock pitch at the top of the document. A great pitch can be delivered in one minute: the business in a sentence, why it matters now, the key variables, the recommendation, and what breaks it. This is the last thing written, after the full analysis is done.

## Completion

The final report must be a well-written, concise, readable investment memo — not a checklist dump. Compress minor items, expand the ones that drive the judgment

Acceptance gates:
- Every checklist item answered directly, compressed, marked immaterial, or marked unknown with the gap named
- Specialist analysis was the primary analytical surface
- Checklist was audited during brainstorm validation
- Load-bearing claims have inline citations
- Stock pitch prepended at the top
- Plan file was written before analysis began
- After the Markdown deep dive is fully written, apply the shared `format-report` skill and render the HTML next to it. Its structural, table, rendering, and visual-inspection rules are authoritative.
