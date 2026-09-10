from pathlib import Path
import re

ROOT = Path('.')
BASE = 'https://free-reliable-appliance-pickup.github.io/free-reliable-appliance-pickup-solutions/'
LOGO_OG = f'<meta property="og:image" content="{BASE}assets/free-reliable-appliance-pickup-logo.svg">'

# 1) Use the first real appliance photo already present on each indexable page as its OG image.
for path in ROOT.rglob('index.html'):
    text = path.read_text(encoding='utf-8')
    if 'noindex' in text.lower():
        continue
    if LOGO_OG not in text:
        continue
    m = re.search(r'<img[^>]+src=["\'](?:\.\./|/free-reliable-appliance-pickup-solutions/|https://free-reliable-appliance-pickup\.github\.io/free-reliable-appliance-pickup-solutions/)?assets/(major-appliance-pickup-photo-[123]\.jpg)["\']', text, re.I)
    if not m:
        continue
    image = m.group(1)
    text = text.replace(LOGO_OG, f'<meta property="og:image" content="{BASE}assets/{image}">')
    text = text.replace('<meta property="og:image:alt" content="Free Reliable Appliance Pickup logo">',
                        '<meta property="og:image:alt" content="Real major household appliance handled by Free Reliable Appliance Pickup">')
    path.write_text(text, encoding='utf-8')
    print('OG image updated:', path)

# 2) Enrich the homepage Organization entity with real regional contact points.
path = ROOT / 'index.html'
text = path.read_text(encoding='utf-8')
if '"contactPoint"' not in text.split('"@type":"Service"', 1)[0]:
    marker = f'"url":"{BASE}",\n      "areaServed"'
    contact = f'''"url":"{BASE}",\n      "contactPoint":[\n        {{"@type":"ContactPoint","contactType":"customer service","telephone":"+1-503-868-4455","areaServed":["Oregon","Washington"]}},\n        {{"@type":"ContactPoint","contactType":"customer service","telephone":"+1-909-375-6685","areaServed":["Inland Empire","Orange County","Riverside County","Coachella Valley","Victor Valley","San Gabriel Valley"]}},\n        {{"@type":"ContactPoint","contactType":"customer service","telephone":"+1-310-774-4304","areaServed":["Los Angeles County","California"]}},\n        {{"@type":"ContactPoint","contactType":"customer service","telephone":"+1-720-604-7498","areaServed":["Colorado"]}}\n      ],\n      "areaServed"'''
    if marker not in text:
        raise RuntimeError('Homepage Organization marker not found')
    text = text.replace(marker, contact, 1)
    path.write_text(text, encoding='utf-8')
    print('Homepage Organization contact points added')
