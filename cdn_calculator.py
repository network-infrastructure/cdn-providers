#!/usr/bin/env python3
"""
CDN Providers Directory & Monthly Bandwidth Cost Calculator CLI
Zero-dependency CLI tool to compare 38+ active CDN providers, calculate monthly
egress + HTTP request bills across 1 TB to 500 TB+, inspect free tier restrictions,
and update partner/affiliate URLs across all documentation files.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parent
PROVIDERS_PATH = ROOT_DIR / "providers.json"
SYNC_FILES = [
    ROOT_DIR / "README.md",
    ROOT_DIR / "llms.txt",
    ROOT_DIR / "docs" / "llms.txt",
    *sorted((ROOT_DIR / "docs").glob("*.html")),
    *sorted((ROOT_DIR / "guides").glob("*.md")),
]


def load_data() -> Dict[str, Any]:
    with PROVIDERS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def estimate_monthly_cost(
    provider: Dict[str, Any],
    volume_tb: float,
    requests_millions: float = 10.0,
    region: str = "na-eu",
) -> float:
    """
    Estimate monthly CDN cost (USD) for a given traffic volume in TB (1 TB = 1,000 GB),
    monthly HTTP/HTTPS requests in millions, and region profile ('na-eu', 'asia', 'global').
    """
    if volume_tb <= 0:
        return float(provider.get("min_monthly_usd", 0.0))

    rate_key = {
        "na-eu": "rate_na_eu_gb",
        "asia": "rate_asia_gb",
        "global": "rate_global_blended_gb",
    }.get(region, "rate_na_eu_gb")

    # If the requested volume matches a pre-verified tier benchmark on NA/EU with default requests,
    # and the provider uses tiered volume discounts, blend smoothly or use exact formula.
    free_tb = float(provider.get("free_tb_monthly", 0.0))
    min_monthly = float(provider.get("min_monthly_usd", 0.0))
    rate_gb = float(provider.get(rate_key, 0.0))
    req_rate_10k = float(provider.get("request_cost_per_10k", 0.0))

    # Special handling for unmetered free open-source CDNs
    if provider.get("category") == "opensource":
        return 0.0

    # Special handling for Cloudflare Free/Pro/Business tiers & R2
    pid = provider.get("id", "")
    if pid == "cloudflare":
        if volume_tb <= 15.0:
            return 0.0
        elif volume_tb <= 50.0:
            return 20.0
        elif volume_tb <= 150.0:
            return 200.0
        return 2500.0

    if pid == "cloudflare-pages" or pid == "jetpack-site-accelerator":
        return 0.0

    billable_tb = max(0.0, volume_tb - free_tb) if free_tb >= 0 else 0.0
    billable_gb = billable_tb * 1000.0

    # Volume discount scaling at >50 TB for commercial payg/hyperscaler CDNs
    discount_factor = 1.0
    if volume_tb >= 500.0:
        discount_factor = 0.65
    elif volume_tb >= 100.0:
        discount_factor = 0.80
    elif volume_tb >= 50.0:
        discount_factor = 0.90

    bandwidth_cost = billable_gb * rate_gb * discount_factor

    # Request costs (requests_millions * 1,000,000 / 10,000 = requests_millions * 100 units of 10k)
    free_req_m = 10.0 if pid == "aws-cloudfront" else (1.0 if pid == "gcore" else 0.0)
    billable_req_m = max(0.0, requests_millions - free_req_m)
    request_cost = billable_req_m * 100.0 * req_rate_10k

    # Fastly $50/mo developer credit offset
    total = bandwidth_cost + request_cost
    if pid == "fastly":
        total = max(0.0, total - 50.0)

    return round(max(min_monthly, total), 2)


def filter_providers(
    providers: List[Dict[str, Any]],
    category: str = "all",
    search: str | None = None,
    free_only: bool = False,
) -> List[Dict[str, Any]]:
    results = providers
    if category and category != "all":
        results = [p for p in results if p.get("category", "").lower() == category.lower()]
    if free_only:
        results = [
            p
            for p in results
            if float(p.get("free_tb_monthly", 0.0)) != 0.0
            or p.get("cost_1tb_usd", 1.0) == 0.0
        ]
    if search:
        q = search.lower()
        results = [
            p
            for p in results
            if q in p.get("name", "").lower()
            or q in p.get("best_for", "").lower()
            or q in p.get("free_tier", "").lower()
            or any(q in f.lower() for f in p.get("features", []))
        ]
    return results


def update_affiliate_links(pairs: List[str]) -> None:
    data = load_data()
    affiliates: Dict[str, str] = data.get("affiliates", {})
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"Expected key=url format, got: {pair}")
        key, new_url = pair.split("=", 1)
        key = key.strip().lower()
        new_url = new_url.strip()
        if key not in affiliates:
            raise ValueError(
                f"Unknown partner '{key}'. Valid keys: {', '.join(affiliates.keys())}"
            )
        old_url = affiliates[key]
        affiliates[key] = new_url
        for p in data.get("providers", []):
            if key in p.get("id", "").lower() or key in p.get("name", "").lower():
                p["url"] = new_url
        for file_path in SYNC_FILES:
            if file_path.exists() and old_url and old_url != new_url:
                text = file_path.read_text(encoding="utf-8")
                file_path.write_text(text.replace(old_url, new_url), encoding="utf-8")
        print(f"[OK] Updated {key}: {old_url} -> {new_url}")

    with PROVIDERS_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def print_cost_table(
    providers: List[Dict[str, Any]],
    volume_tb: float,
    requests_m: float,
    region: str,
) -> None:
    if not providers:
        print("No matching CDN providers found.")
        return

    rows = []
    for p in providers:
        est = estimate_monthly_cost(p, volume_tb, requests_m, region)
        rows.append((est, p))
    rows.sort(key=lambda item: (item[0], item[1]["name"]))

    header = (
        f"{'CDN Provider':<36} | {'Category':<11} | {'$/GB (NA/EU)':<12} | "
        f"{f'Est. @ {volume_tb:g} TB/mo':<16} | {'Verified':<10} | {'Official Tariff URL'}"
    )
    print(header)
    print("-" * len(header))
    for est, p in rows:
        rate_str = f"${p['rate_na_eu_gb']:.4f}".rstrip("0").rstrip(".") if p["rate_na_eu_gb"] > 0 else "$0.00 (Free)"
        est_str = "$0.00 (Free)" if est == 0 else f"${est:,.2f}/mo"
        print(
            f"{p['name'][:36]:<36} | {p['category']:<11} | {rate_str:<12} | "
            f"{est_str:<16} | {p['last_verified']:<10} | {p['pricing_url']}"
        )


def print_matrix_table(providers: List[Dict[str, Any]]) -> None:
    header = (
        f"{'CDN Provider':<35} | {'1 TB/mo':>10} | {'10 TB/mo':>10} | "
        f"{'50 TB/mo':>10} | {'100 TB/mo':>11} | {'500 TB/mo':>11} | {'Verified'}"
    )
    print(header)
    print("-" * len(header))
    for p in providers:
        c1 = f"${p['cost_1tb_usd']:,.0f}" if p["cost_1tb_usd"] > 0 else "$0 Free"
        c10 = f"${p['cost_10tb_usd']:,.0f}" if p["cost_10tb_usd"] > 0 else "$0 Free"
        c50 = f"${p['cost_50tb_usd']:,.0f}" if p["cost_50tb_usd"] > 0 else "$0 Free"
        c100 = f"${p['cost_100tb_usd']:,.0f}" if p["cost_100tb_usd"] > 0 else "$0 Free"
        c500 = f"${p['cost_500tb_usd']:,.0f}" if p["cost_500tb_usd"] > 0 else "$0 Free"
        print(
            f"{p['name'][:35]:<35} | {c1:>10} | {c10:>10} | "
            f"{c50:>10} | {c100:>11} | {c500:>11} | {p['last_verified']}"
        )


def print_legacy_table(legacy: List[Dict[str, Any]]) -> None:
    header = f"{'Legacy / Defunct CDN':<36} | {'2026 Status':<44} | {'Recommended Migration'}"
    print(header)
    print("-" * len(header))
    for item in legacy:
        print(
            f"{item['legacy_name'][:36]:<36} | {item['status'][:44]:<44} | {item['recommended_migration']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare CDN providers and calculate monthly bandwidth & request costs (1 TB to 500 TB+)."
    )
    parser.add_argument(
        "-c",
        "--category",
        choices=["all", "payg", "hyperscaler", "free", "opensource", "video", "image", "enterprise"],
        default="all",
        help="Filter by CDN category",
    )
    parser.add_argument(
        "-v",
        "--volume-tb",
        type=float,
        default=10.0,
        help="Monthly bandwidth transfer in Terabytes (TB) for cost calculation (default: 10 TB)",
    )
    parser.add_argument(
        "-r",
        "--requests-m",
        type=float,
        default=25.0,
        help="Monthly HTTP/HTTPS requests in Millions (default: 25M)",
    )
    parser.add_argument(
        "--region",
        choices=["na-eu", "asia", "global"],
        default="na-eu",
        help="Traffic geographic distribution profile (default: na-eu)",
    )
    parser.add_argument(
        "--free-only",
        action="store_true",
        help="Show only CDN providers offering a 100%% free plan or permanent free monthly TB quota",
    )
    parser.add_argument(
        "--matrix",
        action="store_true",
        help="Display side-by-side multi-volume cost matrix (1 TB, 10 TB, 50 TB, 100 TB, 500 TB)",
    )
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Display status and migration alternatives for defunct/acquired CDNs (MaxCDN, StackPath, Edgio, etc.)",
    )
    parser.add_argument("-q", "--search", help="Keyword search across provider names, features, and use cases")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument(
        "--set-affiliate",
        nargs="+",
        metavar="PARTNER=URL",
        help="Update affiliate link(s) across README, HTML pages, guides & providers.json",
    )

    args = parser.parse_args()

    if args.set_affiliate:
        update_affiliate_links(args.set_affiliate)
        return

    data = load_data()

    if args.legacy:
        legacy_list = data.get("legacy_graveyard", [])
        if args.json:
            print(json.dumps(legacy_list, indent=2, ensure_ascii=False))
        else:
            print_legacy_table(legacy_list)
        return

    matched = filter_providers(
        data.get("providers", []),
        category=args.category,
        search=args.search,
        free_only=args.free_only,
    )

    if args.json:
        enriched = []
        for p in matched:
            item = dict(p)
            item["calculated_monthly_usd"] = estimate_monthly_cost(
                p, args.volume_tb, args.requests_m, args.region
            )
            enriched.append(item)
        print(json.dumps(enriched, indent=2, ensure_ascii=False))
    elif args.matrix:
        print_matrix_table(matched)
    else:
        print_cost_table(matched, args.volume_tb, args.requests_m, args.region)


if __name__ == "__main__":
    main()
