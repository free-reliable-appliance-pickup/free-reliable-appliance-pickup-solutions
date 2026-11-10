#!/usr/bin/env python3
"""TTG Kentucky California-Gold pickup request pages: 50 cities x five types + state.

Creates complete customer-facing Free Reliable Appliance Pickup pages while keeping
Kentucky request-only until real operator coverage, Formspree delivery, and owner
release approval are independently verified. Never invent a local business address,
partner, pickup date, price, or completed Kentucky job.
"""
import hashlib
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
SITE="https://freereliableappliancepickup.com"
FORM="https://formspree.io/f/mvzeapzd"
CITIES="Louisville|Lexington|Bowling Green|Owensboro|Covington|Georgetown|Richmond|Elizabethtown|Florence|Nicholasville|Hopkinsville|Independence|Jeffersontown|Frankfort|Henderson|Paducah|Radcliff|Ashland|Erlanger|Madisonville|Winchester|Mount Washington|Burlington|Shepherdsville|Shelbyville|Danville|Somerset|London|Corbin|Pikeville|Murray|Glasgow|Bardstown|Fort Thomas|Newport|Fort Mitchell|Fort Wright|Hebron|Alexandria|Crestview Hills|Union|Versailles|Paris|Lawrenceburg|Harrodsburg|Mount Sterling|Campbellsville|Mayfield|La Grange|Berea".split("|")
KINDS={"appliance":"Appliance","washer-dryer":"Washer & Dryer","refrigerator":"Refrigerator","stove-oven":"Stove & Oven","freezer":"Freezer"}
GROUPS={
"Louisville area":"Louisville|Jeffersontown|Mount Washington|Shepherdsville|Shelbyville|Bardstown|La Grange",
"Lexington and Bluegrass":"Lexington|Georgetown|Richmond|Nicholasville|Frankfort|Winchester|Danville|Versailles|Paris|Lawrenceburg|Harrodsburg|Mount Sterling|Berea",
"Northern Kentucky":"Covington|Florence|Independence|Erlanger|Burlington|Fort Thomas|Newport|Fort Mitchell|Fort Wright|Hebron|Alexandria|Crestview Hills|Union",
"Hardin County corridor":"Elizabethtown|Radcliff",
"South central Kentucky":"Bowling Green|Glasgow|Somerset|London|Corbin|Campbellsville",
"Western Kentucky":"Owensboro|Hopkinsville|Henderson|Paducah|Madisonville|Murray|Mayfield",
"Eastern Kentucky":"Ashland|Pikeville"}
GROUP_OF={city:group for group,group_cities in GROUPS.items() for city in group_cities.split("|")}
if len(CITIES)!=50 or len(set(CITIES))!=50 or set(GROUP_OF)!=set(CITIES):
    raise RuntimeError("Must have exactly 50 unique, geographically classified Kentucky city markets")

