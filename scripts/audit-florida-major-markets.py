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
            if not any(x.get("value") == city for x in p.fields.get("city",[])): errors.append(f"{path}: incorrect city")
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
    for r in data["cities"]:
        k=re.sub(r"[^a-z0-9]+","-",r["city"].lower()).strip("-")
        if f"/{k}-fl-appliance-pickup/" not in hub: errors.append(f"hub missing {r['city']}")
    if 'name="robots" content="index, follow' not in hub: errors.append("Florida statewide hub lost index status")
    print("FLORIDA_MAJOR_MARKET_CITIES",len(data["cities"]))
    print("FLORIDA_GUIDES_AUDITED",len(paths))
    print("FLORIDA_AUDIT_ERRORS",len(errors))
    for error in errors[:70]: print("FAIL",error)
    if errors: sys.exit(1)
    print("PASS: Florida city/category/photograph/request-only/form/routing and hub links")
if __name__=="__main__": main()
