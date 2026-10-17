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


# Existing indexable California specialty forms keep static campaign source,
# original city/state/appliance/condition and mobile keypad, even without JS.
CALIFORNIA_SPECIALTY_ATTRIBUTION = (
    "anaheim-refrigerator-pickup", "costa-mesa-refrigerator-pickup",
    "fontana-freezer-pickup", "fontana-refrigerator-pickup",
    "huntington-beach-refrigerator-pickup", "irvine-refrigerator-pickup",
    "ontario-freezer-pickup", "ontario-refrigerator-pickup",
    "ontario-stove-oven-pickup", "pomona-freezer-pickup",
    "pomona-refrigerator-pickup", "pomona-stove-oven-pickup",
    "riverside-freezer-pickup", "riverside-refrigerator-pickup",
    "riverside-stove-oven-pickup", "san-bernardino-freezer-pickup",
    "san-bernardino-refrigerator-pickup", "san-bernardino-stove-oven-pickup",
    "santa-ana-refrigerator-pickup",
)
for slug in CALIFORNIA_SPECIALTY_ATTRIBUTION:
    page = Path(slug) / "index.html"
    if not page.is_file():
        errors.append(f"{slug}: missing specialty request page")
        continue
    html = page.read_text(encoding="utf-8", errors="replace")
    form = next((f for f in re.findall(r'<form\b[^>]*>.*?</form>', html, re.I | re.S)
                 if 'formspree.io/f/mvzeapzd' in f), "")
    if not form:
        errors.append(f"{slug}: no pickup form")
        continue
    if form.count('name="source_page"') != 1 or f'name="source_page" value="{slug}"' not in form:
        errors.append(f"{slug}: missing or duplicate static provenance")
    for name in ("city", "state", "condition", "appliance"):
        if f'name="{name}"' not in form:
            errors.append(f"{slug}: missing original routing field {name}")
    phone = re.search(r'<input\b[^>]*name="phone"[^>]*>', form, re.I)
    for hint in ('type="tel"', 'autocomplete="tel"', 'inputmode="tel"'):
        if not phone or hint not in phone.group(0):
            errors.append(f"{slug}: phone missing {hint}")
    if 'src="/assets/customer-routing.js"' not in html:
        errors.append(f"{slug}: original customer routing script missing")


# Legacy noindex foothill specialty pages still accept customer requests.
# Preserve original city-specific provenance while leaving SEO consolidation alone.
FOOTHILL_NOINDEX_SPECIALTY_SLUGS = (
    "claremont-freezer-pickup", "claremont-refrigerator-pickup",
    "claremont-stove-oven-pickup", "la-verne-freezer-pickup",
    "la-verne-refrigerator-pickup", "la-verne-stove-oven-pickup",
    "san-dimas-freezer-pickup", "san-dimas-refrigerator-pickup",
    "san-dimas-stove-oven-pickup", "upland-freezer-pickup",
    "upland-refrigerator-pickup", "upland-stove-oven-pickup",
)
for slug in FOOTHILL_NOINDEX_SPECIALTY_SLUGS:
    path = Path(slug) / "index.html"
    if not path.is_file():
        errors.append(f"{slug}: page missing")
        continue
    html = path.read_text(encoding="utf-8", errors="replace")
    form = next((x for x in re.findall(r'<form\b[^>]*>.*?</form>', html, re.I | re.S)
                 if 'formspree.io/f/mvzeapzd' in x), "")
    if not form or form.count('name="source_page"') != 1 or f'name="source_page" value="{slug}"' not in form:
        errors.append(f"{slug}: static source missing or incorrect")
    for name in ("city", "state", "appliance", "condition"):
        if f'name="{name}"' not in form:
            errors.append(f"{slug}: missing required existing {name}")
    phone = re.search(r'<input\b[^>]*name="phone"[^>]*>', form, re.I)
    for hint in ('type="tel"', 'autocomplete="tel"', 'inputmode="tel"'):
        if not phone or hint not in phone.group(0):
            errors.append(f"{slug}: phone missing {hint}")
    if 'name="robots" content="noindex, follow' not in html:
        errors.append(f"{slug}: protected noindex status changed")
    if 'src="/assets/customer-routing.js"' not in html:
        errors.append(f"{slug}: missing customer router")

