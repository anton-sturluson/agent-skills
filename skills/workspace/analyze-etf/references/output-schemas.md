# `analyze-etf` output schemas

## Classified holdings

Preferred schema:

```csv
fund,ticker,name,weight,weight_type,currency,category,secondary_category,confidence,theme_relevance,exclude_from_operating_distribution,notes,source_url,source_name,as_of_date
```

Minimum schema:

```csv
fund,ticker,name,weight,category,confidence,notes,source_url
```

Definitions:
- `weight`: source portfolio weight as percent of fund assets.
- `weight_type`: usually `percent_of_fund_assets`.
- `category`: one primary taxonomy category.
- `secondary_category`: optional explanatory tag; do not aggregate on this by default.
- `theme_relevance`: `direct`, `enabler`, `adjacent`, `generic/weak`, `non-operating`.
- `exclude_from_operating_distribution`: true for cash, FX, futures, derivatives, ETFs/funds, collateral, receivables/payables, and other non-operating rows.

## Category summary — wide

```csv
fund,{category_1},{category_2},...,direct_theme_ex_adjacent,operating_weight_covered_pct,excluded_weight_pct,top10_concentration_pct,holdings_count,operating_holdings_count,as_of_date
```

Category columns are normalized to operating-company weight unless explicitly labeled raw.

## Category summary — long

```csv
fund,category,normalized_weight_pct,raw_weight_pct,holdings_count,top_holdings,as_of_date
```

Use long format for audit and flexible charting.

## Candidate blends

```csv
blend,fund_weights,{category_1},{category_2},...,direct_theme_ex_adjacent_pct,weighted_top10_concentration_pct,notes
```

Example `fund_weights`: `ROBO:0.75;KOID:0.25`.

## Pair summary

```csv
pair,included_funds,excluded_funds,{pair_category_columns},pair_direct_theme_ex_adjacent_pct,pair_top10_concentration_pct,biggest_miss_category,biggest_miss_weight_pct,biggest_miss_name_count
```

## Pair misses by category

```csv
pair,miss_category,missed_weight_in_excluded_funds,missed_name_count,example_missed_companies
```

## Pair top misses

```csv
pair,missed_company,category,aggregate_weight_in_excluded_funds,excluded_fund_weights
```

`excluded_fund_weights` should be parseable, e.g. `KOID:2.26;BOTZ:0.41`.
