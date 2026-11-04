#!/usr/bin/env python3
"""VGM source-only regression guard for two existing Salem pickup forms.

No customer forms are submitted and passing does not prove live form delivery.
"""
from html.parser import HTMLParser
from pathlib import Path

FORM_ACTION = "https://formspree.io/f/mvzeapzd"
PAGES = {
    "salem-appliance-pickup": "General major appliance pickup",
    "salem-refrigerator-freezer-pickup": "Refrigerator and freezer pickup",
}

class FormScanner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.forms = []
        self.active = None
        self.current_select = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "form":
            record = {"action": attrs.get("action"), "fields": {}, "selects": {}}
            self.forms.append(record)
            self.active = record
        elif self.active is not None and tag in ("input", "select", "textarea"):
            name = attrs.get("name")
            if name:
                self.active["fields"][name] = attrs
            if tag == "select":
                self.current_select = {"attrs": attrs, "options": []}
                if name:
                    self.active["selects"][name] = self.current_select
        elif self.active is not None and tag == "option" and self.current_select is not None:
            self.current_select["options"].append(attrs)

    def handle_endtag(self, tag):
        if tag == "select":
            self.current_select = None
        elif tag == "form":
            self.active = None
            self.current_select = None

def problems(raw, slug, service):
    p = FormScanner()
    p.feed(raw)
    forms = [x for x in p.forms if x["action"] == FORM_ACTION]
    if len(forms) != 1:
        return ["expected exactly one customer intake form"]
    form = forms[0]
    errors = []
    for name in ("name", "phone", "address", "city", "zip", "appliance", "condition"):
        if "required" not in form["fields"].get(name, {}):
            errors.append(f"{name}: required lead field absent")
    if form["fields"].get("source_page", {}).get("value") != slug:
        errors.append("source_page attribution missing")
    if form["fields"].get("service", {}).get("value") != service:
        errors.append("service attribution changed")
    for name in ("location", "stairs"):
        item = form["selects"].get(name)
        if not item or "required" not in item["attrs"]:
            errors.append(f"{name}: not a required select")
            continue
        opts = item["options"]
        if len(opts) < 2 or opts[0].get("value") != "":
            errors.append(f"{name}: first option must be blank; no auto-default")
    return errors

def main():
    total = 0
    for slug, service in PAGES.items():
        path = Path(slug) / "index.html"
        raw = path.read_text(encoding="utf-8")
        found = problems(raw, slug, service)
        if found:
            raise SystemExit(f"FAIL {slug}: {'; '.join(found)}")
        # Deliberately break each requirement to prove the guard detects regression.
        bad_required = raw.replace('<select name="location" required>', '<select name="location">', 1)
        if bad_required == raw or not problems(bad_required, slug, service):
            raise SystemExit(f"FAIL {slug}: missing-required negative fixture passed")
        bad_default = raw.replace(
            '<select name="stairs" required><option value="">',
            '<select name="stairs" required><option value="No stairs">',
            1,
        )
        if bad_default == raw or not problems(bad_default, slug, service):
            raise SystemExit(f"FAIL {slug}: preselected-stairs negative fixture passed")
        print(f"PASS {slug}: phone/address/intake attribution, required location/stairs, two negative fixtures")
        total += 1
    print(f"SALEM_ACCESS_FORMS_TESTED={total}; NEGATIVE_FIXTURES_TESTED={total * 2}")

if __name__ == "__main__":
    main()
