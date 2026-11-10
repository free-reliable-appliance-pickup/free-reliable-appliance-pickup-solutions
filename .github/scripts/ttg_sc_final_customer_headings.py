#!/usr/bin/env python3
"""Finish the customer-facing Free Appliance Pickup language on all SC pages.
Do not change factual service warnings, forms, photos, routes, or indexing policy.
"""
import json
import re
from pathlib import Path

pages = json.loads(Path("data/ttg-state-batches/SC.json").read_text(encoding="utf-8"))["pages"]
assert len(pages) == 251
modified = 0
old_style = 0
for path in pages:
    p = Path(path)
    old = p.read_text(encoding="utf-8")
    s = old
    if path == "south-carolina-appliance-pickup/index.html":
        s = s.replace("<h2>What may qualify for free pickup review?</h2>", "<h2>Appliances We Consider for Free Pickup</h2>")
        s = s.replace("<strong>eligibility review only</strong>", "<strong>pickup inquiries only</strong>")
    else:
        m = re.search(r"<h1>Free (.*?) Pickup in (.*?), SC</h1>", s)
        if m is None:
            raise ValueError("Unexpected title in " + path)
        kind, city = m.group(1), m.group(2)
        old_h = "<h2>" + city + " used-appliance eligibility</h2>"
        if old_h in s:
            old_style += 1
            section = "Major Appliances We Review" if kind == "Appliance" else kind + " Pickup Options"
            s = s.replace(old_h, "<h2>" + section + " in " + city + "</h2>")
        s = s.replace("<h2>How this eligibility request works</h2>", "<h2>How Free " + kind + " Pickup Works in " + city + "</h2>")
        s = re.sub(r"<h2>Send " + re.escape(city) + r" [^<]+ request</h2>", lambda _: "<h2>Request Free " + kind + " Pickup in " + city + ", SC</h2>", s)
        s = s.replace("<h2>" + city + " appliance pickup guides</h2>", "<h2>Free Appliance Pickup by Type in " + city + "</h2>")
        s = s.replace("<h2>Independent South Carolina recycling alternatives</h2>", "<h2>Other Appliance Recycling Options</h2>")
        s = s.replace(">Check free Pickup</a>", ">Request Free " + kind + " Pickup</a>")
        s = s.replace(">Request Free " + city + " " + kind + " Pickup</button>", ">Request Free " + kind + " Pickup in " + city + ", SC</button>")
        s = s.replace(city + "/Florence · Request review only", city + "/Florence · Free pickup request")
    s = s.replace("for eligibility review and may be shared", "to review your pickup request and may be shared")
    s = s.replace("an eligible item and confirmed operator", "a qualifying appliance and confirmed operator")
    if not (s.count("<h1") == 1 and 'noindex, follow' in s and 'Free Reliable <span>Appliance Pickup</span>' in s and 'id="request"' in s and "https://formspree.io/f/mvzeapzd" in s and '<link rel="canonical"' in s):
        raise ValueError("Safety requirement failed: " + path)
    if re.search(r"<h[123][^>]*>[^<]*eligibility[^<]*</h[123]>", s, re.I):
        raise ValueError("Old eligibility headline remains: " + path)
    if s != old:
        p.write_text(s, encoding="utf-8")
        modified += 1
assert old_style >= 100, f"Expected old specialty headings, found only {old_style}"
print(f"Validated {len(pages)} South Carolina pages. Corrected {old_style} old-style city specialty pages; total modified: {modified}.")
