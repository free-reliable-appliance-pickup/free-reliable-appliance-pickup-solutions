#!/usr/bin/env python3
"""Fail-closed static audit for Georgia request-only city guides.

This audit tests committed source, not a deployed website, customer emails,
real pickup operators, SEO rankings, or whether photos were actually received.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

BASE = "https://freereliableappliancepickup.com/"
ACTION = "https://formspree.io/f/mvzeapzd"
COMMON_REQUIRED = (
    "name", "phone", "address", "city", "zip",
    "appliance", "condition", "floor", "stairs", "photos_available",
)


class Page(HTMLParser):
    """Read only real HTML elements, not misleading strings in scripts."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = []
        self.links = []
        self.images = []
        self.forms = []
        self.fields = {}
        self.labels = {}
        self._form = None
        self._label = None
        self._jsonld = None
        self.jsonld = []
        self._title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            self.meta.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag == "img":
            self.images.append(a)
        elif tag == "form":
            self._form = a
            self.forms.append(a)
        elif tag in ("input", "select", "textarea") and self._form is not None:
            name = a.get("name")
            if name:
                self.fields.setdefault(name, []).append((tag, a))
                if self._label is not None:
                    self._label["names"].append(name)
        elif tag == "label" and self._form is not None:
            self._label = {"text": [], "names": []}
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._jsonld = []
        elif tag == "title":
            self._title = True

    def handle_data(self, data):
        if self._label is not None:
            self._label["text"].append(data)
        if self._jsonld is not None:
            self._jsonld.append(data)
        if self._title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == "label" and self._label is not None:
            words = " ".join("".join(self._label["text"]).split()).casefold()
            for name in self._label["names"]:
                self.labels.setdefault(name, []).append(words)
            self._label = None
        elif tag == "form":
            self._form = None
        elif tag == "script" and self._jsonld is not None:
            self.jsonld.append("".join(self._jsonld))
            self._jsonld = None
        elif tag == "title":
            self._title = False


