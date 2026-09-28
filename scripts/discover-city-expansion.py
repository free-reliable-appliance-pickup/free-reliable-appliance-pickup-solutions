#!/usr/bin/env python3
"""Discover nearby U.S. Census Places for SEO market planning.

This tool is intentionally discovery-only. It does not publish location pages.
It compares authoritative Census place geography with existing indexable
*-appliance-pickup pages in this repository so expansion can be researched
without hand-entering every nearby city.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENSUS_URL = (
    "https://www2.census.gov/geo/docs/maps-data/data/gazetteer/"
    "2025_Gazetteer/2025_Gaz_place_national.zip"
)
USER_AGENT = "FreeReliableAppliancePickup-CityDiscovery/1.0"


def slugify(value: str) -> str:
    value = value.lower().replace("’", "").replace("'", "")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


def clean_place_name(name: str) -> str:
    return re.sub(
        r"\s+(city|town|village|borough|municipality|CDP)$",
        "",
        name.strip(),
        flags=re.I,
    )


def norm_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", clean_place_name(value).lower())


def haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 3958.7613
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def fetch_places() -> list[dict[str, str]]:
    req = urllib.request.Request(CENSUS_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as resp:
        payload = resp.read()
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        txt_names = [n for n in zf.namelist() if n.lower().endswith(".txt")]
        if not txt_names:
            raise RuntimeError("Census Gazetteer ZIP did not contain a text file")
        text = zf.read(txt_names[0]).decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text), delimiter="|")
    rows = []
    for row in reader:
        rows.append({str(k).strip(): (v or "").strip() for k, v in row.items() if k})
    return rows


def existing_city_pages() -> set[str]:
    out: set[str] = set()
    for p in ROOT.glob("*-appliance-pickup/index.html"):
        slug = p.parent.name
        if slug.endswith("-appliance-pickup"):
            out.add(slug[: -len("-appliance-pickup")])
    return out


def find_seed(rows: list[dict[str, str]], state: str, seed: str) -> dict[str, str]:
    wanted = norm_name(seed)
    candidates = [
        r for r in rows
        if r.get("USPS", "").upper() == state.upper()
        and norm_name(r.get("NAME", "")) == wanted
    ]
    if not candidates:
        examples = sorted(
            clean_place_name(r.get("NAME", ""))
            for r in rows
            if r.get("USPS", "").upper() == state.upper()
            and wanted in norm_name(r.get("NAME", ""))
        )[:10]
        hint = f" Similar matches: {', '.join(examples)}" if examples else ""
        raise SystemExit(f"Seed place {seed!r} was not found in Census Places for {state}.{hint}")
    candidates.sort(key=lambda r: (r.get("NAME", "").upper().endswith(" CDP"), r.get("GEOID", "")))
    return candidates[0]


def to_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "").strip()
    if not value:
        raise ValueError(f"missing {key}")
    return float(value)


def build_candidates(
    rows: list[dict[str, str]],
    state: str,
    seed_row: dict[str, str],
    radius: float,
    limit: int,
) -> list[dict[str, object]]:
    seed_lat = to_float(seed_row, "INTPTLAT")
    seed_lon = to_float(seed_row, "INTPTLONG")
    existing = existing_city_pages()
    out: list[dict[str, object]] = []
    seen: set[str] = set()

    for row in rows:
        if row.get("USPS", "").upper() != state.upper():
            continue
        name = clean_place_name(row.get("NAME", ""))
        if not name:
            continue
        city_slug = slugify(name)
        if not city_slug or city_slug in seen:
            continue
        try:
            lat = to_float(row, "INTPTLAT")
            lon = to_float(row, "INTPTLONG")
        except ValueError:
            continue
        miles = haversine_miles(seed_lat, seed_lon, lat, lon)
        if miles > radius:
            continue
        seen.add(city_slug)
        out.append(
            {
                "place": name,
                "census_name": row.get("NAME", ""),
                "state": state.upper(),
                "geoid": row.get("GEOID", ""),
                "distance_miles": round(miles, 1),
                "latitude": lat,
                "longitude": lon,
                "suggested_slug": f"{city_slug}-appliance-pickup",
                "page_exists": city_slug in existing,
                "status": "existing" if city_slug in existing else "candidate",
            }
        )

    out.sort(key=lambda x: (float(x["distance_miles"]), str(x["place"])))
    return out[:limit]


def write_reports(
    candidates: list[dict[str, object]],
    state: str,
    seed: str,
    radius: float,
    limit: int,
) -> tuple[Path, Path]:
    stamp = datetime.now(timezone.utc).isoformat()
    report_dir = ROOT / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    stem = f"city-expansion-{state.lower()}-{slugify(seed)}"
    json_path = report_dir / f"{stem}.json"
    md_path = report_dir / f"{stem}.md"

    payload = {
        "generated_at_utc": stamp,
        "source": CENSUS_URL,
        "state": state.upper(),
        "seed": seed,
        "radius_miles": radius,
        "limit": limit,
        "note": "Discovery only. Candidate pages require local research and quality review before publishing.",
        "counts": {
            "total": len(candidates),
            "existing": sum(bool(x["page_exists"]) for x in candidates),
            "candidates": sum(not bool(x["page_exists"]) for x in candidates),
        },
        "places": candidates,
    }
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        f"# City Expansion Discovery — {seed}, {state.upper()}",
        "",
        "- Census source: 2025 U.S. Census Gazetteer Places",
        f"- Radius: {radius:g} miles",
        f"- Places returned: {len(candidates)}",
        f"- Existing appliance-pickup pages: {payload['counts']['existing']}",
        f"- New research candidates: {payload['counts']['candidates']}",
        "",
        "> Discovery only: this report does not publish new location pages. A candidate should be promoted only after local intent, service coverage, unique local information and page quality are verified.",
        "",
        "| Miles | Place | Status | Suggested slug |",
        "|---:|---|---|---|",
    ]
    for item in candidates:
        lines.append(
            f"| {item['distance_miles']} | {item['place']} | {item['status']} | {item['suggested_slug']} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", default="CA", help="Two-letter USPS state code")
    ap.add_argument("--seed", default="Rancho Cucamonga", help="Seed Census Place name")
    ap.add_argument("--radius", type=float, default=60.0, help="Search radius in miles")
    ap.add_argument("--limit", type=int, default=80, help="Maximum places in report")
    args = ap.parse_args()

    if not re.fullmatch(r"[A-Za-z]{2}", args.state):
        raise SystemExit("--state must be a two-letter USPS code")
    if args.radius <= 0 or args.radius > 500:
        raise SystemExit("--radius must be > 0 and <= 500 miles")
    if args.limit < 1 or args.limit > 500:
        raise SystemExit("--limit must be between 1 and 500")

    rows = fetch_places()
    seed_row = find_seed(rows, args.state.upper(), args.seed)
    canonical_seed = clean_place_name(seed_row.get("NAME", args.seed))
    candidates = build_candidates(rows, args.state.upper(), seed_row, args.radius, args.limit)
    json_path, md_path = write_reports(candidates, args.state.upper(), canonical_seed, args.radius, args.limit)

    missing = [x for x in candidates if not x["page_exists"]]
    existing = [x for x in candidates if x["page_exists"]]
    print(f"CENSUS_SOURCE={CENSUS_URL}")
    print(f"SEED={canonical_seed},{args.state.upper()}")
    print(f"RADIUS_MILES={args.radius:g}")
    print(f"PLACES_RETURNED={len(candidates)}")
    print(f"EXISTING_PAGES={len(existing)}")
    print(f"NEW_CANDIDATES={len(missing)}")
    print(f"JSON_REPORT={json_path.relative_to(ROOT)}")
    print(f"MARKDOWN_REPORT={md_path.relative_to(ROOT)}")
    for item in missing[:20]:
        print(f"CANDIDATE {item['distance_miles']:>5} mi {item['place']} -> {item['suggested_slug']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
