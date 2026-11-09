#!/usr/bin/env python3
"""Read-only production smoke check for all manifest-listed Illinois request pages.

Checks GET responses, page metadata, request form structure, and hub navigation.
Never sends a form, tests a phone number, confirms local operators, or indexes pages.
"""
import json
from html.parser import HTMLParser
from pathlib import Path
import sys
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://freereliableappliancepickup.com/"
FORM = "https://formspree.io/f/mvzeapzd"
REQUIRED = ("name", "phone", "address", "city", "state", "zip", "appliance",
            "condition", "floor", "stairs", "photos_available", "access", "message")


class Extract(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.robots, self.canonical, self.forms, self.images = [], [], [], []
        self.fields, self.scripts, self.links, self.state_options = {}, [], [], []
        self.in_form = False
        self.in_state_select = False
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "meta" and a.get("name", "").lower() == "robots":
            self.robots.append(a.get("content", ""))
        if tag == "link" and "canonical" in (a.get("rel") or "").lower().split():
            self.canonical.append(a.get("href"))
        if tag == "a":
            self.links.append(a.get("href"))
        if tag == "img":
            self.images.append(a)
        if tag == "script" and a.get("src"):
            self.scripts.append(a["src"])
        if tag == "form":
            self.forms.append(a)
            self.in_form = True
        if self.in_form and tag == "select" and a.get("name") == "state":
            self.in_state_select = True
        if self.in_state_select and tag == "option":
            self.state_options.append(a.get("value"))
        if self.in_form and tag in {"input", "select", "textarea"} and a.get("name"):
            self.fields.setdefault(a["name"], []).append(a)

    def handle_endtag(self, tag):
        if tag == "select":
            self.in_state_select = False
        if tag == "form":
            self.in_form = False
            self.in_state_select = False


def check_page(slug, content, manifest_pages=()):
    p = Extract()
    p.feed(content)
    errors = []
    if p.h1 != 1:
        errors.append("expected one H1")
    if p.canonical != [BASE + slug + "/"]:
        errors.append("incorrect self-canonical")
    directives = {x.strip().lower() for x in p.robots[0].split(",")} if len(p.robots) == 1 else set()
    if not {"noindex", "follow"} <= directives or {"index", "nofollow"} & directives:
        errors.append("unverified Illinois market must be noindex, follow")
    if p.forms != [{"action": FORM, "method": "POST"}] and not (
        len(p.forms) == 1 and p.forms[0].get("action") == FORM
        and p.forms[0].get("method", "").lower() == "post"):
        errors.append("expected one POST to the correct Formspree endpoint")
    for name in REQUIRED:
        a = p.fields.get(name, [])
        if len(a) != 1 or "required" not in a[0]:
            errors.append("missing or nonrequired " + name)
    source = p.fields.get("source_page", [])
    if len(source) != 1 or source[0].get("value") != slug:
        errors.append("source_page mismatch")
    if p.state_options != ["", "IL"]:
        errors.append("state selection must be limited to Illinois")
    if len(p.images) != 1 or not p.images[0].get("alt"):
        errors.append("exactly one described appliance image required")
    if "/assets/customer-routing.js" not in p.scripts:
        errors.append("customer routing script missing")
    if "/privacy/" not in p.links:
        errors.append("privacy policy link missing")
    if slug == "illinois-appliance-pickup":
        for path in manifest_pages:
            other = path.removesuffix("/index.html")
            if other != slug and "/" + other + "/" not in p.links:
                errors.append("missing Illinois hub link: " + other)
    return errors


def fetch_html(path):
    url = BASE + path
    error = None
    for attempt in range(2):
        try:
            request = Request(url, headers={"User-Agent": "TTG-Illinois-ReadOnly-Smoke/1.0"})
            with urlopen(request, timeout=15) as resp:
                if resp.status != 200:
                    raise ValueError("HTTP " + str(resp.status))
                return resp.read(300_000).decode("utf-8")
        except (OSError, UnicodeError, ValueError) as exc:
            error = exc
            if attempt == 0:
                time.sleep(2)
    raise RuntimeError(str(error))


def main():
    manifest = json.loads((ROOT / "data/ttg-state-batches/IL.json").read_text(encoding="utf-8"))
    pages = manifest["pages"]
    failures = []
    for path in pages:
        slug = path.removesuffix("/index.html")
        try:
            problems = check_page(slug, fetch_html(slug + "/"), pages)
        except RuntimeError as exc:
            problems = [str(exc)]
        failures.extend(f"{slug}: {problem}" for problem in problems)
        print(f"{'FAIL' if problems else 'PASS'} {BASE}{slug}/")
    try:
        directory = fetch_html("service-areas/")
        if 'href="../illinois-appliance-pickup/"' not in directory:
            failures.append("service-areas/: Illinois hub is not linked")
    except RuntimeError as exc:
        failures.append("service-areas/: " + str(exc))
    print(f"Illinois live request-only smoke: {len(pages)} pages; {len(failures)} problems.")
    for failure in failures:
        print("ERROR:", failure, file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