# Protect priority lead attribution and Everett's explicit condition selection.
# Operational checks only: do not change city pages' indexing or SEO experiments.
ATTRIBUTION_PAGES = (
    "rancho-cucamonga", "upland", "fontana", "portland", "salem",
    "denver", "aurora", "claremont", "la-verne", "san-dimas", "pomona",
    "ontario", "montclair", "west-covina", "keizer", "lakewood",
    "everett", "seattle", "tacoma",
)
for city in ATTRIBUTION_PAGES:
    slug = city + "-appliance-pickup"
    source = Path(slug) / "index.html"
    if not source.is_file():
        errors.append(f"{slug}: missing priority pickup page")
        continue
    raw = source.read_text(encoding="utf-8", errors="replace")
    form = next((v for v in re.findall(r'<form\b[^>]*>.*?</form>', raw, re.I | re.S)
                 if 'formspree.io/f/mvzeapzd' in v), "")
    if not form:
        errors.append(f"{slug}: missing Formspree request form")
        continue
    if form.count('name="source_page"') != 1 or f'name="source_page" value="{slug}"' not in form:
        errors.append(f"{slug}: incorrect source page attribution")
    if form.count('name="service"') != 1 or 'name="service" value="General major appliance pickup"' not in form:
        errors.append(f"{slug}: incorrect service attribution")
    phone = re.search(r'<input\b[^>]*name="phone"[^>]*>', form, re.I)
    if not phone or not re.search(r'\brequired\b', phone.group(0), re.I):
        errors.append(f"{slug}: phone must be required")
    condition = re.search(r'<select\b[^>]*name="condition"[^>]*>.*?</select>', form, re.I | re.S)
    if not condition or not re.search(r'<select\b[^>]*\brequired\b', condition.group(0), re.I):
        errors.append(f"{slug}: explicit required condition selection missing")
    if city == "everett":
        if 'name="robots" content="noindex, follow' not in raw:
            errors.append("everett: noindex policy changed")
        for field in ("city", "state", "appliance", "appliances_access_condition", "property_type", "photos_available"):
            if f'name="{field}"' not in form:
                errors.append(f"everett: missing {field} field")

# Keep Spokane requests usable without changing its coverage-dependent noindex policy.
spokane_source = Path("spokane-appliance-pickup/index.html")
if not spokane_source.is_file():
    errors.append("spokane: missing request page")
else:
    spokane_html = spokane_source.read_text(encoding="utf-8", errors="replace")
    if 'name="robots" content="noindex, follow' not in spokane_html or 'href="https://freereliableappliancepickup.com/service-areas/"' not in spokane_html:
        errors.append("spokane: protected consolidation metadata changed")
    spokane_form = next((f for f in re.findall(r'<form\b[^>]*>.*?</form>', spokane_html, re.I | re.S) if 'formspree.io/f/mvzeapzd' in f), "")
    if not spokane_form:
        errors.append("spokane: missing direct customer request")
    else:
        for key in ("source_page", "service", "state", "city", "zip", "appliance", "condition", "phone"):
            if f'name="{key}"' not in spokane_form:
                errors.append(f"spokane: missing {key}")
        for key in ("appliance", "condition"):
            if not select_ok(spokane_form, key):
                errors.append(f"spokane: {key} selection must be required with blank prompt")