DETAILS={
"Louisville":"For older houses, apartment stairways, and garage pickups, include doorway widths, floor and parking details.",
"Lexington":"When a refrigerator or laundry set is inside a home, note whether it is on the ground floor and whether the doorway is clear.",
"Bowling Green":"State whether the appliance is ready in a garage, rental house, apartment or storage area and whether a truck can park nearby.",
"Owensboro":"Describe the carry-out path and any stairs if a refrigerator, laundry set or stove is being replaced.",
"Covington":"Describe apartment floors, shared doors and narrow stair landings before an operator reviews the job.",
"Georgetown":"Tell us if the unit is at a garage, townhouse or apartment, and whether it can be safely loaded.",
"Richmond":"For housing move-outs and appliance replacements, provide each appliance's working status and floor location.",
"Elizabethtown":"Note the driveway, storage location, stairs and any disconnected appliances when requesting removal.",
"Florence":"Explain whether the appliance is at a house or apartment and if elevators, stairs, gates or parking affect access.",
"Nicholasville":"Provide door clearance and safe utility-disconnection status so the request can be assessed.",
"Hopkinsville":"List your quantity, condition and moving distance from the appliance to the loading area.",
"Independence":"For garage or interior pickups, tell us if stairs or narrow doorways are involved.",
"Jeffersontown":"Describe access from the appliance to safe loading and whether there is enough room for a large fridge.",
"Frankfort":"State whether a unit is at a home, apartment or basement and if there are exterior steps.",
"Henderson":"If replacing multiple appliances, tell us which units work and which need repair.",
"Paducah":"Describe loading access for used washers, dryers, freezers, refrigerators or ranges.",
"Radcliff":"For a move-out or appliance upgrade, include clear photos and accurate stair information.",
"Ashland":"Mention any steep driveway, basement stairs or long carry before scheduling is discussed.",
"Erlanger":"Provide the floor, steps and parking situation, especially for larger refrigerator units.",
"Madisonville":"Tell us which appliances have been tested and whether the load contains mostly working units.",
"Winchester":"Note access through porches, stairs, garages or narrow hallways.",
"Mount Washington":"For homes in the Louisville area, provide the street pickup location and access notes.",
"Burlington":"Explain whether the appliance is in a ground-floor garage or needs a carry-out from a house.",
"Shepherdsville":"Give the unit count and whether a truck could reach a garage or driveway for loading.",
"Shelbyville":"For home replacement or downsizing requests, give condition tests and photo availability.",
"Danville":"Report any basement, stair or narrow-door access before a possible pickup match.",
"Somerset":"List the precise number of appliances and whether utility connections are already safely disconnected.",
"London":"For larger properties or homes away from central streets, describe the approach and carry distance.",
"Corbin":"Describe the appliance's tested function and stairs from storage to the loading spot.",
"Pikeville":"For hillier access or a long driveway, describe steps, turns and how a truck could approach.",
"Murray":"If appliances are in student housing or rental units, include floor, timing preferences and access details.",
"Glasgow":"State if the request is for one working machine or several appliances of mixed condition.",
"Bardstown":"For older homes, garages and rental transitions, include the carry path and door clearance.",
"Fort Thomas":"Describe narrow stairs, landings and shared corridors where relevant.",
"Newport":"If the appliance is in a multi-unit building, report floors, stairs and parking access.",
"Fort Mitchell":"Tell us if a large appliance must travel around corners or down stairways.",
"Fort Wright":"Describe whether the appliance is in a garage, basement or upper-floor unit.",
"Hebron":"For garage pickups or household move-outs, state appliance sizes and working condition.",
"Alexandria":"Give exact ZIP, floor and safe loading details rather than assuming a nearby route.",
"Crestview Hills":"Report apartment access, elevator availability and whether the appliance is ready to move.",
"Union":"Describe parking and whether the appliance can be safely reached through exterior doors.",
"Versailles":"Include working-condition tests and whether large appliances pass through doorways.",
"Paris":"Note any narrow doorway, porch or basement steps from the appliance's location.",
"Lawrenceburg":"Tell us if appliances have been disconnected safely and if loading requires steps.",
"Harrodsburg":"Describe any long carry, interior stairs or narrow door before a local review.",
"Mount Sterling":"State which appliance needs pickup and whether access is through a garage or residence.",
"Campbellsville":"For home upgrades, give clear photos and list any repair issues or damage.",
"Mayfield":"Provide the condition and access for each used appliance, including safe utility disconnection.",
"La Grange":"For a house, townhouse or garage request, note stairs and a clear loading path.",
"Berea":"Describe whether units are in an apartment, house, basement or storage space."
}
if set(DETAILS)!=set(CITIES):raise RuntimeError("Missing unique practical pickup detail for a Kentucky city")

TYPE_NOTES={
"appliance":("Washers, dryers, refrigerator units, freezers and stoves or ranges are the main items we review.","Photograph each appliance and list tested working status, quantity, known defects and damage."),
"washer-dryer":("Working washer and dryer sets are a strong reuse candidate; singles and repairable laundry units are considered individually.","Photograph both front panels and the interiors. Tell us which unit washes, spins, heats or dries properly."),
"refrigerator":("Working cold-storage refrigerators are prioritized. Broken, leaking or untested units need a separate review.","Include full exterior, inside compartments and model label photos. Describe cooling, ice maker and water dispenser operation."),
"stove-oven":("Both gas and electric stove or oven requests can be submitted. A safe professional disconnect may be needed before moving.","Show the cooktop, oven interior and model label, and state fuel type, tested burners and oven operation."),
"freezer":("Working chest or upright freezers are prioritized; leaking or nonworking units are considered case by case.","Show the interior, exterior and model label. State whether the freezer maintains temperature and whether it is empty.")
}
GROUP_PHOTOS=[
"/salem-group-appliances.webp",
"/assets/california/city-heroes/fontana-multi-appliance.webp",
"/assets/rancho-cucamonga/rancho-cucamonga-multi-appliance-group.webp"]
SINGLE_PHOTOS={
"refrigerator":["/assets/california/real-appliances/real-refrigerator.jpg","/assets/rancho-cucamonga/rancho-cucamonga-refrigerator-pickup-real-refrigerator.jpg","/assets/rancho-cucamonga/rancho-cucamonga-refrigerator-real-french-door-20261016.jpg"],
"freezer":["/assets/california/real-appliances/real-freezer.jpg","/assets/rancho-cucamonga/rancho-cucamonga-freezer-pickup-real-freezer.jpg","/assets/rancho-cucamonga/rancho-cucamonga-freezer-real-upright-20261016.jpg"],
"stove-oven":["/assets/california/real-appliances/real-stove-range.jpg","/assets/california/real-appliances/fontana-stove-range-hero.jpg","/assets/rancho-cucamonga/rancho-cucamonga-stove-range-oven-pickup-real-stove.jpg"]}
def slugify(text):
    return re.sub(r"[^a-z0-9]+","-",text.lower()).strip("-")
