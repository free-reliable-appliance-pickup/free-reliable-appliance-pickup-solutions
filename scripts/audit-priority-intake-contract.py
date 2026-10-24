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
# Targeted mobile input-hint regression checks for verified OC and IE form repairs.
MOBILE_HINT_PAGES = {
    "orange-appliance-pickup", "laguna-hills-appliance-pickup",
    "mission-viejo-appliance-pickup", "san-clemente-appliance-pickup",
    "placentia-appliance-pickup",
    "laguna-niguel-appliance-pickup",
    "bloomington-appliance-pickup", "colton-appliance-pickup",
    "highland-appliance-pickup",
    # Verified Corona, Moreno Valley and San Bernardino customer mobile hints.
    "corona-appliance-pickup", "moreno-valley-appliance-pickup",
    "san-bernardino-appliance-pickup",
    "pasadena-appliance-pickup", "arcadia-appliance-pickup",
    "san-dimas-appliance-pickup", "la-verne-appliance-pickup",
    # Verified Long Beach / Bellflower / Compton / South Gate mobile intake hints.
    "long-beach-appliance-pickup", "bellflower-appliance-pickup",
    "compton-appliance-pickup", "south-gate-appliance-pickup",
    # Verified Southeast Los Angeles County mobile form input repairs.
    "pico-rivera-appliance-pickup",
    "norwalk-appliance-pickup",
    "downey-appliance-pickup",
    "la-mirada-appliance-pickup",
    "cerritos-appliance-pickup",
    # Verified Whittier, Montebello and Rialto phone/ZIP input repairs.
    "whittier-appliance-pickup", "montebello-appliance-pickup",
    "rialto-appliance-pickup",
    # Existing SGV forms repaired for mobile keyboard and autofill.
    "covina-appliance-pickup",
    "west-covina-appliance-pickup",
    "el-monte-appliance-pickup",
    "la-puente-appliance-pickup",
    "baldwin-park-appliance-pickup",
    "temple-city-appliance-pickup",
    "rosemead-appliance-pickup",
    "monterey-park-appliance-pickup",
    "san-gabriel-appliance-pickup",
    "alhambra-appliance-pickup",
    # Verified Chino, Chino Hills, Pomona, Claremont and Redlands keypad hints.
    "chino-appliance-pickup", "chino-hills-appliance-pickup",
    "pomona-appliance-pickup", "claremont-appliance-pickup",
    "redlands-appliance-pickup",
    # Verified five-city California telephone/ZIP mobile input hints.
    "riverside-appliance-pickup", "anaheim-appliance-pickup",
    "ontario-appliance-pickup", "rancho-cucamonga-appliance-pickup",
    "fontana-appliance-pickup",
}

