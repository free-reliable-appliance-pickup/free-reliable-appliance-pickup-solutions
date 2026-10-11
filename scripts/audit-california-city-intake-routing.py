#!/usr/bin/env python3
"""Audit existing California general-city appliance intake routing.

Strictly checks the vetted repair set; other pages are printed as a read-only
inventory for a later city-vs-regional eligibility review. Never writes pages,
submits customer data, changes indexability, or assumes pickup coverage.
"""
from pathlib import Path
import re
import sys

REPAIRED = (
    "bell", "bell-gardens", "commerce", "maywood", "artesia", "cudahy",
    "signal-hill", "vernon", "paramount", "la-mirada", "cerritos",
    "south-gate", "santa-fe-springs", "huntington-park", "lynwood",
    "compton", "carson", "inglewood", "hawthorne", "gardena", "lawndale",
    "beverly-hills", "malibu", "el-segundo", "culver-city",
    "santa-monica", "manhattan-beach", "redondo-beach", "calabasas",
    "west-hollywood",
    "bakersfield",
    "banning",
    "berkeley",
    "calimesa",
    "carlsbad",
    "cathedral-city",
    "chula-vista",
    "coachella",
    "concord",
    "coronado",
    "cypress",
    "del-mar",
    "desert-hot-springs",
    "el-cajon",
    "encinitas",
    "escondido",
    "fremont",
    "hawaiian-gardens",
    "hayward",
    "hermosa-beach",
    "imperial-beach",
    "indian-wells",
    "indio",
    "la-habra",
    "la-habra-heights",
    "la-mesa",
    "la-palma",
    "la-quinta",
    "lakewood-ca",
    "lemon-grove",
    "loma-linda",
    "lomita",
    "los-alamitos",
    "menifee",
    "murrieta",
    "muscoy",
    "national-city",
    "oakland",
    "oceanside",
    "oxnard",
    "palm-desert",
    "palm-springs",
    "palo-alto",
    "perris",
    "poway",
    "rancho-mirage",
    "richmond",
    "san-fernando",
    "san-francisco",
    "san-jose",
    "san-luis-obispo",
    "san-marcos",
    "santa-barbara",
    "santa-clara",
    "santa-maria",
    "santee",
    "seal-beach",
    "solana-beach",
    "south-el-monte",
    "stanton",
    "sunnyvale",
    "ventura",
    "villa-park",
    "visalia",
    "vista",
    "walnut-creek",
    "wildomar",
)
FORM_ENDPOINT = "https://formspree.io/f/mvzeapzd"
errors = []

def field(form, name):
    pattern = r"<(?:input|select|textarea)\b[^>]*\bname=[" + chr(34) + chr(39) + "]" + re.escape(name) + "[" + chr(34) + chr(39) + r"][^>]*>"
    match = re.search(pattern, form, re.I | re.S)
    return match.group(0) if match else ""

def form_for(html):
    forms = re.findall(r"<form\b[^>]*>[\s\S]*?</form>", html, re.I)
    forms = [x for x in forms if FORM_ENDPOINT in x]
    return forms

for slug in REPAIRED:
    path = Path(f"{slug}-appliance-pickup") / "index.html"
    if not path.exists():
        errors.append(f"{slug}: file missing")
        continue
    html = path.read_text(encoding="utf-8", errors="replace")
    forms = form_for(html)
    if len(forms) != 1:
        errors.append(f"{slug}: expected exactly 1 Formspree form, got {len(forms)}")
        continue
    form = forms[0]
    city = "Lakewood" if slug == "lakewood-ca" else " ".join(p.title() for p in slug.split("-"))
    for name in ("city", "state", "source_page", "phone", "appliance", "condition"):
        if not field(form, name):
            errors.append(f"{slug}: missing field {name}")
    for name, val in (("city", city), ("state", "California"), ("source_page", slug + "-appliance-pickup")):
        tag = field(form, name)
        if f'value="{val}"' not in tag:
            errors.append(f"{slug}: {name} not set to {val!r}")
    phone = field(form, "phone")
    for hint in ('type="tel"', 'autocomplete="tel"', 'inputmode="tel"'):
        if hint not in phone:
            errors.append(f"{slug}: phone missing {hint}")
    if 'src="/assets/customer-routing.js"' not in html:
        errors.append(f"{slug}: customer routing script not loaded")
    if len(re.findall(r"<h1\b", html, re.I)) != 1:
        errors.append(f"{slug}: H1 count is not exactly 1")

