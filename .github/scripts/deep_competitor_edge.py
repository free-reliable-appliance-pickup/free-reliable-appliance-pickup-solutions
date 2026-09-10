from pathlib import Path

ROOT = Path('.')
BASE = 'https://free-reliable-appliance-pickup.github.io/free-reliable-appliance-pickup-solutions/'


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def write(path, text):
    (ROOT / path).write_text(text, encoding='utf-8')


def set_representative_og(path, image, alt):
    text = read(path)
    old_img = f'<meta property="og:image" content="{BASE}assets/free-reliable-appliance-pickup-logo.svg">'
    new_img = f'<meta property="og:image" content="{BASE}assets/{image}">'
    text = text.replace(old_img, new_img)
    text = text.replace('<meta property="og:image:alt" content="Free Reliable Appliance Pickup logo">',
                        f'<meta property="og:image:alt" content="{alt}">')
    write(path, text)


def add_local_resource(path, heading, paragraphs, url, label):
    text = read(path)
    if 'id="local-disposal-options"' in text:
        return
    block = '\n<section class="official-local-resource" id="local-disposal-options">\n'
    block += f'<h2>{heading}</h2>\n'
    for p in paragraphs:
        block += f'<p>{p}</p>\n'
    block += f'<p><a href="{url}" rel="noopener">{label}</a></p>\n'
    block += '<p class="note">Local programs, eligibility, accepted items, fees and preparation rules can change. Confirm current requirements on the official source before setting an appliance out.</p>\n'
    block += '</section>\n'
    markers = [
        '<section>\n<h2>Appliance Pickup Guides</h2>',
        '<section id="appliance-guides">',
        '<section>\n<h2>How Free Pickup Works</h2>'
    ]
    for marker in markers:
        if marker in text:
            text = text.replace(marker, block + marker, 1)
            write(path, text)
            return
    raise RuntimeError(f'No insertion marker found in {path}')


