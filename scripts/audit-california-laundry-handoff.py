#!/usr/bin/env python3
"""Static regression test for seven California washer/dryer pickup forms.

No customer submission, live deployment or Google search ranking is tested.
"""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CITIES = {
    "la-verne": "La Verne",
    "chino-hills": "Chino Hills",
    "arcadia": "Arcadia",
    "azusa": "Azusa",
    "duarte": "Duarte",
    "brea": "Brea",
    "anaheim-hills": "Anaheim Hills",
}
REQUIRED = (
    "name", "phone", "address", "city", "zip", "appliance", "condition",
    "location", "stairs", "photos_available"
)


class Controls(HTMLParser):
    def __init__(self):
        super().__init__()
        self.fields = []
        self.current_select = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag in ("input", "select", "textarea"):
            control = {"tag": tag, "attrs": attributes, "options": []}
            self.fields.append(control)
            if tag == "select":
                self.current_select = control
        elif tag == "option" and self.current_select is not None:
            self.current_select["options"].append(attributes)

    def handle_endtag(self, tag):
        if tag == "select":
            self.current_select = None


def field(controls, name):
    results = [x for x in controls if x["attrs"].get("name") == name]
    return results[0] if len(results) == 1 else None


def native_required(control):
    # Inspect attribute names exactly: data-required is not required.
    return control is not None and "required" in control["attrs"]


def blank_first(control):
    return (control is not None and control["tag"] == "select"
            and len(control["options"]) > 1
            and control["options"][0].get("value") == ""
            and not any("selected" in opt for opt in control["options"][1:]))


def validate_source(slug, city, source):
    issues = []
    matches = re.findall(r"<form\b[^>]*>.*?</form>", source, re.I | re.S)
    forms = [f for f in matches if
             'action="https://formspree.io/f/mvzeapzd"' in f.split(">", 1)[0]]
    if len(forms) != 1 or len(matches) != 1:
        return [f"{slug}: expected exactly one native Formspree form"]
    form = forms[0]
    if not re.search(r"<form\b[^>]*\bmethod=\"POST\"", form, re.I):
        issues.append(f"{slug}: Formspree form must use POST")
    parsed = Controls()
    parsed.feed(form)

    for name, expected in (("source_page", slug + "-washer-dryer-pickup"),
                           ("state", "California"), ("city", city)):
        control = field(parsed.fields, name)
        if control is None or control["attrs"].get("value") != expected:
            issues.append(f"{slug}: missing, conflicting or duplicate {name}")

    for name in REQUIRED:
        control = field(parsed.fields, name)
        if not native_required(control):
            issues.append(f"{slug}: {name} missing, duplicate or not natively required")

    for name in ("appliance", "condition", "location", "stairs", "photos_available"):
        control = field(parsed.fields, name)
        if not blank_first(control):
            issues.append(f"{slug}: {name} lacks blank-first required choice")

    photos = field(parsed.fields, "photos_available")
    if photos is None or not {"text_after_submit", "already_shared", "link_after_submit",
                              "need_help"}.issubset(
                                  {o.get("value") for o in photos["options"]}):
        issues.append(f"{slug}: expected photo-sharing and help choices")

    for name in ("photo_link", "paid_removal_preference"):
        control = field(parsed.fields, name)
        if control is None or native_required(control):
            issues.append(f"{slug}: {name} missing, duplicate or not optional")

    phone = field(parsed.fields, "phone")
    if phone is None or any(phone["attrs"].get(k) != v
                            for k, v in (("type", "tel"), ("autocomplete", "tel"),
                                         ("inputmode", "tel"))):
        issues.append(f"{slug}: mobile phone control changed")
    zip_control = field(parsed.fields, "zip")
    if zip_control is None or zip_control["attrs"].get("inputmode") != "numeric":
        issues.append(f"{slug}: ZIP numeric keyboard changed")
    if "This form does not upload photos directly" not in form:
        issues.append(f"{slug}: photo handoff statement absent")
    # Validate customer consent choices independently of the quote disclosure.
    # Some existing pages use different but equivalent disclosure wording.
    quotes = field(parsed.fields, "paid_removal_preference")
    if quotes is None or not {"free_only", "quote_ok"}.issubset(
            {o.get("value") for o in quotes["options"]}):
        issues.append(f"{slug}: paid removal consent choice changed")
    if any('type="file"' in tag for tag in re.findall(r"<input\b[^>]*>", form, re.I)):
        issues.append(f"{slug}: unexpected photo file upload control")
    return issues


def self_test():
    good = """<form action="https://formspree.io/f/mvzeapzd" method="POST">
    <input name="source_page" value="la-verne-washer-dryer-pickup">
    <input name="state" value="California">
    <input name="city" value="La Verne" required>
    <input name="name" required><input name="phone" type="tel" autocomplete="tel" inputmode="tel" required>
    <input name="address" required><input name="zip" inputmode="numeric" required>
    <select name="appliance" required><option value=""></option><option>Washer</option></select>
    <select name="condition" required><option value=""></option><option>Working</option></select>
    <select name="location" required><option value=""></option><option>Garage</option></select>
    <select name="stairs" required><option value=""></option><option>None</option></select>
    <select name="photos_available" required><option value=""></option>
    <option value="text_after_submit"></option><option value="already_shared"></option>
    <option value="link_after_submit"></option><option value="need_help"></option></select>
    <input name="photo_link"><select name="paid_removal_preference">
    <option value=""></option><option value="free_only"></option><option value="quote_ok"></option></select>
    This form does not upload photos directly. A quote is not a booking or charge.
    </form>"""
    if validate_source("la-verne", "La Verne", good):
        raise AssertionError("valid fixture rejected")
    changes = (
        good.replace('name="city" value="La Verne" required',
                     'name="city" value="La Verne" required><input name="city" value="Elsewhere"'),
        good.replace('name="photos_available" required',
                     'name="photos_available" data-required="true"'),
        good.replace('<option value=""></option><option>Garage</option>',
                     '<option value="garage"></option><option>Garage</option>'),
        good.replace('<option>Garage</option>',
                     '<option selected>Garage</option>'),
        good.replace('<option value="free_only"></option><option value="quote_ok"></option>',
                     '<option value="removed"></option>'),
    )
    for changed in changes:
        if not validate_source("la-verne", "La Verne", changed):
            raise AssertionError("negative fixture incorrectly accepted")
    print("CALIFORNIA_LAUNDRY_NEGATIVE_TESTS_PASSED", len(changes))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    problems = []
    for slug, city in CITIES.items():
        path = ROOT / (slug + "-washer-dryer-pickup") / "index.html"
        if not path.is_file():
            problems.append(f"{slug}: missing pickup page")
            continue
        problems.extend(validate_source(slug, city, path.read_text(encoding="utf-8")))
    for error in problems:
        print("ERROR", error)
    print("CALIFORNIA_LAUNDRY_FORMS_CHECKED", len(CITIES))
    print("CALIFORNIA_LAUNDRY_FORM_ERRORS", len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
