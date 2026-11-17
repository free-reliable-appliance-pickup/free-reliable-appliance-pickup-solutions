#!/usr/bin/env python3
"""Read-only static test of six existing Arizona laundry request forms.

No user data or network submissions are used. This cannot prove live requests.
"""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CITIES = {
    "goodyear": "Goodyear",
    "mesa": "Mesa",
    "chandler": "Chandler",
    "scottsdale": "Scottsdale",
    "glendale-az": "Glendale",
    "surprise": "Surprise",
}


class Fields(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__()
        self.controls = []
        self.select = None
        self.parents = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        first_legend_of = None
        if tag == "legend" and self.parents and self.parents[-1]["tag"] == "fieldset":
            fieldset = self.parents[-1]
            if not fieldset["first_legend_seen"]:
                fieldset["first_legend_seen"] = True
                first_legend_of = fieldset
        disabled_by_fieldset = any(
            node["tag"] == "fieldset" and node["disabled"]
            and not any(child["first_legend_of"] is node
                        for child in self.parents[i + 1:])
            for i, node in enumerate(self.parents)
        )
        if tag in ("input", "select", "textarea"):
            f = {"tag": tag, "attrs": a, "options": [],
                 "disabled_by_fieldset": disabled_by_fieldset}
            self.controls.append(f)
            if tag == "select":
                self.select = f
        elif tag == "option" and self.select is not None:
            self.select["options"].append(a)
        if tag not in self.VOID:
            self.parents.append({"tag": tag,
                                 "disabled": tag == "fieldset" and "disabled" in a,
                                 "first_legend_seen": False,
                                 "first_legend_of": first_legend_of})

    def handle_endtag(self, tag):
        if tag == "select":
            self.select = None
        for i in range(len(self.parents) - 1, -1, -1):
            if self.parents[i]["tag"] == tag:
                del self.parents[i:]
                break


def one(fields, name):
    matches = [f for f in fields if f["attrs"].get("name") == name]
    return matches[0] if len(matches) == 1 else None


def required(field):
    return (field is not None and "required" in field["attrs"]
            and "disabled" not in field["attrs"]
            and not field["disabled_by_fieldset"])


def blank_first(field):
    return (field is not None and field["tag"] == "select"
            and len(field["options"]) > 1 and field["options"][0].get("value") == "")


def validate(slug, city, html):
    errors = []
    matches = re.findall(r"<form\b[^>]*>.*?</form>", html, re.I | re.S)
    forms = [x for x in matches
             if 'action="https://formspree.io/f/mvzeapzd"' in x.split(">", 1)[0]]
    if len(matches) != 1 or len(forms) != 1:
        return [f"{slug}: not exactly one native Formspree form"]
    form = forms[0]
    if not re.search(r'<form\b[^>]*\bmethod="POST"', form, re.I):
        errors.append(f"{slug}: form must POST")
    parser = Fields()
    parser.feed(form)
    for name, expected in (("source_page", slug + "-washer-dryer-pickup"),
                           ("state", "Arizona"), ("city", city)):
        f = one(parser.controls, name)
        if f is None or f["attrs"].get("value") != expected:
            errors.append(f"{slug}: missing/duplicate/incorrect {name}")
    for name in ("name", "phone", "address", "zip", "appliance", "condition",
                 "location", "stairs", "photos_available"):
        if not required(one(parser.controls, name)):
            errors.append(f"{slug}: {name} must be unique and natively required")
    for name in ("appliance", "condition", "location", "stairs", "photos_available"):
        if not blank_first(one(parser.controls, name)):
            errors.append(f"{slug}: {name} selection must be blank-first")
    photos = one(parser.controls, "photos_available")
    photo_choices = {x.get("value") for x in photos["options"]} if photos else set()
    if not {"text_after_submit", "already_shared", "link_after_submit",
            "need_help"}.issubset(photo_choices):
        errors.append(f"{slug}: missing photo-sharing help or handoff choice")
    for name in ("photo_link", "paid_removal_preference"):
        f = one(parser.controls, name)
        if f is None or "required" in f["attrs"]:
            errors.append(f"{slug}: {name} must be unique and optional")
    phone = one(parser.controls, "phone")
    if phone is None or any(phone["attrs"].get(k) != v for k, v in
                            (("type", "tel"), ("autocomplete", "tel"),
                             ("inputmode", "tel"))):
        errors.append(f"{slug}: mobile phone control changed")
    zip_code = one(parser.controls, "zip")
    if zip_code is None or zip_code["attrs"].get("inputmode") != "numeric":
        errors.append(f"{slug}: ZIP keypad control changed")
    paid = one(parser.controls, "paid_removal_preference")
    if paid and not {"free_only", "quote_ok"}.issubset(
            {x.get("value") for x in paid["options"]}):
        errors.append(f"{slug}: quote consent options changed")
    if ("This form does not upload photos directly" not in form
            or "A quote is not a booking or a charge" not in form):
        errors.append(f"{slug}: photo or conditional quote disclosure missing")
    if re.search(r'<input\b[^>]*type="file"', form, re.I):
        errors.append(f"{slug}: unexpected photo file upload")
    return errors


def self_test():
    good = '''<form action="https://formspree.io/f/mvzeapzd" method="POST">
    <input name="source_page" value="goodyear-washer-dryer-pickup">
    <input name="city" value="Goodyear"><input name="state" value="Arizona">
    <input name="name" required><input name="phone" type="tel" autocomplete="tel" inputmode="tel" required>
    <input name="address" required><input name="zip" inputmode="numeric" required>
    <select name="appliance" required><option value=""></option><option>Washer</option></select>
    <select name="condition" required><option value=""></option><option>Working</option></select>
    <select name="location" required><option value=""></option><option>Garage</option></select>
    <select name="stairs" required><option value=""></option><option>None</option></select>
    <select name="photos_available" required><option value=""></option>
    <option value="text_after_submit"></option><option value="already_shared"></option>
    <option value="link_after_submit"></option><option value="need_help"></option></select>
    <input type="url" name="photo_link">
    <select name="paid_removal_preference"><option value=""></option>
    <option value="free_only"></option><option value="quote_ok"></option></select>
    This form does not upload photos directly. A quote is not a booking or a charge.
    </form>'''
    assert not validate("goodyear", "Goodyear", good), "valid form rejected"
    # HTML permits required controls inside the first legend of a disabled fieldset.
    exempt = (good.replace('<select name="photos_available" required>',
                           '<fieldset disabled><legend><select name="photos_available" required>')
              .replace('<input type="url" name="photo_link">',
                       '</legend></fieldset><input type="url" name="photo_link">'))
    assert not validate("goodyear", "Goodyear", exempt), "first-legend exception broken"
    corruptions = [
        good.replace('name="city" value="Goodyear"',
                     'name="city" value="Goodyear"><input name="city" value="Phoenix"'),
        good.replace('name="photos_available" required',
                     'name="photos_available" data-required="true"'),
        good.replace('name="photos_available" required',
                     'name="photos_available" required disabled'),
        good.replace('<select name="photos_available" required>',
                     '<fieldset disabled><select name="photos_available" required>')
            .replace('<input type="url" name="photo_link">',
                     '</fieldset><input type="url" name="photo_link">'),
        good.replace('name="photo_link"', 'name="photo_link" required disabled'),
        good.replace('<select name="photos_available" required>',
                     '<fieldset disabled><legend>Other</legend>'
                     '<legend><select name="photos_available" required>')
            .replace('<input type="url" name="photo_link">',
                     '</legend></fieldset><input type="url" name="photo_link">'),
        good.replace('<option value=""></option><option>Garage</option>',
                     '<option value="garage"></option><option>Garage</option>'),
    ]
    assert all(validate("goodyear", "Goodyear", x) for x in corruptions), "negative guard failed"
    print("ARIZONA_LAUNDRY_NEGATIVE_TESTS_PASSED", len(corruptions))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    problems = []
    for slug, city in CITIES.items():
        file = ROOT / (slug + "-washer-dryer-pickup") / "index.html"
        if not file.is_file():
            problems.append(f"{slug}: source HTML missing")
            continue
        problems.extend(validate(slug, city, file.read_text(encoding="utf-8")))
    for problem in problems:
        print("ERROR", problem)
    print("ARIZONA_LAUNDRY_FORMS_CHECKED", len(CITIES))
    print("ARIZONA_LAUNDRY_FORM_ERRORS", len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
