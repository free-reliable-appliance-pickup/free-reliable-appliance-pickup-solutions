#!/usr/bin/env python3
"""Read-only guard for essential address, ZIP and photo intake in sixteen Orange County pages.

Does not send requests, verify live deployment, or establish operator coverage.
"""
from html.parser import HTMLParser
from pathlib import Path
import argparse
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LAUNDRY = {
    "costa-mesa": "Costa Mesa",
    "huntington-beach": "Huntington Beach",
    "dana-point": "Dana Point",
    "ladera-ranch": "Ladera Ranch",
    "coto-de-caza": "Coto de Caza",
    "laguna-beach": "Laguna Beach",
    "laguna-woods": "Laguna Woods",
    "trabuco-canyon": "Trabuco Canyon",
    "laguna-niguel": "Laguna Niguel",
    "rancho-santa-margarita": "Rancho Santa Margarita",
    "san-juan-capistrano": "San Juan Capistrano",
    "san-clemente": "San Clemente",
    "laguna-hills": "Laguna Hills",
    "aliso-viejo": "Aliso Viejo",
}
REFRIGERATORS = {"costa-mesa": "Costa Mesa", "huntington-beach": "Huntington Beach"}


class FormFields(HTMLParser):
    def __init__(self):
        super().__init__()
        self.fields = []
        self.open_select = None

    def handle_starttag(self, tag, attrs):
        if tag in ("input", "select", "textarea"):
            control = {"tag": tag, "attrs": dict(attrs), "options": []}
            self.fields.append(control)
            if tag == "select":
                self.open_select = control
        elif tag == "option" and self.open_select is not None:
            self.open_select["options"].append(dict(attrs))

    def handle_endtag(self, tag):
        if tag == "select":
            self.open_select = None


def exactly_one(fields, name):
    matches = [x for x in fields if x["attrs"].get("name") == name]
    return matches[0] if len(matches) == 1 else None


def required(field):
    return (field is not None and "required" in field["attrs"]
            and "disabled" not in field["attrs"])


def blank_first(field):
    return (field is not None and field["tag"] == "select" and
            len(field["options"]) > 1 and field["options"][0].get("value") == "")


def validate(source, slug, city, service):
    issues = []
    matches = re.findall(r"<form\b[^>]*>.*?</form>", source, re.I | re.S)
    native = [f for f in matches if
              'action="https://formspree.io/f/mvzeapzd"' in f.split(">", 1)[0]]
    if len(native) != 1 or len(matches) != 1:
        return [f"{slug}: expected a single native Formspree pickup form"]
    form = native[0]
    if not re.search(r'<form\b[^>]*\bmethod="POST"', form, re.I):
        issues.append(f"{slug}: form must submit with POST")

    parser = FormFields()
    parser.feed(form)
    fields = parser.fields
    for name, expected in (("source_page", slug), ("city", city),
                           ("state", "California")):
        control = exactly_one(fields, name)
        if control is None or control["attrs"].get("value") != expected:
            issues.append(f"{slug}: missing, duplicate or incorrect {name} attribution")
    for name in ("name", "phone", "address", "zip", "condition",
                 "location", "stairs", "photos_available"):
        if not required(exactly_one(fields, name)):
            issues.append(f"{slug}: {name} must be unique and browser-required")

    appliance = exactly_one(fields, "appliance")
    if service == "refrigerator":
        if appliance is None or appliance["attrs"].get("value") != "Refrigerator":
            issues.append(f"{slug}: refrigerator-only appliance attribution missing")
    elif not required(appliance) or not blank_first(appliance):
        issues.append(f"{slug}: laundry appliance must be a required blank-first choice")

    for name in ("condition", "location", "stairs", "photos_available"):
        if not blank_first(exactly_one(fields, name)):
            issues.append(f"{slug}: {name} must start with an empty choice")
    photo = exactly_one(fields, "photos_available")
    if photo is None or not {"text_after_submit", "already_shared",
                             "link_after_submit", "need_help"}.issubset(
                                {o.get("value") for o in photo["options"]}):
        issues.append(f"{slug}: missing photo sharing and assistance choices")

    for name in ("photo_link", "paid_removal_preference"):
        control = exactly_one(fields, name)
        if control is None or required(control):
            issues.append(f"{slug}: {name} must be unique and optional")
    paid = exactly_one(fields, "paid_removal_preference")
    if paid is None or not {"free_only", "quote_ok"}.issubset(
            {o.get("value") for o in paid["options"]}):
        issues.append(f"{slug}: paid quote requires an explicit opt-in choice")

    address = exactly_one(fields, "address")
    if address is None or address["attrs"].get("autocomplete") != "street-address":
        issues.append(f"{slug}: complete street-address field missing")
    phone = exactly_one(fields, "phone")
    if phone is None or any(phone["attrs"].get(k) != v for k, v in
                            (("type", "tel"), ("autocomplete", "tel"),
                             ("inputmode", "tel"))):
        issues.append(f"{slug}: mobile phone field changed")
    zip_control = exactly_one(fields, "zip")
    if zip_control is None or zip_control["attrs"].get("inputmode") != "numeric":
        issues.append(f"{slug}: numeric ZIP keyboard missing")
    if (zip_control is None or zip_control["attrs"].get("type") != "text"
            or zip_control["attrs"].get("pattern") != "[0-9]{5}"):
        issues.append(f"{slug}: missing effective five-digit ZIP validation")
    if "This form does not upload photos directly" not in form:
        issues.append(f"{slug}: photo handoff disclosure absent")
    if re.search(r'<input\b[^>]*type="file"', form, re.I):
        issues.append(f"{slug}: file upload unsupported in free Formspree form")
    return issues


