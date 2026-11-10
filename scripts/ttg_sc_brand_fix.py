#!/usr/bin/env python3
"""Apply California-style Free Reliable Appliance Pickup branding to SC city guides.
Preserve actual route qualification, disclosure, noindex, and existing form endpoints.
"""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
KINDS = {'appliance':'Appliance','washer-dryer':'Washer & Dryer','refrigerator':'Refrigerator','stove-oven':'Stove & Oven','freezer':'Freezer'}
HEADER = '<header class="site-header"><div class="site-brand-row"><a href="/" aria-label="Free Reliable Appliance Pickup home"><img class="site-brand-logo" src="/file_00000000b7c082308dccc73e5bd3acd2.png" alt="Free Reliable Appliance Pickup logo" width="118" height="118"></a><div class="site-brand-copy"><p class="site-brand-name">Free Reliable <span>Appliance Pickup</span></p><p class="site-tagline">Cleaner • Greener • Brighter Neighborhoods</p></div><div class="site-hours">Mon–Sun · 8AM–8PM</div></div><nav class="site-nav" aria-label="Main navigation"><div class="site-nav-inner"><a href="/">Home</a><a href="/how-appliance-pickup-works/">How It Works</a><a href="/service-areas/">Service Areas</a><a href="/free-pickup-qualification/">Qualifications</a><a href="#request">Request Pickup</a><a href="/contact/">Contact</a></div></nav></header>'

def single(c, pattern, text):
    c,n=re.subn(pattern, lambda m:text, c, count=1)
    if n!=1: raise ValueError('Failed replacement: '+pattern[:50])
    return c

def update(c, city, kind):
    appliance=KINDS[kind]
    h1=f'Free {appliance} Pickup in {city}, SC'
    title=f'{city}, SC Free {appliance} Pickup | Free Reliable Appliance Pickup'
    desc=(f'Request free {appliance.lower()} pickup in {city}, South Carolina with Free Reliable Appliance Pickup. '
          'Send appliance photos and condition details. Local route availability must be confirmed.')
    c=c.replace('nav,main{max-width:1050px', 'nav[aria-label="Breadcrumb"],main{max-width:1050px').replace('nav{padding:14px 0}', 'nav[aria-label="Breadcrumb"]{padding:14px 0}')
    if 'class="site-brand-name"' not in c: c=single(c, r'<nav aria-label="Breadcrumb">', HEADER+'<nav aria-label="Breadcrumb">')
    c=single(c, r'<title>[^<]*</title>', '<title>'+escape(title)+'</title>')
    c=single(c, r'<meta name="description" content="[^"]*">', '<meta name="description" content="'+escape(desc,quote=True)+'">')
    c=single(c, r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="'+escape(title,quote=True)+'">')
    c=single(c, r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="'+escape(desc,quote=True)+'">')
    if 'property="og:site_name"' not in c:
        c=single(c, r'<meta property="og:type" content="website">', '<meta property="og:site_name" content="Free Reliable Appliance Pickup"><meta property="og:type" content="website">')
    c=single(c, r'<h1>[^<]*</h1>', '<h1>'+escape(h1)+'</h1>')
    c=single(c, r'("@type":"WebPage","name":")[^"]+', '"@type":"WebPage","name":"'+h1)
    c=c.replace('Check eligibility and request review', 'Request Free '+escape(appliance)+' Pickup')
    c=c.replace('Submit Appliance request', 'Request Free '+escape(appliance)+' Pickup')
    c=re.sub(r'<h2>Request[^<]*eligibility review</h2>', '<h2>Request Free '+escape(appliance)+' Pickup in '+escape(city)+', SC</h2>',c,flags=re.I)
    c=c.replace(' · conditional requests</strong>', ' · appliance pickup requests</strong>')
    c=c.replace(' appliance pickup eligibility</a>', ' Free Appliance Pickup</a>').replace(' pickup eligibility</a>', ' Pickup</a>')
    c=re.sub(r'<strong>Free pickup, a truck route and ZIP coverage have not been verified for this new [^<]+ page\. Submitting the form does not book collection\.</strong>', '<strong>Free pickup depends on appliance condition and confirmed local operator availability. Submission does not book a pickup.</strong>',c)
    return c

hub=(ROOT/'south-carolina-appliance-pickup/index.html').read_text(encoding='utf-8')
cities=sorted(set(re.findall(r'href="/([a-z-]+)-sc-appliance-pickup/"', hub)))
if len(cities)!=50: raise RuntimeError(f'Expected 50 city pages, found {len(cities)}')
updated=[]
for city_slug in cities:
    city=' '.join(word.capitalize() for word in city_slug.split('-'))
    for kind in KINDS:
        path=ROOT/f'{city_slug}-sc-{kind}-pickup/index.html'
        if not path.is_file(): raise FileNotFoundError(path)
        c=path.read_text(encoding='utf-8')
        new=update(c,city,kind)
        if new.count('<h1>')!=1 or new.count('class="site-brand-name"')!=1 or 'name="robots" content="noindex, follow"' not in new or '<form ' not in new: raise RuntimeError(str(path))
        updated.append((path,new))
for path,c in updated: path.write_text(c, encoding='utf-8')
print(f'Updated {len(updated)} South Carolina city and appliance pages.')
