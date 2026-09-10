from pathlib import Path

ROOT = Path('.')
TARGET = 'old-appliance-disposal-options/'

# Homepage: add a fourth helpful-guide card and nav resource link.
p = ROOT / 'index.html'
t = p.read_text(encoding='utf-8')
if TARGET not in t:
    marker = '<div class="card"><h3><a href="landlord-property-manager-appliance-pickup/">Landlord &amp; Property Manager Guide</a></h3><p>Plan appliance removal for rentals, turnovers, garages and multi-unit properties.</p></div>'
    addition = marker + '\n<div class="card"><h3><a href="old-appliance-disposal-options/">What to Do With an Old Appliance</a></h3><p>Compare reuse, qualifying free pickup, retailer take-back, municipal collection and responsible recycling options.</p></div>'
    if marker not in t:
        raise RuntimeError('homepage guide marker missing')
    t = t.replace(marker, addition, 1)
    p.write_text(t, encoding='utf-8')
    print('linked homepage')

# Supporting guides: add contextual links near closing main content/footer.
links = {
    'about/index.html': '<p><a href="../old-appliance-disposal-options/">Compare reuse, pickup and responsible appliance disposal options</a></p>',
    'free-pickup-qualification/index.html': '<p><a href="../old-appliance-disposal-options/">If an appliance does not qualify, compare other reuse and disposal options</a></p>',
    'refrigerator-pickup/index.html': '<p><a href="../old-appliance-disposal-options/">See safe reuse, pickup and recycling options for old appliances</a></p>',
    'washer-dryer-pickup/index.html': '<p><a href="../old-appliance-disposal-options/">Compare reuse, pickup and recycling options for old appliances</a></p>',
    'stove-oven-pickup/index.html': '<p><a href="../old-appliance-disposal-options/">Compare reuse, pickup and disposal options for old appliances</a></p>',
    'freezer-pickup/index.html': '<p><a href="../old-appliance-disposal-options/">See safe reuse, pickup and recycling options for old appliances</a></p>'
}

for rel, link in links.items():
    p = ROOT / rel
    if not p.exists():
        continue
    t = p.read_text(encoding='utf-8')
    if 'old-appliance-disposal-options/' in t:
        continue
    if '</main>' in t:
        t = t.replace('</main>', f'<section class="related-disposal-guide"><h2>Need Another Appliance Disposal Option?</h2>{link}</section>\n</main>', 1)
        p.write_text(t, encoding='utf-8')
        print('linked', rel)