def city_url(city,kind):
    return f"/{slugify(city)}-ky-{kind}-pickup/"
def state_url():
    return "/kentucky-appliance-pickup/"
def link(url,label):
    return '<a href="'+escape(url,quote=True)+'">'+escape(label)+'</a>'
def photo(src,alt):
    if not (ROOT/src.lstrip("/")).is_file():raise RuntimeError("Missing real photo: "+src)
    return '<img src="'+escape(src,quote=True)+'" alt="'+escape(alt,quote=True)+'" width="960" height="720" loading="eager" decoding="async">'
def unique_washer_photos():
    pool=list((ROOT/"assets/laundry/city-heroes").glob("*washer-dryer*.jpg"))
    pool+=list((ROOT/"assets/laundry/original-user-heroes").glob("*.jpg"))
    pool+=list((ROOT/"assets/laundry/heroes").glob("*.webp"))
    pool=sorted(set(pool))
    seen=set(); photos=[]
    for path in pool:
        key=hashlib.sha256(path.read_bytes()).digest()
        if key in seen:continue
        seen.add(key)
        photos.append("/"+path.relative_to(ROOT).as_posix())
    if len(photos)<50:raise RuntimeError("Need 50 distinct real laundry photos; found "+str(len(photos)))
    return photos[:50]
