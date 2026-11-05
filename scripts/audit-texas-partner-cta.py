#!/usr/bin/env python3
"""Texas customer pickup intake safety: never present as partner recruitment."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

class Extract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.form_actions = []
        self.images = []
        self.fields = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'form':
            self.form_actions.append(a.get('action', ''))
        if tag == 'img':
            self.images.append(a.get('src', ''))
        if tag in {'input', 'select', 'textarea'} and a.get('name'):
            self.fields.append((a['name'], a.get('value', '')))
        if tag == 'a':
            self.links.append(a.get('href', ''))

page = Path('texas-appliance-pickup/index.html').read_text(encoding='utf-8')
parsed = Extract()
parsed.feed(page)
errors = []
# Existing pickup partners can fulfill eligible customer requests. What is
# inactive is recruitment/monetization, not existing operational partnerships.
if re.search(r'\brecruit(?:ing|ment)?\b|join (?:the )?partner network|'
             r'apply for [^<]*partner|partner (?:program|application|membership)|'
             r'paid partner(?:ship)?|texas-pickup-partner-opportunity',
             page, re.IGNORECASE):
    errors.append('Texas customer page promotes inactive partner recruitment or monetization')
if 'existing local pickup partners are available' not in page:
    errors.append('Texas page lost accurate conditional existing-partner fulfillment explanation')
if not Path('partners/index.html').is_file():
    errors.append('Future partnership program infrastructure was unexpectedly removed')
if len(parsed.form_actions) != 1 or parsed.form_actions[0] != 'https://formspree.io/f/mvzeapzd':
    errors.append('Texas customer form was changed or duplicated')
if len(parsed.images) != 2:
    errors.append('Texas statewide page should have one logo and one real garage photo')
if '<meta name="robots" content="index, follow' not in page:
    errors.append('Texas statewide index directive was changed')
if '<link rel="canonical" href="https://freereliableappliancepickup.com/texas-appliance-pickup/">' not in page:
    errors.append('Texas statewide canonical URL changed')
if 'Free Appliance Pickup Texas | Request Eligibility Review' not in page:
    errors.append('Texas title must describe customer eligibility rather than recruiting')
if not ('id="texas-city-shortcut"' in page and 'id="request"' in page
        and page.index('id="texas-city-shortcut"') < page.index('id="request"')):
    errors.append('Pickup-city selector or intake form placement changed')
fields = dict(parsed.fields)
for required in ('name','phone','address','city','zip','appliance','condition','floor','stairs','photos_available','state','source_page'):
    if required not in fields:
        errors.append('Missing customer pickup form field: '+required)
if fields.get('state') != 'TX':
    errors.append('Pickup form state changed')
if fields.get('source_page') != 'texas-appliance-pickup':
    errors.append('Pickup form source attribution changed')
if any('/partners/' in href for href in parsed.links):
    errors.append('Texas customer form links to a partner application')

print('TEXAS_CUSTOMER_INTAKE_ERRORS', len(errors))
for error in errors:
    print('ERROR', error)
if errors:
    sys.exit(1)
print('PASS: Texas customer pickup intake does not recruit partners; form, photo, indexability and source tracking preserved')
