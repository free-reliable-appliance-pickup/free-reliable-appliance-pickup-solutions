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
    require(form.get('action')=='https://formspree.io/f/mvzeapzd' and
            form.get('method','').lower()=='post',
            'future Formspree source form unexpectedly modified or lost')
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
# The inactive form is hidden/inert even without JavaScript; runtime also replaces
# its POST action and stops submit to avoid accidental public partner inquiries.
guard=Path('assets/partner-program-prelaunch.js').read_text(encoding='utf-8')
require('<script src="/assets/partner-program-prelaunch.js" defer></script>' in page,
        'public partner-page prelaunch guard script not loaded')
for text in ("setAttribute('action', '#')", "setAttribute('method', 'GET')",
             "event.preventDefault()", "event.stopImmediatePropagation()",
             "submit.disabled = true", "section.hidden = true", "section.inert = true"):
    require(text in guard, 'missing partner-form runtime guard: '+text)
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
