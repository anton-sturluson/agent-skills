#!/usr/bin/env python3
"""Aggregate classified ETF holdings into category distribution summaries.

Input classified CSVs must include at least: fund,ticker,name,weight,category.
Optional fields: exclude_from_operating_distribution,theme_relevance,as_of_date,canonical_name.
"""
from __future__ import annotations

import argparse
import csv
import glob
import re
from collections import defaultdict
from pathlib import Path

NON_OPERATING_CATEGORY = "Cash / funds / derivatives / other"
KNOWN_META = {
    "fund",
    "direct_theme_ex_adjacent",
    "direct_theme_ex_adjacent_pct",
    "operating_weight_covered_pct",
    "excluded_weight_pct",
    "top10_concentration",
    "top10_concentration_pct",
    "holdings_count",
    "operating_holdings_count",
    "as_of_date",
}


def truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}


def canonical_company(row: dict[str, str]) -> str:
    if row.get("canonical_name"):
        return row["canonical_name"].strip()
    name = (row.get("name") or row.get("ticker") or "").upper()
    name = re.sub(r"\b(INC|CORP|CORPORATION|CO|LTD|PLC|NV|AG|SA|SE|CLASS|SHS|HOLDINGS?|GROUP|LIMITED|ADR|COMMON|STOCK)\b", " ", name)
    name = re.sub(r"[^A-Z0-9]+", " ", name).strip()
    return re.sub(r"\s+", " ", name) or (row.get("ticker") or "UNKNOWN")


def read_rows(patterns: list[str]) -> list[dict[str, str]]:
    paths: list[Path] = []
    for pattern in patterns:
        matches = [Path(p) for p in glob.glob(pattern)]
        paths.extend(matches or [Path(pattern)])
    rows: list[dict[str, str]] = []
    for path in paths:
        with path.open(newline="") as f:
            reader = csv.DictReader(f)
            required = {"fund", "ticker", "name", "weight", "category"}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise SystemExit(f"{path} missing required columns: {sorted(missing)}")
            for row in reader:
                row["_source_file"] = str(path)
                rows.append(row)
    return rows


def is_operating(row: dict[str, str]) -> bool:
    if truthy(row.get("exclude_from_operating_distribution")):
        return False
    return (row.get("category") or "").strip() != NON_OPERATING_CATEGORY


def parse_weight(row: dict[str, str]) -> float:
    raw = str(row.get("weight", "")).replace("%", "").replace(",", "").strip()
    return float(raw) if raw else 0.0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", help="Classified CSV files or globs")
    ap.add_argument("-o", "--out-dir", required=True, help="Output directory")
    ap.add_argument("--direct-relevance", default="direct,enabler", help="theme_relevance values counted as direct_theme_ex_adjacent")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = read_rows(args.inputs)
    direct_values = {x.strip().lower() for x in args.direct_relevance.split(",") if x.strip()}

    by_fund: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_fund[row["fund"].strip()].append(row)

    categories = sorted({r["category"].strip() for r in rows if r.get("category") and r["category"].strip() != NON_OPERATING_CATEGORY})
    wide_rows: list[dict[str, object]] = []
    long_rows: list[dict[str, object]] = []

    for fund, fund_rows in sorted(by_fund.items()):
        weighted_rows = [(r, parse_weight(r)) for r in fund_rows]
        total_weight = sum(w for _, w in weighted_rows)
        operating = [(r, w) for r, w in weighted_rows if is_operating(r)]
        excluded = [(r, w) for r, w in weighted_rows if not is_operating(r)]
        operating_weight = sum(w for _, w in operating)
        excluded_weight = sum(w for _, w in excluded)
        denom = operating_weight or 1.0

        by_category = defaultdict(float)
        by_category_count = defaultdict(int)
        by_category_names: dict[str, list[tuple[float, str]]] = defaultdict(list)
        issuer_weight = defaultdict(float)
        direct_weight = 0.0
        as_of_dates = sorted({r.get("as_of_date", "").strip() for r, _ in weighted_rows if r.get("as_of_date")})

        for row, weight in operating:
            category = row["category"].strip()
            by_category[category] += weight
            by_category_count[category] += 1
            by_category_names[category].append((weight, row.get("name") or row.get("ticker") or ""))
            issuer_weight[canonical_company(row)] += weight
            relevance = (row.get("theme_relevance") or "").strip().lower()
            if relevance in direct_values or (not relevance and category != NON_OPERATING_CATEGORY):
                direct_weight += weight

        top10 = sum(sorted(issuer_weight.values(), reverse=True)[:10])
        wide: dict[str, object] = {"fund": fund}
        for category in categories:
            wide[category] = round(by_category[category] / denom * 100, 2)
        wide.update(
            {
                "direct_theme_ex_adjacent": round(direct_weight / denom * 100, 2),
                "operating_weight_covered_pct": round(operating_weight, 2),
                "excluded_weight_pct": round(excluded_weight, 2),
                "top10_concentration_pct": round(top10, 2),
                "holdings_count": len(fund_rows),
                "operating_holdings_count": len(operating),
                "as_of_date": ";".join(as_of_dates),
                "raw_total_weight_pct": round(total_weight, 2),
            }
        )
        wide_rows.append(wide)

        for category in categories:
            top_names = "; ".join(name for _, name in sorted(by_category_names[category], reverse=True)[:5])
            long_rows.append(
                {
                    "fund": fund,
                    "category": category,
                    "normalized_weight_pct": round(by_category[category] / denom * 100, 2),
                    "raw_weight_pct": round(by_category[category], 2),
                    "holdings_count": by_category_count[category],
                    "top_holdings": top_names,
                    "as_of_date": ";".join(as_of_dates),
                }
            )

    wide_path = out_dir / "category-distribution-summary.csv"
    wide_fields = ["fund"] + categories + [
        "direct_theme_ex_adjacent",
        "operating_weight_covered_pct",
        "excluded_weight_pct",
        "top10_concentration_pct",
        "holdings_count",
        "operating_holdings_count",
        "as_of_date",
        "raw_total_weight_pct",
    ]
    with wide_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=wide_fields)
        writer.writeheader()
        writer.writerows(wide_rows)

    long_path = out_dir / "category-distribution-long.csv"
    with long_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["fund", "category", "normalized_weight_pct", "raw_weight_pct", "holdings_count", "top_holdings", "as_of_date"])
        writer.writeheader()
        writer.writerows(long_rows)

    print(f"Wrote {wide_path}")
    print(f"Wrote {long_path}")


if __name__ == "__main__":
    main()
