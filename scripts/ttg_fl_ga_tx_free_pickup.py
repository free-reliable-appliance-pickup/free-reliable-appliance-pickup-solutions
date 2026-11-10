#!/usr/bin/env python3
"""California model customer-facing Free Pickup copy: Florida, Georgia, Texas.

No changes to route availability, Formspree endpoint or field names, canonical
URLs, photos, internal link hrefs, consent requirements, or robots/indexing.
Run --apply for guarded batch, then --check for idempotent verification.
"""
from pathlib import Path
from html import escape, unescape
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
STATES={"FL":"Florida", "GA":"Georgia", "TX":"Texas"}
KINDS={"appliance":"Appliance", "washer-dryer":"Washer & Dryer",
       "refrigerator":"Refrigerator", "stove-oven":"Stove & Oven",
       "freezer":"Freezer"}
FORM="https://formspree.io/f/mvzeapzd"

def items():
    pairs={}
    for code, state in STATES.items():
        for kind in KINDS:
            for path in ROOT.glob("*-"+code.lower()+"-"+kind+"-pickup/index.html"):
                rel=path.relative_to(ROOT).as_posix()
                pairs[rel]=(code,kind,False)
        state_rel=state.lower()+"-appliance-pickup/index.html"
        pairs[state_rel]=(code,"appliance",True)
    if len(pairs)<800:
        raise RuntimeError(f"Unexpectedly few FL, GA, TX request pages ({len(pairs)}); stop")
    return sorted(pairs.items())

def strip_tags(html):
    return unescape(re.sub(r"<[^>]*>", "", html)).strip()

def clean_text(text):
    replacements=[
        (r"\bfree appliance pickup eligibility requests?\b","free appliance pickup requests"),
        (r"\bfree appliance pickup eligibility\b","free appliance pickup"),
        (r"\bappliance pickup eligibility\b","appliance pickup"),
        (r"\bfree pickup eligibility\b","free pickup availability"),
        (r"\bpickup eligibility\b","pickup availability"),
        (r"\beligibility reviews?\b","pickup reviews"),
        (r"\beligibility requests?\b","pickup requests"),
        (r"\beligibility inquiries?\b","pickup requests"),
        (r"\beligibility guides?\b","pickup guides"),
        (r"\beligibility checks?\b","pickup reviews"),
        (r"\beligibility\b","pickup information"),
        (r"\bcheck eligibility\b","request free pickup"),
    ]
    for old,new in replacements:
        text=re.sub(old,new,text,flags=re.I)
    text=re.sub(r"\b(?:pickup|request) review review\b","pickup review",text,flags=re.I)
    text=re.sub(r"\bfree free\b","free",text,flags=re.I)
    text=re.sub(r"\ban pickup\b","a pickup",text,flags=re.I)
    return text

def city_for(rel,code,raw):
    m=re.match(r"^([a-z0-9-]+)-"+code.lower()+r"-",Path(rel).parent.name)
    if not m: raise RuntimeError("Unrecognized city page "+rel)
    slug=m.group(1)
    h1=re.search(r"<h1\b[^>]*>([\s\S]*?)</h1>",raw,re.I)
    title=re.search(r"<title>([^<]+)</title>",raw,re.I)
    for text in [strip_tags(h1.group(1)) if h1 else "", unescape(title.group(1)) if title else ""]:
        # Prefer correctly styled city names already present on the original page.
        m1=re.search(r"\bin\s+(.+?),\s*"+code+r"\b",text,re.I)
        if m1:
            city=m1.group(1).split(" Pickup in ")[-1].strip()
            if city and len(city)<80:return city
        m2=re.search(r"^(.+?),\s*"+code+r"\b",text,re.I)
        if m2:
            city=m2.group(1).strip()
            if city and "Pickup" not in city and len(city)<80:return city
    special={"mckinney":"McKinney","mcallen":"McAllen","desoto":"DeSoto",
             "st-petersburg":"St. Petersburg","st-augustine":"St. Augustine",
             "la-porte":"La Porte","el-paso":"El Paso","fort-worth":"Fort Worth",
             "fort-lauderdale":"Fort Lauderdale","north-miami":"North Miami"}
    return special.get(slug," ".join(s.capitalize() for s in slug.split("-")))

def update_meta(s,key,value,attribute="property"):
    pattern=r"(<meta\b(?=[^>]*\b"+attribute+r'="'+re.escape(key)+r'")[^>]*\bcontent=")[^"]*(")'
    return re.sub(pattern,lambda m:m.group(1)+escape(value,quote=True)+m.group(2),s,flags=re.I)

def update_schema(m,title,description):
    try: obj=json.loads(m.group(2))
    except (ValueError,TypeError):return m.group(0)
    def walk(n):
        if isinstance(n,list):
            for a in n:walk(a)
        elif isinstance(n,dict):
            tp=n.get("@type",[])
            typ=[tp] if isinstance(tp,str) else tp if isinstance(tp,list) else []
            if "WebPage" in typ:
                n["name"]=title
                if "description" in n:n["description"]=description
            for key,val in list(n.items()):
                if isinstance(val,(dict,list)):walk(val)
                elif isinstance(val,str) and key in ("name","description","text","headline") and "eligibilit" in val.lower():
                    n[key]=clean_text(val)
    walk(obj)
    return m.group(1)+json.dumps(obj,ensure_ascii=False,separators=(",",":"))+m.group(3)

