from pathlib import Path

ROOT = Path('.')

UPDATES = {
    'oregon-appliance-pickup/index.html': '''
<section id="oregon-request-regions">
<h2>Oregon Pickup Request Regions</h2>
<p>We organize Oregon requests by practical route areas rather than creating a separate promise for every city. Coverage is confirmed for the exact address, appliance condition and access before scheduling.</p>
<div class="grid">
<div class="card"><h3>Portland Metro</h3><p><a href="../portland-appliance-pickup/">Portland</a> is the main metro page. Requests may also be reviewed from Beaverton, Hillsboro, Gresham, Tigard, Lake Oswego, Oregon City, Milwaukie, Tualatin, Sherwood, Wilsonville, Troutdale, Clackamas and Happy Valley.</p></div>
<div class="card"><h3>Salem, Keizer &amp; Mid-Willamette Valley</h3><p>Use the <a href="../salem-appliance-pickup/">Salem</a> or <a href="../keizer-appliance-pickup/">Keizer</a> page for local details. Nearby requests can include Woodburn, Silverton, Stayton, Dallas, Monmouth, Independence, Albany, Corvallis, McMinnville, Newberg and surrounding communities, subject to current route coverage.</p></div>
<div class="card"><h3>Oregon Coast Requests</h3><p>Astoria, Seaside, Cannon Beach, Warrenton, Lincoln City, Newport and Florence requests may be submitted for review. Coastal availability varies by route, appliance condition and partner coverage, so pickup is not guaranteed until confirmed.</p></div>
</div>
<p>For every Oregon request, include the city or ZIP code, appliance condition, photos and whether the item is in a garage, first floor, upstairs, basement or outside.</p>
</section>
''',
    'washington-appliance-pickup/index.html': '''
<section id="washington-request-regions">
<h2>Washington Pickup Request Regions</h2>
<p>Washington requests are reviewed by route area and current partner coverage. Listing a community here means a request can be submitted for review; it does not guarantee free pickup before the appliance and access details are confirmed.</p>
<div class="grid">
<div class="card"><h3>Seattle &amp; Puget Sound</h3><p>Use the <a href="../seattle-appliance-pickup/">Seattle appliance pickup page</a> for Seattle-specific details. Nearby requests can include Tacoma, Shoreline, Everett, Bellevue, Lakewood, Burien, Redmond, Kirkland, Auburn, Marysville and Federal Way.</p></div>
<div class="card"><h3>Vancouver &amp; Clark County</h3><p>Vancouver and surrounding Clark County requests can be submitted using the Oregon &amp; Washington regional contact. Send the exact ZIP code and pickup access because route availability can differ across Southwest Washington.</p></div>
<div class="card"><h3>Other Washington Markets</h3><p>Olympia, Bellingham, Yakima, Kennewick and Spokane requests may also be reviewed for available service or partner coverage. Photos and working-condition details help determine whether a route is practical before scheduling.</p></div>
</div>
</section>
''',
    'colorado-appliance-pickup/index.html': '''
<section id="colorado-request-regions">
<h2>Denver Metro &amp; Colorado Pickup Request Regions</h2>
<p>Colorado requests are grouped around practical Denver Metro route areas. Free pickup remains qualification-based and is confirmed only after appliance condition, access and current coverage are reviewed.</p>
<div class="grid">
<div class="card"><h3>Denver, Aurora &amp; Central Metro</h3><p>Start with the <a href="../denver-appliance-pickup/">Denver</a> or <a href="../aurora-appliance-pickup/">Aurora</a> page. Lakewood and Wheat Ridge requests may also be reviewed based on the current route.</p></div>
<div class="card"><h3>South &amp; Southeast Metro</h3><p>Centennial, Parker, Englewood, Littleton, Highlands Ranch and Castle Rock requests may be reviewed. Include stairs, floor level, parking and any gated-community or loading restrictions.</p></div>
<div class="card"><h3>North &amp; West Metro</h3><p>Arvada, Westminster, Thornton, Commerce City, Brighton, Broomfield, Golden and Northglenn requests may be reviewed within available route coverage.</p></div>
</div>
<p>Washers and dryers are high-priority categories, and upright or chest freezers are also important Colorado pickup categories. Send the condition of every appliance separately when submitting a multi-appliance load.</p>
</section>
'''
}

for rel, block in UPDATES.items():
    path = ROOT / rel
    text = path.read_text(encoding='utf-8')
    section_id = block.split('id="', 1)[1].split('"', 1)[0]
    if f'id="{section_id}"' in text:
        print('already present', rel)
        continue
    marker = '<section>\n<h2>Frequently Asked Questions</h2>'
    if marker not in text:
        raise RuntimeError(f'FAQ marker missing: {rel}')
    text = text.replace(marker, block + marker, 1)
    path.write_text(text, encoding='utf-8')
    print('updated', rel)
