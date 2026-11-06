#!/usr/bin/env python3
"""Read-only audit of Texas catalog photo-category and disclosure consistency.

This validates source metadata and visible copy, not the visual truth of photos,
Formspree receipt, route availability, or publication approval.

Default run reports visible photo-disclosure gaps, failing only structural errors.
--strict-disclosures also fails when a guide has no visible photo disclosure.
"""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

TYPES = ("appliance", "washer-dryer", "refrigerator", "freezer", "stove-oven")
ALLOWED = {
    "appliance": re.compile(r"\bappliances?\b|\bgarage\b|\bgroup\b", re.I),
    "washer-dryer": re.compile(r"wash(?:er|ing)|dryer|laundry", re.I),
    "refrigerator": re.compile(r"refrigerat|fridge", re.I),
    "freezer": re.compile(r"freezer", re.I),
    "stove-oven": re.compile(r"stove|range|oven", re.I),
}
DISCLOSURE = re.compile(
    r"(?:representative|illustrative|example|existing (?:photo|appliance)|"
    r"not (?:a|an|the) (?:documented|completed|actual|local)|"
    r"not photographed (?:in|during)|not proof of (?:local|a))",
    re.I,
)
BASE = "https://freereliableappliancepickup.com/"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.images = []
        self.fields = {}
        self.forms = []
        self.in_form = False
        self.in_head = False
        self.in_title = False
        self.in_h1 = False
        self.in_caption = False
        self.skip = 0
        self.body = []
        self.title = []
        self.h1 = []
        self.captions = []
        self.robots = []
        self.canonicals = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "head":
            self.in_head = True
        elif tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.in_h1 = True
        elif tag == "figcaption":
            self.in_caption = True
        if tag in ("script", "style", "template"):
            self.skip += 1
        if tag == "img" and a.get("src"):
            if not re.search(r"(?:logo|brand|icon)", a["src"], re.I):
                self.images.append(a)
        if tag == "link" and a.get("rel", "").lower() == "canonical":
            self.canonicals.append(a.get("href", ""))
        if tag == "meta" and self.in_head and a.get("name", "").lower() == "robots":
            self.robots.append(a.get("content", "").lower())
        if tag == "form":
            self.forms.append({"action": a.get("action", ""), "fields": {}})
            self.in_form = True
        if self.in_form and tag in ("input", "select", "textarea") and a.get("name"):
            self.forms[-1]["fields"].setdefault(a["name"].lower(), []).append(a)

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        elif tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
        elif tag == "figcaption":
            self.in_caption = False
        elif tag == "form":
            self.in_form = False
        if tag in ("script", "style", "template"):
            self.skip = max(0, self.skip - 1)

    def handle_data(self, data):
        if self.skip:
            return
        text = data.strip()
        if not text:
            return
        if self.in_title:
            self.title.append(text)
        if self.in_h1:
            self.h1.append(text)
        if self.in_caption:
            self.captions.append(text)
        if not self.in_head:
            self.body.append(text)


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-")


def is_texas(page):
    return any(
        c.get("value", "").casefold() in ("tx", "texas")
        for form in page.forms
        for c in form["fields"].get("state", [])
    )


def guide(city, typ):
    stem = slug(city)
    candidates = (
        Path(f"{stem}-tx-{typ}-pickup/index.html"),
        Path(f"{stem}-{typ}-pickup/index.html"),
    )
    for path in candidates:
        if path.is_file():
            p = Page()
            p.feed(path.read_text(encoding="utf-8", errors="replace"))
            if is_texas(p):
                return path, p
    return None, None