CSS="""*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f3f7f4;color:#18392b;font:16px/1.6 Arial,Helvetica,sans-serif}a{color:#075d3b}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #19a052;outline-offset:2px}.site-header{background:#fff}.site-brand-row{max-width:1100px;margin:auto;padding:13px 18px;display:flex;align-items:center;gap:15px;flex-wrap:wrap}.site-brand-logo{width:92px;height:92px;object-fit:contain}.site-brand-copy{flex:1;min-width:185px}.site-brand-name{margin:0;font-size:clamp(21px,3.7vw,30px);line-height:1.16;font-weight:800;color:#063f70}.site-brand-name span{color:#0c8d36}.site-tagline{margin:5px 0 0;color:#416076;font-size:14px}.site-hours{color:#087c37;font-weight:800}.site-nav{background:#063f70}.site-nav-inner{max-width:1100px;margin:auto;padding:12px 18px;display:flex;gap:17px;flex-wrap:wrap}.site-nav a{color:#fff;text-decoration:none;font-weight:750;font-size:14px}.breadcrumb,main{width:min(1100px,94%);margin:auto}.breadcrumb{padding:14px 0;font-size:14px}.hero{background:linear-gradient(125deg,#075d3b,#164c3c);color:#fff}.hero-grid{max-width:1100px;margin:auto;padding:37px 20px;display:grid;grid-template-columns:1.15fr .85fr;gap:24px;align-items:center}.hero h1{font-size:clamp(30px,5vw,49px);line-height:1.13;margin:10px 0 16px}.hero p{margin:10px 0}.hero img{width:100%;height:auto;max-height:345px;object-fit:cover;border-radius:12px}.hero figcaption{font-size:12px;opacity:.9}.hero figure{margin:0}.cta{display:inline-block;background:#fff;color:#075d3b;padding:12px 19px;font-weight:800;border-radius:8px;text-decoration:none;margin-top:10px}section{padding:25px;margin:22px 0;background:#fff;border:1px solid #d6e6da;border-radius:13px}section h2{margin-top:0;line-height:1.3;font-size:clamp(21px,3vw,27px);color:#075d3b}.notice{border-left:5px solid #b6862b;padding:12px 16px;background:#fff9e9;margin:14px 0}.cards,.links{display:grid;grid-template-columns:repeat(auto-fit,minmax(208px,1fr));gap:12px}.cards>div,.links>div{background:#f6faf7;border:1px solid #d1e1d5;border-radius:10px;padding:12px}.links a{font-weight:750}.form-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.form-grid>label{display:block;font-weight:700;min-width:0}.form-grid input:not([type=checkbox]),.form-grid select,.form-grid textarea{display:block;width:100%;min-width:0;min-height:44px;margin-top:5px;padding:10px;border:1px solid #829d89;border-radius:8px;font:inherit;background:#fff}.form-grid textarea{min-height:100px}.wide{grid-column:1/-1}.privacy-ack{display:flex!important;align-items:flex-start;gap:10px;font-weight:650!important;line-height:1.45;margin:12px 0}.form-grid .privacy-ack input[type=checkbox]{display:block!important;flex:0 0 22px;width:22px!important;min-width:22px!important;height:22px!important;min-height:22px!important;margin:3px 0 0!important;padding:0!important;accent-color:#08753e}.submit{display:block;width:100%;padding:15px;background:#075d3b;color:#fff;border:0;border-radius:8px;font-size:16px;font-weight:800;cursor:pointer}.muted{font-size:14px;color:#405b4b}.step{margin:14px 0}.site-request-next-steps{border:1px solid #d1e1d5;background:#f6faf7;border-radius:12px;padding:15px;margin:16px 0}.site-request-next-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.site-request-next-grid>div{background:#fff;border:1px solid #dcebe0;padding:12px;border-radius:9px;min-width:0}.site-request-next-grid strong,.site-request-next-grid span{display:block;overflow-wrap:anywhere}.site-request-next-grid span{margin-top:6px}.site-photo-first-intake{padding:14px;margin:16px 0;background:#eaf6ed;border-radius:11px}.site-photo-text-button{display:inline-block;padding:9px 13px;margin-top:9px;background:#075d3b;color:#fff!important;border-radius:7px;text-decoration:none}.site-request-next-steps h3{margin:0 0 10px}footer{background:#16392a;color:#fff;padding:23px;text-align:center}footer a{color:#fff}.skip{position:absolute;left:-20000px}.skip:focus{left:6px;top:6px;z-index:4;background:#fff;padding:10px}@media(max-width:720px){.hero-grid{grid-template-columns:1fr;padding:28px 18px}.form-grid,.site-request-next-grid{grid-template-columns:1fr}.wide{grid-column:auto}.site-brand-row{gap:10px}.site-brand-logo{width:72px;height:72px}section{padding:16px}.site-photo-text-button{display:block;text-align:center}}"""
def header():
    return '<header class="site-header"><div class="site-brand-row">'+link("/","Free Reliable Appliance Pickup home").replace("Free Reliable Appliance Pickup home",'<img class="site-brand-logo" src="/assets/brand/free-reliable-appliance-pickup-logo-236.webp" width="92" height="92" alt="Free Reliable Appliance Pickup logo">')+'<div class="site-brand-copy"><p class="site-brand-name">Free Reliable <span>Appliance Pickup</span></p><p class="site-tagline">Cleaner • Greener • Brighter Neighborhoods</p></div><div class="site-hours">8 AM–8 PM</div></div><nav class="site-nav"><div class="site-nav-inner">'+link("/","Home")+link("/how-appliance-pickup-works/","How It Works")+link("/service-areas/","Service Areas")+link("#request","Request Free Pickup")+link("/contact/","Contact")+'</div></nav></header>'
