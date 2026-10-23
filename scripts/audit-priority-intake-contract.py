#!/usr/bin/env python3
"""VGM regression guard for priority general-appliance customer request forms.

Checks source HTML, not delivery. A passing check never proves Formspree receipt,
a live GitHub Pages deployment, indexing, or organic rankings.
"""
from html.parser import HTMLParser
from pathlib import Path
import argparse
import sys

FORM_ACTION = "https://formspree.io/f/mvzeapzd"
SERVICE = "General major appliance pickup"
# Preserve existing meaningful form labels; do not rewrite customer pages as part of a test.
SOURCE_OVERRIDES = {"phoenix-appliance-pickup": "Phoenix city page"}
SERVICE_OVERRIDES = {"columbus-appliance-pickup": "general appliance pickup"}

# Existing general-market pages only. Do not invent or publish new city URLs.
CITIES = (
    "rancho-cucamonga", "fontana", "upland", "claremont",
    "la-verne", "san-dimas", "pomona", "pasadena", "arcadia",
    "riverside", "portland", "salem", "vancouver", "seattle",
    "tacoma", "spokane", "denver", "aurora", "phoenix",
    "columbus", "fresno", "ontario", "montclair",
    "san-bernardino", "bloomington", "monterey-park",
    "whittier", "montebello", "rialto",
    "palm-springs", "la-canada-flintridge", "altadena", "san-marino",
    "la-mirada", "cerritos", "pico-rivera", "downey",
    "norwalk", "long-beach", "south-el-monte", "san-fernando", "sylmar",
    "temecula", "murrieta", "victorville", "palm-desert",
    "loma-linda", "banning", "beaumont", "hemet",
    "hesperia", "apple-valley", "adelanto", "phelan", "el-mirage",
)


class FormReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.forms = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "form":
            self.current = {"attrs": attrs, "fields": []}
            self.forms.append(self.current)
        elif self.current is not None and tag in ("input", "select", "textarea"):
            self.current["fields"].append((tag, attrs))

    def handle_endtag(self, tag):
        if tag == "form":
            self.current = None


def inspect(page_html, page_label):
    parsed = FormReader()
    parsed.feed(page_html)
    pickup_forms = [
        f for f in parsed.forms
        if f["attrs"].get("action", "").rstrip("/") == FORM_ACTION
    ]
    errors = []
    if len(pickup_forms) != 1:
        return [f"{page_label}: expected exactly one customer Formspree form, found {len(pickup_forms)}"]

    form = pickup_forms[0]
    if form["attrs"].get("method", "").lower() != "post":
        errors.append(f"{page_label}: customer form must POST")

    fields = {}
    for tag, attrs in form["fields"]:
        name = attrs.get("name")
        if name:
            fields.setdefault(name, []).append((tag, attrs))

    for name, expected in (
        ("source_page", SOURCE_OVERRIDES.get(page_label, page_label)),
        ("service", SERVICE_OVERRIDES.get(page_label, SERVICE)),
    ):
        values = fields.get(name, [])
        if len(values) != 1:
            errors.append(f"{page_label}: expected one {name} field, found {len(values)}")
        elif values[0][0] != "input" or values[0][1].get("type", "").lower() != "hidden" or values[0][1].get("value") != expected:
            errors.append(f"{page_label}: invalid hidden {name} attribution")

    phones = fields.get("phone", [])
    if len(phones) != 1:
        errors.append(f"{page_label}: expected one phone field, found {len(phones)}")
    elif phones[0][0] != "input" or phones[0][1].get("type", "").lower() != "tel" or "required" not in phones[0][1]:
        errors.append(f"{page_label}: phone must be a required telephone input")

    return errors


def self_test():
    good = (
        '<form action="' + FORM_ACTION + '" method="POST">'
        '<input type="hidden" name="source_page" value="home">'
        '<input type="hidden" name="service" value="' + SERVICE + '">'
        '<input type="tel" name="phone" required>'
        '</form>'
    )
    assert not inspect(good, "home"), "valid fixture rejected"
    negative = {
        "no source": good.replace('name="source_page"', 'name="other"'),
        "wrong source": good.replace('value="home"', 'value="wrong"'),
        "no service": good.replace('name="service"', 'name="other_service"'),
        "no phone required": good.replace('name="phone" required', 'name="phone"'),
        "wrong method": good.replace('method="POST"', 'method="GET"'),
        "wrong endpoint": good.replace(FORM_ACTION, "https://example.org/form"),
        "two forms": good + good,
    }
    for name, test in negative.items():
        assert inspect(test, "home"), f"negative fixture passed incorrectly: {name}"
    print(f"FIXTURE_TESTS_PASSED 1 positive + {len(negative)} negative")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0

    pages = [("home", Path("index.html"))]
    pages.extend((f"{city}-appliance-pickup", Path(city + "-appliance-pickup") / "index.html") for city in CITIES)
    failures = []
    inspected = 0
    for label, path in pages:
        if not path.is_file():
            failures.append(f"{label}: page source does not exist: {path}")
            continue
        inspected += 1
        failures.extend(inspect(path.read_text(encoding="utf-8"), label))
    print(f"PRIORITY_INTAKE_PAGES_INSPECTED {inspected}")
    print(f"PRIORITY_INTAKE_EXPECTED {len(pages)}")
    print(f"PRIORITY_INTAKE_FAILURES {len(failures)}")
    for problem in failures:
        print("FAIL:", problem)
    return 1 if failures or inspected != len(pages) else 0


if __name__ == "__main__":
    sys.exit(main())