city_resources = {
    'fresno-appliance-pickup/index.html': {
        'image': 'major-appliance-pickup-photo-2.jpg',
        'alt': 'Major household appliance example for Fresno appliance pickup requests',
        'heading': 'Fresno Appliance Disposal Alternative',
        'paragraphs': [
            'If a request does not qualify for our pickup, eligible City of Fresno residential solid-waste customers can review the city’s One-Time Bulky Item Pickup program. The city currently lists stoves and ovens among accepted bulky items, while refrigerators and freezers are listed separately as not accepted through that specific program.',
            'Because appliance acceptance differs by type, checking the city’s current instructions can help Fresno residents choose an appropriate backup option.'
        ],
        'url': 'https://www.fresno.gov/publicutilities/trash-disposal-recycling/residential-services/one-time-bulky-item-pickup/',
        'label': 'Official City of Fresno bulky-item pickup information'
    },
    'modesto-appliance-pickup/index.html': {
        'image': 'major-appliance-pickup-photo-2.jpg',
        'alt': 'Major household appliance example for Modesto appliance pickup requests',
        'heading': 'Modesto Bulky-Item Alternative',
        'paragraphs': [
            'If a request does not qualify for our pickup, City of Modesto residential solid-waste customers can review the city’s Bulky Item Collection program. The city describes scheduled bulky-item pickup options for residential customers and also publishes current drop-off opportunities.',
            'Use the official city information to confirm current appointment limits, placement rules and appliance acceptance before using the municipal program.'
        ],
        'url': 'https://permits.modestogov.com/373/Bulky-Item-Collection',
        'label': 'Official City of Modesto bulky-item collection information'
    },
    'oakland-appliance-pickup/index.html': {
        'image': 'major-appliance-pickup-photo-3.jpg',
        'alt': 'Major household appliance example for Oakland appliance pickup requests',
        'heading': 'Oakland Bulky-Junk Alternative',
        'paragraphs': [
            'If a request does not qualify for our pickup, Oakland residents can review the City of Oakland’s waste and recycling information for bulky-junk service. The city directs residents to its bulky pickup and drop-off programs and explains that renters and owners can contact the contracted provider directly for available appointments.',
            'This is a useful backup option for appliances or loads that do not meet our qualification rules.'
        ],
        'url': 'https://www.oaklandca.gov/My-Household/Waste-and-Recycling',
        'label': 'Official City of Oakland waste and bulky-service information'
    },
    'sacramento-appliance-pickup/index.html': {
        'image': 'major-appliance-pickup-photo-2.jpg',
        'alt': 'Major household appliance example for Sacramento appliance pickup requests',
        'heading': 'Sacramento Appliance Pickup Alternative',
        'paragraphs': [
            'If a request does not qualify for our pickup, City of Sacramento residential customers can review the city’s Appliance and E-Waste Pickup program. The city currently describes scheduled appliance appointments for residential collection customers and lists refrigerators, washers, dryers, stoves, ranges, ovens, dishwashers and freezers among accepted appliance categories.',
            'Multi-family properties may have different service arrangements, so residents should confirm the current city rules for their property type.'
        ],
        'url': 'https://www.cityofsacramento.gov/public-works/recycling-solid-waste/Collectionservices/service_requests/appliance_pickup',
        'label': 'Official City of Sacramento appliance and e-waste pickup information'
    },
    'san-jose-appliance-pickup/index.html': {
        'image': 'major-appliance-pickup-photo-1.jpg',
        'alt': 'Major household appliance example for San Jose appliance pickup requests',
        'heading': 'San José No-Cost Junk Pickup Alternative',
        'paragraphs': [
            'If a request does not qualify for our pickup, San José residents can review the city’s no-cost junk pickup program. The city currently lists refrigerators among the large items that can be scheduled for curbside collection and provides different instructions for single-family homes, mobile homes, apartments and condominiums.',
            'Check the city’s current service lookup and appointment instructions for the exact property before setting out an appliance.'
        ],
        'url': 'https://www.sanjoseca.gov/your-government/departments-offices/environmental-services/recycling-garbage/residents',
        'label': 'Official City of San José residential recycling and junk-pickup information'
    },
    'san-diego-appliance-pickup/index.html': {
        'image': 'major-appliance-pickup-photo-3.jpg',
        'alt': 'Major household appliance example for San Diego appliance pickup requests',
        'heading': 'San Diego Appliance Recycling Alternative',
        'paragraphs': [
            'If a request does not qualify for our pickup, the City of San Diego directs residents to WasteFreeSD for local reuse, recycling and disposal options for appliances and other bulky items. The city also notes that its planned municipal bulky-item curbside program is currently paused, so residents should verify the current option that applies to their address.',
            'For working or repairable appliances, the city also encourages reuse or donation when practical.'
        ],
        'url': 'https://www.sandiego.gov/environmental-services/recycling',
        'label': 'Official City of San Diego appliance recycling resources'
    },
    'san-francisco-appliance-pickup/index.html': {
        'image': 'major-appliance-pickup-photo-3.jpg',
        'alt': 'Major household appliance example for San Francisco appliance pickup requests',
        'heading': 'San Francisco Bulky-Item Alternative',
        'paragraphs': [
            'If a request does not qualify for our pickup, eligible San Francisco residents can review the city’s bulky-item recycling program. San Francisco Environment describes scheduled curbside bulky-item collection for eligible residents, including appliances and other large household items.',
            'Residents and apartment tenants should confirm the current appointment allowance, accepted items and set-out instructions before using the program.'
        ],
        'url': 'https://www.sfenvironment.org/bulky-items',
        'label': 'San Francisco Environment bulky-item information'
    },
    'bakersfield-appliance-pickup/index.html': {
        'image': 'major-appliance-pickup-photo-1.jpg',
        'alt': 'Major household appliance example for Bakersfield appliance pickup requests',
        'heading': 'Bakersfield Solid-Waste Alternative',
        'paragraphs': [
            'If a request does not qualify for our pickup, Bakersfield residents can review the City of Bakersfield Solid Waste Division’s current garbage, recycling and large-item information. The city periodically publishes bulky-item drop-off opportunities, and appliance acceptance can vary by event and appliance type.',
            'Refrigerant-containing appliances can have different handling rules, so confirm the current city instructions before transporting or setting out a refrigerator, freezer or air-conditioning unit.'
        ],
        'url': 'https://www.bakersfieldcity.us/garbage-recycling',
        'label': 'Official City of Bakersfield garbage and recycling information'
    },
    'stockton-appliance-pickup/index.html': {
        'image': 'major-appliance-pickup-photo-1.jpg',
        'alt': 'Major household appliance example for Stockton appliance pickup requests',
        'heading': 'Stockton Clean Sweep Alternative',
        'paragraphs': [
            'If a request does not qualify for our pickup, Stockton residents can check the City of Stockton’s Clean Sweep information for current bulky-item service options. Stockton’s contracted waste-service materials identify appliances among the types of bulky items that may be handled through scheduled service.',
            'Confirm the current appointment period, provider, accepted items and set-out requirements for your address before using the municipal option.'
        ],
        'url': 'https://www.stocktonca.gov/cleansweep',
        'label': 'City of Stockton Clean Sweep information'
    }
}