# Prevent Central Valley lead-classification regressions. Each of these
# existing city forms must submit its precise service without JavaScript.
CENTRAL_VALLEY_SERVICE_TAGS = {
    "fresno-appliance-pickup": "General major appliance pickup",
    "fresno-washer-dryer-pickup": "Washer and dryer pickup",
    "fresno-refrigerator-pickup": "Refrigerator pickup",
    "fresno-freezer-pickup": "Freezer pickup",
    "fresno-stove-oven-pickup": "Stove range and oven pickup",
    "stockton-appliance-pickup": "General major appliance pickup",
    "stockton-washer-dryer-pickup": "Washer and dryer pickup",
    "sacramento-appliance-pickup": "General major appliance pickup",
    "sacramento-washer-dryer-pickup": "Washer and dryer pickup",
}
for slug, service in CENTRAL_VALLEY_SERVICE_TAGS.items():
    path = Path(slug) / "index.html"
    if not path.is_file():
        errors.append(f"{slug}: missing Central Valley form page")
        continue
    raw = path.read_text(encoding="utf-8", errors="replace")
    forms = re.findall(r'<form\b[^>]*>.*?</form>', raw, re.I | re.S)
    intake = [f for f in forms if "formspree.io/f/mvzeapzd" in f]
    if len(intake) != 1:
        errors.append(f"{slug}: expected one Formspree pickup form")
        continue
    form = intake[0]
    if form.count('name="service"') != 1 or f'name="service" value="{service}"' not in form:
        errors.append(f"{slug}: missing or incorrect service classification")
    if form.count('name="source_page"') != 1 or f'name="source_page" value="{slug}"' not in form:
        errors.append(f"{slug}: missing or incorrect source page")
    phone = re.search(r'<input\b[^>]*name="phone"[^>]*>', form, re.I)
    condition = re.search(r'<select\b[^>]*name="condition"[^>]*>', form, re.I)
    if not phone or not re.search(r'\brequired\b', phone.group(0), re.I):
        errors.append(f"{slug}: required phone missing")
    if not condition or not re.search(r'\brequired\b', condition.group(0), re.I):
        errors.append(f"{slug}: required condition missing")

print("CENTRAL_VALLEY_SERVICE_TAG_FORMS_CHECKED", len(CENTRAL_VALLEY_SERVICE_TAGS))


# Washington request pages: maintain the established noindex policy on city
# partner-review pages, and keep local lead provenance reliable without JS.
WASHINGTON_REQUEST_FORMS = {
    "seattle-appliance-pickup": ("Seattle", True),
    "tacoma-appliance-pickup": ("Tacoma", True),
    "olympia-appliance-pickup": ("Olympia", True),
    "puget-sound-appliance-pickup": (None, False),
    "washington-appliance-pickup": (None, False),
}
for slug, (city, intentionally_noindex) in WASHINGTON_REQUEST_FORMS.items():
    path = Path(slug) / "index.html"
    if not path.exists():
        errors.append(f"{slug}: missing Washington pickup page")
        continue
    raw = path.read_text(encoding="utf-8", errors="replace")
    form = next((v for v in re.findall(r'<form\b[^>]*>.*?</form>', raw, re.I | re.S)
                 if "formspree.io/f/mvzeapzd" in v), "")
    if not form:
        errors.append(f"{slug}: expected established Formspree request form")
        continue
    for name, value in (("source_page", slug), ("state", "Washington"),
                        ("service", "General major appliance pickup")):
        if form.count(f'name="{name}"') != 1 or f'name="{name}" value="{value}"' not in form:
            errors.append(f"{slug}: incorrect or duplicated {name}")
    if city and f'name="city"' not in form:
        errors.append(f"{slug}: pickup city missing")
    for name in ("appliance", "condition"):
        if not select_ok(form, name):
            errors.append(f"{slug}: required {name} choice is missing or has no blank prompt")
    phone = re.search(r'<input\b[^>]*name="phone"[^>]*>', form, re.I)
    if not phone or not re.search(r'\brequired\b', phone.group(0), re.I):
        errors.append(f"{slug}: required phone input missing")
    elif 'type="tel"' not in phone.group(0):
        errors.append(f"{slug}: phone must show phone keypad on mobile")
    if intentionally_noindex:
        if not re.search(r'<meta[^>]+name="robots"[^>]+content="noindex', raw, re.I):
            errors.append(f"{slug}: protected noindex setting missing")
        if re.search(r'<meta[^>]+name="googlebot"[^>]+content="index', raw, re.I):
            errors.append(f"{slug}: conflicting googlebot index instruction")
print("WASHINGTON_REQUEST_FORMS_CHECKED", len(WASHINGTON_REQUEST_FORMS))

print("HIGH_DESERT_FORMS_CHECKED",len(HIGH_DESERT_FORMS))
print("OREGON_MOBILE_FORMS_CHECKED",len(OREGON_MOBILE_PAGES))
print(f"PRIORITY_INTAKE_FORMS_CHECKED {len(CITIES)}")
print(f"PRIORITY_INTAKE_ERRORS {len(errors)}")
for error in errors:
    print("ERROR", error)
sys.exit(1 if errors else 0)
