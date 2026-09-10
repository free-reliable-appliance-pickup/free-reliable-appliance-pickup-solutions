from pathlib import Path
import re
import json

BASE = "https://free-reliable-appliance-pickup.github.io/free-reliable-appliance-pickup-solutions/"
p = Path("partners/index.html")
text = p.read_text(encoding="utf-8")

text = re.sub(r'<title>.*?</title>', '<title>Appliance Pickup Partner Program | Join Our Network</title>', text, count=1, flags=re.I | re.S)
text = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apply to join the Free Reliable Appliance Pickup partner network. Choose service cities and tell us about your vehicle, experience and pickup capacity.">', text, count=1, flags=re.I)
text = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="index, follow">', text, count=1, flags=re.I)

if '"@type":"WebPage"' not in text and '"@type": "WebPage"' not in text:
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": BASE + "partners/#webpage",
                "url": BASE + "partners/",
                "name": "Appliance Pickup Partner Program",
                "description": "Partner application and service-area selection for appliance pickup operators, repair shops, recyclers, resellers and hauling businesses.",
                "isPartOf": {"@id": BASE + "#website"},
                "about": {"@id": BASE + "#organization"},
            },
            {
                "@type": "Organization",
                "@id": BASE + "#organization",
                "name": "Free Reliable Appliance Pickup",
                "url": BASE,
                "logo": BASE + "assets/free-reliable-appliance-pickup-logo.svg",
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "Who can apply to become an appliance pickup partner?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Appliance pickup operators, repair or refurbishment businesses, recyclers, resellers, haulers and other reliable local operators may apply. Applications are reviewed before approval."
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "Does selecting a city guarantee territory or lead volume?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "No. City selection is an application preference only. Territory availability, approval, lead volume and partner terms vary by market and are reviewed before access is approved."
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "What information should a partner application include?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Include your contact information, primary city and state, vehicle type, appliance pickup experience, preferred cities and details about your service capacity and availability."
                        },
                    },
                ],
            },
        ],
    }
    tag = '<script type="application/ld+json">' + json.dumps(data, separators=(",", ":")) + '</script>\n'
    text = re.sub(r'</head>', tag + '</head>', text, count=1, flags=re.I)

if 'free-reliable-appliance-pickup-logo.svg' in text and '<header>\n<img' not in text:
    text = text.replace('<header>\n', '<header>\n<img src="../assets/free-reliable-appliance-pickup-logo.svg" alt="Free Reliable Appliance Pickup logo" width="110" height="110" style="max-width:110px;height:auto;margin-bottom:12px">\n', 1)

if 'id="partner-fit"' not in text:
    section = '''
<section class="card" id="partner-fit">
<h2>Who the Partner Network Is For</h2>
<div class="steps">
<div class="step"><strong>Appliance Pickup Operators</strong>Local operators with a truck, trailer, van or box truck who can safely move major household appliances.</div>
<div class="step"><strong>Repair &amp; Refurbishment Businesses</strong>Operators who can identify reusable or repairable washers, dryers, refrigerators, freezers, stoves and ranges.</div>
<div class="step"><strong>Recyclers &amp; Haulers</strong>Businesses that can responsibly handle appliance removal and route jobs efficiently in approved service areas.</div>
<div class="step"><strong>Resellers &amp; Flippers</strong>Experienced operators who understand condition, demand, repair value and safe appliance transport.</div>
</div>
<div class="green-box"><strong>Application first, approval second.</strong> Selecting cities does not guarantee territory, exclusivity, lead volume or pricing. We review market coverage and operator capacity before approving access.</div>
</section>

<section class="card" id="lead-quality">
<h2>What Makes a Useful Appliance Pickup Request</h2>
<p>Our customer intake is designed to collect the details a pickup operator needs before committing to a route. Requests can include appliance type, working condition, photos, city or ZIP code, floor level, stairs, doorway or hallway access, garage or outside placement and additional pickup notes.</p>
<p>That information helps reduce wasted trips and helps partners decide whether an appliance fits their route, vehicle and business model. Working appliances receive priority in our customer-facing service, and individual requests are still reviewed for location, access, demand and available coverage.</p>
<p><a href="../free-pickup-qualification/">Read customer pickup qualification</a> · <a href="../appliance-pickup-checklist/">See the pickup checklist</a> · <a href="../how-appliance-pickup-works/">How appliance pickup works</a></p>
</section>

<section class="card" id="real-partner-proof">
<h2>Real Appliance Example</h2>
<figure style="margin:0;max-width:720px"><img src="../assets/major-appliance-pickup-photo-2.jpg" alt="Real major appliance from Free Reliable Appliance Pickup work and inventory" loading="lazy" decoding="async" style="width:100%;height:auto;border-radius:10px"><figcaption>Real appliance photo from our work and inventory, not a stock image. Actual pickup opportunities vary by market and request.</figcaption></figure>
</section>
'''
    marker = '<section class="card" id="territories">'
    if marker in text:
        text = text.replace(marker, section + '\n' + marker, 1)
    else:
        text = text.replace('</main>', section + '\n</main>', 1)

if 'id="partner-faq"' not in text:
    faq = '''
<section class="card" id="partner-faq">
<h2>Partner Program Questions</h2>
<h3>Who can apply?</h3><p>Reliable appliance pickup operators, repair or refurbishment businesses, recyclers, haulers and resellers may apply. We review each application before approval.</p>
<h3>Does choosing a city guarantee territory?</h3><p>No. Your selected cities show where you want opportunities. Approval, territory availability, exclusivity, lead volume and partner terms vary by market.</p>
<h3>What should I include in my application?</h3><p>Include your primary market, vehicle type, appliance pickup experience, preferred cities, availability and anything that helps us understand the routes and appliance types you can handle.</p>
</section>
'''
    text = text.replace('</main>', faq + '\n</main>', 1)

if '../contact/' not in text:
    text = text.replace('</footer>', '<p><a href="../service-areas/" style="color:white">Service Areas</a> · <a href="../about/" style="color:white">About</a> · <a href="../contact/" style="color:white">Contact</a> · <a href="../terms/" style="color:white">Service Terms</a></p>\n</footer>', 1)
else:
    if 'href="../about/"' not in text:
        text = text.replace('</footer>', '<p><a href="../service-areas/" style="color:white">Service Areas</a> · <a href="../about/" style="color:white">About</a> · <a href="../contact/" style="color:white">Contact</a> · <a href="../terms/" style="color:white">Service Terms</a></p>\n</footer>', 1)

p.write_text(text, encoding="utf-8")
