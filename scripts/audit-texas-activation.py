#!/usr/bin/env python3
"""VGM Texas activation gate: read-only, no automatic page indexing.

Use: python3 scripts/audit-texas-activation.py
     python3 scripts/audit-texas-activation.py --markdown

This audit compares live site-source HTML, published sitemaps, the explicit
indexability inventories, the market-routing map and the partner registry.
No business address, partner identity or customer lead is included in output.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://freereliableappliancepickup.com/"
MAJOR = ["Houston Metro", "Dallas-Fort Worth", "Austin Metro", "San Antonio Metro", "El Paso Metro"]


class PickupPage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.head = True
        self.robots = []
        self.canonical = []
        self.forms = []
        self.in_form = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and a.get("name", "").lower() == "robots":
            self.robots.append(a.get("content", "").lower())
        if tag == "link" and a.get("rel", "").lower() == "canonical":
            self.canonical.append(a.get("href", ""))
        if tag == "form":
            self.forms.append({"attributes": a, "inputs": {}})
            self.in_form = True
        if self.in_form and tag == "input" and a.get("name"):
            self.forms[-1]["inputs"].setdefault(a["name"].lower(), []).append(a)

    def handle_endtag(self, tag):
        if tag == "form":
            self.in_form = False


def read_approvals(path):
    return {x.strip().strip("/") for x in Path(path).read_text(encoding="utf-8").splitlines()
            if x.strip() and not x.lstrip().startswith("#")}


def read_sitemap():
    root = ET.parse("sitemap.xml").getroot()
    return {x.text.strip() for x in root.iter() if x.tag.endswith("loc") and x.text}


def slug(path):
    return path.parent.as_posix().strip("/")


def url_for(page_slug):
    return BASE + page_slug.strip("/") + "/"


def pickup_in_texas(page):
    return any(
        inp.get("value", "").strip().lower() in {"tx", "texas"}
        for form in page.forms
        for inp in form["inputs"].get("state", [])
    )


def record_market(city, markets, catalog):
    key = str(city or "").strip().casefold()
    entry = catalog.get(key)
    if not entry:
        return None
    return markets.get(entry.get("region"))


def primary_partner_confirmed(route, partners):
    """Code-only minimum; real coverage still requires a separate manual check."""
    if not route:
        return False
    if route.get("status") == "direct":
        return route.get("territory_status") == "protected" and bool(route.get("phone"))
    if route.get("status") != "partner-supported":
        return False
    pid = route.get("partner_id")
    if not pid or route.get("territory_status") not in {"assigned", "protected"}:
        return False
    row = partners.get(pid)
    return bool(row and row.get("primary_state_code") == "TX"
                and row.get("status") in {"active", "approved"})


def collect():
    routing = json.loads(Path("data/market-routing.json").read_text(encoding="utf-8"))
    catalog_data = json.loads(Path("data/cities.json").read_text(encoding="utf-8"))
    partner_data = json.loads(Path("data/partners.json").read_text(encoding="utf-8"))
    markets = {m["region"]: m for m in routing["markets"]
               if m.get("state_code") == "TX" and not m.get("city")}
    catalog = {c["city"].casefold(): c for c in catalog_data["cities"]
               if c.get("state_code") == "TX"}
    partners = {p.get("partner_id"): p for p in partner_data.get("partners", [])
                if p.get("partner_id")}
    approved = (read_approvals("data/approved-indexable-locations.txt") |
                read_approvals("data/approved-indexable-service-pages.txt"))
    sitemap = read_sitemap()
    errors, texas_pages = [], {}
    for path in sorted(Path(".").rglob("index.html")):
        if ".github" in path.parts or ".git" in path.parts:
            continue
        page = PickupPage()
        page.feed(path.read_text(encoding="utf-8", errors="replace"))
        if not pickup_in_texas(page):
            continue
        page_slug = slug(path)
        noindex = any("noindex" in x for x in page.robots)
        in_sitemap = url_for(page_slug) in sitemap
        if len(page.canonical) != 1 or page.canonical[0] != url_for(page_slug):
            errors.append(f"{page_slug}: missing or mismatched self-canonical")
        if in_sitemap and noindex:
            errors.append(f"{page_slug}: noindex page found in sitemap")
        if page_slug == "texas-appliance-pickup":
            if noindex or not in_sitemap or page_slug not in approved:
                errors.append("texas-appliance-pickup: statewide indexable hub lost approval")
        elif not noindex:
            # A TX city can NEVER become indexable solely because a page exists.
            if page_slug not in approved or not in_sitemap:
                errors.append(f"{page_slug}: indexable without sitemap + explicit approval")
            form_cities = [
                inp.get("value", "").strip()
                for form in page.forms for inp in form["inputs"].get("city", [])
                if inp.get("value", "").strip()
            ]
            if len(set(form_cities)) != 1:
                errors.append(f"{page_slug}: indexable city page has no unambiguous city")
            else:
                market = record_market(form_cities[0], markets, catalog)
                if not primary_partner_confirmed(market, partners):
                    errors.append(f"{page_slug}: indexable without verified route + approved partner registry status")
        texas_pages[page_slug] = {"noindex": noindex, "in_sitemap": in_sitemap}

    expected_regions = {r for r in markets}
    # Baseline reviewed 2026-11-05: Sachse, Watauga and Balch Springs added as
    # request-only Dallas–Fort Worth markets; no operator or indexing approvals.
    # Melissa (Dallas–Fort Worth) and Iowa Colony (Houston Metro) are added as
    # request-only catalog entries; no market activation or SEO approval.
    if len(catalog) != 167:
        errors.append(f"Texas city catalog changed to {len(catalog)}: review mapping and update baseline")
    for city_name in ("Sachse", "Watauga", "Balch Springs"):
        row = catalog.get(city_name.casefold())
        if not row or row.get("region") != "Dallas-Fort Worth":
            errors.append(f"{city_name}: missing from request-only Dallas-Fort Worth catalog mapping")
    for city_name, region in (("Melissa", "Dallas-Fort Worth"), ("Iowa Colony", "Houston Metro")):
        row = catalog.get(city_name.casefold())
        if not row or row.get("region") != region:
            errors.append(f"{city_name}: missing expected request-only Texas region mapping")
    # Liberty Hill / Bulverde: request-only metro mapping, with no operator approval.
    for city_name, region in (("Liberty Hill", "Austin Metro"), ("Bulverde", "San Antonio Metro")):
        row = catalog.get(city_name.casefold())
        if not row or row.get("region") != region:
            errors.append(f"{city_name}: missing expected request-only Texas region mapping")
    if len(expected_regions) != 22:
        errors.append(f"Texas regional queues changed to {len(expected_regions)}: review mapping and update baseline")
    # Seagoville and Lockhart remain request-only markets with no verified operator.
    for city_name, region in (("Seagoville", "Dallas-Fort Worth"), ("Lockhart", "Austin Metro")):
        row = catalog.get(city_name.casefold())
        if not row or row.get("region") != region:
            errors.append(f"{city_name}: missing expected request-only Texas region mapping")
    # Castle Hills and Dayton remain request-only markets with no verified operator.
    for city_name, region in (("Castle Hills", "San Antonio Metro"), ("Dayton", "Houston Metro")):
        row = catalog.get(city_name.casefold())
        if not row or row.get("region") != region:
            errors.append(f"{city_name}: missing expected request-only Texas region mapping")
    # Anna and Dripping Springs remain request-only with no verified operators.
    for city_name, region in (("Anna", "Dallas-Fort Worth"), ("Dripping Springs", "Austin Metro")):
        row = catalog.get(city_name.casefold())
        if not row or row.get("region") != region:
            errors.append(f"{city_name}: missing expected request-only Texas region mapping")
    missing_regions = {row.get("region") for row in catalog.values()} - expected_regions
    for region in sorted(missing_regions):
        errors.append(f"Texas city catalog references missing region: {region}")
    stats = []
    order = MAJOR + sorted(expected_regions - set(MAJOR))
    for region in order:
        route = markets.get(region, {})
        city_count = sum(1 for c in catalog.values() if c.get("region") == region)
        recorded = primary_partner_confirmed(route, partners)
        stats.append({
            "region": region, "cities": city_count,
            "route_status": route.get("status", "missing"),
            "verified_in_registry": recorded,
            "next_action": ("Manual city content + real pickup validation"
                            if recorded else "Confirm operator, capacity, service area, and record approval")
        })
    return {
        "texas_pages": len(texas_pages),
        "indexable_pages": sum(not x["noindex"] for x in texas_pages.values()),
        "request_only_pages": sum(x["noindex"] for x in texas_pages.values()),
        "cities": len(catalog), "regions": len(markets),
        "regions_with_recorded_operator": sum(x["verified_in_registry"] for x in stats),
        "approved_texas_city_pages": len([s for s in approved if s in texas_pages and s != "texas-appliance-pickup"]),
        "texas_approved_statewide_hub": "texas-appliance-pickup" in approved,
        "rows": stats, "errors": errors,
    }


def markdown(result):
    a = result
    out = [
        "# Texas market activation readiness",
        "",
        "**Read-only website source audit.** This does not prove real pickup availability or Google indexing.",
        "",
        f"- Texas pickup request pages inspected: **{a['texas_pages']}**",
        f"- Indexable Texas pickup pages: **{a['indexable_pages']}** (includes statewide hub)",
        f"- Texas pilot request pages with noindex: **{a['request_only_pages']}**",
        f"- Cities mapped: **{a['cities']}** across **{a['regions']}** regions",
        f"- Regions with a valid recorded operator/route: **{a['regions_with_recorded_operator']}**",
        f"- Explicitly approved Texas city pages: **{a['approved_texas_city_pages']}**",
        "",
        "| Texas region | Mapped cities | Code status | Recorded operator route |",
        "|---|---:|---|---|",
    ]
    for row in a["rows"]:
        out.append(
            f"| {row['region']} | {row['cities']} | {row['route_status']} | "
            + ("Yes — manual review still required" if row["verified_in_registry"] else "Not yet recorded") + " |"
        )
    out += [
        "",
        "## Activation process",
        "",
        "1. Confirm an actual local operator, appliance types, accepted condition, safe-access rules, ZIP coverage, capacity and response process.",
        "2. Record a verified, approved operator and actual market assignment through the approved partner workflow; never paste customer details or personal partner contacts into public pages.",
        "3. Review the selected city page for distinct, useful local information and accurate service limitations. Keep one genuine appliance photo per page.",
        "4. Update the explicit approved-page inventory and sitemap together; change robots to index only for the supported, reviewed page. Respect the site's existing indexable-location quality ceiling.",
        "5. Run all sitewide SEO audits, deploy, and verify indexing status in Search Console. A successful deploy alone does not prove Google indexing or ranking.",
        "",
        f"**Automated policy errors:** {len(a['errors'])}",
    ]
    out.extend("- " + error for error in a["errors"][:80])
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    report = collect()
    if "--markdown" in sys.argv:
        print(markdown(report), end="")
    else:
        for key in ("texas_pages", "indexable_pages", "request_only_pages",
                    "cities", "regions", "regions_with_recorded_operator",
                    "approved_texas_city_pages"):
            print(key.upper(), report[key])
        print("TEXAS_ACTIVATION_ERRORS", len(report["errors"]))
        for error in report["errors"][:80]:
            print("ERROR", error)
        if not report["errors"]:
            print("PASS: Texas pilot indexing safeguards and activation sources are consistent")
    sys.exit(1 if report["errors"] else 0)
