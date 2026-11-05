#!/usr/bin/env python3
"""Audit explicit owner-selected Texas cities and four specialist request pages each."""
from pathlib import Path
from html.parser import HTMLParser
import json, re, sys
CITIES=["Houston","San Antonio","Dallas","Fort Worth","Austin","El Paso","Arlington","Corpus Christi","Plano","Lubbock","Laredo","Irving","Garland","Frisco","Grand Prairie","McKinney","Amarillo","Brownsville","Denton","Killeen","Mesquite","McAllen","Pasadena","Waco","Midland","Round Rock","Lewisville","Carrollton","Abilene","Pearland","College Station","Odessa","New Braunfels","League City","Conroe","Richardson","Tyler","Allen","Beaumont","Edinburg","Sugar Land","Georgetown","Wichita Falls","San Angelo","Temple","Bryan","Leander","Mission","Baytown","Mansfield","Longview","Pharr","Flower Mound","Cedar Park","San Marcos","Missouri City","Harlingen","North Richland Hills","Kyle","Pflugerville","Rowlett","Victoria","Forney","Celina","Wylie","Little Elm","Texas City","Burleson","DeSoto","Port Arthur","Rockwall","Galveston","Sherman","Grapevine","Waxahachie","Cedar Hill","Huntsville","Bedford","The Colony","Keller","Prosper","Weslaco","Princeton","Rosenberg","Lancaster","Weatherford","Seguin","Cibolo","Duncanville"]
TYPES=("washer-dryer","refrigerator","freezer","stove-oven")
class Scan(HTMLParser):
    def __init__(self):
        super().__init__();self.images=[];self.forms=0;self.fields={};self.in_form=False;self.meta=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="meta" and a.get("name")=="robots":self.meta.append(a.get("content",""))
        src=a.get("src") or ""
        if tag=="img" and not any(v in src.lower() for v in ["logo","brand","icon"]):self.images.append(src)
        if tag=="form":self.forms+=1;self.in_form=True
        if self.in_form and tag in ("input","select","textarea") and a.get("name"):self.fields[a["name"]]=a
    def handle_endtag(self,tag):
        if tag=="form":self.in_form=False
def slug(s):return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")
errs=[];missing=[];total=0;general_total=0
for city in CITIES:
    s=slug(city)
    general=next((Path(x) for x in [f"{s}-tx-appliance-pickup/index.html",f"{s}-appliance-pickup/index.html"] if Path(x).exists()),None)
    if general is None:
        errs.append(f"{city}: missing general city page")
    else:
        general_total+=1
        gtext=general.read_text(encoding="utf-8");gscan=Scan();gscan.feed(gtext)
        if "Pickup partner applications" in gtext:errs.append(str(general)+": closed partner program mislabeled as applications")
        if f"What happens after a {city} request?" in gtext:errs.append(str(general)+": awkward city heading")
        if not gscan.meta or not any("noindex" in x for x in gscan.meta):
            errs.append(str(general)+": noindex missing on general page")
        if len(gscan.images)!=1:
            errs.append(str(general)+f": expected one real image, found {len(gscan.images)}")
        if len(gscan.images)==1:
            src=gscan.images[0].split("?")[0]
            if not src.startswith("/") or not Path(src[1:]).is_file():
                errs.append(str(general)+": general page image missing "+src)
        if gscan.forms!=1 or "formspree.io/f/mvzeapzd" not in gtext:
            errs.append(str(general)+": general page form mismatch")
        if "customer-routing.js" not in gtext:
            errs.append(str(general)+": shared routing missing on general page")
        for field in ("name","phone","address","city","zip","appliance","condition","floor","stairs","photos_available","state","source_page"):
            if field not in gscan.fields:
                errs.append(str(general)+": general page field missing "+field)
        if gscan.fields.get("state",{}).get("value","").lower() not in ("tx","texas"):
            errs.append(str(general)+": non-TX state in general page")
        if gscan.fields.get("source_page",{}).get("value","")!=general.parent.name:
            errs.append(str(general)+": source_page not matching general page slug")
        if f'href="https://freereliableappliancepickup.com/{general.parent.name}/"' not in gtext:
            errs.append(str(general)+": self-canonical URL missing")

    for typ in TYPES:
        options=[f"{s}-tx-{typ}-pickup/index.html",f"{s}-{typ}-pickup/index.html"]
        f=next((Path(x) for x in options if Path(x).exists()),None)
        if f is None:missing.append(f"{city} {typ}");continue
        total+=1;text=f.read_text(encoding="utf-8");scan=Scan();scan.feed(text)
        if "Pickup partner applications" in text:errs.append(str(f)+": closed partner program mislabeled as applications")
        if f"What happens after a {city} request?" in text:errs.append(str(f)+": awkward city heading")
        if not scan.meta or not any("noindex" in x for x in scan.meta):errs.append(str(f)+": noindex missing")
        if len(scan.images)!=1:errs.append(str(f)+f": expected one real image, found {len(scan.images)}")
        if len(scan.images)==1:
            src=scan.images[0].split("?")[0]
            if not src.startswith("/") or not Path(src[1:]).is_file():errs.append(str(f)+": image missing "+src)
        if scan.forms!=1 or "formspree.io/f/mvzeapzd" not in text:errs.append(str(f)+": Formspree form mismatch")
        if "customer-routing.js" not in text:errs.append(str(f)+": shared routing missing")
        for field in ("name","phone","address","city","zip","appliance","condition","floor","stairs","photos_available","state","source_page"):
            if field not in scan.fields:errs.append(str(f)+": field missing "+field)
        if scan.fields.get("state",{}).get("value","").lower() not in ("tx","texas"):errs.append(str(f)+": non-TX hidden state")
        if scan.fields.get("source_page",{}).get("value","")!=f.parent.name:errs.append(str(f)+": source_page not matching slug")
        if f'href="https://freereliableappliancepickup.com/{f.parent.name}/"' not in text:errs.append(str(f)+": self-canonical URL missing")
print("OWNER_TEXAS_CITIES",len(CITIES),"APPLIANCE_CATEGORIES",len(TYPES),"GENERAL_PAGES_CHECKED",general_total,"SPECIALIST_PAGES_CHECKED",total,"PAGES_CHECKED",total+general_total,"MISSING",len(missing),"ERRORS",len(errs))
for e in (missing+errs)[:80]:print("FAIL",e)
sys.exit(1 if missing or errs or total!=356 or general_total!=89 else 0)
