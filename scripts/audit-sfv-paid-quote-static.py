#!/usr/bin/env python3
"""VGM: inspect source-only California static paid quote fallback."""
from html.parser import HTMLParser
from pathlib import Path

PAGES = {
    # California regional forms must preserve optional consent without JavaScript.
    "inland-empire-appliance-pickup": "inland-empire-appliance-pickup/index.html",
    "san-gabriel-valley-appliance-pickup": "san-gabriel-valley-appliance-pickup/index.html",
    # SGV source-only fallback: no JavaScript needed for customer quote preference.
    "pasadena-appliance-pickup": "pasadena-appliance-pickup/index.html",
    "arcadia-appliance-pickup": "arcadia-appliance-pickup/index.html",
    "san-fernando-appliance-pickup": "san-fernando-appliance-pickup/index.html",
    "san-fernando-washer-dryer-pickup": "san-fernando-washer-dryer-pickup/index.html",
    "north-hollywood-appliance-pickup": "north-hollywood-appliance-pickup/index.html",
    "san-fernando-valley-appliance-pickup": "san-fernando-valley-appliance-pickup/index.html",
    "van-nuys-appliance-pickup": "van-nuys-appliance-pickup/index.html",
    "granada-hills-appliance-pickup": "granada-hills-appliance-pickup/index.html",
    "pacoima-appliance-pickup": "pacoima-appliance-pickup/index.html",
    "northridge-appliance-pickup": "northridge-appliance-pickup/index.html",
    "mission-hills-appliance-pickup": "mission-hills-appliance-pickup/index.html",
    "sylmar-appliance-pickup": "sylmar-appliance-pickup/index.html",
    # Other verified California customer forms: same owner-approved no-JS fallback.
    "burbank-appliance-pickup": "burbank-appliance-pickup/index.html",
    "glendale-appliance-pickup": "glendale-appliance-pickup/index.html",
    "calabasas-appliance-pickup": "calabasas-appliance-pickup/index.html",
    "fresno-appliance-pickup": "fresno-appliance-pickup/index.html",
    "orange-county-appliance-pickup": "orange-county-appliance-pickup/index.html",
    "anaheim-appliance-pickup": "anaheim-appliance-pickup/index.html",
    "irvine-appliance-pickup": "irvine-appliance-pickup/index.html",
    # Verified existing OC no-JS quote fallback repairs (2026-10-24).
    "santa-ana-appliance-pickup": "santa-ana-appliance-pickup/index.html",
    "lake-forest-appliance-pickup": "lake-forest-appliance-pickup/index.html",
    "ontario-appliance-pickup": "ontario-appliance-pickup/index.html",
    # Existing Inland Empire request forms: approved quote choice works without JS.
    "montclair-appliance-pickup": "montclair-appliance-pickup/index.html",
    "chino-appliance-pickup": "chino-appliance-pickup/index.html",
    "chino-hills-appliance-pickup": "chino-hills-appliance-pickup/index.html",
    "redlands-appliance-pickup": "redlands-appliance-pickup/index.html",
    # Verified IE intake gaps: static quote preference also works without JavaScript.
    "colton-appliance-pickup": "colton-appliance-pickup/index.html",
    "bloomington-appliance-pickup": "bloomington-appliance-pickup/index.html",
    "highland-appliance-pickup": "highland-appliance-pickup/index.html",
    # Verified Riverside County and San Bernardino city no-JS consent gaps (2026-10-24).
    "corona-appliance-pickup": "corona-appliance-pickup/index.html",
    "moreno-valley-appliance-pickup": "moreno-valley-appliance-pickup/index.html",
    "san-bernardino-appliance-pickup": "san-bernardino-appliance-pickup/index.html",
    # Verified Azusa and Irwindale no-JS quote consent gaps (2026-10-24).
    "azusa-appliance-pickup": "azusa-appliance-pickup/index.html",
    "irwindale-appliance-pickup": "irwindale-appliance-pickup/index.html",
    # Verified existing SGV city form no-JS quote gaps (2026-10-24).
    "covina-appliance-pickup": "covina-appliance-pickup/index.html",
    "west-covina-appliance-pickup": "west-covina-appliance-pickup/index.html",
    "el-monte-appliance-pickup": "el-monte-appliance-pickup/index.html",
    "la-puente-appliance-pickup": "la-puente-appliance-pickup/index.html",
    "baldwin-park-appliance-pickup": "baldwin-park-appliance-pickup/index.html",
    "temple-city-appliance-pickup": "temple-city-appliance-pickup/index.html",
    "rosemead-appliance-pickup": "rosemead-appliance-pickup/index.html",
    "monterey-park-appliance-pickup": "monterey-park-appliance-pickup/index.html",
    "san-gabriel-appliance-pickup": "san-gabriel-appliance-pickup/index.html",
    "alhambra-appliance-pickup": "alhambra-appliance-pickup/index.html",
    # Verified San Gabriel Valley no-JS customer quote gaps (2026-10-24).
    "duarte-appliance-pickup": "duarte-appliance-pickup/index.html",
    "monrovia-appliance-pickup": "monrovia-appliance-pickup/index.html",
    "glendora-appliance-pickup": "glendora-appliance-pickup/index.html",
    # Verified Whittier, Montebello and Rialto customer quote-choice gaps (2026-10-24).
    "whittier-appliance-pickup": "whittier-appliance-pickup/index.html",
    "montebello-appliance-pickup": "montebello-appliance-pickup/index.html",
    "rialto-appliance-pickup": "rialto-appliance-pickup/index.html",
    # Verified Southeast Los Angeles County optional quote consent (2026-10-24).
    "pico-rivera-appliance-pickup": "pico-rivera-appliance-pickup/index.html",
    "norwalk-appliance-pickup": "norwalk-appliance-pickup/index.html",
    "downey-appliance-pickup": "downey-appliance-pickup/index.html",
    "la-mirada-appliance-pickup": "la-mirada-appliance-pickup/index.html",
    "cerritos-appliance-pickup": "cerritos-appliance-pickup/index.html",
    # Verified Southeast LA customer consent: static no-JS fallback (2026-10-24).
    "long-beach-appliance-pickup": "long-beach-appliance-pickup/index.html",
    "bellflower-appliance-pickup": "bellflower-appliance-pickup/index.html",
    "compton-appliance-pickup": "compton-appliance-pickup/index.html",
    "south-gate-appliance-pickup": "south-gate-appliance-pickup/index.html",
    # Verified coastal Orange County static quote consent gaps (2026-10-24).
    "huntington-beach-appliance-pickup": "huntington-beach-appliance-pickup/index.html",
    "costa-mesa-appliance-pickup": "costa-mesa-appliance-pickup/index.html",
    "newport-beach-appliance-pickup": "newport-beach-appliance-pickup/index.html",
    "laguna-niguel-appliance-pickup": "laguna-niguel-appliance-pickup/index.html",
    # Verified SGV and OC customer no-JS quote choices (2026-10-24).
    "san-marino-appliance-pickup": "san-marino-appliance-pickup/index.html",
    "sierra-madre-appliance-pickup": "sierra-madre-appliance-pickup/index.html",
    "buena-park-appliance-pickup": "buena-park-appliance-pickup/index.html",
    "yorba-linda-appliance-pickup": "yorba-linda-appliance-pickup/index.html",
    "mission-viejo-appliance-pickup": "mission-viejo-appliance-pickup/index.html",
}
# Existing Los Angeles appliance-category forms use descriptive source-page attribution.
# Validate the no-JavaScript quote choice without changing the source identifiers.
LA_SPECIALTY_SOURCE = {
    "los-angeles-refrigerator-pickup": "Los Angeles refrigerator page",
    "los-angeles-freezer-pickup": "Los Angeles freezer page",
    "los-angeles-stove-oven-pickup": "Los Angeles stove oven page",
}
# Same owner-approved fallback on four existing Oregon request forms.
OREGON_PAGES = {
    "portland-appliance-pickup": "portland-appliance-pickup/index.html",
    "salem-appliance-pickup": "salem-appliance-pickup/index.html",
    "portland-washer-dryer-pickup": "portland-washer-dryer-pickup/index.html",
    "salem-washer-dryer-pickup": "salem-washer-dryer-pickup/index.html",
}
ENDPOINT = "https://formspree.io/f/mvzeapzd"

