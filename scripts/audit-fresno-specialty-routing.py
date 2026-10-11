#!/usr/bin/env python3
"""Check Fresno appliance-specific lead intake field compatibility.

Read-only source audit. Does not submit customer information or establish
real-world route availability.
"""
from pathlib import Path
import re
import sys

SLUGS = (
    "fresno-washer-dryer-pickup",
    "fresno-stove-oven-pickup",
    "fresno-freezer-pickup",
    "fresno-refrigerator-pickup",
)
FORM_ENDPOINT = "https://formspree.io/f/mvzeapzd"
PHONE_LINK = "tel:+13107744304"
errors = []

def input_tag(form, field):
    return next((
        match.group(0)
        for match in re.finditer(r"<input\b[^>]*>", form, re.I)
        if re.search(r'\bname=["\']' + re.escape(field) + r'["\']', match.group(0), re.I)
    ), "")

for slug in SLUGS:
    path = Path(slug) / "index.html"
    if not path.exists():
        errors.append(f"{slug}: missing page")
        continue
    html = path.read_text(encoding="utf-8", errors="replace")
    forms = re.findall(r"<form\b[^>]*>.*?</form>", html, re.I | re.S)
    forms = [form for form in forms if FORM_ENDPOINT in form]
    if len(forms) != 1:
        errors.append(f"{slug}: expected exactly one approved intake form, found {len(forms)}")
        continue
    form = forms[0]
    for name in ("state", "city", "source_page", "appliance", "condition", "phone", "zip"):
        if not re.search(r'\bname=["\']' + re.escape(name) + r'["\']', form, re.I):
            errors.append(f"{slug}: missing field {name}")
    for field, expected in (
        ("city", 'value="Fresno"'),
        ("state", 'value="California"'),
        ("source_page", f'value="{slug}"'),
    ):
        tag = input_tag(form, field)
        if 'type="hidden"' not in tag or expected not in tag:
            errors.append(f"{slug}: incorrect hidden {field} for lead routing")

    phone = input_tag(form, "phone")
    for attr in ('type="tel"', 'autocomplete="tel"', 'inputmode="tel"'):
        if attr not in phone:
            errors.append(f"{slug}: phone input missing {attr}")
    zip_input = input_tag(form, "zip")
    for attr in ('inputmode="numeric"', 'autocomplete="postal-code"'):
        if attr not in zip_input:
            errors.append(f"{slug}: ZIP input missing {attr}")
    if 'src="/assets/customer-routing.js"' not in html and 'src="../assets/customer-routing.js"' not in html:
        errors.append(f"{slug}: routing script not loaded")
    if PHONE_LINK not in html:
        errors.append(f"{slug}: missing published authorized 310 contact link")
    if len(re.findall(r"<h1\b", html, re.I)) != 1:
        errors.append(f"{slug}: expected exactly one H1")
    if not re.search(r'<button\b[^>]*\btype="submit"', form, re.I):
        errors.append(f"{slug}: missing explicit submit button")

# Searchers may land on Clovis, Sanger, Selma and Fowler when their
# appliance pickup address is actually in Fresno. Preserve a visible,
# editable city field to let customer-routing.js classify the address.
NEARBY_CITY_PAGES = {
    "clovis-appliance-pickup": "Clovis",
    "sanger-appliance-pickup": "Sanger",
    "selma-appliance-pickup": "Selma",
    "fowler-appliance-pickup": "Fowler",
}

for slug, original_city in NEARBY_CITY_PAGES.items():
    path = Path(slug) / "index.html"
    if not path.exists():
        errors.append(f"{slug}: missing nearby-city page")
        continue
    html = path.read_text(encoding="utf-8", errors="replace")
    forms = [item for item in re.findall(r"<form\b[^>]*>.*?</form>", html, re.I | re.S) if FORM_ENDPOINT in item]
    if len(forms) != 1:
        errors.append(f"{slug}: expected one approved nearby-city pickup form")
        continue
    form = forms[0]
    city = input_tag(form, "city")
    if not city or 'type="text"' not in city or 'required' not in city:
        errors.append(f"{slug}: actual pickup city is not customer-editable and required")
    if f'value="{original_city}"' not in city:
        errors.append(f"{slug}: prefilled city no longer matches page's local city")
    for name in ("state", "source_page", "appliance", "condition", "phone", "zip"):
        if f'name="{name}"' not in form:
            errors.append(f"{slug}: lead attribution field {name} missing")
    if 'src="/assets/customer-routing.js"' not in html and 'src="../assets/customer-routing.js"' not in html:
        errors.append(f"{slug}: missing customer routing script")
    if PHONE_LINK not in html:
        errors.append(f"{slug}: wrong contact line")

# A county-wide page must collect the actual city and ZIP separately;
# a combined city_zip field cannot be classified by customer-routing.js.
county_slug = "fresno-county-appliance-pickup"
county_path = Path(county_slug) / "index.html"
if not county_path.exists():
    errors.append("Fresno County pickup page missing")
else:
    html = county_path.read_text(encoding="utf-8", errors="replace")
    forms = [item for item in re.findall(r"<form\b[^>]*>.*?</form>", html, re.I | re.S) if FORM_ENDPOINT in item]
    if len(forms) != 1:
        errors.append("Fresno County page: expected exactly one pickup form")
    else:
        form = forms[0]
        city = input_tag(form, "city")
        zip_input = input_tag(form, "zip")
        if not city or 'type="text"' not in city or 'required' not in city or 'value=' in city:
            errors.append("Fresno County: actual city must be required and blank for entry")
        if not zip_input or 'required' not in zip_input:
            errors.append("Fresno County: ZIP must be a separate required field")
        if 'name="city_zip"' in form:
            errors.append("Fresno County: ambiguous combined city_zip field remains")
        for name in ("state", "source_page", "appliance", "condition"):
            if f'name="{name}"' not in form:
                errors.append(f"Fresno County: attribution field {name} missing")
        if 'src="/assets/customer-routing.js"' not in html and 'src="../assets/customer-routing.js"' not in html:
            errors.append("Fresno County: customer routing script missing")
        if PHONE_LINK not in html:
            errors.append("Fresno County: incorrect 310 area contact link")

print("FRESNO_SPECIALTY_ROUTING_FORMS_CHECKED", len(SLUGS))
print("FRESNO_NEARBY_ROUTING_FORMS_CHECKED", len(NEARBY_CITY_PAGES) + 1)
print("FRESNO_SPECIALTY_ROUTING_ERRORS", len(errors))
for issue in errors:
    print("ERROR", issue)
sys.exit(1 if errors else 0)