def audit():
    catalog = json.loads(Path("data/cities.json").read_text(encoding="utf-8"))
    cities = sorted(
        (c["city"] for c in catalog["cities"] if c.get("state_code") == "TX"),
        key=str.casefold,
    )
    errors = []
    warnings = []
    image_usage = {typ: Counter() for typ in TYPES}
    visited = set()
    for city in cities:
        for typ in TYPES:
            path, p = guide(city, typ)
            label = f"{city} {typ}"
            if path is None:
                errors.append(f"{label}: missing TX city/category page")
                continue
            name = path.parent.name
            if name in visited:
                errors.append(f"{label}: duplicate mapped page {name}")
                continue
            visited.add(name)
            if len(p.images) != 1:
                errors.append(f"{name}: expected exactly one non-logo photo, found {len(p.images)}")
            else:
                photo = p.images[0]
                src = photo["src"].split("?", 1)[0].split("#", 1)[0]
                alt = photo.get("alt", "").strip()
                image_usage[typ][src] += 1
                if not src.startswith("/") or src.startswith("//") or not Path(src.lstrip("/")).is_file():
                    errors.append(f"{name}: missing/non-local representative photo {src}")
                if not alt:
                    errors.append(f"{name}: photo missing alt text")
                elif not ALLOWED[typ].search(alt):
                    # A general group photo can accurately enumerate its
                    # appliances without using the literal word "appliance".
                    types_in_alt = sum(bool(re.search(r"\b" + token + r"\b", alt, re.I))
                                       for token in ("washer", "dryer", "stove", "refrigerator", "freezer"))
                    if typ != "appliance" or types_in_alt < 2:
                        errors.append(f"{name}: alt text lacks {typ} category")
                # Filename is an additional heuristic, not proof of what a photo
                # depicts. Flag ambiguous assets for human review below.
                if typ != "appliance" and not ALLOWED[typ].search(src):
                    warnings.append(f"{name}: photo filename requires manual category verification ({src})")
            if len(p.canonicals) != 1 or p.canonicals[0] != f"{BASE}{name}/":
                errors.append(f"{name}: missing or incorrect self-canonical")
            if not any("noindex" in robots for robots in p.robots):
                errors.append(f"{name}: unverified city guide lost noindex")
            if city.casefold() not in " ".join(p.title).casefold():
                errors.append(f"{name}: city absent from title")
            if city.casefold() not in " ".join(p.h1).casefold():
                errors.append(f"{name}: city absent from H1")
            if len(p.forms) != 1 or not is_texas(p):
                errors.append(f"{name}: missing or multiple TX forms")
            else:
                form = p.forms[0]
                if form["action"] != "https://formspree.io/f/mvzeapzd":
                    errors.append(f"{name}: wrong Formspree action")
                source = form["fields"].get("source_page", [])
                if len(source) != 1 or source[0].get("value") != name:
                    errors.append(f"{name}: source_page not tied to page URL")
            # The alt attribute is not ordinarily visible. Check actual
            # human-visible body text for photographic provenance.
            visible = " ".join(p.body)
            if not DISCLOSURE.search(visible):
                warnings.append(f"{name}: no visible illustration/photo-provenance disclosure")
    print("TEXAS_CATALOG_CITIES", len(cities))
    print("TEXAS_EXPECTED_CATEGORY_GUIDES", len(cities) * len(TYPES))
    print("TEXAS_GUIDES_INSPECTED", len(visited))
    print("TEXAS_STRUCTURE_ERRORS", len(errors))
    print("TEXAS_DISCLOSURE_OR_FILENAME_REVIEW_WARNINGS", len(warnings))
    for typ in TYPES:
        imgs = image_usage[typ]
        print("CATEGORY_PHOTO_ASSETS", typ, len(imgs), "pages", sum(imgs.values()))
        for path, count in imgs.most_common(30):
            print("PHOTO_ASSET", typ, count, path)
    for problem in errors[:200]:
        print("FAIL", problem)
    for problem in warnings:
        print("REVIEW", problem)
    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict-disclosures", action="store_true")
    args = ap.parse_args()
    errors, warnings = audit()
    if errors or (args.strict_disclosures and warnings):
        sys.exit(1)
    print("PASS: Source-level TX page inventory and nonindex/form/image metadata checks. "
          "Warnings require manual review; this is not deployment approval.")


if __name__ == "__main__":
    main()
