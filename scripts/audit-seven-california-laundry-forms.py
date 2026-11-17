#!/usr/bin/env python3
"""Source-only regression audit for seven California laundry pickup forms.

Does not contact Formspree, validate live pickup coverage, or prove deployment.
"""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CITIES = ("chino", "covina", "glendora", "hemet", "moreno-valley",
          "perris", "rowland-heights")
ACTION = "https://formspree.io/f/mvzeapzd"
REQUIRED = ("name", "phone", "address", "zip", "appliance", "condition",
            "location", "stairs", "photos_available")
DROPDOWNS = ("appliance", "condition", "location", "stairs", "photos_available")
PHOTO_CHOICES = {"text_after", "already_shared", "share_link", "not_ready"}


class NativeFormParser(HTMLParser):
    """Track real HTML tags and exact attribute names, ignoring comments."""
    def __init__(self):
        super().__init__()
        self.forms = []
        self.current = None
        self.active_select = None

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == "form":
            self.current = {"attrs": attrs, "fields": []}
        elif self.current is not None and tag in ("input", "select", "textarea"):
            control = {"tag": tag, "attrs": attrs, "options": []}
            self.current["fields"].append(control)
            if tag == "select":
                self.active_select = control
        elif self.current is not None and tag == "option" and self.active_select is not None:
            self.active_select["options"].append(attrs)

    def handle_endtag(self, tag):
        if tag == "select":
            self.active_select = None
        elif tag == "form" and self.current is not None:
            self.forms.append(self.current)
            self.current = None


def exactly_one(fields, name):
    matches = [field for field in fields if field["attrs"].get("name") == name]
    return matches[0] if len(matches) == 1 else None


def browser_required(field):
    return (field is not None and "required" in field["attrs"]
            and "disabled" not in field["attrs"])


def blank_first(field):
    if field is None or field["tag"] != "select":
        return False
    opts = field["options"]
    return (len(opts) > 1 and opts[0].get("value") == ""
            and ("disabled" not in opts[0] or "selected" in opts[0])
            and not any("selected" in option for option in opts[1:]))


def validate(source, slug):
    parser = NativeFormParser()
    parser.feed(source)
    errors = []
    if len(parser.forms) != 1:
        return [f"{slug}: expected exactly one real HTML form"]
    form = parser.forms[0]
    attrs = form["attrs"]
    if attrs.get("action", "").rstrip("/") != ACTION or attrs.get("method", "").upper() != "POST":
        errors.append(f"{slug}: expected a native Formspree POST")
    fields = form["fields"]
    for name in REQUIRED:
        if not browser_required(exactly_one(fields, name)):
            errors.append(f"{slug}: {name} is missing, duplicate, disabled, or not required")
    for name in DROPDOWNS:
        if not blank_first(exactly_one(fields, name)):
            errors.append(f"{slug}: {name} must have a real blank-first selection")
    for name, value in (("source_page", slug), ("state", "California")):
        field = exactly_one(fields, name)
        if field is None or field["attrs"].get("value") != value:
            errors.append(f"{slug}: missing or incorrect {name} attribution")
    photo = exactly_one(fields, "photos_available")
    if photo is None or not PHOTO_CHOICES.issubset(
            {opt.get("value") for opt in photo["options"]}):
        errors.append(f"{slug}: incomplete photo-sharing choices")
    photo_link = exactly_one(fields, "photo_link")
    if (photo_link is None or photo_link["attrs"].get("type") != "url"
            or browser_required(photo_link)):
        errors.append(f"{slug}: photo_link must be a unique optional URL")
    phone = exactly_one(fields, "phone")
    if phone is None or phone["attrs"].get("type") != "tel":
        errors.append(f"{slug}: phone field must use tel input type")
    paid = exactly_one(fields, "paid_removal_preference")
    if paid is not None and browser_required(paid):
        errors.append(f"{slug}: paid quote preference must remain optional")
    if any(field["attrs"].get("type") == "file" for field in fields):
        errors.append(f"{slug}: direct file upload is unsupported in this form")
    if "This form does not upload files" not in source:
        errors.append(f"{slug}: missing truthful photo-upload disclosure")
    return errors


def self_test():
    choices = ''.join(f'<option value="{v}"></option>' for v in sorted(PHOTO_CHOICES))
    good = (f'<form action="{ACTION}" method="POST">'
            '<input name="source_page" value="chino-washer-dryer-pickup">'
            '<input name="state" value="California">'
            '<input name="name" required><input name="phone" type="tel" required>'
            '<input name="address" required><input name="zip" required>'
            + ''.join(f'<select name="{n}" required><option value=""></option>'
                      '<option value="working"></option></select>'
                      for n in DROPDOWNS if n != "photos_available")
            + '<select name="photos_available" required><option value=""></option>'
            + choices + '</select><input name="photo_link" type="url">'
            + 'This form does not upload files</form>')
    if validate(good, "chino-washer-dryer-pickup"):
        raise AssertionError("valid form rejected: " + str(validate(good, "chino-washer-dryer-pickup")))
    mutations = (
        good.replace('method="POST"', 'method="GET" data-method="POST"'),
        good.replace('name="phone" type="tel" required', 'name="phone" type="tel" data-required="true"'),
        good.replace('<option value=""></option>', '<option data-value="" value="working"></option>', 1),
        good.replace('<option value=""></option>', '<option value="" disabled></option>', 1),
        good.replace('<option value="working"></option>', '<option value="working" selected></option>', 1),
        good.replace('name="source_page"', 'name="data-source_page"'),
        good.replace('name="photo_link" type="url"', 'name="photo_link" type="url" required'),
        '<!-- ' + good + ' -->',
    )
    for i, broken in enumerate(mutations):
        if not validate(broken, "chino-washer-dryer-pickup"):
            raise AssertionError(f"bad form {i} was incorrectly accepted")
    print("CALIFORNIA_SEVEN_NEGATIVE_TESTS_PASSED", len(mutations))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return 0
    issues = []
    for city in CITIES:
        slug = f"{city}-washer-dryer-pickup"
        path = ROOT / slug / "index.html"
        if not path.is_file():
            issues.append(f"{slug}: HTML page missing")
            continue
        issues.extend(validate(path.read_text(encoding="utf-8"), slug))
    for issue in issues:
        print("ERROR", issue)
    print("CALIFORNIA_SEVEN_LAUNDRY_FORMS_CHECKED", len(CITIES))
    print("CALIFORNIA_SEVEN_LAUNDRY_FORM_ERRORS", len(issues))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