def revise(s,rel,code,kind,is_state):
    original=s
    city=STATES[code] if is_state else city_for(rel,code,s)
    label=KINDS[kind]
    loc=STATES[code] if is_state else city+", "+code
    h1_text="Free "+label+" Pickup in "+loc
    title=h1_text+" | Free Reliable Appliance Pickup"
    h1=re.search(r"(<h1\b[^>]*>)([\s\S]*?)(</h1>)",s,re.I)
    if not h1:raise RuntimeError("Missing H1 "+rel)
    s=s[:h1.start(2)]+escape(h1_text)+s[h1.end(2):]
    title_nodes=list(re.finditer(r"<title>([^<]*)</title>",s,re.I))
    if len(title_nodes)!=1:raise RuntimeError("Missing/duplicate title "+rel)
    s=s[:title_nodes[0].start(1)]+escape(title)+s[title_nodes[0].end(1):]
    s=update_meta(s,"og:title",title)
    s=update_meta(s,"twitter:title",title,"name")
    desc_match=re.search(r'(<meta\b(?=[^>]*name="description")[^>]*content=")([^"]*)(")',s,re.I)
    if desc_match:
        description=clean_text(unescape(desc_match.group(2)))
        s=s[:desc_match.start(2)]+escape(description,quote=True)+s[desc_match.end(2):]
    else:
        description="Request free "+label.lower()+" pickup in "+loc+" with Free Reliable Appliance Pickup. Pickup is subject to confirmed local availability."
    s=update_meta(s,"og:description",description)
    s=update_meta(s,"twitter:description",description,"name")
    s=re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)([\s\S]*?)(</script>)',
             lambda m:update_schema(m,title,description),s,flags=re.I)
    # Do not alter CSS/JS, HTML attributes, form input names, or legal link URLs.
    pieces=re.split(r'(<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>)',s,flags=re.I)
    for i in range(0,len(pieces),2):
        pieces[i]=re.sub(r"(?<=>)[^<>]+(?=<)",lambda m:clean_text(m.group(0)),pieces[i])
    s="".join(pieces)
    # Explicitly normalize customer-submission buttons; preserve any ZIP search,
    # call, text, or continuation buttons that do not submit a pickup form.
    # Normalize buttons without touching those containing icons or markup.
    def normalize_button(m):
        attrs,body=m.group(1),m.group(2)
        old=strip_tags(body).lower()
        if re.search(r'\btype=["\']button["\']',attrs,re.I):return m.group(0)
        if not any(word in old for word in ("submit","eligib","request")):return m.group(0)
        if "paid" in old or "quote" in old:return m.group(0)
        return "<button"+attrs+">Request Free "+escape(label)+" Pickup</button>"
    s=re.sub(r'<button([^>]*)>([^<>]*)</button>',normalize_button,s,flags=re.I)
    return s

def validate(before,after,rel,code,kind,is_state):
    label="Free "+KINDS[kind]+" Pickup"
    errs=[]
    def assert_condition(condition,msg):
        if not condition:errs.append(msg)
    title=re.search(r"<title>(.*?)</title>",after,re.I|re.S)
    h1=re.search(r"<h1[^>]*>([\s\S]*?)</h1>",after,re.I)
    assert_condition(bool(title and label in strip_tags(title.group(1))),"title")
    assert_condition(bool(h1 and label in strip_tags(h1.group(1))),"H1")
    assert_condition("Free Reliable Appliance Pickup" in after,"brand")
    assert_condition(FORM in after,"Formspree")
    assert_condition(len(re.findall(r"<form\b",before,re.I))==len(re.findall(r"<form\b",after,re.I)),"form count")
    assert_condition(len(re.findall(r"<img\b",before,re.I))==len(re.findall(r"<img\b",after,re.I)),"photo count")
    assert_condition(re.findall(r'<meta\b[^>]*name="robots"[^>]*>',before,re.I)==re.findall(r'<meta\b[^>]*name="robots"[^>]*>',after,re.I),"robots metadata")
    assert_condition(re.findall(r'href="([^"]+)"',before)==re.findall(r'href="([^"]+)"',after),"links")
    assert_condition(re.findall(r'\bname="([^"]+)"',before)==re.findall(r'\bname="([^"]+)"',after),"input names")
    # Validate only customer-facing title, main heading and buttons for this pass;
    # service terms may truthfully use 'qualifying' or 'eligible' outside the headline.
    for name,raw in (("title",title.group(1) if title else ""),("H1",h1.group(1) if h1 else "")):
        assert_condition("eligibilit" not in strip_tags(raw).lower(),"eligibility in "+name)
    for m in re.finditer(r'<button\b[^>]*>([\s\S]*?)</button>',after,re.I):
        assert_condition("eligibilit" not in strip_tags(m.group(1)).lower(),"eligibility button")
    for block in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>([\s\S]*?)</script>',after,re.I):
        try:json.loads(block)
        except ValueError:errs.append("invalid JSON-LD")
    assert_condition("pickup in Free " not in after,"duplicate city")
    if errs:raise RuntimeError(rel+": "+", ".join(errs))

def main(mode):
    pages=items()
    updated=[]
    for rel,params in pages:
        path=ROOT/rel
        s=path.read_text(encoding="utf-8")
        after=revise(s,rel,*params) if mode=="--apply" else s
        validate(s,after,rel,*params)
        if after!=s:updated.append((path,after))
    for path,content in updated:
        path.write_text(content,encoding="utf-8")
    print(f"PASS: validated {len(pages)} FL, GA, TX city and state request pages; changed {len(updated)} in mode {mode}")

if __name__=="__main__":
    if len(sys.argv)!=2 or sys.argv[1] not in ("--apply","--check"):
        sys.exit("Usage: python3 scripts/ttg_fl_ga_tx_free_pickup.py --apply|--check")
    main(sys.argv[1])
