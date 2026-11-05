#!/usr/bin/env python3
"""Enforce future-only public Partner Program while preserving existing operations."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms=[]
        self.main=[]
        self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='form': self.forms.append(a)
        if tag=='main': self.main.append(a)
        if tag=='a': self.links.append(a.get('href',''))

page=Path('partners/index.html').read_text(encoding='utf-8')
parsed=Parser()
parsed.feed(page)
errors=[]
def require(ok,msg):
    if not ok: errors.append(msg)
require('<meta name="robots" content="noindex, follow' in page,
        'prelaunch program must not advertise an indexable application')
require(len(parsed.forms)==1, 'the future partner form must be retained exactly once')
if len(parsed.forms)==1:
    form=parsed.forms[0]
    require(form.get('id')=='partnerForm','future form id altered')
    require(form.get('data-public-enrollment')=='paused','partner enrollment not marked paused')
    require(form.get('action')=='#' and form.get('method','').lower()=='get',
            'public partner form must not send requests to Formspree')
    require(form.get('data-future-form-action')=='https://formspree.io/f/mvzeapzd',
            'future Formspree action missing from inactive configuration')
    require(form.get('onsubmit')=='return false',
            'partner form needs a no-submit safeguard while paused')
require(any('hidden' in m and 'inert' in m and
            m.get('data-partnership-program')=='future-only'
            for m in parsed.main), 'future program content and form must be hidden and inert')
require('Public partner applications are not open yet' in page,
        'visible future-program announcement missing')
require('existing local partners' in page,
        'existing operational pickup partnerships must be preserved')
require('selling partner memberships, territories, subscriptions or leads at this time' in page,
        'inactive paid program disclosure missing')
require('<a href="/contact/">' in page, 'existing partner contact path unavailable')
require('name="Primary State"' in page and 'name="Preferred Lead Access Model"' in page,
        'future form field infrastructure unexpectedly deleted')
require('href="#apply"' not in page.split('<main class="container" hidden',1)[0],
        'public navigation still links into inactive application')
require(not any((form.get('action') or '').startswith('https://formspree.io/f/') for form in parsed.forms),
        'public partner form still posts to shared customer inbox')
require('data-future-form-action=' in page,
        'future activation route not retained')
jsonld=re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>',page)
if not jsonld:
    errors.append('original JSON-LD missing')
else:
    try: json.loads(jsonld.group(1))
    except json.JSONDecodeError: errors.append('original JSON-LD invalid')
print('PARTNER_PRELAUNCH_ERRORS',len(errors))
for e in errors: print('ERROR',e)
if errors: sys.exit(1)
print('PASS: paid partner enrollment remains paused, form retained, customer operations unaffected')
