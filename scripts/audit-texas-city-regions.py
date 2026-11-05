#!/usr/bin/env python3
"""Audit Texas city-page routing without claiming local operator coverage."""
from pathlib import Path
import json
import re
import sys

catalog = json.loads(Path("data/cities.json").read_text(encoding="utf-8"))
routing = json.loads(Path("data/market-routing.json").read_text(encoding="utf-8"))
slug = lambda n: re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")
cities = {slug(x["city"]): x for x in catalog["cities"] if x.get("state_code") == "TX"}
markets = {x["region"]: x for x in routing["markets"] if x.get("state_code") == "TX" and not x.get("city")}
pages = sorted(Path(".").glob("*-tx-appliance-pickup/index.html"))
county_hubs = {"dallas-county", "collin-county", "tarrant-county"}
problems = []
for path in pages:
    city_slug = path.parent.name.removesuffix("-tx-appliance-pickup")
    if city_slug in county_hubs:
        continue  # County-level pages require the customer's actual city.
    info = cities.get(city_slug)
    if not info:
        problems.append(f"{path}: city missing from TX region catalog")
        continue
    market = markets.get(info.get("region", ""))
    if not market:
        problems.append(f"{path}: no TX metro region matching {info.get('region')}")
        continue
    if market.get("status") not in ("partner-recruiting", "request-only"):
        problems.append(f"{path}: unexpected verified/active status without partner review")
    if market.get("partner_id") or market.get("territory_status") == "assigned" or market.get("phone"):
        problems.append(f"{path}: unverified territory has assigned partner or phone")
    html = path.read_text(encoding="utf-8", errors="replace")
    if '<meta name="robots" content="noindex, follow">' not in html:
        problems.append(f"{path}: unverified page lost noindex safeguard")

print("TX_CITY_PAGES_CHECKED", len(pages) - len(county_hubs))
print("TX_REGIONAL_QUEUES", len(markets))
print("TX_CATALOG_CITIES", len(cities))
print("TX_ROUTING_ISSUES", len(problems))
for problem in problems:
    print("FAIL", problem)
if problems:
    sys.exit(1)
print("PASS: Texas pilot city pages map to non-promissory lead regions")
