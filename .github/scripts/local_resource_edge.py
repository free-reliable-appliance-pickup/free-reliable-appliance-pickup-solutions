from pathlib import Path
import re

resources = {
    "los-angeles-appliance-pickup/index.html": '''
<section class="official-local-resource" id="local-disposal-options">
<h2>Los Angeles Appliance Disposal Alternative</h2>
<p>If an appliance does not qualify for our pickup, City of Los Angeles residents with eligible LASAN curbside service can review the city's metal appliance pickup program. LASAN lists refrigerators, freezers, washers, dryers, dishwashers, air conditioners and water heaters among accepted household metal appliances and asks residents to schedule before collection.</p>
<p><a href="https://sanitation.lacity.gov/services/metal-appliance-pickup" rel="noopener">Official LA Sanitation metal appliance pickup information</a></p>
<p class="notice">City programs, eligibility, preparation rules and availability can change. Confirm current requirements on the official page before setting an appliance out.</p>
</section>''',
    "portland-appliance-pickup/index.html": '''
<section class="official-local-resource" id="local-disposal-options">
<h2>Portland Metro Appliance Disposal Alternative</h2>
<p>If an appliance does not qualify for our pickup, Metro Central Transfer Station in Portland accepts large metal appliances. Metro lists metal dishwashers, microwaves, water heaters, stoves, ovens, washers and dryers in its appliance category; coolant-containing appliances such as refrigerators and freezers have separate handling and fees.</p>
<p><a href="https://www.oregonmetro.gov/waste-disposal-and-prevention/need-get-rid-something/metro-central-transfer-station" rel="noopener">Official Metro Central appliance disposal information</a></p>
<p class="notice">Check Metro's current fees, limits and preparation requirements before transporting an appliance.</p>
</section>''',
    "salem-appliance-pickup/index.html": '''
<section class="official-local-resource" id="local-disposal-options">
<h2>Salem-Keizer Appliance Disposal Alternative</h2>
<p>If an appliance does not qualify for our pickup, Marion County's Salem-Keizer Recycling &amp; Transfer Station accepts appliances. The county currently lists separate fees for appliances without refrigerant and appliances designed to contain refrigerant, because refrigerant must be handled professionally.</p>
<p><a href="https://www.co.marion.or.us/PW/ES/disposal/Pages/skrts.aspx" rel="noopener">Official Marion County Salem-Keizer transfer station information</a></p>
<p class="notice">Confirm current fees, hours and acceptance rules with Marion County before your trip.</p>
</section>''',
    "aurora-appliance-pickup/index.html": '''
<section class="official-local-resource" id="local-disposal-options">
<h2>Aurora Appliance Reuse &amp; Recycling Alternative</h2>
<p>If an appliance does not qualify for our pickup, the City of Aurora's appliance resource page lists local reuse and recycling options. The city notes that Habitat for Humanity ReStore may accept clean, fully working appliances that meet its age requirements and directs residents to additional recycling resources for other appliances.</p>
<p><a href="https://www.auroragov.org/residents/trash___recycling/recycling_opportunities/appliances" rel="noopener">Official City of Aurora appliance recycling information</a></p>
<p class="notice">Acceptance rules belong to the listed organizations and can change. Confirm directly before transporting an appliance.</p>
</section>''',
    "denver-appliance-pickup/index.html": '''
<section class="official-local-resource" id="local-disposal-options">
<h2>Denver Large-Item &amp; Disposal Resources</h2>
<p>If an appliance does not qualify for our pickup, Denver residents can use the City and County of Denver's waste-service resources to review large-item collection schedules and disposal options. Because appliance handling can vary by item, residents should confirm the correct program through Denver 311 before setting out or transporting an appliance.</p>
<p><a href="https://denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Recycle-Compost-Trash/Resources/Expanded-Waste-Collection-Services" rel="noopener">Official Denver waste collection resources</a></p>
<p class="notice">Confirm current appliance eligibility, collection rules and any fees with Denver before disposal.</p>
</section>''',
    "phoenix-appliance-pickup/index.html": '''
<section class="official-local-resource" id="local-disposal-options">
<h2>Phoenix Appliance Recycling Alternative</h2>
<p>If an appliance does not qualify for our pickup, the City of Phoenix provides appliance recycling information for residents. Phoenix lists transfer-station drop-off options and a scheduled curbside appliance pickup service, with different rules for appliances that contain refrigerant.</p>
<p><a href="https://www.phoenix.gov/administration/departments/publicworks/residential-trash-recycling/residential-recycling/appliance-recycling.html" rel="noopener">Official City of Phoenix appliance recycling information</a></p>
<p class="notice">Check the city's current customer eligibility, preparation requirements and fees before using the program.</p>
</section>''',
    "seattle-appliance-pickup/index.html": '''
<section class="official-local-resource" id="local-disposal-options">
<h2>Seattle Special-Item Appliance Pickup Alternative</h2>
<p>If an appliance does not qualify for our pickup, Seattle Public Utilities offers special-item collection for large appliances and publishes transfer-station appliance disposal rates. Refrigerators and freezers can have special safety and refrigerant-related requirements.</p>
<p><a href="https://www.seattle.gov/utilities/your-services/collection-and-disposal/recycling/special-item-pickup" rel="noopener">Official Seattle Public Utilities special-item pickup information</a></p>
<p class="notice">Confirm current prices, size limits, scheduling and refrigerator/freezer preparation rules with Seattle Public Utilities.</p>
</section>''',
    "riverside-appliance-pickup/index.html": '''
<section class="official-local-resource" id="local-disposal-options">
<h2>Riverside Appliance Disposal Alternative</h2>
<p>If an appliance does not qualify for our pickup, the City of Riverside offers bulky-item and cleanup programs for residents. Its current resources list several large appliances and explain that refrigerators and other refrigerant-containing appliances require different handling from ordinary curbside bulky items.</p>
<p><a href="https://www.riversideca.gov/publicworks/trash-recycling/clean-riverside" rel="noopener">Official Clean Up Riverside disposal information</a></p>
<p class="notice">Programs, event dates, residency requirements and accepted items can change. Verify current details with the City of Riverside.</p>
</section>''',
    "palm-desert-appliance-pickup/index.html": '''
<section class="official-local-resource" id="local-disposal-options">
<h2>Palm Desert Bulky Appliance Pickup Alternative</h2>
<p>If an appliance does not qualify for our pickup, the City of Palm Desert says residents can schedule bulky-item collection through its contracted waste service. Large appliances are listed among bulky items, and multifamily residents may also coordinate through their property manager.</p>
<p><a href="https://www.palmdesert.gov/community/waste" rel="noopener">Official City of Palm Desert waste and bulky-item information</a></p>
<p class="notice">Confirm current item limits, scheduling, eligibility and preparation requirements before setting an appliance out.</p>
</section>''',
    "las-vegas-appliance-pickup/index.html": '''
<section class="official-local-resource" id="local-disposal-options">
<h2>Las Vegas &amp; Nevada Appliance Recycling Alternative</h2>
<p>If an appliance does not qualify for our pickup, the Nevada Division of Environmental Protection maintains statewide recycling guidance. NDEP notes that appliances can be taken to many transfer stations and that refrigerant-containing appliances commonly require special handling or a fee.</p>
<p><a href="https://ndep.nv.gov/nevada-recycles/recycle/where-can-i-recycle" rel="noopener">Official Nevada recycling and appliance disposal guidance</a></p>
<p class="notice">Confirm the receiving facility, current fees and refrigerant requirements before transporting an appliance.</p>
</section>''',
}

for filename, section in resources.items():
    p = Path(filename)
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    if 'id="local-disposal-options"' in text:
        continue
    # Prefer insertion before FAQ content; otherwise before main closing tag.
    m = re.search(r'<section[^>]*>\s*<h2[^>]*>[^<]*(?:FAQ|Frequently Asked Questions)', text, flags=re.I)
    if m:
        text = text[:m.start()] + section + "\n" + text[m.start():]
    elif "</main>" in text:
        text = text.replace("</main>", section + "\n</main>", 1)
    else:
        text = text.replace("</body>", section + "\n</body>", 1)
    p.write_text(text, encoding="utf-8")
