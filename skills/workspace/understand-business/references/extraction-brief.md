# Evidence Extraction Subagent Contract

Give this file unchanged to each evidence subagent, together with one assigned topic, scope questions, source paths, lookback, and output path.

## Boundary

Extract only facts needed for the assigned topic. Do not write analysis, a thesis, ratings, recommendations, or valuation. Do not rebuild the metrics spine unless a scope question explicitly asks for a source check. If evidence belongs mainly to another topic, note the handoff rather than developing a second brief.

## Method

1. Survey the available annual filings or local equivalents, governance filings, transcripts, investor materials, and structured data. Confirm the source set rather than assuming a glob is complete.
2. Use Minerva bulk extraction for breadth and direct reading for verification, footnotes, contradictions, and thin results. Follow cross-references and narrow the search until each scope question is answered or shown to be unanswerable.
3. Prefer primary evidence. Use secondary or management sources only when primary evidence is unavailable or the source itself is relevant.
4. Deduplicate repeated disclosures. State what remained stable, what changed, and when.

## Output

Write one compact brief with:

- **Findings:** facts organized by the assigned scope questions
- **Change Over Time:** material changes across the lookback
- **Contradictions and Definitions:** conflicting disclosures, changed metrics, or non-comparable terms
- **Evidence Gaps:** undisclosed, not derivable, or inapplicable items
- **Sources:** direct citations sufficient for one-click verification

Use tables only when they clarify a time series or comparison; order years oldest to newest. Label reported and derived figures and state formulas. Do not infer missing values.

## Acceptance test

The main agent can answer the assigned questions from this brief without re-reading every source, can verify load-bearing facts quickly, and can see exactly what remains uncertain without the subagent's opinion coloring the evidence.
