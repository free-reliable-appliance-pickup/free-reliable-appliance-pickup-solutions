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
)
FORM_ENDPOINT = "https://formspree.io/f/mvzeapzd"
errors = []

def field(form, name):
    pattern = r"<(?:input|select|textarea)\\b[^>]*\\bname=[\\\"']" + re.escape(name) + r"[\\\"'][^>]*>"
    match = re.search(pattern, form, re.I | re.S)
    return match.group(0) if match else ""

def form_for(html):
    forms = re.findall(r"<form\\b[^>]*>[\\s\\S]*?</form>", html, re.I)
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
    city = " ".join(p.title() for p in slug.split("-"))
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
    if len(re.findall(r"<h1\\b", html, re.I)) != 1:
        errors.append(f"{slug}: H1 count is not exactly 1")

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
print("STRICT_ERRORS", len(errors))
for error in errors:
    print("ERROR", error)
print("READ_ONLY_OTHER_CA_APPLIANCE_PAGES_MISSING_CITY", len(diagnostic))
print("NOTE: inventory includes regional hubs and does not prove every such page needs a fixed city.")
for slug in diagnostic[:70]:
    print("READ_ONLY_MISSING_CITY", slug)
sys.exit(1 if errors else 0)
