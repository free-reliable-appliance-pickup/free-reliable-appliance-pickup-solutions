#!/usr/bin/env python3
"""One-time form-first finalization of 251 South Carolina pickup pages."""
from pathlib import Path
import json
import re

manifest = json.loads(Path('data/ttg-state-batches/SC.json').read_text(encoding='utf8'))
assert manifest['state_code'] == 'SC' and len(manifest['pages']) == 251
changed = 0
for rel in manifest['pages']:
    path = Path(rel)
    original = path.read_text(encoding='utf8')
    html = original
    title = re.search(r'<h1>Free (.*?) Pickup in [^<]+</h1>', html)
    if not title:
        raise ValueError(f'Missing free-pickup title: {rel}')
    label = title.group(1)
    html = re.sub(r'<button type="submit">[^<]*</button>',
                  f'<button type="submit">Request Free {label} Pickup</button>', html, count=1)
    request = re.search(r'<section id="request">(?s:.*?)</section>', html)
    if not request or '<form ' not in request.group():
        raise ValueError(f'Missing full request form: {rel}')
    section = request.group()
    html = html.replace(section, '', 1)
    html = html.replace('<main id="main">', '<main id="main">' + section, 1)
    if not (
        html.count('<h1') == 1
        and html.count('<form ') == 1
        and html.count('<section id="request">') == 1
        and html.count('<figure><img') == 1
        and '<main id="main"><section id="request">' in html
        and 'Free Reliable Appliance Pickup' in html
        and 'noindex, follow' in html
        and 'https://formspree.io/f/mvzeapzd' in html
        and not re.search('eligibility', html, re.I)
    ):
        raise ValueError(f'Failed landing page verification: {rel}')
    if html != original:
        path.write_text(html, encoding='utf8')
        changed += 1

print(f'South Carolina form-first California model: {len(manifest["pages"])} verified, {changed} updated')
