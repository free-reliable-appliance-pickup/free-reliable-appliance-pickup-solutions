#!/usr/bin/env python3
"""One-time South Carolina customer-facing California Gold Model cleanup."""
from pathlib import Path
import json
import re

manifest = json.loads(Path("data/ttg-state-batches/SC.json").read_text(encoding="utf8"))
assert manifest["state_code"] == "SC" and len(manifest["pages"]) == 251

changed = 0
for rel in manifest["pages"]:
    file = Path(rel)
    html = file.read_text(encoding="utf8")
    original = html
    match = re.search(r'<h1>Free (.*?) Pickup in (.*?)(?:, SC)?</h1>', html)
    if rel == "south-carolina-appliance-pickup/index.html":
        category = "Appliance"
        city = "South Carolina"
    elif match:
        category, city = match.group(1), match.group(2)
        city = city.replace(", SC", "")
    else:
        raise ValueError(f"Cannot identify main free-pickup heading: {rel}")
    category = category.replace("&amp; dryer", "&amp; Dryer")
    html = html.replace("Free Washer &amp; dryer", "Free Washer &amp; Dryer")

    html = re.sub(r'<h2>[^<]* used-appliance eligibility</h2>',
                  f'<h2>Free {category} Pickup Details in {city}</h2>', html)
    html = re.sub(r'<h2>How this eligibility request works</h2>',
                  f'<h2>How to Request Free {category} Pickup</h2>', html)
    html = html.replace("How the conditional request works",
                        f"How Free {category} Pickup Works in {city}")
    html = html.replace("These 50 city guides provide <strong>eligibility review only</strong>.",
                        "These 50 city guides explain how to request free appliance pickup.")
    html = html.replace("for eligibility review", "to review your pickup request")
    html = re.sub(r'>([^<>]+?) eligibility</a>',
                  lambda m: '>' + m.group(1) + ' Free Appliance Pickup</a>', html, flags=re.I)
    html = html.replace("Send " + city + " " + category.lower() + " request",
                        f"Request Free {category} Pickup in {city}")
    html = re.sub(r'\\beligibility\\b', 'pickup review', html, flags=re.I)
    html = re.sub(r'<button type="submit">[^<]+</button>',
                  f'<button type="submit">Request Free {category} Pickup</button>', html, count=1)

    section_match = re.search(r'<section id="request">[\\s\\S]*?</section>', html)
    if not section_match or "<form " not in section_match.group(0):
        raise ValueError(f"Missing request section: {rel}")
    section = section_match.group(0)
    html = html.replace(section, "", 1)
    if '<main id="main">' not in html:
        raise ValueError(f"Missing main: {rel}")
    html = html.replace('<main id="main">', '<main id="main">' + section, 1)

    if not (
        html.count('<h1') == 1
        and html.count('<form ') == 1
        and html.count('<section id="request">') == 1
        and '<main id="main"><section id="request">' in html
        and html.count('<figure><img') == 1
        and 'Free Reliable Appliance Pickup' in html
        and 'noindex, follow' in html
        and 'https://formspree.io/f/mvzeapzd' in html
        and '<link rel="canonical"' in html
        and not re.search(r'eligibility', html, re.I)
    ):
        raise ValueError(f"Failed final landing-page checks: {rel}")
    if html != original:
        file.write_text(html, encoding="utf8")
        changed += 1

print(f"South Carolina California model: {len(manifest['pages'])} pages checked; {changed} updated. All have brand, form first, free-pickup headings, one genuine illustrative photo, noindex, no eligibility labels.")
