#!/usr/bin/env python3
"""Texas customer-only form safety test: no recruitment promotion."""
from pathlib import Path
from html.parser import HTMLParser
import sys


class Extract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.forms = 0
        self.images = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a":
            self.links.append((a.get("href", ""), a.get("class", "")))
        if tag == "form":
            self.forms += 1
        if tag == "img":
            self.images += 1


page = Path("texas-appliance-pickup/index.html").read_text(encoding="utf-8")
parsed = Extract()
parsed.feed(page)
errors = []
if 'id="texas-pickup-partner-opportunity"' in page or '/partners/' in page:
    errors.append("customer page links to a recruiting application")
if 'recruit' in page.lower():
    errors.append("Texas customer page still contains recruitment copy")
if "<title>Free Appliance Pickup Texas | Request Eligibility Review</title>" not in page:
    errors.append("Texas SEO title lost accurate customer pickup intent")
if parsed.forms != 1 or "https://formspree.io/f/mvzeapzd" not in page:
    errors.append("original customer form changed")
if parsed.images != 2:
    errors.append("Texas statewide page should have brand logo and one real garage photo")
if '<meta name="robots" content="index, follow' not in page:
    errors.append("Texas statewide indexing directive changed")
if not page.index('id="texas-city-shortcut"') < page.index('id="texas-houston-gold-expansion"'):
    errors.append("Texas customer form shortcut is no longer before metro areas")
print("TEXAS_PARTNER_CTA_ERRORS", len(errors))
for error in errors:
    print("ERROR", error)
if errors:
    sys.exit(1)
print("PASS: Texas public page is customer-only with original form and real garage photo")
