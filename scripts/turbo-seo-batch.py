#!/usr/bin/env python3
"""
Turbo SEO batch updater.

Purpose:
- Maintain contextual neighbor links on EXISTING approved California appliance pages.
- Never create new location pages.
- Update sitemap lastmod only for pages actually changed.
- Replace older priority-local-network blocks with one stable managed block.
- Validate critical indexability/canonical signals before writing.

Usage:
  python3 scripts/turbo-seo-batch.py          # dry run
  python3 scripts/turbo-seo-batch.py --write  # write changes
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "turbo-seo-network.json"
SITEMAP = ROOT / "sitemap.xml"
BASE = "https://freereliableappliancepickup.com/"

MANAGED_RE = re.compile(
    r"<!--\s*(?:turbo-seo-network-v1|priority-local-network-v3|priority-local-network-v4)\s*-->"
    r"\s*<section\b[\s\S]*?</section>",
    re.I,
)

def display_name(slug: str) -> str:
    base = slug.removesuffix("-appliance-pickup")
    return " ".join(part.capitalize() for part in base.split("-"))

def page_path(slug: str) -> Path:
    return ROOT / slug / "index.html"

def self_url(slug: str) -> str:
    return f"{BASE}{slug}/"

def page_exists(slug: str) -> bool:
    return page_path(slug).is_file()

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

def build_block(slug: str, region: str, hub: str, neighbors: list[str]) -> str:
    city = display_name(slug)
    usable = [n for n in neighbors if page_exists(n) and n != slug]
    links = [
        f'<a href="/{n}/">{display_name(n)}</a>'
        for n in usable[:7]
    ]
    if page_exists(hub) and hub != slug:
        links.append(f'<a href="/{hub}/">{region} hub</a>')

    if links:
        link_html = " · ".join(links)
    else:
        link_html = f'<a href="/{hub}/">{region} hub</a>' if page_exists(hub) else ""

    return (
        '<!-- turbo-seo-network-v1 -->\n'
        f'<section class="turbo-seo-network-v1" aria-labelledby="turbo-network-{slug}">\n'
        f'  <h2 id="turbo-network-{slug}">{city} appliance pickup within the {region} service network</h2>\n'
        f'  <p>{city} is connected to nearby pickup routes within {region}. '
        'Use the closest city page when the pickup address falls near a city boundary so the request can be reviewed against the most relevant local route and access conditions.</p>\n'
        '  <p>Priority appliance categories include qualifying washers, dryers, refrigerators, freezers and stoves/ranges. '
        'Free pickup depends on appliance condition, safe access and current route availability; an available local pickup professional may complete the request.</p>\n'
        + (f'  <p><strong>Nearby service pages:</strong> {link_html}</p>\n' if link_html else '')
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

def update_sitemap(sitemap: str, slugs: list[str], stamp: str) -> str:
    out = sitemap
    for slug in slugs:
        pattern = re.compile(
            rf"(<loc>{re.escape(self_url(slug))}</loc>\s*<lastmod>)[^<]+(</lastmod>)",
            re.I,
        )
        out, count = pattern.subn(rf"\g<1>{stamp}\g<2>", out, count=1)
        if count == 0:
            print(f"WARN sitemap entry not found for {slug}")
    return out

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    changed: list[str] = []
    skipped: list[str] = []
    failures: list[str] = []

    for region, region_cfg in cfg["regions"].items():
        hub = region_cfg["hub"]
        for slug, neighbors in region_cfg["members"].items():
            path = page_path(slug)
            if not path.exists():
                skipped.append(slug)
                continue

            html = path.read_text(encoding="utf-8", errors="replace")
            problems = critical_checks(slug, html)
            if problems:
                failures.append(f"{slug}: " + ", ".join(problems))
                continue

            block = build_block(slug, region, hub, neighbors)
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
        sitemap = SITEMAP.read_text(encoding="utf-8", errors="replace")
        new_sitemap = update_sitemap(sitemap, changed, date.today().isoformat())
        if new_sitemap != sitemap:
            SITEMAP.write_text(new_sitemap, encoding="utf-8")

    print(f"MODE={'WRITE' if args.write else 'DRY_RUN'}")
    print(f"TARGETS_CHANGED={len(changed)}")
    for slug in changed:
        print("CHANGED", slug)
    print(f"TARGETS_SKIPPED_MISSING={len(skipped)}")
    for slug in skipped:
        print("SKIPPED", slug)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
