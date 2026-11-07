#!/usr/bin/env python3
"""Read-only Florida major-market publication gate (no route or indexing activation)."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import sys

TYPES = ("appliance", "washer-dryer", "refrigerator", "freezer", "stove-oven")

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_form = False
        self.fields = {}
        self.images = []
        self.robots = []
        self.canonicals = []
        self.forms = []
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "form":
            self.forms.append(a)
            self.in_form = True
        if tag in ("input","select","textarea") and self.in_form and a.get("name"):
            self.fields.setdefault(a["name"], []).append(a)
        if tag == "img":
            self.images.append(a)
        if tag == "meta" and a.get("name", "").lower() == "robots":
            self.robots.append(a.get("content","").lower())
        if tag == "link" and a.get("rel") == "canonical":
            self.canonicals.append(a.get("href"))
        if tag == "script" and a.get("src"):
            self.scripts.append(a.get("src"))
    def handle_endtag(self, tag):
        if tag == "form":
            self.in_form = False

def main():
    data = json.loads(Path("data/florida-major-market-plan.json").read_text())
    base = "https://freereliableappliancepickup.com/"
    errors = []
    if len(data["cities"]) != 64:
        errors.append(f'Unexpected Florida city inventory: {len(data["cities"])}; expected 64')
    paths = []
    for row in data["cities"]:
        city = row["city"]
        slug = re.sub(r"[^a-z0-9]+","-",city.lower()).strip("-")
        for kind in TYPES:
            path = Path(f"{slug}-fl-{kind}-pickup/index.html")
            paths.append(path)
            if not path.exists():
                errors.append(f"missing {path}")
                continue
            txt = path.read_text(encoding="utf-8")
            p = Page()
            p.feed(txt)
            candidates = [x for x in p.images if "site-brand-logo" not in x.get("class","") and "/assets/brand/" not in x.get("src","")]
            required = ("name", "phone", "email", "address", "city", "zip", "appliance", "condition", "floor", "stairs", "photos_available", "paid_option", "access_notes")
            if len(candidates) != 1: errors.append(f"{path}: expected exactly one appliance photo, got {len(candidates)}")
            if len(p.forms) != 1 or "formspree.io/f/" not in p.forms[0].get("action",""): errors.append(f"{path}: form action")
            if any(name not in p.fields for name in required): errors.append(f"{path}: missing form fields")
            if not any(x.get("value")=="FL" for x in p.fields.get("state",[])): errors.append(f"{path}: incorrect state")
            city_fields = p.fields.get("city", [])
            needs_explicit_city = kind == "appliance" and city in {"Jacksonville", "Tampa", "Tallahassee"}
            if needs_explicit_city:
                # Two-phase migration: main currently has a prefilled guide city;
                # after #868, #869 and #871 merge, remove legacy_prefilled_city.
                # The new actual-city form must be labeled, visible, required and enabled.
                city_field = city_fields[0] if len(city_fields) == 1 else {}
                labeled_city_input = re.search(
                    r'<label>\s*Actual pickup city\s*<input\b[^>]*\bname="city"[^>]*>\s*</label>',
                    txt, re.I
                )
                safe_text_input = (
                    len(city_fields) == 1
                    and city_field.get("type", "text").lower() == "text"
                    and "required" in city_field
                    and "disabled" not in city_field
                    and bool(labeled_city_input)
                )
                explicit_pickup_city = (
                    safe_text_input
                    and city_field.get("value", "") == ""
                    and city_field.get("placeholder") == "Actual pickup city"
                )
                legacy_prefilled_city = (
                    safe_text_input
                    and city_field.get("value") == city
                    and "placeholder" not in city_field
                )
                correct_city = explicit_pickup_city or legacy_prefilled_city
            else:
                correct_city = len(city_fields) == 1 and city_fields[0].get("value") == city
            if not correct_city:
                errors.append(f"{path}: incorrect or unconfirmed pickup city")
            if not any("noindex" in x for x in p.robots): errors.append(f"{path}: accidental indexing")
            if p.canonicals != [base+path.parent.name+"/"]: errors.append(f"{path}: canonical mismatch")
            if "/assets/customer-routing.js" not in p.scripts: errors.append(f"{path}: routing js missing")
            if "not a documented completed pickup" not in txt: errors.append(f"{path}: photo provenance missing")
            if "Request-only Florida territory" not in txt: errors.append(f"{path}: request-only notice missing")
            if re.search(r"\bpartner recruiting\b|become a partner|partner signup",txt,re.I): errors.append(f"{path}: recruiting in customer-facing copy")
    markets = {m["region"]:m for m in json.loads(Path("data/market-routing.json").read_text())["markets"] if m.get("state_code")=="FL"}
    catalog = {(x["state_code"],x["city"]):x for x in json.loads(Path("data/cities.json").read_text())["cities"]}
    for r in data["cities"]:
        if ("FL",r["city"]) not in catalog: errors.append(f"missing catalog: {r['city']}")
        if catalog.get(("FL",r["city"]),{}).get("region")!=r["region"]: errors.append(f"region mismatch: {r['city']}")
        if markets.get(r["region"],{}).get("status")!="request-only": errors.append(f"unsafe market status: {r['region']}")
    hub = Path("florida-appliance-pickup/index.html").read_text()
    hub_form = Page()
    hub_form.feed(hub)
    for name in ("name", "phone", "address", "city", "zip", "appliance", "condition", "floor", "stairs", "photos_available", "paid_option", "photo_link"):
        if name not in hub_form.fields:
            errors.append(f"Florida statewide form is missing {name}")
    if not any("required" in f for f in hub_form.fields.get("photos_available", [])):
        errors.append("Florida statewide form must ask photo availability")
    if 'enctype="multipart/form-data"' in hub or 'type="file"' in hub:
        errors.append("Florida hub must not promise unsupported Formspree Free file uploads")
    if "can apply for the markets they can actually cover" in hub:
        errors.append("Florida hub retains unapproved recruiting invitation")
    for r in data["cities"]:
        k=re.sub(r"[^a-z0-9]+","-",r["city"].lower()).strip("-")
        if f'<details class="florida-city-choice" data-florida-city="{k}">' not in hub:
            errors.append(f"hub lacks five-guide selector for {r['city']}")
        for kind in TYPES:
            link = f'href="/{k}-fl-{kind}-pickup/"'
            if hub.count(link) != 1:
                errors.append(f"hub missing or duplicated {kind} guide for {r['city']}: {hub.count(link)}")
    # Regression gate: major metro and Lee/Collier neighbors link to same appliance type.
    priority_neighbors = {
        "fort-lauderdale": ("hollywood", "pompano-beach", "pembroke-pines", "miramar", "coral-springs"),
        "west-palm-beach": ("boynton-beach", "delray-beach", "boca-raton"),
        "bonita-springs": ("naples", "fort-myers", "cape-coral"),
    }
    for city_slug, neighbors in priority_neighbors.items():
        for kind in TYPES:
            page_path = Path(f"{city_slug}-fl-{kind}-pickup/index.html")
            if not page_path.exists():
                errors.append(f"missing nearby-navigation guide: {page_path}")
                continue
            content = page_path.read_text(encoding="utf-8")
            for neighbor_slug in neighbors:
                expected = f'href="/{neighbor_slug}-fl-{kind}-pickup/"'
                if content.count(expected) != 1:
                    errors.append(f"{page_path}: missing or duplicated nearby guide {neighbor_slug} ({kind})")
    if 'name="robots" content="index, follow' not in hub: errors.append("Florida statewide hub lost index status")
    print("FLORIDA_MAJOR_MARKET_CITIES",len(data["cities"]))
    print("FLORIDA_GUIDES_AUDITED",len(paths))
    print("FLORIDA_AUDIT_ERRORS",len(errors))
    for error in errors[:70]: print("FAIL",error)
    if errors: sys.exit(1)
    print("PASS: Florida city/category/photograph/request-only/form/routing and hub links")
if __name__=="__main__": main()
