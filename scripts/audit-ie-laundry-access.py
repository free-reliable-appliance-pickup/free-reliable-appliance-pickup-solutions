#!/usr/bin/env python3
"""Offline regression guard for eight existing Inland Empire laundry pickup forms.

Does not transmit customer data, test live Formspree delivery, or assert service availability.
"""
from pathlib import Path
import re
import sys

CITIES = {
    "eastvale": "Eastvale",
    "jurupa-valley": "Jurupa Valley",
    "moreno-valley": "Moreno Valley",
    "menifee": "Menifee",
    "perris": "Perris",
    "murrieta": "Murrieta",
    "banning": "Banning",
    "beaumont": "Beaumont",
}
FORM_RE = re.compile(r"<form\b[^>]*>[\s\S]*?</form>", re.I)
SELECT_RE = re.compile(r"<select\b([^>]*)>([\s\S]*?)</select>", re.I)
INPUT_RE = re.compile(r"<input\b[^>]*>", re.I)
OPTION_RE = re.compile(r"<option\b[^>]*>", re.I)


def attribute(tag, name):
    match = re.search(r'(?<![\w:-])' + re.escape(name) + r'\s*=\s*["\x27]([^"\x27]*)["\x27]', tag, re.I)
    return match.group(1) if match else None


def required(tag):
    return bool(re.search(r"(?<![\w:-])required(?=\s|=|>|$)", tag, re.I))


def check_form(html, slug, city):
    problems = []
    forms = FORM_RE.findall(html)
    if len(forms) != 1:
        return [f"{slug}: expected exactly one pickup form (found {len(forms)})"]
    form = forms[0]
    opening_tag = form.split(">", 1)[0] + ">"
    if attribute(opening_tag, "action") != "https://formspree.io/f/mvzeapzd":
        problems.append(f"{slug}: form action must match the exact Formspree endpoint")
    inputs = INPUT_RE.findall(form)
    selects = [(attrs, options) for attrs, options in SELECT_RE.findall(form)]
    fields = [attribute(tag, "name") for tag in inputs]
    fields += [attribute("<select " + attrs + ">", "name") for attrs, _ in selects]
    fields += [attribute(tag, "name") for tag in re.findall(r"<textarea\b[^>]*>", form, re.I)]
    for field in ("name", "phone", "address", "zip", "appliance", "condition", "location", "stairs"):
        if fields.count(field) != 1:
            problems.append(f"{slug}: {field} must occur exactly once")
    for field, value in (
        ("source_page", slug + "-washer-dryer-pickup"),
        ("state", "California"),
        ("service", "Washer and dryer pickup"),
    ):
        matches = [tag for tag in inputs if attribute(tag, "name") == field]
        if len(matches) != 1 or attribute(matches[0], "value") != value or attribute(matches[0], "type") != "hidden":
            problems.append(f"{slug}: missing or incorrect hidden {field} attribution")
    # Some pages use a static hidden city; Banning/Beaumont already have a
    # native required visible city with the correct default. Preserve both.
    city_inputs = [tag for tag in inputs if attribute(tag, "name") == "city"]
    if len(city_inputs) != 1 or attribute(city_inputs[0], "value") != city or (
        attribute(city_inputs[0], "type") != "hidden" and not required(city_inputs[0])
    ):
        problems.append(f"{slug}: missing or incorrect city attribution")
    for field in ("name", "phone", "address", "zip"):
        matches = [tag for tag in inputs if attribute(tag, "name") == field]
        if len(matches) != 1 or not required(matches[0]):
            problems.append(f"{slug}: {field} must be required")
    for field in ("appliance", "condition", "location", "stairs"):
        found = [(attrs, options) for attrs, options in selects
                 if attribute("<select " + attrs + ">", "name") == field]
        if len(found) != 1:
            problems.append(f"{slug}: {field} must be one native select control")
            continue
        attrs, options = found[0]
        if not required("<select " + attrs + ">"):
            problems.append(f"{slug}: {field} selector must be required")
        first = OPTION_RE.search(options)
        if not first or attribute(first.group(), "value") != "":
            problems.append(f"{slug}: {field} selector must start with a blank-value prompt")
        # A later selected option silently chooses a real answer even if the
        # first option is empty; native required validation would not fire.
        if any(re.search(r"(?<![\w:-])selected(?=\s|=|>|$)", tag, re.I)
               for tag in OPTION_RE.findall(options)[1:]):
            problems.append(f"{slug}: {field} has a nonblank selected default")
        if field in ("location", "stairs") and "not sure" not in options.lower() and "unknown" not in options.lower():
            problems.append(f"{slug}: {field} must allow an honest unknown answer")
    return problems


def self_test():
    slug = "eastvale"
    city = "Eastvale"
    fixed = '<form action="https://formspree.io/f/mvzeapzd" method="POST">'
    for key, value in (("source_page", slug + "-washer-dryer-pickup"),
                       ("state", "California"), ("city", city),
                       ("service", "Washer and dryer pickup")):
        fixed += f'<input type="hidden" name="{key}" value="{value}">'
    for field in ("name", "phone", "address", "zip"):
        fixed += f'<input name="{field}" required>'
    for field in ("appliance", "condition", "location", "stairs"):
        fixed += f'<select name="{field}" required><option value="">Select</option><option>Unknown / not sure</option></select>'
    fixed += '</form>'
    assert check_form(fixed, slug, city) == [], "hidden-city positive fixture failed"
    visible_city = fixed.replace(
        '<input type="hidden" name="city" value="Eastvale">',
        '<input name="city" value="Eastvale" required>',
    )
    assert check_form(visible_city, slug, city) == [], "visible-required-city positive fixture failed"
    assert check_form(
        visible_city.replace('<input name="city" value="Eastvale" required>',
                             '<input name="city" value="Eastvale">'),
        slug, city,
    ), "optional visible city escaped"
    negative = [
        fixed.replace('name="location" required', 'name="location"'),
        fixed.replace('<select name="stairs" required><option value="">',
                      '<select name="stairs" required><option value="none">'),
        fixed.replace('name="city" value="Eastvale"', 'name="city" value=""'),
        fixed.replace('<select name="location" required><option value="">Select</option><option>Unknown / not sure</option></select>', ''),
        fixed.replace('name="source_page"', 'name="source_missing"'),
        fixed.replace('name="location" required', 'data-name="location" required'),
        fixed.replace('name="location" required', 'name="location" data-required="true"'),
        fixed.replace('https://formspree.io/f/mvzeapzd"', 'https://formspree.io/f/mvzeapzd-typo"'),
        fixed.replace(
            '<select name="location" required><option value="">Select</option><option>Unknown / not sure</option></select>',
            '<input name="location" required>',
        ),
        fixed.replace(
            '<select name="location" required><option value="">Select</option><option>Unknown / not sure</option></select>',
            '<select name="location" required><option value="">Select</option><option selected>Unknown / not sure</option></select>',
        ),
    ]
    for i, broken in enumerate(negative, 1):
        assert check_form(broken, slug, city), f"negative fixture {i} escaped"
    print("PASS: two valid city-layout fixtures and eleven negative intake regressions")


def main():
    self_test()
    failures = []
    for slug, city in CITIES.items():
        path = Path(slug + "-washer-dryer-pickup") / "index.html"
        if not path.is_file():
            failures.append(f"{slug}: missing existing laundry page")
            continue
        failures += check_form(path.read_text(encoding="utf-8"), slug, city)
    if failures:
        print("\n".join(failures))
        sys.exit(1)
    print(f"PASS: {len(CITIES)} existing Inland Empire laundry intake forms validated without any form submission")


if __name__ == "__main__":
    main()
