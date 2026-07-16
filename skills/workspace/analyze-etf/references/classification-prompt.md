# Per-ETF classification subagent prompt

Use this pattern when spawning one subagent per ETF.

```text
Classify {FUND} ETF holdings for the {THEME} ETF analysis.

Inputs:
- Taxonomy: {ABSOLUTE_PATH_TO_TAXONOMY_MD}
- Holdings source: {OFFICIAL_OR_REPUTABLE_SOURCE_URL_OR_FILE}
- Output folder: {ABSOLUTE_PATH_TO_CATEGORY_ANALYSIS}/subagent-outputs/

Instructions:
1. Fetch or read full holdings from the source. Prefer official sponsor data when possible.
2. Preserve source weights as percentages of fund assets, e.g. 2.48 not 0.0248.
3. Preserve or record source URL, source name, holdings as-of date, retrieval date, and caveats.
4. Keep cash, FX, futures, swaps, options, ETFs/funds, collateral, receivables/payables, and other non-operating rows in the CSV; mark them `Cash / funds / derivatives / other` and `exclude_from_operating_distribution=true` if that column exists.
5. Assign exactly one primary category per operating holding using the taxonomy.
6. Classify by current business economics, not ETF marketing or press releases.
7. For software names, distinguish direct theme software from generic AI/cloud/cyber/enterprise software.
8. Flag low-confidence or ambiguous classifications, especially holdings above ~1% weight.
9. Write classified CSV to `{fund-lower}-classified.csv`.
10. Write short notes to `{fund-lower}-notes.md`, including source quality, holdings date, weight reconciliation, ambiguous names, top category weights, and caveats.

CSV columns, preferred:
fund,ticker,name,weight,weight_type,currency,category,secondary_category,confidence,theme_relevance,exclude_from_operating_distribution,notes,source_url,source_name,as_of_date

CSV columns, minimum acceptable if the source is sparse:
fund,ticker,name,weight,category,confidence,notes,source_url

Do not make a final ETF recommendation. Classification only.
```

## Main-agent review after subagents

After subagents finish:
- Check every CSV has required columns.
- Reconcile weight sums.
- Compare holdings dates.
- Review high-weight low/medium confidence rows.
- Audit category labels that could mislead the conclusion.
- Normalize issuer/entity names before overlap, concentration, and pair-miss work.
