# Table Formatting

Use Pandoc fenced divs to assign size and profile classes to a Markdown table. Leave a blank line between the div markers and the table:

```markdown
::: {.table-compact .profile-time-series}

| Metric | 2022 | 2023 | 2024 |
|:--|--:|--:|--:|
| Revenue (\$m) | 100 | 112 | 125 |

:::
```

## Size classes

Choose the least compressed class that fits cleanly.

- No class: normal tables with few columns and short labels.
- `table-compact`: moderate tables that need slightly tighter spacing.
- `table-dense`: wide financial or operating tables with many columns.
- `table-micro`: exceptional cases only. Restructure or split the table before using it.

Never use compression to preserve a table that should be divided into two coherent tables.

## Profiles

- `profile-financial-wide`: wide financial statements or metric tables. Use tabular numerals and keep numeric cells on one line.
- `profile-time-series`: chronological columns. Order oldest to newest and keep period headings on one line.
- `profile-comparison`: side-by-side company, segment, scenario, or product comparisons. Keep comparison dimensions consistent across columns.

Combine one size class with at most one profile unless a second profile clearly adds non-conflicting behavior.

## Content rules

- Escape literal currency dollar signs as `\$` so Pandoc does not parse text across table rows as inline math.
- State scale and currency once: for example, `Revenue (\$m)` or `All figures in USD millions`.
- Use one precision convention within a table.
- Left-align labels and align comparable numeric values consistently.
- Distinguish zero, unavailable, and not meaningful; do not use `0` for missing data.
- Keep source notes outside the table unless row-level sourcing is necessary.
- Put the table near the paragraph that introduces it.
- Explain the decision-relevant pattern immediately after the table.
