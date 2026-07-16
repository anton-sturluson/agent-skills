# ETF holdings taxonomy template

Use this file when creating `category-analysis/taxonomy.md` for a new ETF theme.

## Design rules

- Make the taxonomy specific to the thesis, not to ETF marketing.
- Use one primary category per holding for aggregation.
- Classify by current revenue/profit economics, not press releases or fund narratives.
- Add `theme_relevance`: `direct`, `enabler`, `adjacent`, `generic/weak`, or `non-operating`.
- Add `confidence`: `high`, `medium`, or `low`.
- Keep generic exposure separate from direct theme exposure.
- Always include `Cash / funds / derivatives / other`.

## Suggested category pattern

Adapt names to the theme.

| Category | Definition | Theme relevance default | Examples / notes |
|---|---|---|---|
| Core producers / direct operators | Companies whose main economics directly come from producing or operating the target product/service | direct | In robotics: robot producers, automation systems, surgical robots |
| Critical components / supply chain | Scarce or important physical/digital inputs into the target system | enabler | In robotics: reducers, actuators, sensors, bearings, connectors |
| Infrastructure / compute / enabling hardware | Compute, chips, networks, infrastructure, or hardware platforms enabling deployment | enabler | Split generic infrastructure from truly theme-specific infrastructure when needed |
| Theme-specific software / platforms | Software that directly runs, designs, simulates, orchestrates, secures, or monetizes the target system | direct/enabler | In robotics: autonomy stack, simulation, CAD/PLM, robot fleet orchestration, machine vision software |
| Generic AI/software/cloud/cyber | Broad software/AI/cyber/cloud exposure without a specific theme pathway | generic/weak | Do not merge into direct software unless evidence supports it |
| End-user / adjacent platforms | Companies adopting the theme or adjacent beneficiaries rather than suppliers | adjacent | In robotics: Tesla/EVs, Amazon/logistics, platform companies |
| Cash / funds / derivatives / other | Cash, FX, receivables/payables, futures, swaps, options, ETFs/funds, collateral, irrelevant securities | non-operating | Exclude from operating-company distributions |

## Software-purity rule

If a fund looks attractive because of software exposure, inspect the top software names. Default cybersecurity, observability, generic cloud, databases, networking, enterprise workflow, and broad AI apps to `Generic AI/software/cloud/cyber` unless there is specific evidence of direct theme software exposure.

Direct or theme-enabling software usually includes:
- autonomy or control stacks,
- simulation/digital twin/CAD/PLM/EDA relevant to the theme,
- fleet orchestration,
- embedded/edge deployment software,
- industrial automation software,
- mapping/perception/machine-vision software,
- domain-specific data/AI platform with clear theme use.

## Classification fields

Recommended CSV fields:

```csv
fund,ticker,name,weight,weight_type,currency,category,secondary_category,confidence,theme_relevance,exclude_from_operating_distribution,notes,source_url,source_name,as_of_date
```

Minimum acceptable fields:

```csv
fund,ticker,name,weight,category,confidence,notes,source_url
```
