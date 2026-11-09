#!/usr/bin/env python3
"""TTG FastTrack controlled page factory: prepare, NEVER publish, request-only drafts.

Run:
  python scripts/ttg_fasttrack_generate.py --manifest data/ttg-curated-draft-pages.json
  python scripts/ttg_fasttrack_generate.py --manifest data/ttg-curated-draft-pages.json --output-dir /tmp/ttg-draft-review

The script deliberately refuses to write inside the repository checkout or
overwrite output. Every market requires authored, sourced local information.
Every output is noindex and request-only pending independent coverage review.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    "appliance": "Used Appliance Pickup Eligibility",
    "washer-dryer": "Washer and Dryer Pickup Eligibility",
    "refrigerator": "Refrigerator Pickup Eligibility",
    "freezer": "Freezer Pickup Eligibility",
    "stove-oven": "Stove and Oven Pickup Eligibility",
}
EXPECTED_IMAGE_TYPES = (".jpg", ".jpeg", ".png", ".webp")
FORM_ACTION = "https://formspree.io/f/mvzeapzd"


def safe_text(value: str) -> str:
    return html.escape(str(value), quote=True)


def slug(value: str) -> str:
    import unicodedata
    plain = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")


def validated_pages(root: Path, manifest: Path) -> list[dict]:
    config = json.loads(manifest.read_text(encoding="utf-8"))
    routing = json.loads((root / "data/market-routing.json").read_text(encoding="utf-8"))
    states = {s["state_code"]: s["state"] for s in routing["state_defaults"]}
    if not isinstance(config.get("pages"), list) or not config["pages"]:
        raise ValueError("A nonempty 'pages' list is required")
    output = []
    seen = set()
    local_sections = set()
    for idx, page in enumerate(config["pages"], 1):
        if not isinstance(page, dict):
            raise ValueError(f"Page {idx}: expected object")
        code = str(page.get("state_code", "")).upper()
        city = str(page.get("city", "")).strip()
        category = page.get("category", "")
        if code not in states or not re.fullmatch(r"[A-Za-z .'-]{2,90}", city):
            raise ValueError(f"Page {idx}: invalid state/city")
        if category not in CATEGORIES:
            raise ValueError(f"Page {idx}: unsupported appliance category")
        if page.get("mode") != "request-only":
            raise ValueError(f"Page {idx}: only explicit request-only drafts are allowed")
        page_slug = f"{slug(city)}-{code.lower()}-{category}-pickup"
        if page_slug in seen or (root / page_slug / "index.html").exists():
            raise ValueError(f"Page {idx}: duplicate or already exists in repository: {page_slug}")
        seen.add(page_slug)
        required = {
            "title": 38, "description": 90, "local_context": 150,
            "access_guidance": 130, "condition_guidance": 130,
            "official_resource_note": 120, "photo_alt": 32, "official_resource_label": 12,
        }
        for name, minimum in required.items():
            value = str(page.get(name, "")).strip()
            if len(value) < minimum:
                raise ValueError(f"Page {idx}: {name} must be manually authored ({minimum}+ characters)")
            if "<" in value or ">" in value:
                raise ValueError(f"Page {idx}: HTML markup is not allowed in authored text")
        for name in ("local_context", "access_guidance", "condition_guidance"):
            text_key = re.sub(r"\s+", " ", page[name]).strip().casefold()
            if text_key in local_sections:
                raise ValueError(f"Page {idx}: repeated city/category section: {name}")
            local_sections.add(text_key)
        link = urlparse(str(page.get("official_resource_url", "")))
        if link.scheme != "https" or not link.hostname or link.username or link.password:
            raise ValueError(f"Page {idx}: independent source must be an HTTPS URL")
        image = str(page.get("photo", ""))
        if not image.startswith("/") or image.startswith("//") or "?" in image:
            raise ValueError(f"Page {idx}: photo must be an existing root-relative local asset")
        asset = (root / image.lstrip("/")).resolve()
        if not asset.is_relative_to(root.resolve()) or not asset.is_file():
            raise ValueError(f"Page {idx}: missing/unsafe local photo {image}")
        if asset.suffix.lower() not in EXPECTED_IMAGE_TYPES:
            raise ValueError(f"Page {idx}: unsupported image format")
        output.append({**page, "state_code": code, "state_name": states[code],
                       "city": city, "slug": page_slug})
    return output


def form_markup(city: str, state_code: str, page_slug: str) -> str:
    t = safe_text
    def field(label: str, name: str, kind: str = "text", extra: str = "") -> str:
        return (f'<label>{t(label)}<input name="{name}" type="{kind}" required '
                f'{extra}></label>')
    parts = [
        f'<form action="{FORM_ACTION}" method="POST">',
        f'<input type="hidden" name="source_page" value="{t(page_slug)}">',
        field("Your name", "name", "text", 'autocomplete="name"'),
        field("Phone number", "phone", "tel", 'autocomplete="tel"'),
        '<label>Email (optional)<input name="email" type="email" autocomplete="email"></label>',
        field("Actual street address", "address", "text", 'autocomplete="street-address"'),
        field("Actual city (do not enter a neighboring municipality)", "city", "text",
              'autocomplete="address-level2"'),
        f'<label>State<select name="state" required><option value="{t(state_code)}">'
        f'{t(city)} area, {t(state_code)} only</option></select></label>',
        field("Five-digit ZIP code", "zip", "text", 'inputmode="numeric" pattern="[0-9]{5}"'),
        '<label>Appliance type<select name="appliance" required><option value="">Choose</option>'
        '<option>Washer</option><option>Dryer</option><option>Washer and dryer set</option>'
        '<option>Refrigerator</option><option>Freezer</option><option>Stove, range or oven</option>'
        '<option>Multiple major appliances</option></select></label>',
        '<label>Condition<select name="condition" required><option value="">Choose</option>'
        '<option>Fully working</option><option>Working with issues / repairable</option>'
        '<option>Not working</option><option>Unknown / needs testing</option>'
        '<option value="Mixed Load - Majority Working">Multiple appliances, majority working</option>'
        '</select></label>',
        '<label>Floor / storage area<select name="floor" required><option value="">Choose</option>'
        '<option>Garage or driveway</option><option>First floor</option><option>Second floor</option>'
        '<option>Third floor or above</option><option>Basement</option></select></label>',
        '<label>Stairs or elevator<select name="stairs" required><option value="">Choose</option>'
        '<option>No stairs</option><option>1–5 steps</option><option>One flight</option>'
        '<option>Two or more flights</option><option>Elevator</option></select></label>',
        '<label>Photos available?<select name="photos_available" required>'
        '<option value="">Choose</option><option>Yes, I can send photos</option>'
        '<option>No photos available</option><option>Need help sharing photos</option></select></label>',
        field("Loading, doors, stairs, parking and access details", "access"),
        '<label>Photo URL (optional; the form cannot upload photo files directly)'
        '<input type="url" name="photo_link"></label>',
        '<label>Appliance tests, quantity and anything not working'
        '<textarea name="message" required rows="4"></textarea></label>',
        '<label>Optional separate paid removal quote<select name="paid_option">'
        '<option value="">No paid quote authorized</option>'
        '<option value="quote_ok">I am willing to consider a separate quote</option>'
        '<option value="free_only">Free pickup only</option></select></label>',
        '<p>Your details go through Formspree and may be shared with a potential '
        'independent operator for eligibility review. Read the <a href="/privacy/">'
        'privacy policy</a>. A form submission never confirms an appointment or fee.</p>',
        '<label class="consent"><input type="checkbox" name="privacy_acknowledgment" '
        'value="acknowledged" required> I understand how this request is processed '
        'and that no pickup is guaranteed.</label>',
        '<button type="submit">Send request for review</button></form>',
    ]
    return "\n".join(parts)


def render(page: dict) -> str:
    t = safe_text
    uri = "/" + page["slug"] + "/"
    resource_url = t(page["official_resource_url"])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t(page["title"])}</title>
<meta name="description" content="{t(page["description"])}">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://freereliableappliancepickup.com{uri}">
<link rel="stylesheet" href="/assets/site-brand.css">
<style>body{{margin:0;background:#f4f8f5;color:#15372a;font:16px/1.6 system-ui,sans-serif}}main,nav{{width:min(980px,94%);margin:auto}}nav{{padding:15px 0}}header{{background:#075d3b;color:white;padding:25px 0}}header .wrap{{width:min(980px,94%);margin:auto;display:grid;grid-template-columns:1.15fr 1fr;gap:24px;align-items:center}}header img{{max-width:100%;height:auto;border-radius:12px}}section{{padding:20px;margin:18px 0;background:white;border-radius:12px;border:1px solid #d5e5da}}.notice{{background:#fff8e9;border-left:5px solid #b88424}}form{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}}form label,form p,form button{{grid-column:1/-1}}input,textarea,select{{display:block;width:100%;box-sizing:border-box;padding:11px;font:inherit;margin-top:5px;border:1px solid #739b88;border-radius:8px}}input[type=checkbox]{{width:auto;display:inline;vertical-align:middle}}button{{background:#075d3b;border:0;border-radius:8px;color:white;font:inherit;padding:14px;cursor:pointer}}a{{color:#075d3b}}header a{{color:white}}@media(max-width:700px){{header .wrap,form{{grid-template-columns:1fr}}}}</style>
<script defer src="/assets/customer-routing.js"></script></head><body>
<nav><a href="/">Home</a> / <a href="/service-areas/">Service areas</a> / {t(page["state_name"])} / {t(page["city"])}</nav>
<header><div class="wrap"><div><p>Request-only eligibility guide — {t(page["city"])}, {t(page["state_code"])}</p>
<h1>{t(page["city"])}, {t(page["state_code"])} {t(CATEGORIES[page["category"]])}</h1>
<p>Describe your used major appliance, its working condition and the actual pickup address for review. No active local crew, guaranteed free pickup or scheduled appointment is being advertised.</p>
<a href="#request">Request eligibility review</a></div>
<figure><img src="{t(page["photo"])}" alt="{t(page["photo_alt"])}" loading="eager" decoding="async">
<figcaption>Real used appliance image for illustration; not a completed {t(page["city"])} job.</figcaption></figure></div></header>
<main>
<section class="notice"><strong>Important:</strong> This is not an operating-area confirmation. Do not leave appliances outside for us. Any possible collection requires an approved operator and agreed appointment. A separate paid option, if available, must be quoted and accepted first.</section>
<section><h2>Appliance eligibility in {t(page["city"])}</h2><p>{t(page["local_context"])}</p></section>
<section><h2>Building access and moving details</h2><p>{t(page["access_guidance"])}</p></section>
<section><h2>Working-condition checks for reuse</h2><p>{t(page["condition_guidance"])}</p></section>
<section><h2>Independent city disposal information</h2><p>{t(page["official_resource_note"])}</p>
<p><a href="{resource_url}" rel="noopener noreferrer">{t(page["official_resource_label"])}</a>. This independent resource is not an assigned Free Reliable Appliance Pickup partner or an appointment booked through this site.</p></section>
<section id="request"><h2>Submit a {t(page["city"])} appliance request</h2>
<p>This Formspree request has no native photo-file upload. Photos may be shared later or via an optional link. Free collection is never automatic.</p>
{form_markup(page["city"], page["state_code"], page["slug"])}
<p>Formspree handles receipt and confirmation; do not assume a request succeeded unless you receive confirmation. If needed, use our <a href="/contact/">contact page</a>.</p></section>
</main><footer style="text-align:center;padding:20px"><a href="/privacy/">Privacy</a> · <a href="/service-areas/">Service areas</a></footer>
</body></html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, help="Explicit off-repo review destination")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        manifest = args.manifest if args.manifest.is_absolute() else root / args.manifest
        pages = validated_pages(root, manifest)
        if args.output_dir:
            dest = args.output_dir.resolve()
            if dest.is_relative_to(root):
                raise ValueError("Refusing to generate directly in website repository")
            if any((dest / p["slug"] / "index.html").exists() for p in pages):
                raise ValueError("Refusing to overwrite previously generated review pages")
            for p in pages:
                target = dest / p["slug"] / "index.html"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(render(p), encoding="utf-8")
        print(json.dumps({"validated": len(pages), "generated": len(pages) if args.output_dir else 0,
                          "request_only": True, "indexable": False,
                          "slugs": [p["slug"] for p in pages]}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"FastTrack refused to generate: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
