#!/usr/bin/env python3
from pathlib import Path
import re, xml.etree.ElementTree as ET

PRIORITY = {
"rancho-cucamonga","upland","fontana","san-bernardino","rialto","ontario","montclair","pomona","claremont",
"chino","chino-hills","diamond-bar","rowland-heights","la-puente","covina","west-covina","san-dimas","duarte",
"azusa","arcadia","pasadena","san-marino","el-monte","whittier","pico-rivera","montebello","riverside",
"palm-springs","palm-desert","la-quinta","rancho-mirage","indian-wells","cathedral-city","indio",
"fresno","clovis","sanger","sacramento","stockton","phoenix","mesa","chandler","scottsdale","glendale",
"denver","aurora","wheat-ridge","portland","salem","keizer"
}
BASE="https://freereliableappliancepickup.com/"
ns={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}

root=ET.parse("sitemap.xml").getroot()
active={x.text.strip()[len(BASE):].strip("/") for x in root.findall(".//s:loc",ns) if x.text and x.text.strip().startswith(BASE)}

def has_any(text, terms):
    return any(t in text for t in terms)

rows=[]
for city in sorted(PRIORITY):
    slug=f"{city}-appliance-pickup"
    p=Path(slug)/"index.html"
    if slug not in active or not p.exists():
        continue
    raw=p.read_text(encoding="utf-8",errors="ignore")
    low=raw.lower()
    signals={}
    signals["photo_first"]=has_any(low,["photo","text appliance photos","send photos"])
    signals["access_detail"]=has_any(low,["stairs","elevator","gate","loading","garage","carrying distance","narrow door"])
    signals["trust_flow"]=has_any(low,["free to submit","no account required","submitting a request","request starts","does not create an appointment"])
    laundry=Path(f"{city}-washer-dryer-pickup")/"index.html"
    signals["laundry_bridge"]=(not laundry.exists()) or (f"/{city}-washer-dryer-pickup/" in low)
    signals["appliance_depth"]=has_any(low,["refrigerator-pickup","washer-dryer-pickup","stove-oven-pickup","freezer pickup","refrigerator pickup guide"])
    signals["faq"]=("<h2" in low and "faq" in low and ('"@type":"faqpage"' in low or '"@type": "faqpage"' in low))
    signals["local_fallback"]=has_any(low,["official ","city of ","public works","solid waste","burrtec","republic services","waste management","transfer station","bulky"])
    signals["commercial_recurring"]=has_any(low,["property manager","commercial","recurring","senior","55+","apartment","hotel"])
    signals["local_specificity"]=has_any(low,["zip","neighborhood","hoa","condo","downtown","county","corridor","route"])
    score=sum(signals.values())
    rows.append((score,city,signals))

print("COMPETITOR_GAP_PRIORITY_PAGES",len(rows))
for score,city,signals in sorted(rows,key=lambda x:(x[0],x[1])):
    missing=[k for k,v in signals.items() if not v]
    status="STRONG" if score>=8 else "GOOD" if score>=6 else "NEEDS_WORK"
    print(f"{score}/9 {status:10} {city:20} missing={','.join(missing) if missing else '-'}")
    if missing:
        print(f"::warning file={city}-appliance-pickup/index.html::Competitor-gap audit {score}/9; missing: {', '.join(missing)}")

print("\nBenchmark strategy: live SERP/competitor inspection + GSC opportunity + review-language mining + technical checks + city/appliance intent ownership + local fallback + conversion trust + recheck.")
