#!/usr/bin/env python3
"""TTG Nationwide FastTrack: read-only state/city page inventory.

Run from any directory:
  python scripts/ttg_fasttrack_inventory.py --state IL --details --limit 20
  python scripts/ttg_fasttrack_inventory.py --format csv --output /tmp/ttg-states.csv

Reads the current checkout, not GitHub's PR branches or live website.
A page present in the checkout is NOT verified deployed or index-eligible.
The program never creates pages, changes routing, edits sitemaps or sets index.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE_TYPES = ("appliance", "washer-dryer", "refrigerator", "freezer", "stove-oven")
SUPPORTED_STATUSES = frozenset(("direct", "partner-supported"))


def slugify(value: str) -> str:
    plain = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")


def load_sources(root: Path) -> tuple[dict, dict]:
    with (root / "data/market-routing.json").open(encoding="utf-8") as stream:
        routing = json.load(stream)
    with (root / "data/cities.json").open(encoding="utf-8") as stream:
        cities = json.load(stream)
    defaults = routing.get("state_defaults", [])
    if len(defaults) != 50 or len({x["state_code"] for x in defaults}) != 50:
        raise ValueError("State defaults must contain 50 unique states")
    if not isinstance(cities.get("cities"), list) or not isinstance(routing.get("markets"), list):
        raise ValueError("Missing cities or markets list")
    return routing, cities


def status_for(city: dict, state: dict, markets: list[dict]) -> tuple[str, str]:
    code, name = state["state_code"], city["city"].casefold().strip()
    exact = next((m for m in markets
                  if m.get("state_code") == code
                  and m.get("city", "").casefold().strip() == name), None)
    region_name = city.get("region", "")
    region = next((m for m in markets
                   if m.get("state_code") == code and not m.get("city")
                   and m.get("region", "").casefold() == region_name.casefold()), None)
    selected = exact or region or state
    return selected.get("status", "request-only"), ("exact" if exact else "region" if region else "state")


def page_presence(root: Path, city_slug: str, code: str, page_type: str,
                  city_code_sets: dict[str, set[str]]) -> dict:
    """Keep a same-name city in another state from claiming the wrong page."""
    explicit = f"{city_slug}-{code.lower()}-{page_type}-pickup/index.html"
    legacy = f"{city_slug}-{page_type}-pickup/index.html"
    if (root / explicit).is_file():
        return {"file": explicit, "source": "state-scoped"}
    if (root / legacy).is_file():
        if len(city_code_sets.get(city_slug, {code})) > 1:
            return {"file": legacy, "source": "ambiguous-needs-manual-attribution"}
        return {"file": legacy, "source": "legacy-unscoped-needs-manual-verification"}
    return {"file": None, "source": "not-found-in-checkout"}


def collect(root: Path) -> tuple[list[dict], list[dict]]:
    routing, lookup = load_sources(root)
    states = sorted(routing["state_defaults"], key=lambda item: item["state"])
    codes = {s["state_code"] for s in states}
    names = {s["state_code"]: s for s in states}
    cities: dict[tuple[str, str], dict] = {}
    collisions: dict[str, set[str]] = defaultdict(set)

    def register(item: dict) -> None:
        code = item.get("state_code")
        city_name = str(item.get("city", "")).strip()
        if code not in codes or not city_name:
            return
        key = (code, slugify(city_name))
        if key not in cities:
            cities[key] = {"city": city_name, "state_code": code,
                           "region": item.get("region", ""), "priority": item.get("priority", 3)}
        elif not cities[key].get("region") and item.get("region"):
            cities[key]["region"] = item["region"]
        collisions[key[1]].add(code)

    for city in lookup["cities"]:
        register(city)
    # Additional market research is a planning input, never fulfillment evidence.
    # IL/GA were not yet listed in cities.json when FastTrack was introduced.
    candidates_file = root / "data/ttg-market-candidates.json"
    if candidates_file.is_file():
        with candidates_file.open(encoding="utf-8") as stream:
            candidates = json.load(stream)
        if not isinstance(candidates.get("cities"), list):
            raise ValueError("FastTrack candidates must include a cities list")
        for item in candidates["cities"]:
            register(item)
    # Exact-market cities absent from cities.json should still appear in inventory.
    for market in routing["markets"]:
        if market.get("city"):
            register(market)

    details: list[dict] = []
    grouped: dict[str, list[dict]] = defaultdict(list)
    for (code, city_slug), city in sorted(cities.items()):
        state = names[code]
        route, resolution = status_for(city, state, routing["markets"])
        files = {page_type: page_presence(root, city_slug, code, page_type, collisions)
                 for page_type in PAGE_TYPES}
        scoped = sum(p["source"] == "state-scoped" for p in files.values())
        unscoped = sum(p["source"].startswith(("legacy-unscoped", "ambiguous")) for p in files.values())
        record = {
            "state": state["state"], "state_code": code,
            "city": city["city"], "region": city.get("region", ""),
            "priority": city.get("priority", 3), "routing_status": route,
            "routing_source": resolution, "state_scoped_files": scoped,
            "unverified_unscoped_files": unscoped, "page_slots": files,
            "index_permission": "manual_coverage_and_quality_review_required",
            "next_step": ("verify_operator_and_page_quality" if route in SUPPORTED_STATUSES
                          else "research_market_and_confirm_fulfillment"),
        }
        details.append(record)
        grouped[code].append(record)

    summaries: list[dict] = []
    for state in states:
        code = state["state_code"]
        rows = grouped[code]
        hub = f"{slugify(state['state'])}-appliance-pickup/index.html"
        summary = {
            "state": state["state"], "state_code": code,
            "state_default_status": state["status"],
            "tracked_cities": len(rows),
            "city_files_state_scoped": sum(x["state_scoped_files"] for x in rows),
            "city_files_unverified_unscoped": sum(x["unverified_unscoped_files"] for x in rows),
            "state_hub_in_checkout": (root / hub).is_file(),
            "state_hub_file": hub if (root / hub).is_file() else None,
            "cities_with_supported_routing_record": sum(
                x["routing_status"] in SUPPORTED_STATUSES for x in rows),
            "release_status": "not_determined_by_source_inventory",
            "indexing_status": "not_determined_by_source_inventory",
        }
        summaries.append(summary)
    return summaries, details


def render_csv(items: list[dict], *, detailed: bool) -> str:
    columns = (["state", "state_code", "city", "region", "priority",
                "routing_status", "routing_source", "state_scoped_files",
                "unverified_unscoped_files", "index_permission", "next_step"]
               if detailed else
               ["state", "state_code", "state_default_status", "tracked_cities",
                "city_files_state_scoped", "city_files_unverified_unscoped",
                "state_hub_in_checkout", "state_hub_file",
                "cities_with_supported_routing_record", "release_status", "indexing_status"])
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(items)
    return buf.getvalue()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT,
                        help="Repository checkout containing data/market-routing.json and data/cities.json")
    parser.add_argument("--state", help="Two-letter state code or state name")
    parser.add_argument("--details", action="store_true", help="List city records rather than state summaries")
    parser.add_argument("--limit", type=int, default=0, help="Limit city records (0 = all)")
    parser.add_argument("--format", choices=("json", "csv"), default="json")
    parser.add_argument("--output", type=Path, help="Write report to this path instead of stdout")
    args = parser.parse_args(argv)
    if args.limit < 0:
        parser.error("--limit must not be negative")
    try:
        summaries, details = collect(args.root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    if args.state:
        states = {s["state_code"]: s["state"] for s in summaries}
        wanted = args.state.casefold().strip()
        code = next((c for c, name in states.items() if c.casefold() == wanted
                     or name.casefold() == wanted), None)
        if code is None:
            parser.error("Unknown state: " + args.state)
        summaries = [s for s in summaries if s["state_code"] == code]
        details = [d for d in details if d["state_code"] == code]
    if args.details:
        details.sort(key=lambda r: (r["state_code"], r["priority"], r["city"].casefold()))
        result = details[:args.limit] if args.limit else details
    else:
        result = summaries
    report = (render_csv(result, detailed=args.details)
              if args.format == "csv" else json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    if args.output:
        args.output.write_text(report, encoding="utf-8")
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