def self_test():
    good = """<form action="https://formspree.io/f/mvzeapzd" method="POST">
    <input name="source_page" value="costa-mesa-washer-dryer-pickup">
    <input name="city" value="Costa Mesa"><input name="state" value="California">
    <input name="name" required><input type="tel" name="phone" required autocomplete="tel" inputmode="tel">
    <input name="address" autocomplete="street-address" required>
    <input name="zip" type="text" inputmode="numeric" pattern="[0-9]{5}" required>
    <select name="appliance" required><option value=""></option><option>Washer</option></select>
    <select name="condition" required><option value=""></option><option>Working</option></select>
    <select name="location" required><option value=""></option><option>Garage</option></select>
    <select name="stairs" required><option value=""></option><option>None</option></select>
    <select name="photos_available" required><option value=""></option>
    <option value="text_after_submit"></option><option value="already_shared"></option>
    <option value="link_after_submit"></option><option value="need_help"></option></select>
    <input name="photo_link"><select name="paid_removal_preference">
    <option value=""></option><option value="free_only"></option>
    <option value="quote_ok"></option></select>
    This form does not upload photos directly.
    </form>"""
    if validate(good, "costa-mesa-washer-dryer-pickup", "Costa Mesa", "laundry"):
        raise AssertionError("valid fixture wrongly rejected")
    broken = (
        good.replace('name="address" autocomplete="street-address" required',
                     'name="address" autocomplete="street-address" data-required="true"'),
        good.replace('name="zip" type="text" inputmode="numeric" pattern="[0-9]{5}" required',
                     'name="zip" type="text" pattern="[0-9]{5}" required'),
        good.replace('name="zip" type="text" inputmode="numeric" pattern="[0-9]{5}" required',
                     'name="zip" type="text" inputmode="numeric" required'),
        good.replace('name="address" autocomplete="street-address" required',
                     'name="address" autocomplete="street-address" required disabled'),
        good.replace('name="city" value="Costa Mesa"',
                     'name="city" value="Costa Mesa"><input name="city" value="Elsewhere"'),
        good.replace('name="location" required><option value="">',
                     'name="location" required><option value="garage">'),
        good.replace('name="photos_available" required',
                     'name="photos_available" data-required="true"'),
    )
    if any(not validate(x, "costa-mesa-washer-dryer-pickup", "Costa Mesa", "laundry")
           for x in broken):
        raise AssertionError("negative regression fixture was accepted")
    print("ORANGE_COUNTY_ESSENTIAL_NEGATIVE_TESTS_PASSED", len(broken))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    problems = []
    count = 0
    for name, markets, service in (("washer-dryer-pickup", LAUNDRY, "laundry"),
                                   ("refrigerator-pickup", REFRIGERATORS, "refrigerator")):
        for city_slug, city in markets.items():
            slug = city_slug + "-" + name
            path = ROOT / slug / "index.html"
            count += 1
            if not path.is_file():
                problems.append(f"{slug}: source page missing")
                continue
            problems.extend(validate(path.read_text(encoding="utf-8"),
                                     slug, city, service))
    for issue in problems:
        print("ERROR", issue)
    print("ORANGE_COUNTY_ESSENTIAL_FORMS_CHECKED", count)
    print("ORANGE_COUNTY_ESSENTIAL_FORM_ERRORS", len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
