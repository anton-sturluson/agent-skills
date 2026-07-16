#!/usr/bin/env python3
"""Generate two-ETF pair summaries and miss analysis from classified holdings."""
from __future__ import annotations

import argparse
import csv
import glob
import itertools
import re
from collections import Counter, defaultdict
from pathlib import Path

NON_OPERATING_CATEGORY = "Cash / funds / derivatives / other"
META_COLUMNS = {
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
    "raw_total_weight_pct",
}


def truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}


def parse_weight(row: dict[str, str]) -> float:
    raw = str(row.get("weight", "")).replace("%", "").replace(",", "").strip()
    return float(raw) if raw else 0.0


def is_operating(row: dict[str, str]) -> bool:
    if truthy(row.get("exclude_from_operating_distribution")):
        return False
    return (row.get("category") or "").strip() != NON_OPERATING_CATEGORY


def canon(row: dict[str, str]) -> str:
    if row.get("canonical_name"):
        return row["canonical_name"].strip()
    s = (row.get("name") or row.get("ticker") or "").upper()
    s = re.sub(r"\b(INC|CORP|CORPORATION|CO|LTD|PLC|NV|AG|SA|SE|CLASS|SHS|HOLDINGS?|GROUP|LIMITED|ADR|COMMON|STOCK)\b", " ", s)
    s = re.sub(r"[^A-Z0-9]+", " ", s).strip()
    return re.sub(r"\s+", " ", s) or (row.get("ticker") or "UNKNOWN")


def read_classified(patterns: list[str]) -> dict[str, list[dict[str, str]]]:
    paths: list[Path] = []
    for pattern in patterns:
        matches = [Path(p) for p in glob.glob(pattern)]
        paths.extend(matches or [Path(pattern)])
    by_fund: dict[str, list[dict[str, str]]] = defaultdict(list)
    for path in paths:
        with path.open(newline="") as f:
            reader = csv.DictReader(f)
            required = {"fund", "ticker", "name", "weight", "category"}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise SystemExit(f"{path} missing required columns: {sorted(missing)}")
            for row in reader:
                row["_company"] = canon(row)
                row["_weight"] = parse_weight(row)
                if is_operating(row):
                    by_fund[row["fund"].strip()].append(row)
    return by_fund


def compute_summary(by_fund: dict[str, list[dict[str, str]]]) -> tuple[list[str], dict[str, dict[str, float]], dict[str, float]]:
    categories = sorted({r["category"].strip() for rows in by_fund.values() for r in rows})
    dist: dict[str, dict[str, float]] = {}
    top10: dict[str, float] = {}
    for fund, rows in by_fund.items():
        denom = sum(r["_weight"] for r in rows) or 1.0
        d = defaultdict(float)
        issuer_w = defaultdict(float)
        for r in rows:
            d[r["category"].strip()] += r["_weight"]
            issuer_w[r["_company"]] += r["_weight"]
        dist[fund] = {c: d[c] / denom * 100 for c in categories}
        top10[fund] = sum(sorted(issuer_w.values(), reverse=True)[:10])
    return categories, dist, top10