def form_block(slug, city, label, kind):
    e=lambda s:escape(s,quote=True)
    options=lambda x:"".join(f"<option>{escape(v)}</option>" for v in x)
    extra=""
    if kind=="stove-oven":
        extra='<label>Stove fuel type<select name="fuel_type" required><option value="">Choose fuel type</option>'+options(["Electric","Natural gas","Propane","Dual fuel","Not sure"])+'</select></label><label>Safe disconnection status<select name="connection_status" required><option value="">Choose status</option>'+options(["Already safely disconnected","A qualified professional will disconnect before pickup","Still connected; professional required","Not sure"])+'</select></label>'
    return (f'<form method="POST" action="{FORM}"><input type="hidden" name="_subject" value="KY {e(city)} {e(label)} pickup request"><input type="hidden" name="source_page" value="{e(slug)}"><div class="form-grid">'
      '<label>Full name<input name="name" autocomplete="name" required></label>'
      '<label>Phone number<input type="tel" name="phone" autocomplete="tel" required></label>'
      '<label>Email (optional)<input type="email" name="email" autocomplete="email"></label>'
      '<label>Street pickup address<input name="address" autocomplete="street-address" required></label>'
      f'<label>Pickup city<input name="city" autocomplete="address-level2" placeholder="{e(city)}" required></label>'
      '<label>Pickup state<select name="state" required><option value="">Choose state</option><option value="KY" selected>Kentucky</option></select></label>'
      '<label>Five-digit ZIP<input name="zip" autocomplete="postal-code" inputmode="numeric" pattern="[0-9]{5}" required></label>'
      '<label>Appliance type<select name="appliance" required><option value="">Select type</option>'+options(["Washer","Dryer","Washer and dryer set","Refrigerator","Freezer","Stove, oven or range","Multiple major appliances","Dishwasher with two or more working major appliances"])+'</select></label>'
      '<label>Working condition<select name="condition" required><option value="">Select condition</option>'+options(["Fully working","Works with minor issues","Not working","Not tested","Group with mostly working items"])+'</select></label>'
      '<label>Floor or location<select name="floor" required><option value="">Choose location</option>'+options(["Garage or driveway","First floor","Second floor","Third floor or higher","Basement","Other"])+'</select></label>'
      '<label>Stairs or elevator<select name="stairs" required><option value="">Choose access</option>'+options(["No stairs","1–5 steps","One flight","Two or more flights","Elevator","Not sure"])+'</select></label>'
      '<label>Current appliance photos available?<select name="photos_available" required><option value="">Choose one</option>'+options(["Yes, I can share current photos","No photos yet","Need help sharing photos"])+'</select></label>'+extra+
      '<label class="wide">Would you consider a separately approved removal quote if free pickup is unavailable?<select name="paid_option"><option value="">No paid service authorized</option><option value="quote_only">Only after I see and approve an actual quote</option><option value="free_only">Free pickup only</option></select></label>'
      '<label class="wide">Access and loading path<input name="access" required placeholder="Parking, elevator, stairs, gates, driveway, carry distance"></label>'
      '<label class="wide">Current appliance photo link (optional)<input type="url" name="photo_link" placeholder="https://"></label>'
      '<label class="wide">Appliance details, count, tested function and damage<textarea name="message" rows="4" required placeholder="Which appliances work? Any problems? How will they be safely reached?"></textarea></label>'
      '<div class="wide"><p class="muted"><strong>Privacy:</strong> Your contact, pickup location, item condition and access details are processed through Formspree and may be shared with a prospective independent pickup operator. Read our '+link("/privacy/","Privacy Policy")+'. Do not submit ID or payment details.</p>'
      '<label class="privacy-ack"><input type="checkbox" name="privacy_acknowledgment" value="acknowledged" required>I understand submitting a request does not book or guarantee free pickup.</label>'
      f'<button class="submit" type="submit">Request Free {e(label)} Pickup</button>'
      '<p class="muted">Requesting pickup costs nothing. Free collection depends on appliance condition, safe access and a confirmed accepting operator; paid removal requires your separate approval.</p></div></div></form>')
