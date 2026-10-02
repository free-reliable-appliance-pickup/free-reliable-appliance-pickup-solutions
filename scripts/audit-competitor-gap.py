#!/usr/bin/env python3
from pathlib import Path
import os
import xml.etree.ElementTree as ET

PRIORITY = {
"rancho-cucamonga","upland","fontana","san-bernardino","rialto","ontario","montclair","pomona","claremont",
"chino","chino-hills","diamond-bar","rowland-heights","la-puente","covina","west-covina","san-dimas","duarte",
"azusa","arcadia","pasadena","san-marino","el-monte","whittier","pico-rivera","montebello","riverside",
"palm-springs","palm-desert","la-quinta","rancho-mirage","indian-wells","cathedral-city","indio",
"fresno","clovis","sanger","fowler","selma","sacramento","stockton","phoenix","mesa","chandler","scottsdale","glendale","glendale-az",
"denver","aurora","wheat-ridge","portland","salem","keizer"
}
BASE="https://freereliableappliancepickup.com/"
ns={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}

# These actions turn a diagnostic warning into an immediately usable countermove.
COUNTERMOVES = {
    "photo_first": "Add an above-the-fold request path for clear appliance photos and condition details.",
    "access_detail": "Add stairs, elevator, gate, garage/driveway, doorway, loading and carrying-distance guidance.",
    "trust_flow": "Clarify that submission is free where true, no account is required, and a request is not a confirmed appointment.",
    "laundry_bridge": "Link the broad city page to the dedicated city washer/dryer page so the two pages do not compete for the same intent.",
    "appliance_depth": "Connect the city page to useful refrigerator, washer/dryer, freezer and stove/oven guides without spawning thin local specialty pages.",
    "faq": "Add a real FAQ section plus matching FAQPage structured data based on recurring customer questions.",
    "local_fallback": "Add an official city/hauler/public-works alternative for requests that do not qualify.",
    "commercial_recurring": "Add property-manager, apartment, senior/55+, hotel or recurring-program guidance where the market supports it.",
    "local_specificity": "Add truthful ZIP, neighborhood, access, county/corridor or route details that are genuinely useful in this city.",
}

BENCHMARKS = [
    ("TakeMyAppliance", "city depth + simple no-account request + partner matching + nearby-market links",
     "Counter with clearer qualification rules, supported-market phone/text, real photos, official fallback guidance and stronger recurring-property paths."),
    ("AppliancePickupNow", "very broad California/city inventory + photo-first request flow",
     "Counter with concentrated authority in real priority/partner markets instead of matching a giant city count."),
    ("Local paid junk haulers", "direct phone/text + photo estimates + same-day/fast-service messaging + operational detail",
     "Counter with the qualifying-free value proposition and transparent review; never imply guaranteed same-day service when it is not confirmed."),
]

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
    signals["trust_flow"]=has_any(low,["free to submit","no account required","submitting a request","request starts","does not create an appointment","pickup is confirmed only after","before pickup is confirmed","before service is confirmed","before confirming service"])
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
strong=good=needs=0
gap_counts={k:0 for k in COUNTERMOVES}
battle_lines=[]
for score,city,signals in sorted(rows,key=lambda x:(x[0],x[1])):
    missing=[k for k,v in signals.items() if not v]
    if score>=8:
        status="STRONG"; strong+=1
    elif score>=6:
        status="GOOD"; good+=1
    else:
        status="NEEDS_WORK"; needs+=1
    print(f"{score}/9 {status:10} {city:20} missing={','.join(missing) if missing else '-'}")
    if missing:
        for key in missing: gap_counts[key]+=1
        actions=" | ".join(COUNTERMOVES[k] for k in missing)
        print(f"COUNTERMOVE {city}: {actions}")
        print(f"::warning file={city}-appliance-pickup/index.html::Competitor-gap audit {score}/9; missing: {', '.join(missing)}. Countermove: {actions}")
        battle_lines.append((score,city,missing,actions))
    else:
        print(f"PROTECT {city}: 9/9. Do not rewrite just to make a change; verify live SERP/GSC evidence before the next edit.")


# Laundry-specific competitor-gap scan for the same priority markets.
# This keeps washer/dryer pages protected without forcing separate washer and dryer URLs.
LAUNDRY_COUNTERMOVES = {
    "photo_first": "Add clear washer/dryer photos and tested-condition guidance.",
    "access_detail": "Add stairs, elevator, laundry-closet, hallway, gate, parking/loading and carrying-distance guidance.",
    "trust_flow": "Clarify that submission starts a review and does not automatically guarantee free pickup.",
    "general_bridge": "Link back to the matching city general appliance page so laundry and broad appliance intent stay separated.",
    "washer_intent": "Add a dedicated washer-pickup section with fill, wash/agitation, drain and spin testing.",
    "dryer_intent": "Add a dedicated dryer-pickup section with gas/electric, tumble and heat testing.",
    "faq": "Add useful washer/dryer FAQs plus matching FAQPage structured data.",
    "local_fallback": "Add the official city, hauler, donation or recycling fallback for machines that do not qualify.",
    "commercial_recurring": "Add apartment, property-manager or recurring laundry guidance where relevant.",
    "local_specificity": "Add truthful city-specific neighborhood, ZIP, access, county or route detail.",
}

