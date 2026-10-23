#!/usr/bin/env python3
"""VGM source-only regression for optional static paid removal preferences on six coastal forms."""
from html.parser import HTMLParser
from pathlib import Path
import sys

SLUGS = ("ventura", "oxnard", "malibu")
PAGES = tuple(f"{city}-{kind}-pickup" for city in SLUGS for kind in ("appliance", "washer-dryer"))
ENDPOINT = "https://formspree.io/f/mvzeapzd"
OPTIONS = ["", "free_only", "quote_ok"]

class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.forms = []
        self.current = None
        self.sel = None
    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == "form":
            self.current = {"attrs": attrs, "inputs": [], "selects": []}
            self.forms.append(self.current)
        elif self.current is not None and tag == "input":
            self.current["inputs"].append(attrs)
        elif self.current is not None and tag == "select":
            self.sel = {"attrs": attrs, "options": []}
            self.current["selects"].append(self.sel)
        elif self.current is not None and tag == "option" and self.sel is not None:
            self.sel["options"].append(attrs.get("value"))
    def handle_endtag(self, tag):
        if tag == "select": self.sel = None
        if tag == "form": self.current = None

def check(slug, html):
    doc = Reader()
    doc.feed(html)
    problems = []
    if len(doc.forms) != 1:
        return [f"{slug}: one pickup form required, found {len(doc.forms)}"]
    form = doc.forms[0]
    if form["attrs"].get("action") != ENDPOINT or form["attrs"].get("method", "").upper() != "POST":
        problems.append(f"{slug}: original POST endpoint changed")
    if len([i for i in form["inputs"] if i.get("name") == "source_page" and i.get("value") == slug]) != 1:
        problems.append(f"{slug}: lost source_page")
    if len([i for i in form["inputs"] if i.get("name") == "phone" and i.get("type") == "tel" and "required" in i]) != 1:
        problems.append(f"{slug}: required phone changed")
    selects = [s for s in form["selects"] if s["attrs"].get("name") == "paid_removal_preference"]
    if len(selects) != 1:
        problems.append(f"{slug}: expected exactly one static quote preference")
    elif "required" in selects[0]["attrs"] or selects[0]["options"] != OPTIONS:
        problems.append(f"{slug}: consent must be optional and default empty with free_only/quote_ok")
    return problems

def fixture_checks():
    slug = PAGES[0]
    good = (f'<form action="{ENDPOINT}" method="POST">'
            f'<input type="hidden" name="source_page" value="{slug}">'
            '<input type="tel" name="phone" required>'
            '<select name="paid_removal_preference"><option value=""></option>'
            '<option value="free_only"></option><option value="quote_ok"></option></select></form>')
    assert not check(slug, good)
    invalid = (good.replace('value=""', 'value="quote_ok"'), good.replace('type="tel" ', ''),
               good.replace('name="source_page"', 'name="other"'),
               good.replace('<select name="paid_removal_preference"', '<select required name="paid_removal_preference"'),
               good.replace(ENDPOINT, "https://example.org/x"))
    for change in invalid:
        assert check(slug, change), "unsafe form fixture accepted"

if __name__ == "__main__":
    fixture_checks()
    failures = []
    for slug in PAGES:
        path = Path(slug) / "index.html"
        if not path.is_file():
            failures.append(f"{slug}: missing original page")
            continue
        failures.extend(check(slug, path.read_text(encoding="utf-8")))
    script = Path("assets/paid-removal-choice.js").read_text(encoding="utf-8")
    if "form.querySelector('[name=\"paid_removal_preference\"]')" not in script:
        failures.append("Dynamic control must skip forms already containing static selector")
    print("COASTAL_STATIC_PAID_QUOTE_PAGES", len(PAGES))
    print("COASTAL_STATIC_PAID_QUOTE_ERRORS", len(failures))
    for f in failures: print("FAIL:", f)
    sys.exit(1 if failures else 0)