class Forms(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms = []
        self.active = None
    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == "form":
            self.active = {"attrs": attrs, "inputs": [], "selects": []}
            self.forms.append(self.active)
        elif self.active is not None:
            if tag == "input": self.active["inputs"].append(attrs)
            if tag == "select": self.active["selects"].append({"attrs": attrs, "options": [], "option_attrs": []})
            if tag == "option" and self.active["selects"]:
                self.active["selects"][-1]["options"].append(attrs.get("value"))
                self.active["selects"][-1]["option_attrs"].append(attrs)
    def handle_endtag(self, tag):
        if tag == "form": self.active = None

def inspect(label, html, expected_source=None):
    parser = Forms(); parser.feed(html)
    problems = []
    forms = [f for f in parser.forms if f["attrs"].get("action") == ENDPOINT]
    if len(forms) != 1:
        return [f"{label}: expected exactly one approved Formspree form, got {len(forms)}"]
    form = forms[0]
    if form["attrs"].get("method", "").lower() != "post": problems.append(f"{label}: must POST")
    inputs = form["inputs"]
    if len([a for a in inputs if a.get("name") == "source_page" and a.get("value") == (expected_source or label)]) != 1:
        problems.append(f"{label}: missing source_page attribution")
    if len([a for a in inputs if a.get("name") == "phone" and a.get("type") == "tel" and "required" in a]) != 1:
        problems.append(f"{label}: required telephone missing")
    choices = [s for s in form["selects"] if s["attrs"].get("name") == "paid_removal_preference"]
    if len(choices) != 1:
        problems.append(f"{label}: expected one static optional paid quote selector")
    else:
        s = choices[0]
        if "required" in s["attrs"]: problems.append(f"{label}: paid quote selector must be optional")
        if s["options"] != ["", "free_only", "quote_ok"]:
            problems.append(f"{label}: default / free-only / quote-only consent values changed")
        if any("selected" in a for a in s["option_attrs"][1:]):
            problems.append(f"{label}: paid quote or free-only must not be preselected")
    return problems

def fixture_checks():
    label = "san-fernando-valley-appliance-pickup"
    good = (
        f'<form action="{ENDPOINT}" method="POST">'
        f'<input type="hidden" name="source_page" value="{label}">'
        '<input name="phone" type="tel" required>'
        '<select name="paid_removal_preference">'
        '<option value=""></option><option value="free_only"></option>'
        '<option value="quote_ok"></option></select></form>'
    )
    assert inspect(label, good) == [], "valid optional quote preference rejected"
    unsafe = (
        good.replace('<option value=""></option>', '<option value="quote_ok"></option>'),
        good.replace('<select name="paid_removal_preference">', '<select required name="paid_removal_preference">'),
        good.replace('name="paid_removal_preference"', 'name="unknown"'),
        good.replace('type="tel" required', 'type="tel"'),
        good.replace('name="source_page"', 'name="other_page"'),
        good.replace(ENDPOINT, "https://example.org/unauthorized"),
        good.replace('<option value="quote_ok"></option>', '<option value="quote_ok" selected></option>'),
    )
    for tampered in unsafe:
        assert inspect(label, tampered), "unsafe fixture went undetected"
    special = good.replace(f'value="{label}"', 'value="Los Angeles refrigerator page"')
    assert not inspect("los-angeles-refrigerator-pickup", special, "Los Angeles refrigerator page")
    assert inspect("los-angeles-refrigerator-pickup", special, "wrong attribution")

if __name__ == "__main__":
    fixture_checks()
    errors = []
    for label, path in {**PAGES, **OREGON_PAGES}.items():
        errors.extend(inspect(label, Path(path).read_text(encoding="utf-8")))
    for label, source in LA_SPECIALTY_SOURCE.items():
        path = Path(label) / "index.html"
        errors.extend(inspect(label, path.read_text(encoding="utf-8"), source))
    # Guard against silently accepting automatic paid consent.
    first = Path(next(iter(PAGES.values()))).read_text(encoding="utf-8")
    assert "quote_ok" in first and 'value=""' in first
    print(f"SFV_STATIC_PAID_QUOTE_PAGES {len(PAGES)}")
    print(f"CALIFORNIA_STATIC_PAID_QUOTE_PAGES {len(PAGES)}")
    print(f"OREGON_STATIC_PAID_QUOTE_PAGES {len(OREGON_PAGES)}")
    print(f"LA_SPECIALTY_STATIC_PAID_QUOTE_PAGES {len(LA_SPECIALTY_SOURCE)}")
    print(f"TOTAL_STATIC_PAID_QUOTE_PAGES {len(PAGES) + len(OREGON_PAGES) + len(LA_SPECIALTY_SOURCE)}")
    print(f"SFV_STATIC_PAID_QUOTE_ERRORS {len(errors)}")
    for error in errors: print("FAIL:", error)
    raise SystemExit(1 if errors else 0)
