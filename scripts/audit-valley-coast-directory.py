#!/usr/bin/env python3
"""VGM directory-link regression for the already published Valley and Coast pages.

Does not claim pickup availability, search ranking or Google indexation.
"""
from html.parser import HTMLParser
from pathlib import Path
import sys

LINKS = {
    "san-fernando-valley-appliance-pickup",
    "san-fernando-appliance-pickup",
    "van-nuys-appliance-pickup",
    "north-hollywood-appliance-pickup",
    "northridge-appliance-pickup",
    "granada-hills-appliance-pickup",
    "pacoima-appliance-pickup",
    "sylmar-appliance-pickup",
    "malibu-appliance-pickup",
    "malibu-washer-dryer-pickup",
    "ventura-appliance-pickup",
    "ventura-washer-dryer-pickup",
    "oxnard-appliance-pickup",
    "oxnard-washer-dryer-pickup",
    "calabasas-appliance-pickup",
    "santa-monica-appliance-pickup"
}
SECTION = "valley-coast-existing-request-pages"

class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.inside = False
        self.depth = 0
        self.links = []
        self.sections = 0
    def handle_starttag(self, tag, items):
        attrs = dict(items)
        if tag == "section" and attrs.get("id") == SECTION:
            self.sections += 1
            self.inside = True
            self.depth = 1
        elif self.inside:
            if tag in ("section", "div", "p", "h2", "h3", "a"):
                pass
            if tag == "a":
                self.links.append(attrs.get("href"))
    def handle_endtag(self, tag):
        if self.inside and tag == "section":
            self.inside = False

def main():
    path = Path("service-areas/index.html")
    source = path.read_text(encoding="utf-8")
    parser = Reader()
    parser.feed(source)
    problems = []
    if parser.sections != 1:
        problems.append(f"Expected exactly one curated section, found {parser.sections}")
    found = [h for h in parser.links if h and h.startswith("/")]
    expected = [f"/{p}/" for p in sorted(LINKS)]
    if sorted(found) != expected:
        problems.append("Curated section links differ from 16 approved existing request paths")
    for slug in sorted(LINKS):
        if not (Path(slug) / "index.html").is_file():
            problems.append(f"Missing destination {slug}/index.html")
        if source.count(f'href="/{slug}/"') != 1:
            problems.append(f"Directory should link exactly once to {slug}")
    if "document.querySelectorAll('main a[href]')" not in source:
        problems.append("Existing location-search link discovery was changed")
    section = source.split('id="' + SECTION + '"', 1)[-1].split("</section>", 1)[0]
    if "does not guarantee a partner or appointment" not in section:
        problems.append("Availability qualification message missing")
    print("VGM_DIRECTORY_TARGET_PAGES", len(LINKS))
    print("VGM_DIRECTORY_ERRORS", len(problems))
    for problem in problems:
        print("FAIL:", problem)
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
