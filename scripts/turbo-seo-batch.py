#!/usr/bin/env python3
"""
Turbo SEO batch updater.

One run maintains BOTH:
- existing approved priority appliance-pickup pages
- matching existing washer-dryer-pickup pages

It never creates new location pages. It updates managed regional-link blocks,
refreshes sitemap lastmod values for changed URLs, and validates basic SEO signals.

Usage:
  python3 scripts/turbo-seo-batch.py
  python3 scripts/turbo-seo-batch.py --write
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "turbo-seo-network.json"
BASE = "https://freereliableappliancepickup.com/"
SITEMAPS = [
    ROOT / "sitemap.xml",
    ROOT / "sitemap-regular-washer-dryer.xml",
]

MANAGED_RE = re.compile(
    r"<!--\s*(?:turbo-seo-network-v1|priority-local-network-v3|priority-local-network-v4)\s*-->"
    r"\s*<section\b[\s\S]*?</section>",
    re.I,
)

def display_name(slug: str) -> str:
    base = slug
    for suffix in ("-washer-dryer-pickup", "-appliance-pickup"):
        if base.endswith(suffix):
            base = base[:-len(suffix)]
            break
    special = {"la": "LA", "san": "San"}
    words = []
    for part in base.split("-"):
        words.append(special.get(part, part.capitalize()))
    return " ".join(words)

def page_path(slug: str) -> Path:
    return ROOT / slug / "index.html"

def self_url(slug: str) -> str:
    return f"{BASE}{slug}/"

def page_exists(slug: str) -> bool:
    return page_path(slug).is_file()

def page_is_indexable(slug: str) -> bool:
    path = page_path(slug)
    if not path.is_file():
        return False
    html = path.read_text(encoding="utf-8", errors="replace")
    robots = re.search(r"<meta\b[^>]*name=[\"']robots[\"'][^>]*>", html, re.I)
    return not (robots and "noindex" in robots.group(0).lower())

def to_laundry(slug: str) -> str:
    if slug.endswith("-appliance-pickup"):
        return slug[:-len("-appliance-pickup")] + "-washer-dryer-pickup"
    return slug

def critical_checks(slug: str, html: str) -> list[str]:
    problems = []
    low = html.lower()
    if self_url(slug).lower() not in low:
        problems.append("missing self URL/canonical signal")
    robots = re.search(r"<meta\b[^>]*name=[\"']robots[\"'][^>]*>", html, re.I)
    if robots and "noindex" in robots.group(0).lower():
        problems.append("page is noindex")
    if not re.search(r"<h1\b[^>]*>[\s\S]*?</h1>", html, re.I):
        problems.append("missing H1")
    if not re.search(r"<title>[\s\S]*?</title>", html, re.I):
        problems.append("missing title")
    return problems

def build_block(slug: str, region: str, hub: str, neighbors: list[str], kind: str, scope: str = "local") -> str:
    city = display_name(slug)
    usable = [n for n in neighbors if page_is_indexable(n) and n != slug][:7]
    links = [f'<a href="/{n}/">{display_name(n)}</a>' for n in usable]
    if page_is_indexable(hub) and hub != slug:
        links.append(f'<a href="/{hub}/">{region} hub</a>')
    link_html = " · ".join(links)

    if kind == "laundry":
        heading = f"{city} washer and dryer pickup within the {region} service network"
        if scope == "statewide":
            body = (
                f"{city} is connected to other approved washer and dryer pickup pages within {region}. "
                "Use the page matching the actual pickup location so access, floor level, stairs, parking "
                "and route availability can be reviewed against the correct service area."
            )
        else:
            body = (
                f"{city} is connected to nearby washer and dryer pickup routes within {region}. "
                "Use the closest city page when the pickup address is near a city boundary so access, "
                "floor level, stairs, parking and route availability can be reviewed against the correct local area."
            )
        service = (
            "We prioritize qualifying washer and dryer sets and individual laundry appliances when the pickup "
            "meets current service requirements. Free pickup depends on condition, safe access and route availability; "
            "an available local pickup professional may complete the request."
        )
    else:
        heading = f"{city} appliance pickup within the {region} service network"
        if scope == "statewide":
            body = (
                f"{city} is connected to other approved appliance pickup pages within {region}. "
                "Use the page matching the actual pickup location so the request can be reviewed against "
                "the most relevant service area, access conditions and current route availability."
            )
        else:
            body = (
                f"{city} is connected to nearby pickup routes within {region}. "
                "Use the closest city page when the pickup address falls near a city boundary so the request can be "
                "reviewed against the most relevant local route and access conditions."
            )
        service = (
            "Priority appliance categories include qualifying washers, dryers, refrigerators, freezers and stoves/ranges. "
            "Free pickup depends on appliance condition, safe access and current route availability; "
            "an available local pickup professional may complete the request."
        )

    return (
        '<!-- turbo-seo-network-v1 -->\n'
        f'<section class="turbo-seo-network-v1" aria-labelledby="turbo-network-{slug}">\n'
        f'  <h2 id="turbo-network-{slug}">{heading}</h2>\n'
        f'  <p>{body}</p>\n'
        f'  <p>{service}</p>\n'
        + (f'  <p><strong>Nearby service pages:</strong> {link_html}</p>\n' if link_html else "")
        + '</section>'
    )

def build_specialty_block(slug: str, label: str, regions: list[str]) -> str:
    usable = [r for r in regions if page_exists(r)]
    links = " · ".join(
        f'<a href="/{r}/">{display_name(r)}</a>'
        for r in usable
    )
    return (
        '<!-- turbo-seo-network-v1 -->\n'
        f'<section class="turbo-seo-specialty-v1" aria-labelledby="turbo-specialty-{slug}">\n'
        f'  <h2 id="turbo-specialty-{slug}">{label}: regional service connections</h2>\n'
        '  <p>This appliance-specific page is connected to the broader regional pickup network so customers can move between appliance-type information and the most relevant local service area without creating duplicate city pages.</p>\n'
        '  <p>Pickup qualification depends on appliance condition, safe access and current route availability. Submit the exact pickup address, photos and condition details for review.</p>\n'
        + (f'  <p><strong>Regional appliance pickup pages:</strong> {links}</p>\n' if links else "")
        + '</section>'
    )

def insert_or_replace(html: str, block: str) -> str:
    if MANAGED_RE.search(html):
        return MANAGED_RE.sub(block, html, count=1)
    request = re.search(r'<section\s+id=[\"\']request[\"\'][^>]*>', html, re.I)
    if request:
        return html[:request.start()] + block + "\n" + html[request.start():]
    main_close = re.search(r"</main>", html, re.I)
    if main_close:
        return html[:main_close.start()] + block + "\n" + html[main_close.start():]
    footer = re.search(r"<footer\b", html, re.I)
    if footer:
        return html[:footer.start()] + block + "\n" + html[footer.start():]
    body_close = re.search(r"</body>", html, re.I)
    if body_close:
        return html[:body_close.start()] + block + "\n" + html[body_close.start():]
    return html + "\n" + block + "\n"

def update_sitemap_text(text: str, slugs: list[str], stamp: str) -> tuple[str, int]:
    out = text
    hits = 0
    for slug in slugs:
        pattern = re.compile(
            rf"(<loc>{re.escape(self_url(slug))}</loc>\s*<lastmod>)[^<]+(</lastmod>)",
            re.I,
        )
        out, count = pattern.subn(rf"\g<1>{stamp}\g<2>", out, count=1)
        hits += count
    return out, hits

def process_target(
    slug: str,
    region: str,
    hub: str,
    neighbors: list[str],
    kind: str,
    scope: str,
    write: bool,
    changed: list[str],
    skipped: list[str],
    failures: list[str],
) -> None:
    path = page_path(slug)
    if not path.exists():
        skipped.append(slug)
        return
    if not page_is_indexable(slug):
        skipped.append(slug)
        return
    html = path.read_text(encoding="utf-8", errors="replace")
    problems = critical_checks(slug, html)
    if problems:
        failures.append(f"{slug}: " + ", ".join(problems))
        return
    block = build_block(slug, region, hub, neighbors, kind, scope)
    new_html = insert_or_replace(html, block)
    if new_html != html:
        changed.append(slug)
        if write:
            path.write_text(new_html, encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    changed: list[str] = []
    skipped: list[str] = []
    failures: list[str] = []

    for region, region_cfg in cfg["regions"].items():
        appliance_hub = region_cfg["hub"]
        laundry_hub = to_laundry(appliance_hub)
        scope = region_cfg.get("scope", "local")

        for appliance_slug, appliance_neighbors in region_cfg["members"].items():
            process_target(
                appliance_slug,
                region,
                appliance_hub,
                appliance_neighbors,
                "appliance",
                scope,
                args.write,
                changed,
                skipped,
                failures,
            )

            laundry_slug = to_laundry(appliance_slug)
            laundry_neighbors = [to_laundry(n) for n in appliance_neighbors]
            process_target(
                laundry_slug,
                region,
                laundry_hub,
                laundry_neighbors,
                "laundry",
                scope,
                args.write,
                changed,
                skipped,
                failures,
            )

    for slug, info in cfg.get("specialty_pages", {}).items():
        path = page_path(slug)
        if not path.exists():
            skipped.append(slug)
            continue
        if not page_is_indexable(slug):
            skipped.append(slug)
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        problems = critical_checks(slug, html)
        if problems:
            failures.append(f"{slug}: " + ", ".join(problems))
            continue
        block = build_specialty_block(slug, info.get("label", display_name(slug)), info.get("regions", []))
        new_html = insert_or_replace(html, block)
        if new_html != html:
            changed.append(slug)
            if args.write:
                path.write_text(new_html, encoding="utf-8")

    if failures:
        print("CRITICAL FAILURES")
        for item in failures:
            print(" -", item)
        return 1

    if args.write and changed:
        stamp = datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
        found = set()
        for sitemap_path in SITEMAPS:
            if not sitemap_path.exists():
                continue
            original = sitemap_path.read_text(encoding="utf-8", errors="replace")
            updated, _ = update_sitemap_text(original, changed, stamp)
            if updated != original:
                sitemap_path.write_text(updated, encoding="utf-8")
            for slug in changed:
                if self_url(slug) in original:
                    found.add(slug)
        for slug in changed:
            if slug not in found:
                print(f"WARN sitemap entry not found for {slug}")

    print(f"MODE={'WRITE' if args.write else 'DRY_RUN'}")
    print(f"TARGETS_CHANGED={len(changed)}")
    print(f"APPLIANCE_CHANGED={sum(s.endswith('-appliance-pickup') for s in changed)}")
    print(f"LAUNDRY_CHANGED={sum(s.endswith('-washer-dryer-pickup') for s in changed)}")
    for slug in changed:
        print("CHANGED", slug)
    print(f"TARGETS_SKIPPED_MISSING={len(skipped)}")
    for slug in skipped:
        print("SKIPPED", slug)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