def audit(root):
    """Verify request integrity and prevent unapproved indexable local claims."""
    paths = sorted(p for p in root.glob("*-ga-*-pickup/index.html")
                   if p.is_file())
    paths += sorted(p for p in root.glob("*-ga-appliance-pickup/index.html")
                    if p.is_file() and p not in paths)
    errors = []
    checks = 0
    unique_laundry_photos = {}
    if len(paths) < 14:
        errors.append(f"expected at least 14 staged Georgia guides; found {len(paths)}")

    sitemap_text = (root / "sitemap.xml").read_text(encoding="utf-8")
    for path in paths:
        slug = path.parent.name
        page_url = BASE + slug + "/"
        raw = path.read_text(encoding="utf-8")
        p = Page()
        p.feed(raw)
        checks += 1

        city_slug = slug.split("-ga-", 1)[0]
        city_name = " ".join(s.capitalize() for s in city_slug.split("-"))
        if city_name not in p.title or "GA" not in p.title:
            errors.append(f"{slug}: page title does not identify the city")
        if not any(m.get("name") == "description"
                   and city_name in m.get("content", "")
                   for m in p.meta):
            errors.append(f"{slug}: description missing actual city")
        robots = [m.get("content", "").lower() for m in p.meta
                  if m.get("name", "").lower() == "robots"]
        if len(robots) != 1 or set(x.strip() for x in robots[0].split(",")) != {"noindex", "follow"}:
            errors.append(f"{slug}: conflicting or absent noindex, follow")
        canonicals = [x.get("href") for x in p.links if x.get("rel") == "canonical"]
        if canonicals != [page_url]:
            errors.append(f"{slug}: wrong or duplicate self canonical")
        if page_url in sitemap_text:
            errors.append(f"{slug}: unverified guide exposed in sitemap")

        if len(p.forms) != 1 or p.forms[0].get("action") != ACTION or p.forms[0].get("method", "").lower() != "post":
            errors.append(f"{slug}: expected exactly one POST to existing Formspree")
        for name in COMMON_REQUIRED:
            values = p.fields.get(name, [])
            if len(values) != 1 or "required" not in values[0][1]:
                errors.append(f"{slug}: {name} must exist once and be required")
        # New Georgia pages have either a combined access_notes field or
        # separate access and message descriptions.
        access_combined = bool(p.fields.get("access_notes") and
                               "required" in p.fields["access_notes"][0][1])
        access_split = all(p.fields.get(n) and
                           "required" in p.fields[n][0][1] for n in ("access", "message"))
        if not (access_combined or access_split):
            errors.append(f"{slug}: access and detailed condition notes required")

        city_fields = p.fields.get("city", [])
        if len(city_fields) == 1:
            typ, attrs = city_fields[0]
            if typ != "input" or attrs.get("type", "text") != "text" or any(
                key in attrs for key in ("value", "hidden", "disabled", "readonly")
            ):
                errors.append(f"{slug}: city must be blank editable text")
            if not any("actual pickup city" in text for text in p.labels.get("city", [])):
                errors.append(f"{slug}: actual-city label missing")
        zip_fields = p.fields.get("zip", [])
        if len(zip_fields) == 1 and zip_fields[0][1].get("pattern") != "[0-9]{5}":
            errors.append(f"{slug}: invalid US ZIP validation")

        for hidden_name, wanted in (("state", "GA"), ("source_page", slug)):
            fields = p.fields.get(hidden_name, [])
            if len(fields) != 1 or fields[0][1].get("type") != "hidden" or fields[0][1].get("value") != wanted:
                errors.append(f"{slug}: wrong {hidden_name} routing attribute")
        if len(p.fields.get("photos_available", [])) == 1 and p.fields["photos_available"][0][0] != "select":
            errors.append(f"{slug}: photo availability must be a customer-selectable field")
        if "paid_option" not in p.fields or "required" in p.fields["paid_option"][0][1]:
            errors.append(f"{slug}: optional quoted-fee choice missing")
        if "photo_link" not in p.fields or p.fields["photo_link"][0][1].get("type") != "url":
            errors.append(f"{slug}: optional photograph link missing")
        if any(attrs.get("type") == "file" for arr in p.fields.values() for _, attrs in arr):
            errors.append(f"{slug}: unsupported direct file upload claim")

        appliance_images = [im for im in p.images if "/assets/brand/" not in im.get("src", "")]
        if len(appliance_images) != 1:
            errors.append(f"{slug}: expected exactly one appliance photo")
        else:
            image = appliance_images[0]
            src = image.get("src", "")
            if slug.endswith("-ga-washer-dryer-pickup"):
                previous = unique_laundry_photos.get(src)
                if previous:
                    errors.append(f"{slug}: washer/dryer illustration duplicates {previous}")
                else:
                    unique_laundry_photos[src] = slug
            if not src.startswith("/") or not (root / src.lstrip("/")).is_file():
                errors.append(f"{slug}: missing local appliance image {src}")
            if len(image.get("alt", "")) < 40 or "not a completed" not in image.get("alt", "").lower():
                errors.append(f"{slug}: truthful photo alt/provenance missing")
            if image.get("width") != "640" or image.get("height") != "440":
                errors.append(f"{slug}: hero intrinsic aspect ratio metadata changed")
        if not p.jsonld:
            errors.append(f"{slug}: JSON-LD missing")
        for block in p.jsonld:
            try:
                schema = json.loads(block)
                if not isinstance(schema, dict) or schema.get("@context") != "https://schema.org":
                    errors.append(f"{slug}: invalid JSON-LD context")
            except json.JSONDecodeError:
                errors.append(f"{slug}: broken JSON-LD")
        if not re.search(r"(coverage[^.]{0,50}not confirmed|coverage is not confirmed|not yet confirmed)", raw, re.I):
            errors.append(f"{slug}: missing no-confirmed-service statement")
        if re.search(r"(become (?:a|our) partner|sign up as a partner|join our partner program)", raw, re.I):
            errors.append(f"{slug}: recruiting call-to-action in customer-only guide")

    print(f"GEORGIA_GUIDES_AUDITED={checks}")
    print(f"GEORGIA_ERRORS={len(errors)}")
    for err in errors[:70]:
        print("FAIL", err)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(audit(Path(".")))
