#!/usr/bin/env python3
"""Validate priority appliance pickup request forms in repository source.

Does not submit customer data or prove a live deployment has completed.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

CITIES = """
montclair san-bernardino chino chino-hills la-verne san-dimas pomona
upland claremont covina west-covina pasadena duarte altadena
temple-city san-marino alhambra el-monte baldwin-park la-puente
diamond-bar rowland-heights whittier pico-rivera montebello irwindale
azusa arcadia monrovia bradbury sierra-madre la-canada-flintridge
la-crescenta rosemead fresno sacramento stockton phoenix denver
aurora portland salem
rialto bloomington colton highland grand-terrace redlands yucaipa
moreno-valley jurupa-valley eastvale corona norco walnut
hacienda-heights avocado-heights south-san-jose-hills san-gabriel
monterey-park city-of-industry
""".split()

REQUIRED_FIELDS = {
    "name", "phone", "zip", "appliance", "condition",
    "condition_details", "stairs", "property_type",
    "photos_available", "message", "source_page", "city"
}

class LabelAudit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag == "label":
            self.depth += 1
            if self.depth > 1:
                self.errors.append("nested label")

    def handle_endtag(self, tag):
        if tag == "label":
            self.depth -= 1
            if self.depth < 0:
                self.errors.append("unexpected closing label")
                self.depth = 0

def fields_in(form):
    return set(re.findall(r'\bname\s*=\s*"([^"]+)"', form, re.I))

def select_ok(form, name):
    match = re.search(
        rf'<select\b([^>]*)\bname="{name}"([^>]*)>(.*?)</select>',
        form, re.I | re.S
    )
    if not match:
        return False
    attributes = match.group(1) + match.group(2)
    options = re.findall(r'<option\b([^>]*)>', match.group(3), re.I | re.S)
    return bool(
        re.search(r'\brequired\b', attributes, re.I)
        and options
        and re.search(r'\bvalue\s*=\s*""', options[0], re.I)
    )

errors = []
for city in CITIES:
    path = Path(city + "-appliance-pickup") / "index.html"
    if not path.is_file():
        errors.append(f"{city}: missing page")
        continue

    html = path.read_text(encoding="utf-8", errors="replace")
    forms = re.findall(r'<form\b[^>]*>.*?</form>', html, re.I | re.S)
    form = next((v for v in forms if "formspree.io/f/mvzeapzd" in v), None)
    if not form:
        errors.append(f"{city}: missing expected intake form")
        continue

    names = fields_in(form)
    missing = REQUIRED_FIELDS - names
    if "location" not in names and "floor" not in names:
        missing.add("location/floor")
    if missing:
        errors.append(f"{city}: missing {', '.join(sorted(missing))}")

    if not re.search(r'<button\b[^>]*\btype="submit"', form, re.I):
        errors.append(f"{city}: no submit button")
    labels = LabelAudit()
    labels.feed(form)
    if labels.depth or labels.errors:
        errors.append(f"{city}: invalid labels: {labels.errors}, depth={labels.depth}")

    for name in ("appliance", "condition"):
        if not select_ok(form, name):
            errors.append(f"{city}: {name} must be required with a blank first option")

# Protected foothill pages: technical contact/access corrections only.
# These source checks must not modify live form data or ranking content.
for foothill_city in ("la-crescenta", "montrose"):
    path = Path(f"{foothill_city}-appliance-pickup") / "index.html"
    if not path.is_file():
        errors.append(f"{foothill_city}: missing foothill page")
        continue
    html = path.read_text(encoding="utf-8", errors="replace")
    forms = re.findall(r'<form[^>]*>.*?</form>', html, re.I | re.S)
    form = next((v for v in forms if "formspree.io/f/mvzeapzd" in v), None)
    if not form:
        errors.append(f"{foothill_city}: missing pickup form")
        continue
    for field_name in ("location", "stairs"):
        if not select_ok(form, field_name):
            errors.append(f"{foothill_city}: {field_name} must have a blank required prompt")
    if "call or text 310-774-4304 with photos" in html:
        errors.append(f"{foothill_city}: contradictory 310 scheduling contact")
    if "call or text 909-375-6685 with photos" not in html:
        errors.append(f"{foothill_city}: missing approved 909 scheduling contact")

print("FOOTHILL_CONTACT_ACCESS_PAGES_TESTED 2")
# Real High Desert city forms must preserve exact lead provenance without JS.
HIGH_DESERT_FORMS = {
    "adelanto": "Adelanto",
    "victorville": "Victorville",
    "hesperia": "Hesperia",
    "apple-valley": "Apple Valley",
    "phelan": "Phelan",
}
for slug, city in HIGH_DESERT_FORMS.items():
    path = Path(slug + "-appliance-pickup") / "index.html"
    if not path.is_file():
        errors.append(f"{slug}: missing High Desert city page")
        continue
    html = path.read_text(encoding="utf-8", errors="replace")
    forms = re.findall(r'<form[^>]*>.*?</form>', html, re.I | re.S)
    intake = [f for f in forms if 'formspree.io/f/mvzeapzd' in f]
    if len(intake) != 1:
        errors.append(f"{slug}: expected one major appliance pickup form")
        continue
    form = intake[0]
    for name, value in (("city", city), ("state", "California"),
                        ("source_page", slug + "-appliance-pickup")):
        if f'name="{name}"' not in form or f'value="{value}"' not in form:
            errors.append(f"{slug}: missing {name} attribution")
    if form.count('name="source_page"') != 1:
        errors.append(f"{slug}: source page attribution is not unique")
    for name in ("appliance", "condition"):
        if f'name="{name}"' not in form and not (name == "appliance" and 'name="appliances"' in form):
            errors.append(f"{slug}: missing {name} request field")
    phone = re.search(r'<input[^>]*name="phone"[^>]*>', form, re.I)
    for hint in ('type="tel"', 'autocomplete="tel"', 'inputmode="tel"'):
        if not phone or hint not in phone.group(0):
            errors.append(f"{slug}: customer phone missing {hint}")
    if '909-375-6685' not in html:
        errors.append(f"{slug}: known High Desert 909 contact missing")
    if 'src="/assets/customer-routing.js"' not in html:
        errors.append(f"{slug}: client routing script missing")

# Keep real Oregon / Portland-Salem city request forms mobile-friendly.
# Source-level checks must work without JavaScript or remote network access.
OREGON_MOBILE_PAGES = (
    "portland-appliance-pickup", "salem-appliance-pickup",
    "keizer-appliance-pickup", "beaverton-appliance-pickup",
    "hillsboro-appliance-pickup", "gresham-appliance-pickup",
    "tigard-appliance-pickup", "happy-valley-appliance-pickup",
    "oregon-city-appliance-pickup", "portland-washer-dryer-pickup",
    "salem-washer-dryer-pickup",
)
for slug in OREGON_MOBILE_PAGES:
    path = Path(slug) / "index.html"
    if not path.is_file():
        errors.append(f"{slug}: missing Oregon request page")
        continue
    html = path.read_text(encoding="utf-8", errors="replace")
    forms = re.findall(r'<form[^>]*>.*?</form>', html, re.I | re.S)
    intake = [f for f in forms if 'formspree.io/f/mvzeapzd' in f]
    if len(intake) != 1:
        errors.append(f"{slug}: expected one pickup intake form")
        continue
    form = intake[0]
    if 'name="state" value="Oregon"' not in form:
        errors.append(f"{slug}: incorrect Oregon form state")
    for field_name in ("city", "source_page", "appliance", "condition"):
        if f'name="{field_name}"' not in form:
            errors.append(f"{slug}: missing {field_name} field")
    phone = re.search(r'<input[^>]*name="phone"[^>]*>', form, re.I)
    if not phone:
        errors.append(f"{slug}: phone input missing")
    else:
        for hint in ('type="tel"', 'autocomplete="tel"', 'inputmode="tel"'):
            if hint not in phone.group(0):
                errors.append(f"{slug}: phone missing {hint}")
    if 'src="/assets/customer-routing.js"' not in html:
        errors.append(f"{slug}: shared customer routing script missing")
    if '503-868-4455' not in html:
        errors.append(f"{slug}: current Oregon contact missing")


# All fourteen High Desert appliance and laundry forms must route without
# relying on JavaScript to invent page provenance or core intake fields.
# Technical-only checks: leave SEO experiment copy and ranking variables untouched.
HIGH_DESERT_INTAKE_SLUGS = (
    "victorville", "hesperia", "apple-valley",
    "adelanto", "phelan", "el-mirage", "high-desert",
)
for community in HIGH_DESERT_INTAKE_SLUGS:
    for service in ("appliance-pickup", "washer-dryer-pickup"):
        slug = f"{community}-{service}"
        path = Path(slug) / "index.html"
        if not path.is_file():
            errors.append(f"{slug}: missing High Desert intake page")
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        forms = re.findall(r'<form\b[^>]*>.*?</form>', html, re.I | re.S)
        intake = [f for f in forms if 'formspree.io/f/mvzeapzd' in f]
        if len(intake) != 1:
            errors.append(f"{slug}: expected exactly one pickup intake form")
            continue
        form = intake[0]
        if form.count('name="source_page"') != 1 or f'name="source_page" value="{slug}"' not in form:
            errors.append(f"{slug}: missing or incorrect static page provenance")
        if 'name="state" value="California"' not in form:
            errors.append(f"{slug}: missing California state")
        for name in ("city", "appliance", "condition"):
            if f'name="{name}"' not in form and not (name == "appliance" and 'name="appliances"' in form):
                errors.append(f"{slug}: missing routing/qualification field {name}")
        phone = re.search(r'<input\b[^>]*name="phone"[^>]*>', form, re.I)
        for hint in ('type="tel"', 'autocomplete="tel"', 'inputmode="tel"'):
            if not phone or hint not in phone.group(0):
                errors.append(f"{slug}: phone missing mobile hint {hint}")
        if '909-375-6685' not in html or 'src="/assets/customer-routing.js"' not in html:
            errors.append(f"{slug}: missing correct High Desert contact or routing script")


# Existing noindex RV city pages still receive requests; make sure their
# original equipment field is retained while customer-routing metadata works.
HIGH_DESERT_RV_CITIES = ("victorville", "hesperia", "apple-valley",
                        "adelanto", "phelan", "el-mirage")
for town in HIGH_DESERT_RV_CITIES:
    slug = town + "-rv-appliance-pickup"
    path = Path(slug) / "index.html"
    if not path.is_file():
        errors.append(f"{slug}: missing RV intake page")
        continue
    html = path.read_text(encoding="utf-8", errors="replace")
    forms = re.findall(r'<form\b[^>]*>.*?</form>', html, re.I | re.S)
    intake = [form for form in forms if 'formspree.io/f/mvzeapzd' in form]
    if len(intake) != 1:
        errors.append(f"{slug}: expected one RV intake form")
        continue
    form = intake[0]
    for name, value in (("source_page", slug),
                        ("state", "California"),
                        ("appliance", "RV Appliance / Equipment")):
        if f'name="{name}" value="{value}"' not in form:
            errors.append(f"{slug}: missing {name} routing metadata")
    for name in ("city", "rv_equipment", "condition", "phone"):
        if f'name="{name}"' not in form:
            errors.append(f"{slug}: missing original RV request field {name}")
    phone = re.search(r'<input\b[^>]*name="phone"[^>]*>', form, re.I)
    for hint in ('type="tel"', 'autocomplete="tel"', 'inputmode="tel"'):
        if not phone or hint not in phone.group(0):
            errors.append(f"{slug}: phone missing mobile hint {hint}")
    if 'content="noindex, follow' not in html or \
        'rel="canonical" href="https://freereliableappliancepickup.com/high-desert-rv-appliance-pickup/"' not in html:
        errors.append(f"{slug}: protected RV consolidation metadata altered")
    if '909-375-6685' not in html or 'src="/assets/customer-routing.js"' not in html:
        errors.append(f"{slug}: missing routing script or known High Desert phone")

rv_hub = Path("high-desert-rv-appliance-pickup/index.html")
if not rv_hub.is_file():
    errors.append("high-desert RV hub missing")
else:
    rv_html = rv_hub.read_text(encoding="utf-8", errors="replace")
    rv_form = next((form for form in re.findall(r'<form\b[^>]*>.*?</form>', rv_html, re.I | re.S)
                    if 'formspree.io/f/mvzeapzd' in form), "")
    for name in ("source_page", "state", "city", "appliance", "condition"):
        if f'name="{name}"' not in rv_form:
            errors.append(f"high-desert RV hub: missing routing field {name}")
    if '<input type="tel" name="phone" required autocomplete="tel" inputmode="tel">' not in rv_form:
        errors.append("high-desert RV hub: phone lacks mobile inputmode")
    if 'name="robots" content="index, follow' not in rv_html or \
        'rel="canonical" href="https://freereliableappliancepickup.com/high-desert-rv-appliance-pickup/"' not in rv_html:
        errors.append("high-desert RV hub: canonical or indexability altered")


# Specialty forms must include enough fields for customer-routing.js to wire
# submissions and preserve the intended Colorado/California market.
SPECIALTY_ROUTE_FIELDS = {
    "aurora-freezer-pickup": ("Colorado", "Aurora", "Freezer"),
    "aurora-refrigerator-pickup": ("Colorado", "Aurora", "Refrigerator"),
    "aurora-stove-oven-pickup": ("Colorado", "Aurora", "Stove / Range / Oven"),
    "denver-freezer-pickup": ("Colorado", "Denver", "Freezer"),
    "denver-refrigerator-pickup": ("Colorado", "Denver", "Refrigerator"),
    "denver-stove-oven-pickup": ("Colorado", "Denver", "Stove / Range / Oven"),
}
for slug, (state, city, appliance) in SPECIALTY_ROUTE_FIELDS.items():
    path = Path(slug) / "index.html"
    if not path.is_file():
        errors.append(f"{slug}: missing specialty page")
        continue
    html = path.read_text(encoding="utf-8", errors="replace")
    forms = re.findall(r'<form\b[^>]*>.*?</form>', html, re.I | re.S)
    form = next((f for f in forms if 'formspree.io/f/mvzeapzd' in f), "")
    if not form:
        errors.append(f"{slug}: missing pickup form")
        continue
    for name, value in (("state", state), ("city", city),
                        ("appliance", appliance), ("source_page", slug)):
        if f'name="{name}" value="{value}"' not in form:
            errors.append(f"{slug}: missing or mismatched {name}")
    if 'name="condition"' not in form or 'src="/assets/customer-routing.js"' not in html:
        errors.append(f"{slug}: missing condition or customer router")
    phone = re.search(r'<input\b[^>]*name="phone"[^>]*>', form, re.I)
    for hint in ('type="tel"', 'autocomplete="tel"', 'inputmode="tel"'):
        if not phone or hint not in phone.group(0):
            errors.append(f"{slug}: missing phone hint {hint}")

slug = "coachella-valley-refrigerator-pickup"
path = Path(slug) / "index.html"
if not path.is_file():
    errors.append(f"{slug}: missing regional refrigerator page")
else:
    html = path.read_text(encoding="utf-8", errors="replace")
    form = next((f for f in re.findall(r'<form\b[^>]*>.*?</form>', html, re.I | re.S)
                 if 'formspree.io/f/mvzeapzd' in f), "")
    for name in ("state", "source_page", "city", "appliance", "condition"):
        if f'name="{name}"' not in form:
            errors.append(f"{slug}: missing {name}")
    if 'name="state" value="California"' not in form or 'src="/assets/customer-routing.js"' not in html:
        errors.append(f"{slug}: regional routing not wired")
    phone = re.search(r'<input\b[^>]*name="phone"[^>]*>', form, re.I)
    for hint in ('type="tel"', 'autocomplete="tel"', 'inputmode="tel"'):
        if not phone or hint not in phone.group(0):
            errors.append(f"{slug}: missing phone hint {hint}")


# Phoenix category forms need a real appliance field, not only page context,
# so the shared customer-router can attach classification and condition review.
PHOENIX_SPECIALTY_APPLIANCES = {
    "phoenix-freezer-pickup": "Freezer",
    "phoenix-refrigerator-pickup": "Refrigerator",
    "phoenix-stove-oven-pickup": "Stove / Range / Oven",
}
for slug, appliance in PHOENIX_SPECIALTY_APPLIANCES.items():
    page = Path(slug) / "index.html"
    if not page.is_file():
        errors.append(f"{slug}: missing Phoenix category page")
        continue
    html = page.read_text(encoding="utf-8", errors="replace")
    form = next((f for f in re.findall(r'<form\b[^>]*>.*?</form>', html, re.I | re.S)
                 if 'formspree.io/f/mvzeapzd' in f), "")
    for name, value in (("appliance", appliance), ("state", "Arizona"),
                        ("city", "Phoenix"), ("source_page", slug)):
        if f'name="{name}" value="{value}"' not in form:
            errors.append(f"{slug}: missing or incorrect {name}")
    if 'name="condition"' not in form or 'src="/assets/customer-routing.js"' not in html:
        errors.append(f"{slug}: routing fields or script absent")
    phone = re.search(r'<input\b[^>]*name="phone"[^>]*>', form, re.I)
    for hint in ('type="tel"', 'autocomplete="tel"', 'inputmode="tel"'):
        if not phone or hint not in phone.group(0):
            errors.append(f"{slug}: missing phone {hint}")
    if '602-726-7552' not in html:
        errors.append(f"{slug}: Phoenix telephone was changed")


# Central Valley specialty pages previously had static classification but no
# city or shared router script, so leads could not acquire routing metadata.
CENTRAL_VALLEY_SPECIALTY_FORMS = {
    "sacramento-refrigerator-pickup": ("Sacramento", "Refrigerator"),
    "stockton-refrigerator-pickup": ("Stockton", "Refrigerator"),
    "stockton-stove-oven-pickup": ("Stockton", "Stove / Range / Oven"),
}
for slug, (city, appliance) in CENTRAL_VALLEY_SPECIALTY_FORMS.items():
    path = Path(slug) / "index.html"
    if not path.is_file():
        errors.append(f"{slug}: missing specialty page")
        continue
    html = path.read_text(encoding="utf-8", errors="replace")
    forms = re.findall(r'<form\b[^>]*>.*?</form>', html, re.I | re.S)
    form = next((f for f in forms if 'formspree.io/f/mvzeapzd' in f), "")
    for name, value in (("state", "California"), ("city", city),
                        ("appliance", appliance), ("source_page", slug)):
        if f'name="{name}" value="{value}"' not in form:
            errors.append(f"{slug}: incorrect or missing {name} routing metadata")
    if 'name="condition"' not in form or html.count('src="/assets/customer-routing.js"') != 1:
        errors.append(f"{slug}: condition or one shared routing script missing")
    phone = re.search(r'<input\b[^>]*name="phone"[^>]*>', form, re.I)
    for hint in ('type="tel"', 'autocomplete="tel"', 'inputmode="tel"'):
        if not phone or hint not in phone.group(0):
            errors.append(f"{slug}: missing phone mobile hint {hint}")
    if '310-774-4304' not in html:
        errors.append(f"{slug}: original Central Valley 310 contact missing")

print("HIGH_DESERT_FORMS_CHECKED",len(HIGH_DESERT_FORMS))
print("OREGON_MOBILE_FORMS_CHECKED",len(OREGON_MOBILE_PAGES))
print(f"PRIORITY_INTAKE_FORMS_CHECKED {len(CITIES)}")
print(f"PRIORITY_INTAKE_ERRORS {len(errors)}")
for error in errors:
    print("ERROR", error)
sys.exit(1 if errors else 0)