# A county-wide form cannot silently assert a particular city.
county_path = Path("fresno-county-appliance-pickup") / "index.html"
if not county_path.exists():
    errors.append("fresno-county: page missing")
else:
    county_html = county_path.read_text(encoding="utf-8", errors="replace")
    county_forms = form_for(county_html)
    if len(county_forms) != 1:
        errors.append("fresno-county: expected exactly one pickup form")
    else:
        county_form = county_forms[0]
        county_city = field(county_form, "city")
        if 'type="text"' not in county_city or "required" not in county_city or 'type="hidden"' in county_city:
            errors.append("fresno-county: pickup city must be an explicitly required customer input")
        if not field(county_form, "state") or not field(county_form, "source_page"):
            errors.append("fresno-county: missing source/state attribution")
        if 'src="/assets/customer-routing.js"' not in county_html:
            errors.append("fresno-county: customer routing script not loaded")

# Two priority laundry forms must retain location and source attribution even
# when browser JavaScript fails or is disabled. Do not hardcode cities on hubs.
LAUNDRY_CITY_FORMS = {
    "alhambra": "Alhambra",
    "baldwin-park": "Baldwin Park",
}
for slug, city in LAUNDRY_CITY_FORMS.items():
    path = Path(f"{slug}-washer-dryer-pickup") / "index.html"
    if not path.is_file():
        errors.append(f"{slug} laundry: missing source HTML")
        continue
    html = path.read_text(encoding="utf-8", errors="replace")
    forms = form_for(html)
    if len(forms) != 1:
        errors.append(f"{slug} laundry: expected exactly one pickup request form")
        continue
    form = forms[0]
    for key, value in (("city", city), ("state", "California"),
                       ("source_page", f"{slug}-washer-dryer-pickup")):
        tag = field(form, key)
        if not tag or f'value="{value}"' not in tag:
            errors.append(f"{slug} laundry: missing or incorrect {key} attribution")
    if 'type="hidden"' not in field(form, "city"):
        errors.append(f"{slug} laundry: source city must be an explicit hidden input")
    if len(re.findall(r'\\bname="city"', form)) != 1:
        errors.append(f"{slug} laundry: expected exactly one explicit city field")
    for key in ("phone", "appliance", "condition"):
        if not field(form, key):
            errors.append(f"{slug} laundry: missing {key}")
    phone = field(form, "phone")
    for hint in ('type="tel"', 'autocomplete="tel"', 'inputmode="tel"'):
        if hint not in phone:
            errors.append(f"{slug} laundry: phone missing {hint}")
    if 'src="/assets/customer-routing.js"' not in html:
        errors.append(f"{slug} laundry: routing script missing")

diagnostic = []
for path in sorted(Path(".").glob("*-appliance-pickup/index.html")):
    html = path.read_text(encoding="utf-8", errors="replace")
    forms = form_for(html)
    if len(forms) != 1:
        continue
    form = forms[0]
    if 'name="state" value="California"' not in form:
        continue
    if not field(form, "city"):
        diagnostic.append(path.parent.name)

print("REPAIRED_CITY_FORMS_TESTED", len(REPAIRED))
print("LAUNDRY_CITY_FORMS_TESTED", len(LAUNDRY_CITY_FORMS))
print("STRICT_ERRORS", len(errors))
for error in errors:
    print("ERROR", error)
print("READ_ONLY_OTHER_CA_APPLIANCE_PAGES_MISSING_CITY", len(diagnostic))
if diagnostic:
    errors.append(f"{len(diagnostic)} California page forms still missing city attribution")
print("NOTE: inventory includes regional hubs and does not prove every such page needs a fixed city.")
for slug in diagnostic[:70]:
    print("READ_ONLY_MISSING_CITY", slug)
sys.exit(1 if errors else 0)