for path, cfg in city_resources.items():
    if not (ROOT / path).exists():
        print('skip missing', path)
        continue
    set_representative_og(path, cfg['image'], cfg['alt'])
    add_local_resource(path, cfg['heading'], cfg['paragraphs'], cfg['url'], cfg['label'])
    print('updated', path)

# Homepage: make the preferred social/search preview image representative instead of the logo.
set_representative_og('index.html', 'major-appliance-pickup-photo-1.jpg', 'Real major household appliance handled by Free Reliable Appliance Pickup')

# About page: strengthen first-hand experience and explain how service guidance is produced.
about = read('about/index.html')
about = about.replace(
    f'<meta property="og:image" content="{BASE}assets/free-reliable-appliance-pickup-logo.svg">',
    f'<meta property="og:image" content="{BASE}assets/major-appliance-pickup-photo-2.jpg">'
)
about = about.replace(
    '<meta property="og:image:alt" content="Free Reliable Appliance Pickup logo">',
    '<meta property="og:image:alt" content="Real household appliance handled by Free Reliable Appliance Pickup">'
)
if 'id="how-guidance-is-built"' not in about:
    block = '''\n  <section id="how-guidance-is-built">\n    <h2>How Our Appliance Pickup Guidance Is Built</h2>\n    <p>Our pickup guidance is based on hands-on appliance pickup, condition review and appliance resale experience. That is why our pages ask practical questions that matter before a crew arrives: does the washer fill, drain and spin; does the dryer heat and tumble; does the refrigerator maintain temperature; and are stairs, tight turns, gates or door removal involved?</p>\n    <p>We use real appliance photos from our work and inventory rather than stock advertising images. For local disposal alternatives, we link to city or other official service information when available so customers still have a useful next step when an appliance does not qualify for our free pickup.</p>\n    <div class="grid">\n      <figure class="card" style="margin:0"><img src="../assets/major-appliance-pickup-photo-1.jpg" alt="Real major appliance from Free Reliable Appliance Pickup work and inventory" loading="lazy" decoding="async" style="width:100%;height:240px;object-fit:cover;border-radius:8px"><figcaption>Real appliance example from our work and inventory.</figcaption></figure>\n      <figure class="card" style="margin:0"><img src="../assets/major-appliance-pickup-photo-2.jpg" alt="Household appliance evaluated by Free Reliable Appliance Pickup" loading="lazy" decoding="async" style="width:100%;height:240px;object-fit:cover;border-radius:8px"><figcaption>Condition and access details are reviewed before scheduling.</figcaption></figure>\n    </div>\n  </section>\n'''
    marker = '  <section>\n    <h2>Helpful Appliance Pickup Guides</h2>'
    if marker in about:
        about = about.replace(marker, block + marker, 1)
    else:
        raise RuntimeError('About insertion marker not found')
write('about/index.html', about)
print('updated about/index.html and index.html')
