#!/usr/bin/env python3
"""VGM: verify Portland's existing location/stairs fields require an explicit choice.
Source-only; does not submit or alter customer leads.
"""
from html.parser import HTMLParser
from pathlib import Path

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms = []
        self.form = None
        self.select = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'form':
            self.form = {'action': a.get('action'), 'fields': {}, 'options': {}}
            self.forms.append(self.form)
        elif self.form is not None and tag in ('input','select','textarea'):
            name = a.get('name')
            if name: self.form['fields'][name] = a
            if tag == 'select' and name:
                self.select = name
                self.form['options'][name] = []
        elif self.form is not None and tag == 'option' and self.select:
            self.form['options'][self.select].append(a)
    def handle_endtag(self, tag):
        if tag == 'select': self.select = None
        if tag == 'form': self.form = None

def errors(raw):
    scan = Scan()
    scan.feed(raw)
    if len(scan.forms) != 1: return ['expected one form']
    f = scan.forms[0]
    out = []
    if f['action'] != 'https://formspree.io/f/mvzeapzd': out.append('form endpoint changed')
    for name in ('name','phone','address','city','zip','appliance','condition','location','stairs'):
        if 'required' not in f['fields'].get(name, {}): out.append(name+' not required')
    for name in ('location','stairs'):
        opts = f['options'].get(name, [])
        if len(opts)<2 or opts[0].get('value') != '': out.append(name+' must start blank')
    for name, expected in [('source_page','portland-appliance-pickup'),('service','General major appliance pickup')]:
        if f['fields'].get(name,{}).get('value')!=expected: out.append(name+' attribution changed')
    return out

html = Path('portland-appliance-pickup/index.html').read_text()
assert errors(html) == [], errors(html)
for name in ('location','stairs'):
    broken = html.replace('name="'+name+'" required>', 'name="'+name+'">', 1)
    assert broken != html and name+' not required' in errors(broken), 'negative required '+name
    broken = html.replace('name="'+name+'" required>\n<option value="">', 'name="'+name+'" required>\n<option value="auto">', 1)
    assert broken != html and name+' must start blank' in errors(broken), 'negative default '+name
assert 'https://freereliableappliancepickup.com/portland-appliance-pickup/' in html
assert '/portland-group-appliances.webp' in html
print('PASS Portland required access fields, existing intake routing, and four negative fixtures')
