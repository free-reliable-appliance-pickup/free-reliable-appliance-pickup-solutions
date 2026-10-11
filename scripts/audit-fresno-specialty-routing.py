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
    if 'src="/assets/customer-routing.js"' not in html:
        errors.append(f"{slug}: routing script not loaded")
    if PHONE_LINK not in html:
        errors.append(f"{slug}: missing published authorized 310 contact link")
    if len(re.findall(r"<h1\b", html, re.I)) != 1:
        errors.append(f"{slug}: expected exactly one H1")
    if not re.search(r'<button\b[^>]*\btype="submit"', form, re.I):
        errors.append(f"{slug}: missing explicit submit button")

print("FRESNO_SPECIALTY_ROUTING_FORMS_CHECKED", len(SLUGS))
print("FRESNO_SPECIALTY_ROUTING_ERRORS", len(errors))
for issue in errors:
    print("ERROR", issue)
sys.exit(1 if errors else 0)
