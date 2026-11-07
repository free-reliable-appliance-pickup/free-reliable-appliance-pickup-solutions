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
        self.template_depth = 0
        self.label_stack = []
        self.labeled_city_fields = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "template":
            self.template_depth += 1
        if tag == "form" and not self.template_depth:
            self.forms.append(a)
            self.in_form = True
        if tag == "label" and self.in_form and not self.template_depth:
            self.label_stack.append({"text": [], "city_fields": [], "for": a.get("for"), "for_present": "for" in a, "hidden": (
                "hidden" in a or a.get("aria-hidden") == "true"
                or "display:none" in (a.get("style") or "").replace(" ", "").lower()
            )})
        if tag in ("input","select","textarea") and self.in_form and not self.template_depth and a.get("name"):
            self.fields.setdefault(a["name"], []).append(a)
            if tag == "input" and a["name"] == "city" and self.label_stack:
                self.label_stack[-1]["city_fields"].append(a)
        if tag == "img":
            self.images.append(a)
        if tag == "meta" and a.get("name", "").lower() == "robots":
            self.robots.append(a.get("content","").lower())
        if tag == "link" and a.get("rel") == "canonical":
            self.canonicals.append(a.get("href"))
        if tag == "script" and a.get("src"):
            self.scripts.append(a.get("src"))
    def handle_data(self, data):
        if self.in_form and not self.template_depth and self.label_stack:
            self.label_stack[-1]["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "label" and self.in_form and not self.template_depth and self.label_stack:
            label = self.label_stack.pop()
            label_text = " ".join("".join(label["text"]).split()).casefold()
            if not label["hidden"] and label_text == "actual pickup city":
                for city_field in label["city_fields"]:
                    # An explicit for= associates the label with that exact ID,
                    # even if the input is nested under the label.
                    target = label["for"]
                    if not label["for_present"] or (target is not None and city_field.get("id") and target == city_field.get("id")):
                        self.labeled_city_fields.append(city_field)
        if tag == "form" and not self.template_depth:
            # An inert <template> form cannot terminate the actual pickup form.
            self.in_form = False
            self.label_stack.clear()
        if tag == "template" and self.template_depth:
            self.template_depth -= 1


def valid_city_field(page, html, city, kind):
    """Verify the submitted city is explicit where nearby-city requests are invited.

    Temporary legacy support is removed only after the three general guides merge.
    """
    fields = page.fields.get("city", [])
    explicit_market = kind == "appliance" and city in {"Jacksonville", "Tampa", "Tallahassee"}
    if not explicit_market:
        if len(fields) != 1:
            return False
        field = fields[0]
        # Prefilled city guides still require a real, editable text control.
        # Hidden/disabled inputs would misattribute an actual nearby pickup.
        return (
            field.get("value") == city
            and (field.get("type") or "text").lower() == "text"
            and "required" in field
            and "disabled" not in field
            and "readonly" not in field
        )

    field = fields[0] if len(fields) == 1 else {}
    # Match the actual input parsed inside this form to its wrapping label.
    # A lookalike label elsewhere on the page, in a comment or in a template
    # must never validate an unlabeled submitted city.
    labeled = any(item is field for item in page.labeled_city_fields)
    safe_text_input = (
        len(fields) == 1
        and (field.get("type") or "text").lower() == "text"
        and "required" in field
        and "disabled" not in field
        and "readonly" not in field
        and bool(labeled)
    )
    explicit = (
        safe_text_input
        and field.get("value", "") == ""
        and field.get("placeholder") == "Actual pickup city"
    )
    # Compatibility only while main has the original three prefilled guides.
    # Remove legacy after #868, #869, #871 merge; tracked by issue #876.
    legacy = (
        safe_text_input
        and field.get("value") == city
        and "placeholder" not in field
    )
    return explicit or legacy

def valid_request_robots(robots):
    """A city guide cannot receive conflicting or duplicate indexing directives."""
    if len(robots) != 1:
        return False
    directives = {part.strip().casefold() for part in robots[0].split(",")}
    return "noindex" in directives and "follow" in directives and not (
        "index" in directives or "nofollow" in directives
    )


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
            correct_city = valid_city_field(p, txt, city, kind)
            if not correct_city:
                errors.append(f"{path}: incorrect or unconfirmed pickup city")
            if not valid_request_robots(p.robots): errors.append(f"{path}: missing, duplicate or conflicting request-only robots directives")
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