def parse_pairs(pairs: str | None, funds: list[str]) -> list[tuple[str, str]]:
    if not pairs:
        return list(itertools.combinations(funds, 2))
    out: list[tuple[str, str]] = []
    for part in pairs.split(","):
        if not part.strip():
            continue
        a, b = re.split(r"[/:+]", part.strip(), maxsplit=1)
        out.append((a.strip(), b.strip()))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", help="Classified CSV files or globs")
    ap.add_argument("-o", "--out-dir", required=True)
    ap.add_argument("--funds", help="Comma-separated serious ETF universe; defaults to all funds found")
    ap.add_argument("--pairs", help="Comma-separated pairs, e.g. ROBO/ROBT,ROBO/KOID. Defaults to all pairs")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    by_fund = read_classified(args.inputs)
    funds = [f.strip() for f in args.funds.split(",")] if args.funds else sorted(by_fund)
    missing = [f for f in funds if f not in by_fund]
    if missing:
        raise SystemExit(f"No classified rows for funds: {missing}")
    pairs = parse_pairs(args.pairs, funds)
    categories, dist, top10 = compute_summary({f: by_fund[f] for f in funds})

    fund_sets = {f: {r["_company"] for r in by_fund[f]} for f in funds}
    company_info: dict[str, dict] = {}
    for fund in funds:
        for row in by_fund[fund]:
            info = company_info.setdefault(row["_company"], {"company": row["_company"], "display": row.get("name") or row["_company"], "category": row["category"], "fund_weights": {}})
            info["fund_weights"][fund] = info["fund_weights"].get(fund, 0.0) + row["_weight"]
            if row["_weight"] >= max(info["fund_weights"].values()):
                info["display"] = row.get("name") or row["_company"]
                info["category"] = row["category"]

    pair_summary_rows = []
    miss_category_rows = []
    top_miss_rows = []
    md: list[str] = ["# Two-ETF Pair Miss Analysis\n", "*Generated from classified holdings. Missed means present in excluded serious ETFs and absent from both ETFs in the pair.*\n", "## Pair Summary\n", "| Pair | Pair shape | Biggest thing missed | Top-10 concentration |", "|---|---|---|---:|"]

    for a, b in pairs:
        included = [a, b]
        excluded = [f for f in funds if f not in included]
        pair_name = f"{a}/{b}"
        pair_set = fund_sets[a] | fund_sets[b]
        excluded_set = set().union(*(fund_sets[f] for f in excluded)) if excluded else set()
        missed = excluded_set - pair_set
        pair_mix = {c: (dist[a].get(c, 0.0) + dist[b].get(c, 0.0)) / 2 for c in categories}
        pair_top10 = (top10[a] + top10[b]) / 2

        miss_by_cat = defaultdict(float)
        miss_names_by_cat = defaultdict(list)
        miss_infos = []
        for company in missed:
            info = company_info[company]
            miss_weight = sum(info["fund_weights"].get(f, 0.0) for f in excluded)
            category = info["category"]
            miss_by_cat[category] += miss_weight
            miss_names_by_cat[category].append(info["display"])
            miss_infos.append((miss_weight, info))
        biggest_cat, biggest_weight = max(miss_by_cat.items(), key=lambda kv: kv[1], default=("None", 0.0))
        biggest_count = len(miss_names_by_cat.get(biggest_cat, []))

        pair_summary = {
            "pair": pair_name,
            "included_funds": ";".join(included),
            "excluded_funds": ";".join(excluded),
            "pair_top10_concentration_pct": round(pair_top10, 2),
            "biggest_miss_category": biggest_cat,
            "biggest_miss_weight_pct": round(biggest_weight, 2),
            "biggest_miss_name_count": biggest_count,
        }
        for c in categories:
            pair_summary[c] = round(pair_mix[c], 2)
        pair_summary_rows.append(pair_summary)

        shape = " / ".join(f"{c}: {pair_mix[c]:.0f}%" for c in categories[:3])
        md.append(f"| {pair_name} | {shape} | {biggest_cat} ({biggest_count} names; {biggest_weight:.1f}) | {pair_top10:.1f}% |")
        md.append(f"\n### {pair_name}\n")
        md.append(f"*Excluded funds:* {', '.join(excluded) or 'None'}. Missed companies: {len(missed)}.\n")
        md.append("| Miss category | Missed weight | Missed names | Examples |")
        md.append("|---|---:|---:|---|")
        for cat, weight in sorted(miss_by_cat.items(), key=lambda kv: -kv[1]):
            examples = "; ".join(miss_names_by_cat[cat][:8])
            md.append(f"| {cat} | {weight:.1f} | {len(miss_names_by_cat[cat])} | {examples} |")
            miss_category_rows.append({"pair": pair_name, "miss_category": cat, "missed_weight_in_excluded_funds": round(weight, 2), "missed_name_count": len(miss_names_by_cat[cat]), "example_missed_companies": examples})
        md.append("\n*Top missed companies:*")
        for weight, info in sorted(miss_infos, reverse=True, key=lambda x: x[0])[:20]:
            weights = ";".join(f"{f}:{info['fund_weights'][f]:.2f}" for f in excluded if f in info["fund_weights"])
            md.append(f"- {info['display']} — {info['category']} ({weights})")
            top_miss_rows.append({"pair": pair_name, "missed_company": info["display"], "category": info["category"], "aggregate_weight_in_excluded_funds": round(weight, 2), "excluded_fund_weights": weights})
        md.append("")

    pair_summary_path = out_dir / "pair-summary.csv"
    pair_fields = ["pair", "included_funds", "excluded_funds"] + categories + ["pair_top10_concentration_pct", "biggest_miss_category", "biggest_miss_weight_pct", "biggest_miss_name_count"]
    with pair_summary_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=pair_fields)
        w.writeheader(); w.writerows(pair_summary_rows)
    with (out_dir / "pair-miss-by-category.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["pair", "miss_category", "missed_weight_in_excluded_funds", "missed_name_count", "example_missed_companies"])
        w.writeheader(); w.writerows(miss_category_rows)
    with (out_dir / "pair-top-misses.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["pair", "missed_company", "category", "aggregate_weight_in_excluded_funds", "excluded_fund_weights"])
        w.writeheader(); w.writerows(top_miss_rows)
    (out_dir / "pair-miss-analysis.md").write_text("\n".join(md))
    print(f"Wrote pair analysis files to {out_dir}")


if __name__ == "__main__":
    main()