# Existing general-market pages only. Do not invent or publish new city URLs.
CITIES = (
    "rancho-cucamonga", "fontana", "upland", "claremont",
    "la-verne", "san-dimas", "pomona", "pasadena", "arcadia",
    "riverside", "portland", "salem", "vancouver", "seattle",
    "tacoma", "spokane", "denver", "aurora", "phoenix",
    "columbus", "fresno", "ontario", "montclair",
    "san-bernardino", "corona", "moreno-valley", "bloomington", "colton", "highland", "monterey-park",
    "whittier", "montebello", "rialto",
    "palm-springs", "la-canada-flintridge", "altadena", "san-marino",
    "la-mirada", "cerritos", "pico-rivera", "downey",
    "norwalk", "long-beach", "bellflower", "compton", "south-gate",
    "south-el-monte", "san-fernando", "sylmar",
    "temecula", "murrieta", "victorville", "palm-desert",
    "loma-linda", "banning", "beaumont", "hemet",
    "hesperia", "apple-valley", "adelanto", "phelan", "el-mirage",
    "walnut", "rowland-heights", "la-crescenta", "sierra-madre",
    "chino", "chino-hills", "west-covina", "covina",
    "glendora", "monrovia", "duarte", "san-gabriel",
    "el-monte", "azusa", "rosemead", "temple-city",
    "south-pasadena", "glendale", "burbank",
    "ventura", "oxnard", "malibu",
    "santa-monica", "calabasas", "west-hollywood",
    "north-hollywood", "santa-clarita",
    "anaheim", "irvine", "huntington-beach", "santa-ana",
    "orange", "laguna-hills", "mission-viejo", "san-clemente", "placentia",
    "garden-grove", "fullerton", "yorba-linda",
    "costa-mesa", "newport-beach", "laguna-niguel",
    "van-nuys", "granada-hills", "pacoima", "northridge", "mission-hills",
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

    # Fresno-only mobile keypad hints; do not change form validation or routing.
    if page_label == "fresno-appliance-pickup":
        if len(phones) == 1 and phones[0][1].get("inputmode") != "tel":
            errors.append(f"{page_label}: phone must hint telephone keypad")
        zips = fields.get("zip", [])
        if len(zips) != 1 or zips[0][0] != "input" or zips[0][1].get("inputmode") != "numeric":
            errors.append(f"{page_label}: ZIP must hint numeric keypad")

    if page_label in MOBILE_HINT_PAGES:
        if len(phones) != 1 or phones[0][1].get("autocomplete") != "tel" or phones[0][1].get("inputmode") != "tel":
            errors.append(f"{page_label}: phone must provide telephone autofill and keypad hints")
        zips = fields.get("zip", [])
        if len(zips) != 1 or zips[0][0] != "input" or zips[0][1].get("autocomplete") != "postal-code" or zips[0][1].get("inputmode") != "numeric":
            errors.append(f"{page_label}: ZIP must provide postal-code autofill and numeric keypad hints")

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
    oc_good = good.replace('value="home"', 'value="orange-appliance-pickup"').replace(
        '<input type="tel" name="phone" required>',
        '<input type="tel" name="phone" required autocomplete="tel" inputmode="tel">'
        '<input name="zip" autocomplete="postal-code" inputmode="numeric">',
    )
    assert not inspect(oc_good, "orange-appliance-pickup"), "valid OC mobile fixture rejected"
    assert inspect(oc_good.replace('inputmode="tel"', 'inputmode="text"'), "orange-appliance-pickup"), "bad phone keypad passed"
    assert inspect(oc_good.replace('autocomplete="postal-code"', 'autocomplete="off"'), "orange-appliance-pickup"), "bad ZIP autofill passed"
    ie_good = oc_good.replace("orange-appliance-pickup", "colton-appliance-pickup")
    assert not inspect(ie_good, "colton-appliance-pickup"), "valid IE mobile fixture rejected"
    assert inspect(ie_good.replace('inputmode="numeric"', 'inputmode="text"'), "colton-appliance-pickup"), "bad IE ZIP keypad passed"
    assert inspect(ie_good.replace('autocomplete="tel"', 'autocomplete="off"'), "colton-appliance-pickup"), "bad IE phone autofill passed"
    sgv_good = oc_good.replace("orange-appliance-pickup", "arcadia-appliance-pickup")
    assert not inspect(sgv_good, "arcadia-appliance-pickup"), "valid SGV mobile fixture rejected"
    assert inspect(sgv_good.replace('inputmode="tel"', 'inputmode="text"'), "arcadia-appliance-pickup"), "bad SGV phone keypad passed"
    assert inspect(sgv_good.replace('autocomplete="postal-code"', 'autocomplete="off"'), "arcadia-appliance-pickup"), "bad SGV ZIP autofill passed"
    ca_good = oc_good.replace("orange-appliance-pickup", "riverside-appliance-pickup")
    assert not inspect(ca_good, "riverside-appliance-pickup"), "valid CA ZIP fixture rejected"
    assert inspect(ca_good.replace('autocomplete="postal-code"', 'autocomplete="off"'), "riverside-appliance-pickup"), "missing CA ZIP autofill passed"
    ie5_good = oc_good.replace("orange-appliance-pickup", "fontana-appliance-pickup")
    assert not inspect(ie5_good, "fontana-appliance-pickup"), "valid CA telephone fixture rejected"
    assert inspect(ie5_good.replace('inputmode="tel"', 'inputmode="text"'), "fontana-appliance-pickup"), "missing CA phone keypad passed"
    ie6_good = oc_good.replace("orange-appliance-pickup", "chino-appliance-pickup")
    assert not inspect(ie6_good, "chino-appliance-pickup"), "valid Chino mobile fixture rejected"
    assert inspect(ie6_good.replace('inputmode="tel"', 'inputmode="text"'), "chino-appliance-pickup"), "bad Chino phone keypad passed"
    print(f"FIXTURE_TESTS_PASSED 7 positive + {len(negative) + 9} negative")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0

    pages = [("home", Path("index.html"))]
    pages.extend((f"{city}-appliance-pickup", Path(city + "-appliance-pickup") / "index.html") for city in CITIES)
    # Existing Valley regional hub uses the same customer request contract.
    pages.append(("san-fernando-valley-appliance-pickup", Path("san-fernando-valley-appliance-pickup/index.html")))
    # Existing request-only state hub; same Formspree intake contract, no coverage expansion.
    pages.append(("idaho-appliance-pickup", Path("idaho-appliance-pickup/index.html")))
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
