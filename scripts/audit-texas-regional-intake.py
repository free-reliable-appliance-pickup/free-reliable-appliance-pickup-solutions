#!/usr/bin/env python3
"""Protect actual-city and machine-type labeling in Texas regional request forms."""
from pathlib import Path
import re
import sys

METROS = ("dallas-fort-worth", "austin-metro", "san-antonio-metro")
CATEGORIES = {
    "washer-dryer": "Washer and dryer set",
    "refrigerator": "Refrigerator",
    "freezer": "Freezer",
    "stove-oven": "Stove / range",
}
TARGETS = [(f"{metro}-{cat}-pickup/index.html", label)
           for metro in METROS for cat, label in CATEGORIES.items()]
TARGETS += [(f"{county}-county-tx-appliance-pickup/index.html", None)
            for county in ("dallas", "collin", "tarrant")]


def field(form, tag, name):
    found = re.findall(
        rf'<{tag}\b[^>]*\bname=["\']{re.escape(name)}["\'][^>]*>',
        form, flags=re.I)
    return found[0] if len(found) == 1 else ""


def verify(path, category):
    html = Path(path).read_text(encoding="utf-8")
    issues = []
    forms = re.findall(r'<form\b[^>]*>.*?</form>', html, flags=re.I | re.S)
    if len(forms) != 1 or "https://formspree.io/f/mvzeapzd" not in forms[0]:
        return ["Missing or incorrect single Formspree intake form"]
    form = forms[0]
    city = field(form, "input", "city")
    if not city or 'required' not in city or 'value=' in city:
        issues.append("Actual pickup city must be required and not prefilled")
    for key in ("name", "phone", "address", "zip"):
        if 'required' not in field(form, "input", key):
            issues.append(f"Missing required {key}")
    if 'pattern="[0-9]{5}"' not in field(form, "input", "zip"):
        issues.append("Invalid five-digit ZIP pattern")
    if not field(form, "input", "source_page"):
        issues.append("Lead source attribution missing")
    if 'required' not in field(form, "select", "photos_available"):
        issues.append("Photo availability not required")
    appliance_field = field(form, "select", "appliance")
    if 'required' not in appliance_field:
        issues.append("Appliance type not required")
    appliance_match = re.search(r'<select\b[^>]*name=["\']appliance["\'][^>]*>(.*?)</select>', form, re.S | re.I)
    options = appliance_match.group(1) if appliance_match else ""
    selected = re.findall(r'<option\b[^>]*\bselected\b[^>]*>(.*?)</option>', options, re.S | re.I)
    if category:
        if len(selected) != 1 or selected[0].strip() != category:
            issues.append(f"Expected category-specific default: {category}")
    else:
        if len(selected) != 1 or "value=\"\" selected disabled" not in options:
            issues.append("County form must require explicit appliance selection")
    if '<meta name="robots" content="noindex, follow">' not in html:
        issues.append("Request-only noindex safeguard altered")
    return issues


errors = []
for path, category in TARGETS:
    for issue in verify(path, category):
        errors.append(f"{path}: {issue}")
print("TEXAS_REGIONAL_FORMS_CHECKED", len(TARGETS))
if errors:
    for error in errors:
        print("FAIL", error)
    sys.exit(1)
print("PASS: 15 Texas forms preserve actual city, correctly selected appliance, photo intake, and noindex")
