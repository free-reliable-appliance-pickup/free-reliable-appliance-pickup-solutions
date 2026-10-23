#!/usr/bin/env python3
"""Regression guard for five existing, owner-page navigation links from SoCal hub.

Source audit only: does not prove Google rank, live deployment, or partner availability.
"""
from html.parser import HTMLParser
from pathlib import Path
import sys

PAGE = Path("southern-california-appliance-pickup/index.html")
LA = ("san-fernando-valley-appliance-pickup", "malibu-appliance-pickup")
COAST = ("ventura-appliance-pickup", "oxnard-appliance-pickup", "central-coast-appliance-pickup")

class LinkReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.append(dict(attrs).get("href"))

def check():
    s = PAGE.read_text(encoding="utf-8")
    errors = []
    la_start = "<section><h2>Los Angeles County & San Gabriel Valley</h2>"
    ca_start = '<section class="vgm-socal-ventura-coast-navigation-20261023" id="socal-ventura-coast-links">'
    orange_start = "<section><h2>Orange County & South Orange County</h2>"
    if any(s.count(x) != 1 for x in (la_start, ca_start, orange_start)):
        return ["Southern California regional owner sections missing or duplicate"]
    la = s.split(la_start, 1)[1].split("</section>", 1)[0]
    ca = s.split(ca_start, 1)[1].split("</section>", 1)[0]
    if s.index(la_start) >= s.index(ca_start) or s.index(ca_start) >= s.index(orange_start):
        errors.append("County/Valley/coast regional navigation appears out of order")
    for slug in LA + COAST:
        if not (Path(slug) / "index.html").is_file():
            errors.append(f"Target missing: {slug}/index.html")
        target = f"/{slug}/"
        parser = LinkReader()
        parser.feed(s)
        if parser.hrefs.count(target) != 1:
            errors.append(f"Expected exactly one outbound link to {target}")
        owning_section = la if slug in LA else ca
        section_parser = LinkReader()
        section_parser.feed(owning_section)
        if section_parser.hrefs.count(target) != 1:
            errors.append(f"Link must be in correct regional section: {target}")
    if "free pickup and a local provider are not guaranteed" not in ca.lower():
        errors.append("Coastal partner availability disclaimer missing")
    print("SOUTHERN_CALIFORNIA_ROUTE_LINKS", len(LA) + len(COAST))
    print("SOUTHERN_CALIFORNIA_ROUTE_ERRORS", len(errors))
    for msg in errors:
        print("FAIL:", msg)
    return errors

if __name__ == "__main__":
    sys.exit(1 if check() else 0)
