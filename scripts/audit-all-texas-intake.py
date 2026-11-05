#!/usr/bin/env python3
"""Read-only VGM audit of Texas appliance-pickup intake pages.

Detects a TX request form by its hidden state value; does not create or
index service pages. One representative appliance photo is required but
the brand logo is not counted as a service photo.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_form = False
        self.form_count = 0
        self.forms = []
        self.scripts = []
        self.images = []
        self.head_robots = []
        self.in_head = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "head":
            self.in_head = True
        if tag == "meta" and self.in_head and a.get("name", "").lower() == "robots":
            self.head_robots.append(a.get("content", "").lower())
        if tag == "script" and a.get("src"):
            self.scripts.append(a.get("src", ""))
        if tag == "img" and a.get("src"):
            self.images.append(a.get("src", ""))
        if tag == "form":
            self.in_form = True
            self.form_count += 1
            self.forms.append({"attrs": a, "fields": {}})
        if self.in_form and tag in ("input", "select", "textarea") and a.get("name"):
            self.forms[-1]["fields"].setdefault(a["name"].lower(), []).append(a)

    def handle_endtag(self, tag):
        if tag == "form":
            self.in_form = False
        if tag == "head":
            self.in_head = False


def check(path):
    content = path.read_text(encoding="utf-8", errors="replace")
    p = Page()
    p.feed(content)
    tx_forms = [
        form for form in p.forms
        if any(field.get("value", "").strip().lower() in ("tx", "texas")
               for field in form["fields"].get("state", []))
    ]
    if not tx_forms:
        return False, []
    failures = []
    if len(tx_forms) != 1 or p.form_count != 1:
        failures.append("expected exactly one Texas Formspree intake form")
    form = tx_forms[0]
    fields = form["fields"]
    if "formspree.io/f/mvzeapzd" not in form["attrs"].get("action", ""):
        failures.append("unexpected or missing Formspree action")
    for field_name in ("name", "phone", "city", "address", "zip"):
        controls = fields.get(field_name, [])
        if len(controls) != 1 or "required" not in controls[0]:
            failures.append("missing/optional required field: " + field_name)
    for field_name in ("state", "source_page", "appliance", "condition", "floor", "stairs", "photos_available"):
        if len(fields.get(field_name, [])) != 1:
            failures.append("missing/duplicated intake field: " + field_name)
    for field_name in ("appliance", "condition", "floor", "stairs", "photos_available"):
        controls = fields.get(field_name, [])
        if controls and "required" not in controls[0]:
            failures.append("select is optional: " + field_name)
    zip_controls = fields.get("zip", [])
    if zip_controls and zip_controls[0].get("pattern") != "[0-9]{5}":
        failures.append("ZIP lacks required five-digit pattern")
    scripts = [s for s in p.scripts if re.search(r"(^|/)customer-routing\.js(?:\?|$)", s)]
    if len(scripts) != 1:
        failures.append("missing/duplicated customer-routing.js include")
    photos = [src for src in p.images if not re.search(r"(?:logo|brand|icon)", src, re.I)]
    if len(photos) != 1:
        failures.append("expected one representative appliance photo (not a logo); found " + str(len(photos)))
    if path.as_posix() != "texas-appliance-pickup/index.html" and not any(
        "noindex" in directive for directive in p.head_robots
    ):
        failures.append("unverified Texas request-market page lacks noindex safeguard")
    return True, failures


def main():
    results = []
    for path in sorted(Path(".").rglob("index.html")):
        if ".git" in path.parts or ".github" in path.parts:
            continue
        is_texas, failures = check(path)
        if is_texas:
            results.append((path, failures))
    failed = [(str(path), failure) for path, failures in results for failure in failures]
    print("TEXAS_FORMS_AUDITED", len(results))
    print("TEXAS_PAGES_WITH_ISSUES", len(set(path for path, _ in failed)))
    print("TEXAS_TOTAL_ISSUES", len(failed))
    for path, failure in failed[:150]:
        print("FAIL", path, "::", failure)
    if failed:
        sys.exit(1)
    print("PASS: TX forms, routing scripts, exact photo rule, and noindex guards verified")


if __name__ == "__main__":
    main()
