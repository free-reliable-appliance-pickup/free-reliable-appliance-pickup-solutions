#!/usr/bin/env python3
"""Check the qualified appliance-pickup request forms on priority city pages.

Static source audit only; it does not submit customer data or verify a live deployment.
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
""".split()

BASE_FIELDS = {
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
                self.errors.append("unexpected label closing tag")
                self.depth = 0

def named_fields(form):
    return set(re.findall(r'\\bname\\s*=\\s*["\\\']([^"\\\']+)["\\\']', form, re.I))

def select_ok(form, field):
    pattern = rf'<select\\b([^>]*)\\bname=["\\\']{field}["\\\']([^>]*)>(.*?)</select>'
    m = re.search(pattern, form, re.I | re.S)
    if not m:
        return False
    attrs = m.group(1) + m.group(2)
    # A blank initial option avoids claiming an appliance is fully working
    # or selecting an appliance type without the customer's input.
    options = re.findall(r'<option\\b([^>]*)>', m.group(3), re.I | re.S)
    return bool(re.search(r'\\brequired\\b', attrs, re.I) and options and
                re.search(r'\\bvalue=["\\\']["\\\']', options[0], re.I))

errors = []
for city in CITIES:
    file = Path(city + "-appliance-pickup") / "index.html"
    if not file.is_file():
        errors.append(f"{city}: missing {file}")
        continue
    html = file.read_text(encoding="utf-8", errors="replace")
    forms = re.findall(r'<form\\b[^>]*>.*?</form>', html, re.I | re.S)
    form = next((x for x in forms if "formspree.io/f/mvzeapzd" in x), None)
    if not form:
        errors.append(f"{city}: no expected Formspree intake form")
        continue
    names = named_fields(form)
    missing = BASE_FIELDS - names
    if "location" not in names and "floor" not in names:
        missing.add("location/floor")
    if missing:
        errors.append(f"{city}: missing fields: {', '.join(sorted(missing))}")
    if not re.search(r'<button\\b[^>]*\\btype=["\\\']submit["\\\']', form, re.I):
        errors.append(f"{city}: missing submit button")
    audit = LabelAudit()
    audit.feed(form)
    if audit.depth != 0 or audit.errors:
        errors.append(f"{city}: label markup invalid: {audit.errors} depth={audit.depth}")
    for field in ("appliance", "condition"):
        if not select_ok(form, field):
            errors.append(f"{city}: {field} must be required with blank first option")

print(f"PRIORITY_INTAKE_FORMS_CHECKED {len(CITIES)}")
print(f"PRIORITY_INTAKE_ERRORS {len(errors)}")
for error in errors:
    print("ERROR", error)
sys.exit(1 if errors else 0)