laundry_rows=[]
for city in sorted(PRIORITY):
    slug=f"{city}-washer-dryer-pickup"
    p=Path(slug)/"index.html"
    if slug not in active or not p.exists():
        continue
    raw=p.read_text(encoding="utf-8",errors="ignore")
    low=raw.lower()
    signals={}
    signals["photo_first"]=has_any(low,["photo","text appliance photos","send photos","laundry photos"])
    signals["access_detail"]=has_any(low,["stairs","elevator","laundry closet","laundry-closet","hallway","gate","loading","parking","carrying distance","narrow door"])
    signals["trust_flow"]=has_any(low,["free to submit","no account required","submitting a request","request starts","pickup is qualification-based","does not automatically guarantee","does not guarantee free","before confirming service","before pickup is confirmed","pickup is confirmed only after","before service is confirmed"])
    signals["general_bridge"]=(f"/{city}-appliance-pickup/" in low)
    signals["washer_intent"]=has_any(low,["free washer pickup","washer pickup in","washing machine pickup","washer test","washer pickup,","washer pickup &","washer pickup and"])
    signals["dryer_intent"]=has_any(low,["free dryer pickup","dryer pickup in","dryer test","dryer haul","dryer pickup,","dryer pickup &","dryer pickup and"])
    signals["faq"]=("<h2" in low and "faq" in low and ('"@type":"faqpage"' in low or '"@type": "faqpage"' in low))
    signals["local_fallback"]=has_any(low,["official ","city of ","public works","solid waste","republic services","waste management","restore","transfer station","bulky","recycling option","disposal backup"])
    signals["commercial_recurring"]=has_any(low,["property manager","commercial","recurring","senior","55+","apartment","multifamily","rental"])
    signals["local_specificity"]=has_any(low,["zip","neighborhood","downtown","county","corridor","route","metro"])
    score=sum(signals.values())
    laundry_rows.append((score,city,signals))

print("\nLAUNDRY_GAP_PRIORITY_PAGES",len(laundry_rows))
laundry_strong=laundry_good=laundry_needs=0
laundry_battle_lines=[]
for score,city,signals in sorted(laundry_rows,key=lambda x:(x[0],x[1])):
    missing=[k for k,v in signals.items() if not v]
    if score>=9:
        status="STRONG"; laundry_strong+=1
    elif score>=7:
        status="GOOD"; laundry_good+=1
    else:
        status="NEEDS_WORK"; laundry_needs+=1
    print(f"{score}/10 {status:10} {city:20} missing={','.join(missing) if missing else '-'}")
    if missing:
        actions=" | ".join(LAUNDRY_COUNTERMOVES[k] for k in missing)
        print(f"LAUNDRY_COUNTERMOVE {city}: {actions}")
        print(f"::warning file={city}-washer-dryer-pickup/index.html::Laundry competitor-gap audit {score}/10; missing: {', '.join(missing)}. Countermove: {actions}")
        laundry_battle_lines.append((score,city,missing,actions))
    else:
        print(f"PROTECT_LAUNDRY {city}: 10/10. Do not rewrite without live SERP/GSC evidence.")

print("\nCOMPETITOR_BENCHMARKS")
for name,strength,counter in BENCHMARKS:
    print(f"- {name}: strength={strength}; {counter}")

print("\nBenchmark strategy: live SERP/competitor inspection + GSC opportunity when available + review-language mining + technical checks + city/appliance intent ownership + local fallback + conversion trust + recheck.")

summary_path=os.environ.get("GITHUB_STEP_SUMMARY")
if summary_path:
    lines=[
        "## Competitor Gap Battle Report",
        "",
        f"Priority general pages scanned: **{len(rows)}** · Strong: **{strong}** · Good: **{good}** · Needs work: **{needs}**",
        f"Priority laundry pages scanned: **{len(laundry_rows)}** · Strong: **{laundry_strong}** · Good: **{laundry_good}** · Needs work: **{laundry_needs}**",
        "",
        "### Exact countermoves",
    ]
    if battle_lines:
        for score,city,missing,actions in battle_lines[:25]:
            lines.append(f"- **{city.replace('-', ' ').title()} general — {score}/9:** {actions}")
    if laundry_battle_lines:
        for score,city,missing,actions in laundry_battle_lines[:25]:
            lines.append(f"- **{city.replace('-', ' ').title()} laundry — {score}/10:** {actions}")
    if not battle_lines and not laundry_battle_lines:
        lines.append("- No on-page benchmark gaps detected. Protect current pages and use live search/ranking evidence before rewriting.")
    lines += ["", "### Competitor pattern → our response"]
    for name,strength,counter in BENCHMARKS:
        lines.append(f"- **{name}:** {strength}. {counter}")
    lines += [
        "",
        "### Decision rule",
        "A green static audit is not a ranking claim. Before changing a strong page, compare the exact live query, the current winner, the intended owner page and later Search Console data when available.",
    ]
    Path(summary_path).write_text("\n".join(lines)+"\n",encoding="utf-8")
