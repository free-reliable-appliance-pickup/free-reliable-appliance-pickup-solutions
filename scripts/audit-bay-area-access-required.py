#!/usr/bin/env python3
"""Source-only guard for Oakland, Richmond and San Francisco pickup access.
No customer data is submitted. Passing never proves inbox receipt or deployment.
"""
from pathlib import Path
import re
import sys

CITIES = {
    "oakland": "Oakland",
    "richmond": "Richmond",
    "san-francisco": "San Francisco",
}
ACTION = 'action="https://formspree.io/f/mvzeapzd"'

def check(html, slug, city):
    errors = []
    forms = re.findall(r'<form\b[^>]*>.*?</form>', html, re.I | re.S)
    intake = [f for f in forms if ACTION in f]
    if len(intake) != 1:
        return [f"{slug}: expected one established Formspree form"]
    form = intake[0]
    for field, value in (
        ("source_page", slug + "-appliance-pickup"),
        ("city", city),
        ("state", "California"),
    ):
        if form.count(f'name="{field}"') != 1 or f'name="{field}" value="{value}"' not in form:
            errors.append(f"{slug}: missing or duplicate {field} attribution")
    for field in ("name", "phone", "address", "zip", "appliance", "condition"):
        tag = re.search(r'<(?:input|select)\b[^>]*\bname="' + field + r'"[^>]*>', form, re.I)
        if not tag or not re.search(r'\brequired\b', tag.group(0), re.I):
            errors.append(f"{slug}: {field} not required")
    for field in ("location", "stairs"):
        selects = re.findall(r'<select\b[^>]*\bname="' + field + r'"[^>]*>.*?</select>', form, re.I | re.S)
        if len(selects) != 1:
            errors.append(f"{slug}: expected one {field} select")
            continue
        select = selects[0]
        opening = select.split(">", 1)[0]
        if not re.search(r'\brequired\b', opening, re.I):
            errors.append(f"{slug}: {field} not required")
        if not re.search(r'<option\s+value="">', select, re.I):
            errors.append(f"{slug}: {field} has no blank prompt")
        elif not re.search(r'^<option\s+value="">', select.split(">", 1)[1], re.I):
            errors.append(f"{slug}: {field} blank prompt not first")
    if form.count('name="message"') != 1:
        errors.append(f"{slug}: access notes missing or duplicated")
    if slug in ("oakland", "san-francisco") and not re.search(
        r'<textarea\b[^>]*name="message"[^>]*\brequired\b', form, re.I
    ):
        errors.append(f"{slug}: previously required message weakened")
    if 'tel:+13107744304' not in html:
        errors.append(f"{slug}: original 310 telephone route missing")
    return errors

def self_test():
    sample = (
        '<form action="https://formspree.io/f/mvzeapzd" method="POST">'
        '<input type="hidden" name="source_page" value="oakland-appliance-pickup">'
        '<input type="hidden" name="city" value="Oakland">'
        '<input type="hidden" name="state" value="California">'
        + ''.join(f'<input name="{field}" required>' for field in
                  ("name", "phone", "address", "zip", "appliance", "condition"))
        + '<select name="location" required><option value="">Select location</option><option>Garage</option></select>'
        + '<select name="stairs" required><option value="">Select stairs</option><option>No Stairs</option></select>'
        + '<textarea name="message" required></textarea></form>'
        + '<a href="tel:+13107744304">Call</a>'
    )
    assert not check(sample, "oakland", "Oakland"), "valid fixture failed"
    bad = [
        sample.replace('name="location" required', 'name="location"'),
        sample.replace('<option value="">Select stairs</option>', '<option>No Stairs</option>'),
        sample.replace('name="stairs"', 'name="not_stairs"'),
        sample.replace('name="address" required', 'name="address"'),
        sample.replace('name="message" required', 'name="message"'),
        sample.replace('tel:+13107744304', 'tel:+19999999999'),
        sample.replace('value="Oakland"', 'value="Elsewhere"'),
    ]
    for i, fixture in enumerate(bad, 1):
        assert check(fixture, "oakland", "Oakland"), f"bad fixture {i} passed"
    print("BAY_AREA_ACCESS_FIXTURES_PASSED 1 positive + 7 negative")

def main():
    self_test()
    errors = []
    for slug, city in CITIES.items():
        path = Path(slug + "-appliance-pickup") / "index.html"
        if not path.is_file():
            errors.append(f"{slug}: missing existing page")
            continue
        errors.extend(check(path.read_text(encoding="utf-8"), slug, city))
    print("BAY_AREA_ACCESS_PAGES_CHECKED", len(CITIES))
    print("BAY_AREA_ACCESS_ERRORS", len(errors))
    for e in errors:
        print("FAIL", e)
    return bool(errors)

if __name__ == "__main__":
    sys.exit(main())
