#!/usr/bin/env python3
"""Check the priority Inland Empire appliance and laundry landing pages.

Run from the repository root: python3 scripts/check_priority_pickup_pages.py
Uses only the Python standard library. No Search Console rank assumptions.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "freereliableappliancepickup.com"
CITIES = ("fontana", "rancho-cucamonga", "ontario", "upland")
KINDS = ("appliance-pickup", "washer-dryer-pickup")
ERRORS = []
CHECKED = 0


def record(page: str, message: str) -> None:
    ERRORS.append(f"{page}: {message}")


def tag_attr(tag: str, attr: str) -> str:
    pattern = r'\b' + re.escape(attr) + r'\s*=\s*(["\'])(.*?)\1'
    found = re.search(pattern, tag, re.I | re.S)
    return html.unescape(found.group(2).strip()) if found else ""


def tags(source: str, name: str) -> list[str]:
    return re.findall(r"<" + name + r"\b[^>]*>", source, flags=re.I | re.S)


def select_tag(source: str, name: str, attr: str, value: str) -> list[str]:
    return [tag for tag in tags(source, name) if tag_attr(tag, attr).lower() == value]


def local_asset(value: str) -> str | None:
    parsed = urlparse(value)
    if parsed.netloc and parsed.netloc != DOMAIN:
        return None
    if parsed.scheme and parsed.scheme != "https":
        return None
    return unquote(parsed.path).lstrip("/")


def load_sitemaps() -> tuple[set[str], dict[str, list[str]]]:
    """Read the indexed URLs and preferred image per URL from both XML files."""
    ns = {
        "s": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "i": "http://www.google.com/schemas/sitemap-image/1.1",
    }
    pages: set[str] = set()
    images: dict[str, list[str]] = {}
    for filename, collect_images in (("sitemap.xml", False), ("sitemap-images.xml", True)):
        try:
            root = ET.parse(ROOT / filename).getroot()
        except (OSError, ET.ParseError) as exc:
            record(filename, f"missing or invalid XML: {exc}")
            continue
        for item in root.findall("s:url", ns):
            loc = (item.findtext("s:loc", default="", namespaces=ns) or "").strip()
            if not loc:
                continue
            if collect_images:
                images.setdefault(loc, []).extend(
                    (element.text or "").strip()
                    for element in item.findall("i:image/i:loc", ns)
                )
            else:
                pages.add(loc)
    home_url = f"https://{DOMAIN}/"
    home_expected = f"https://{DOMAIN}/home-six-appliance-garage.webp"
    if home_url not in pages:
        record("homepage", "missing from sitemap.xml")
    if images.get(home_url) != [home_expected]:
        record("homepage", "garage hero image is missing from image sitemap or duplicated")
    return pages, images


def check(city: str, kind: str, sitemap_urls: set[str], sitemap_images: dict[str, list[str]]) -> None:
    global CHECKED
    slug = f"{city}-{kind}"
    path = ROOT / slug / "index.html"
    if not path.is_file():
        record(slug, "page file is missing")
        return
    source = path.read_text(encoding="utf-8")
    CHECKED += 1

    expected_url = f"https://{DOMAIN}/{slug}/"
    if expected_url not in sitemap_urls:
        record(slug, "priority page missing from sitemap.xml")
    canonical_tags = select_tag(source, "link", "rel", "canonical")
    if len(canonical_tags) != 1 or tag_attr(canonical_tags[0], "href") != expected_url:
        record(slug, "missing, duplicate, or incorrect self-canonical URL")

    desc = select_tag(source, "meta", "name", "description")
    if len(desc) != 1 or not tag_attr(desc[0], "content"):
        record(slug, "missing or duplicate meta description")

    robots_tags = select_tag(source, "meta", "name", "robots")
    if any("noindex" in tag_attr(tag, "content").lower() for tag in robots_tags):
        record(slug, "page is marked noindex")

    title_match = re.findall(r"<title\b[^>]*>(.*?)</title>", source, re.I | re.S)
    title = html.unescape(re.sub(r"<[^>]+>", "", title_match[0])) if title_match else ""
    h1 = re.findall(r"<h1\b[^>]*>(.*?)</h1>", source, re.I | re.S)
    heading = html.unescape(re.sub(r"<[^>]+>", "", h1[0])) if h1 else ""
    city_name = city.replace("-", " ")
    if len(title_match) != 1 or city_name not in title.lower():
        record(slug, "title is missing, duplicated, or not city-specific")
    if len(h1) != 1 or city_name not in heading.lower():
        record(slug, "expected exactly one city-specific H1")

    target_words = ("washer", "dryer", "pickup") if kind == "washer-dryer-pickup" else ("appliance", "pickup")
    for word in target_words:
        if word not in title.lower() or word not in heading.lower():
            record(slug, f"missing primary intent word in title/H1: {word}")
    if "Free Reliable" not in source or "Appliance Pickup" not in source:
        record(slug, "business branding missing from visible page markup")

    hero_match = re.search(
        r'<div\b[^>]*class=["\']site-hero-art["\'][^>]*>[\s\S]*?<img\b[^>]*>',
        source, re.I
    )
    hero_tag = hero_match.group() if hero_match else ""
    hero_img = re.search(r"<img\b[^>]*>", hero_tag, re.I | re.S)
    hero_image = tag_attr(hero_img.group(), "src") if hero_img else ""
    if not hero_image or not tag_attr(hero_img.group(), "alt"):
        record(slug, "hero image or descriptive alt text is missing")

    og = select_tag(source, "meta", "property", "og:image")
    og_image = tag_attr(og[0], "content") if len(og) == 1 else ""
    if not og_image:
        record(slug, "exactly one og:image is required")
    if hero_image and og_image:
        hero_path = local_asset(hero_image)
        og_path = local_asset(og_image)
        if not hero_path or not og_path or hero_path != og_path:
            record(slug, "hero image and social preview image do not match")
        for asset in {hero_path, og_path}:
            if asset and not (ROOT / asset).is_file():
                record(slug, f"missing image asset: {asset}")
        listed = [local_asset(url) for url in sitemap_images.get(expected_url, [])]
        if hero_path and listed != [hero_path]:
            record(slug, "image sitemap must list exactly the same one primary hero photo")

    if not re.search(r'<form\b[^>]*action=["\']https://formspree\.io/f/[^"\']+["\']', source, re.I):
        record(slug, "pickup request form is missing or has a different action")
    if not re.search(r'\bid=["\']request["\']', source, re.I):
        record(slug, "request section anchor is missing")
    if "href=\"#request\"" not in source and "href='#request'" not in source:
        record(slug, "no direct hero-to-request anchor link")
    if "+19093756685" not in source:
        record(slug, "priority 909 phone number is missing")

    sibling = "washer-dryer-pickup" if kind == "appliance-pickup" else "appliance-pickup"
    if f"/{city}-{sibling}/" not in source:
        record(slug, "missing direct link to companion service page")

    structured_nodes = []
    for match in re.finditer(
        r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        source, re.I | re.S
    ):
        try:
            data = json.loads(match.group(1))
            structured_nodes.extend(data.get("@graph", [data]) if isinstance(data, dict) else [])
        except json.JSONDecodeError as exc:
            record(slug, f"invalid JSON-LD: {exc.msg}")
    webpages = [node for node in structured_nodes if node.get("@type") == "WebPage"]
    if len(webpages) != 1:
        record(slug, "expected one WebPage structured-data entry")
    else:
        preferred = webpages[0].get("primaryImageOfPage")
        if isinstance(preferred, dict):
            preferred = preferred.get("url") or preferred.get("contentUrl")
        if local_asset(preferred or "") != local_asset(hero_image):
            record(slug, "WebPage primaryImageOfPage does not match the real hero image")


def main() -> int:
    sitemap_urls, sitemap_images = load_sitemaps()
    for city in CITIES:
        for kind in KINDS:
            check(city, kind, sitemap_urls, sitemap_images)
    if ERRORS:
        for error in ERRORS:
            print("FAIL:", error)
        print(f"FAILED: {len(ERRORS)} issue(s) found across {CHECKED} page(s)")
        return 1
    print(f"PASS: all {CHECKED} city/intent pages pass canonical, title, photo/sitemap consistency, form, phone, link and schema checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
