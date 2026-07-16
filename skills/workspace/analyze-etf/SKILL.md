---
name: analyze-etf
description: Analyze thematic or sector ETFs from holdings-level evidence. Use when comparing ETFs, choosing a core/satellite ETF allocation, evaluating ETF theme purity, classifying ETF holdings by value-chain exposure, producing ETF landscape/comparison rankings, generating category-distribution charts, or analyzing what ETF pairs/blends miss.
---

# Analyze ETF

## Purpose

Use this skill to turn “which ETF(s) best express this thesis?” into a holdings-grounded recommendation. Do not trust ETF names, index marketing, or broad category labels; classify what the fund actually owns and ask what an allocation owns, misses, duplicates, and overpays for.

## Core workflow

1. **Define the thesis and universe**
   - State the exposure Anton wants: producers, suppliers, software, infrastructure, geography, income, factor, etc.
   - Identify obvious ETFs plus contextual near-misses.
   - Create a numbered research folder under `hard-disk/research/{NN}-{theme-slug}/` and maintain `INDEX.md` files.

2. **Build `etf-landscape.md`**
   - Capture ticker, fund name, issuer, AUM, expense ratio, launch date, holdings count, top holdings, top-10 concentration, strategy/index, geography, valuation proxy, liquidity, and holdings date.
   - Add a plain-English note for each ETF: “what you are actually buying.”

3. **Build `etf-comparison-rankings.md`**
   - Compare cost, concentration, breadth, liquidity, valuation, performance, geography, theme purity, overlap with existing holdings, and use-case fit.
   - Include short verdicts after ranking tables. The verdict matters more than the rank.

4. **Collect full holdings**
   - Prefer official sponsor holdings files/pages. Save source URL, source type, retrieval timestamp, holdings `as_of_date`, raw file when useful, and parsing caveats.
   - Reconcile raw weights before analysis; normally expect roughly 99–101% of fund assets.

5. **Create a theme taxonomy**
   - Start from `{baseDir}/references/taxonomy-template.md` and adapt to the thesis.
   - Use one primary category per holding, based on current business economics.
   - Include `Cash / funds / derivatives / other`.
   - Separate direct exposure from generic/adjacent exposure. For software-heavy themes, split true theme software from generic cloud/cyber/enterprise AI.

6. **Classify holdings**
   - For large universes, spawn one subagent per ETF using `{baseDir}/references/classification-prompt.md`.
   - Require each subagent to write `{fund}-classified.csv` and `{fund}-notes.md` under `category-analysis/subagent-outputs/`.
   - Main agent owns taxonomy review, cross-ETF synthesis, charts, pair/blend analysis, and recommendation.

7. **Consolidate category distributions**
   - Use `scripts/consolidate_categories.py` or equivalent logic.
   - Exclude cash/FX/futures/derivatives/fund rows from operating-company distributions but keep them in reconciliation.
   - Report category mix, direct-theme exposure, operating coverage, excluded weight, holdings count, and top-10 concentration.

8. **Generate charts**
   - Use `scripts/plot_category_mix.py` to create stacked category bars plus top-10 concentration and donut small multiples.
   - Export PNG for reports, JPG for Slack if needed, and PDF for review.

9. **Analyze blends and pair misses**
   - Model only meaningful allocation hypotheses, not every possible ratio.
   - Use `scripts/analyze_pairs.py` for narrowed candidate sets.
   - Pair-miss analysis should answer: “If we choose this pair/blend, what categories and companies from the serious comparison universe do we leave out?”

10. **Recommend an allocation**
   - Use a core/satellite frame when appropriate.
   - State the recommended allocation, why it fits the thesis, what it underweights, when it would change, and which ETFs to avoid or treat only as context.

## Validation gates

Do not present conclusions until these are handled or explicitly marked provisional:

- **Source gate:** every ETF has source URL, source type, as-of date, retrieval date, and parsed holdings.
- **Weight gate:** total listed weight reconciles; operating-company denominator is explicit.
- **Freshness gate:** holdings dates are comparable; warn if materially stale or mismatched.
- **Entity gate:** ADRs, local listings, share classes, and duplicates are normalized for overlap/concentration.
- **Taxonomy gate:** category definitions are explicit and generic exposure is not mislabeled as direct theme exposure.
- **Confidence gate:** low-confidence/high-weight classifications are reviewed.
- **Software-purity gate:** if software exposure drives the recommendation, list top software names and label them direct, enabling-but-generic, or adjacent.
- **Concentration gate:** top-10/top-5/single-name concentration is calculated on normalized issuer/company exposure.
- **Miss gate:** pair/blend misses are interpreted; not every missed company is desirable.

## Standard outputs

Create this structure unless the task is explicitly lightweight:

```text
hard-disk/research/{NN}-{theme-slug}/
├── INDEX.md
├── etf-landscape.md
├── etf-comparison-rankings.md
├── category-analysis/
│   ├── INDEX.md
│   ├── taxonomy.md
│   ├── category-distribution-analysis.md
│   ├── category-distribution-summary.csv
│   ├── category-distribution-long.csv
│   ├── candidate-blend-summary.csv
│   ├── pair-miss-analysis.md
│   ├── pair-top-misses.csv
│   ├── pair-summary.csv
│   ├── pair-miss-by-category.csv
│   ├── charts/INDEX.md
│   └── subagent-outputs/INDEX.md
└── sources/INDEX.md          # optional when many raw downloads accumulate
```

Optional deeper work: `company-universe-by-category.md` and financial batches, but those are not required for ETF selection.

## Bundled resources

- `references/taxonomy-template.md` — taxonomy design and relevance rules.
- `references/classification-prompt.md` — prompt pattern for per-ETF classification subagents.
- `references/output-schemas.md` — CSV schemas and column definitions.
- `assets/*.md` — markdown templates for common reports.
- `scripts/consolidate_categories.py` — aggregate classified holdings into category summaries.
- `scripts/analyze_pairs.py` — compute pair summaries, misses by category, and top missed companies.
- `scripts/plot_category_mix.py` — generate category/concentration charts.

## Judgment posture

Numbers and charts are inputs to judgment, not the answer. Always distinguish:

1. what the ETF owns,
2. what category labels imply,
3. what exposure Anton actually gets,
4. what the chosen allocation misses.
