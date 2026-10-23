#!/usr/bin/env python3
"""VGM: inspect source-only San Fernando Valley static paid quote fallback."""
from html.parser import HTMLParser
from pathlib import Path

PAGES = {
    "san-fernando-appliance-pickup": "san-fernando-appliance-pickup/index.html",
    "san-fernando-washer-dryer-pickup": "san-fernando-washer-dryer-pickup/index.html",
    "north-hollywood-appliance-pickup": "north-hollywood-appliance-pickup/index.html",
}
ENDPOINT = "https://formspree.io/f/mvzeapzd"

class Forms(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms = []
        self.active = None
    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == "form":
            self.active = {"attrs": attrs, "inputs": [], "selects": []}
            self.forms.append(self.active)
        elif self.active is not None:
            if tag == "input": self.active["inputs"].append(attrs)
            if tag == "select": self.active["selects"].append({"attrs": attrs, "options": []})
            if tag == "option" and self.active["selects"]:
                self.active["selects"][-1]["options"].append(attrs.get("value"))
    def handle_endtag(self, tag):
        if tag == "form": self.active = None

def inspect(label, html):
    parser = Forms(); parser.feed(html)
    problems = []
    forms = [f for f in parser.forms if f["attrs"].get("action") == ENDPOINT]
    if len(forms) != 1:
        return [f"{label}: expected exactly one approved Formspree form, got {len(forms)}"]
    form = forms[0]
    if form["attrs"].get("method", "").lower() != "post": problems.append(f"{label}: must POST")
    inputs = form["inputs"]
    if len([a for a in inputs if a.get("name") == "source_page" and a.get("value") == label]) != 1:
        problems.append(f"{label}: missing source_page attribution")
    if len([a for a in inputs if a.get("name") == "phone" and a.get("type") == "tel" and "required" in a]) != 1:
        problems.append(f"{label}: required telephone missing")
    choices = [s for s in form["selects"] if s["attrs"].get("name") == "paid_removal_preference"]
    if len(choices) != 1:
        problems.append(f"{label}: expected one static optional paid quote selector")
    else:
        s = choices[0]
        if "required" in s["attrs"]: problems.append(f"{label}: paid quote selector must be optional")
        if s["options"] != ["", "free_only", "quote_ok"]:
            problems.append(f"{label}: default / free-only / quote-only consent values changed")
    return problems

if __name__ == "__main__":
    errors = []
    for label, path in PAGES.items():
        errors.extend(inspect(label, Path(path).read_text(encoding="utf-8")))
    # Guard against silently accepting automatic paid consent.
    first = Path(next(iter(PAGES.values()))).read_text(encoding="utf-8")
    assert "quote_ok" in first and 'value=""' in first
    print(f"SFV_STATIC_PAID_QUOTE_PAGES {len(PAGES)}")
    print(f"SFV_STATIC_PAID_QUOTE_ERRORS {len(errors)}")
    for error in errors: print("FAIL:", error)
    raise SystemExit(1 if errors else 0)