def base_html(slug,title,description,content,city,kind):
    e=lambda s:escape(s,quote=True)
    canon=SITE+"/"+slug+"/"
    jsonld={"@context":"https://schema.org","@graph":[{"@type":"WebPage","name":title,"url":canon,"description":description},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Kentucky Free Appliance Pickup","item":SITE+state_url()}]}]}
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
      f'<title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="robots" content="noindex, follow">'
      f'<link rel="canonical" href="{e(canon)}"><link rel="icon" href="/assets/brand/free-reliable-appliance-pickup-logo-236.webp">'
      '<link rel="stylesheet" href="/assets/site-brand.css?v=20261110-ky-gold"><meta property="og:site_name" content="Free Reliable Appliance Pickup"><meta property="og:type" content="website">'
      f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{e(canon)}">'
      '<script defer src="/assets/customer-routing.js"></script><style>'+CSS+'</style></head><body><a class="skip" href="#main">Skip to main content</a>'
      '<script type="application/ld+json">'+json.dumps(jsonld,ensure_ascii=False,separators=(",",":"))+'</script>'
      +header()+'<nav class="breadcrumb" aria-label="Breadcrumb">'+link("/","Home")+' › '+link(state_url(),"Kentucky")+(' › '+escape(city) if city!="Kentucky" else "")+'</nav>'
      +content+'<footer>Free Reliable Appliance Pickup · '+link(state_url(),"Kentucky Free Appliance Pickup")+' · Local pickup subject to confirmed availability</footer></body></html>')
def alternative(city):
    if city=="Lexington":
        return ('<p>The <a href="https://www.lexingtonky.gov/living/waste-collection/appliances">City of Lexington appliance collection program</a> accepts appointment requests from households with city waste collection service at no charge. It has its own rules, and it is not part of Free Reliable Appliance Pickup.</p>')
    if city=="Louisville":
        return ('<p><a href="https://louisvilleky.gov/government/public-works/large-items">Louisville Metro large-item options</a> describe appointments for city-waste customers and the separate Waste Reduction Center. Refrigerant-containing appliances require appropriate handling; municipal options are independent of our pickup inquiries.</p>')
    if city in {"Elizabethtown","Radcliff"}:
        return ('<p><a href="https://www.hardincountyky.gov/360/Solid-Waste-Recycling-Landfill">Hardin County Solid Waste</a> describes its separate bulky-item collection program for eligible unincorporated-county households. Confirm which program applies to the pickup address and check restrictions directly with the county.</p>')
    return ('<p>For appliances not accepted for reuse, check your local public works department, county solid waste office, retailer take-back or licensed recycler. These are independent options; availability, fees and restrictions vary by municipality and provider.</p>')
def page_for(city,kind,position,washer_photos):
    name=KINDS[kind]; slug=city_url(city,kind).strip("/")
    city_e=escape(city)
    title=f"Free {name} Pickup in {city}, KY | Free Reliable Appliance Pickup"
    description=f"Request free {name.lower()} pickup in {city}, Kentucky with Free Reliable Appliance Pickup. Send photos and working-condition and access details. A local route must be confirmed."
    src=(GROUP_PHOTOS[position%len(GROUP_PHOTOS)] if kind=="appliance" else washer_photos[position] if kind=="washer-dryer" else SINGLE_PHOTOS[kind][position%len(SINGLE_PHOTOS[kind])])
    content=('<header class="hero"><div class="hero-grid"><div><p><strong>'+city_e+', Kentucky · '+escape(GROUP_OF[city])+'</strong></p><h1>Free '+escape(name)+' Pickup in '+city_e+', KY</h1>'
       '<p>Have a used '+escape(name.lower())+' you want removed? Submit its condition, photos and access details to request free pickup. Working appliances are prioritized for possible reuse.</p>'
       '<p><strong>Pickup is not booked:</strong> We must confirm a real accepting local operator and the pickup terms for your ZIP code before arranging any collection.</p>'
       '<p>'+link("#request","Request Free "+name+" Pickup")+'</p></div><figure>'+photo(src,"Real used "+name.lower()+" appliance photo from our existing library; illustration only, not a completed "+city+" Kentucky pickup")+
       '<figcaption>Real existing used-appliance photo, for illustration only; not evidence of a Kentucky pickup.</figcaption></figure></div></header>'
       '<main id="main"><section id="request"><h2>Request Free '+escape(name)+' Pickup in '+city_e+', KY</h2>'
       '<p>Fill out the request form with an actual pickup address, appliance condition and a safe loading path. There is no fee to submit a request.</p>'+form_block(slug,city,name,kind)+'</section>'
       '<section><h2>'+city_e+' Free '+escape(name)+' Pickup Details</h2><div class="cards"><div><strong>Working units first</strong><p>'+escape(TYPE_NOTES[kind][0])+'</p></div>'
       '<div><strong>Photos and tested condition</strong><p>'+escape(TYPE_NOTES[kind][1])+'</p></div>'
       '<div><strong>Access matters</strong><p>'+escape(DETAILS[city])+'</p></div></div>'
       '<p class="notice">Not every broken or hard-to-move appliance can be collected for free. We do not claim a verified truck, route or pickup time in '+city_e+'.</p></section>'
       '<section><h2>How to Request Free '+escape(name)+' Pickup</h2><ol><li class="step"><strong>Describe your appliance:</strong> Give the brand, size if known, test results and quantity.</li>'
       '<li class="step"><strong>Share photos and access:</strong> Include floor, steps, parking, door clearance and whether the appliance is disconnected.</li>'
       '<li class="step"><strong>Confirm a local option:</strong> If an accepting operator is available, pickup terms and timing will be discussed by phone or text.</li>'
       '<li class="step"><strong>Approve any fee separately:</strong> A paid-removal quote is optional and never authorized just by sending the form.</li></ol></section>')
    if kind=="stove-oven":
        content+=('<section><h2>Stove Fuel and Safe Disconnection in '+city_e+'</h2><p>Both gas and electric stove or oven requests are welcome. Identify whether it uses gas, propane, electricity or dual fuel. If still connected to a gas line, use a qualified professional. Do not loosen a gas connection yourself.</p></section>')
    if kind in ("refrigerator","freezer"):
        content+=('<section><h2>Refrigerator and Freezer Handling</h2><p>For cold-storage appliances, share operating-temperature tests and any leaks or compressor problems. Keep the refrigerant system sealed and leave refrigerant handling to qualified professionals. Do not puncture coolant lines.</p></section>')
    content+='<section><h2>More Free Appliance Pickup Pages in '+city_e+'</h2><div class="links">'
    for other,label in KINDS.items():
        content+='<div>'+link(city_url(city,other),"Free "+label+" Pickup in "+city)+'</div>'
    content+='</div><h3>Nearby Kentucky Pickup Request Areas</h3><div class="links">'
    similar=[c for c in CITIES if c!=city and GROUP_OF[c]==GROUP_OF[city]]
    if len(similar)<3:similar+=["Louisville","Lexington","Bowling Green"]
    for neigh in similar[:6]:content+='<div>'+link(city_url(neigh,"appliance"),"Free Appliance Pickup in "+neigh)+'</div>'
    content+='</div></section><section><h2>Independent Recycling and Municipal Alternatives</h2>'+alternative(city)+'<p>Free Reliable Appliance Pickup is a separate reuse-oriented request service. Public collection programs are not our pickup operators or confirmed partners.</p></section></main>'
    return base_html(slug,title,description,content,city,kind)
def state_page():
    slug="kentucky-appliance-pickup"
    title="Free Appliance Pickup in Kentucky | Free Reliable Appliance Pickup"
    description="Request free appliance pickup in Kentucky. Choose from 50 city markets and send appliance condition, photos and access details. Pickup availability must be confirmed."
    content=('<header class="hero"><div class="hero-grid"><div><p><strong>Kentucky · Free Appliance Pickup Requests</strong></p><h1>Free Appliance Pickup in Kentucky</h1>'
       '<p>Need to remove a used washer, dryer, refrigerator, stove, range or freezer? Tell us which appliances work and how they can be reached safely.</p>'
       '<p><strong>Customer requests are open, but Kentucky pickup operators and routes have not been verified.</strong> A form submission is not an appointment and does not guarantee a free removal.</p>'
       +link("#request","Request Free Appliance Pickup")+'</div><figure>'
       +photo(GROUP_PHOTOS[0],"Real used appliances in the business photo library, illustrative only; not a Kentucky pickup")
       +'<figcaption>One real multi-appliance photo from our existing library; not a completed Kentucky pickup.</figcaption></figure></div></header>'
       '<main id="main"><section id="request"><h2>Request Free Appliance Pickup in Kentucky</h2><p>Enter the actual pickup address. We can review the request only after the appliances, condition and local access are described.</p>'
       +form_block(slug,"Kentucky","Appliance","appliance")+'</section>'
       '<section><h2>Kentucky Free Appliance Pickup by City</h2><p>Browse a city below for a free pickup request form. A city page does not prove that an operator currently serves that ZIP code.</p>')
    for group, cities in GROUPS.items():
        content+='<h3>'+escape(group)+'</h3><div class="links">'
        for city in cities.split("|"):
            content+='<div>'+link(city_url(city,"appliance"),"Free Appliance Pickup in "+city+", KY")+'</div>'
        content+='</div>'
    content+='</section><section><h2>Free Appliance Pickup by Appliance Type</h2><p>Each Kentucky city has its own washer and dryer, refrigerator, stove and oven, and freezer pickup request page.</p><div class="links">'
    for kind,label in KINDS.items():
        content+='<div>'+link(city_url("Louisville",kind),"Louisville Free "+label+" Pickup")+'</div>'
        content+='<div>'+link(city_url("Lexington",kind),"Lexington Free "+label+" Pickup")+'</div>'
    content+='</div></section><section><h2>How Free Appliance Pickup Requests Work</h2><ol><li>Provide the appliance count and tested condition.</li><li>Tell us your city, ZIP, floor, stairs, available photos and loading path.</li><li>We assess reuse potential and check whether an actual local pickup operator will accept the job.</li><li>Any approved pickup and any optional paid quote must be confirmed separately.</li></ol><p>Working appliances and mostly working sets are prioritized. Nonworking machines are reviewed case by case. Dishwashers are considered only with two or more working major appliances; microwaves alone are not collected.</p></section><section><h2>Kentucky Public Appliance Disposal Alternatives</h2>'
    content+='<p><a href="https://www.lexingtonky.gov/living/waste-collection/appliances">Lexington municipal appliance collection</a> serves residents with city waste service under that program’s own rules. <a href="https://louisvilleky.gov/government/public-works/large-items">Louisville Metro large-item guidance</a> describes city-program appointments and separate drop-off options. <a href="https://www.hardincountyky.gov/360/Solid-Waste-Recycling-Landfill">Hardin County Solid Waste</a> explains a separate bulky-item program for certain households. These public programs are independent of Free Reliable Appliance Pickup.</p><p>Ask your own city or county about current acceptance, safe refrigerant handling and service-area limits.</p></section></main>'
    return base_html(slug,title,description,content,"Kentucky","appliance")
def run():
    photos=unique_washer_photos()
    pending={}
    for i,city in enumerate(CITIES):
        for kind in KINDS:
            slug=city_url(city,kind).strip("/")
            pending[slug+"/index.html"]=page_for(city,kind,i,photos)
    pending["kentucky-appliance-pickup/index.html"]=state_page()
    if len(pending)!=251:raise RuntimeError("Expected 251 distinct Kentucky pages")
    for rel,data in pending.items():
        path=ROOT/rel
        if path.exists():raise RuntimeError("Page already exists; do not overwrite "+rel)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(data,encoding="utf-8")
    manifest={"state_code":"KY","mode":"request-only","pages":sorted(pending),
        "operator_coverage_verified":False,
        "market_focus":"50 Kentucky cities centered on Louisville, Lexington, Northern Kentucky, Bowling Green, Western Kentucky and retirement/move-out markets.",
        "release_intent":"Request-only, noindex until accepting local operator, receipt and owner approval verified. No existing Kentucky completed jobs claimed.",
        "photo_policy":"Exactly one real existing used-appliance photo per page plus shared business logo. Category-specific; 50 nonduplicate washer/dryer files."}
    (ROOT/"data/ttg-state-batches/KY.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    ledger={"state_code":"KY","verified_cities":[],"form_receipt":{"verified":False,"verified_on":None,"receipt_reference":""},
        "owner_release_approval":{"approved":False,"approved_on":None,"reference":""},
        "instructions":"Do not index Kentucky city pages or advertise an established route until ZIP-specific operator acceptance, real receipt tests and owner release approval."}
    (ROOT/"data/ttg-release-readiness/KY.json").write_text(json.dumps(ledger,indent=2)+"\n",encoding="utf-8")
    service_areas=ROOT/"service-areas/index.html"
    directory=service_areas.read_text(encoding="utf-8")
    anchor='<div class="card"><a href="../south-carolina-appliance-pickup/">'
    new_link='<div class="card"><a href="../kentucky-appliance-pickup/">Kentucky — Free Appliance Pickup requests (local routes unconfirmed)</a></div>'
    if anchor not in directory or "kentucky-appliance-pickup/" in directory:
        raise RuntimeError("Service areas navigation unexpectedly changed; abort")
    service_areas.write_text(directory.replace(anchor,new_link+anchor,1),encoding="utf-8")
    print("Generated Kentucky California Gold: 50 cities, five page types each plus statewide hub = 251 complete customer-form pages.")
    print("One real appliance photo per page; 50 distinct laundry photos; live Formspree endpoint; noindex pending verified Kentucky service.")
if __name__=="__main__":
    run()
