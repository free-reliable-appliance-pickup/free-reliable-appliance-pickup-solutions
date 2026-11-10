#!/usr/bin/env python3
"""One-time customer-facing SC cleanup; keeps route uncertainty and noindex."""
from pathlib import Path
import json
import re

manifest=json.loads(Path("data/ttg-state-batches/SC.json").read_text(encoding="utf8"))
assert manifest["state_code"]=="SC" and len(manifest["pages"])==251

def move_form(html, first_section=True):
    request=re.search(r'<section id="request">[\s\S]*?</section>',html)
    if not request: raise ValueError("Missing request form")
    section=request.group()
    html=html.replace(section,"",1)
    if first_section:
        lead=re.search(r'<main id="main"><section>[\s\S]*?</section>',html)
        if not lead: raise ValueError("Missing opening content section")
        html=html.replace(lead.group(),lead.group()+section,1)
    else:
        if '<main id="main">' not in html: raise ValueError("Missing main")
        html=html.replace('<main id="main">','<main id="main">'+section,1)
    return html

def change_city(html, path):
    match=re.search(r'<h1>Free ([\s\S]*?) Pickup in ([^<]+), SC</h1>',html)
    if not match: raise ValueError("Unrecognized city page H1: "+path)
    category, city=match.group(1),match.group(2)
    html=re.sub(r'<h2>Reviewing [^<]+ in [^<]+</h2>',f'<h2>{("Major Appliances We Review" if category=="Appliance" else category+" Pickup Options")} in {city}</h2>',html,count=1)
    html=html.replace("How the conditional request works",f"How Free {category} Pickup Works in {city}",1)
    html=re.sub(r'>([^<>]+?) eligibility</a>',lambda m:">"+re.sub(r' Appliance$'," Free Appliance",m.group(1))+" Pickup</a>",html)
    html=re.sub(r'<h2>Other [^<]+ appliance guides</h2>',f'<h2>Free Appliance Pickup by Type in {city}</h2>',html,count=1)
    edits={
       "Compare other South Carolina markets":"More South Carolina Pickup Locations",
       "Independent government recycling options":"Other Appliance Recycling Options",
       "Request-only:":"Pickup confirmation:",
       "What to report:":"Helpful appliance details:",
       "List appliances:":"Send appliance details:",
       "Provide real access:":"Describe removal access:",
       "Await confirmation:":"Confirm pickup availability:",
       "Agree only to approved options:":"Review any alternate quote:",
       "No unverified pickup promise":"Pickup availability confirmed individually",
       "Submitting is free but does not book collection or confirm an accepting local truck. Provide actual address, unit condition and removal access. Current photos can be shared after the initial form if needed.":"Requesting free pickup starts here. Send your pickup address, appliance condition and removal access. Free pickup availability is confirmed before any appointment; photos can be shared after the initial form."
    }
    for before,after in edits.items():html=html.replace(before,after)
    html=re.sub(r'<button([^>]*)>Submit ([^<]+) request</button>',lambda m:f'<button{m.group(1)}>Request Free {m.group(2)} Pickup</button>',html)
    return move_form(html)

def change_hub(html):
    html=html.replace("South Carolina · Fast-growing markets and retirement communities","South Carolina · Major appliance pickup requests")
    html=re.sub(r'<section><h2>South Carolina market and competitor opportunity</h2><p>[\s\S]*?</p><div class="grid">',
       '<section><h2>Free Appliance Pickup Areas in South Carolina</h2><p>Looking for pickup of a washer, dryer, refrigerator, freezer or stove? Choose your actual city and send photos, working condition and removal-access details. Qualifying machines may be accepted for free pickup after local availability is confirmed.</p><div class="grid">',html,count=1)
    html=html.replace("No statewide fleet, free route, active local operator or guaranteed pickup is confirmed by listing these cities.","Pickup availability must be confirmed for your exact city, appliance condition and removal access.")
    html=html.replace("South Carolina Free Appliance Pickup City Guides","South Carolina Free Appliance Pickup by City")
    return move_form(html,first_section=False)

count=0
for rel in manifest["pages"]:
    file=Path(rel)
    original=file.read_text(encoding="utf8")
    revised=change_hub(original) if rel=="south-carolina-appliance-pickup/index.html" else change_city(original,rel)
    if not (revised.count("<h1")==1 and "noindex, follow" in revised and "Free Reliable" in revised and 'id="request"' in revised and 'https://formspree.io/f/mvzeapzd' in revised and re.search(r'<link rel="canonical"',revised)):
        raise ValueError("Unsafe page transformation: "+rel)
    if re.search(r' eligibility</a>',revised,re.I):raise ValueError("Eligibility link remains: "+rel)
    if revised != original:
        file.write_text(revised,encoding="utf8")
        count+=1
print(f"South Carolina customer-copy validation: {len(manifest['pages'])} pages checked, {count} changed.")
