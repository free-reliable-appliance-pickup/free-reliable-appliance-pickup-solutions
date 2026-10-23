#!/usr/bin/env python3
"""Read-only source inventory of sitemap URLs AND extra on-disk HTML pages.
Not a Google indexing/ranking/lead delivery measurement or deployment audit.
"""
import argparse
from collections import Counter, defaultdict
from html import unescape
from pathlib import Path
import re
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
IMPORTANT = ["rancho-cucamonga","upland","claremont","la-verne","san-dimas","pomona",
"fontana","ontario","montclair","pasadena","corona","los-angeles","salem","portland",
"vancouver","seattle","tacoma","spokane","denver","aurora","phoenix","sacramento",
"stockton","columbus"]

def attributes(tag):
    return {k.lower():unescape(d or s) for k,d,s in
        re.findall(r'([\w-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')',tag)}

def attr_tag(html, tag_type, filter_name, filter_value, result):
    for tag in re.findall(r'<'+tag_type+r'\b[^>]*>',html,re.I):
        a=attributes(tag)
        if a.get(filter_name,"").lower()==filter_value:
            return a.get(result,"")
    return ""

def clean(html):
    return re.sub(r'\s+',' ',unescape(re.sub(r'<[^>]+>',' ',html))).strip()

def content(html):
    m=re.search(r'<main\b[^>]*>(.*?)</main>',html,re.I|re.S)
    s=m.group(1) if m else html
    return re.sub(r'<(?:script|style|noscript|svg|nav|footer)\b[^>]*>.*?</(?:script|style|noscript|svg|nav|footer)>',
        ' ',s,flags=re.I|re.S)

def slug(uri):
    path=urlsplit(uri).path or '/'
    return path if path.endswith('/') else path+'/'

def category(path):
    for ending,label in [('-washer-dryer-pickup/','washer/dryer'),('-refrigerator-pickup/','refrigerator'),
        ('-stove-oven-pickup/','stove/oven'),('-freezer-pickup/','freezer'),
        ('-appliance-pickup/','general appliance')]:
        if path.endswith(ending):return label
    return 'hubs, guides, other'

def inspect():
    root=ET.parse(ROOT/'sitemap.xml')
    urls=[x.text.strip() for x in root.findall('.//{*}loc') if x.text]
    pages=[]; missing=[]
    for url in urls:
        if urlsplit(url).hostname!='freereliableappliancepickup.com':
            missing.append((url,'wrong host'));continue
        path=slug(url)
        filename=ROOT/(path.lstrip('/')+'index.html')
        if not filename.is_file():
            missing.append((path,'HTML file missing'));continue
        html=filename.read_text(encoding='utf-8',errors='replace')
        body=content(html)
        title=re.search(r'<title[^>]*>(.*?)</title>',html,re.I|re.S)
        paragraphs={clean(p).lower() for p in
            re.findall(r'<p\b[^>]*>(.*?)</p>',body,re.I|re.S)
            if len(clean(p).split())>=12}
        pages.append(dict(path=path,
            title=clean(title.group(1)) if title else '',
            description=attr_tag(html,'meta','name','description','content'),
            robots=attr_tag(html,'meta','name','robots','content').lower(),
            canonical=attr_tag(html,'link','rel','canonical','href'),
            h1=len(re.findall(r'<h1\b[^>]*>',html,re.I)),
            words=len(clean(body).split()),
            paragraphs=paragraphs,category=category(path)))
    # Pages outside the sitemap can still be public, intentionally excluded, or
    # noindex. Scan their HTML source without assuming the files are deployed.
    sitemap_paths={slug(u) for u in urls if urlsplit(u).hostname=='freereliableappliancepickup.com'}
    omitted=[]
    for file in sorted(ROOT.rglob('index.html')):
        relative=file.relative_to(ROOT)
        if any(part.startswith('.') or part in ('node_modules','vendor','dist','build','tmp','test-fixtures')
               for part in relative.parts[:-1]):
            continue
        candidate='/' if relative.as_posix()=='index.html' else '/'+relative.parent.as_posix()+'/'
        if candidate in sitemap_paths:
            continue
        html=file.read_text(encoding='utf-8',errors='replace')
        robots=attr_tag(html,'meta','name','robots','content').lower()
        canonical=attr_tag(html,'link','rel','canonical','href')
        omitted.append(dict(path=candidate,robots=robots,canonical=canonical,
                            noindex=bool(re.search(r'\\bnoindex\\b',robots)),
                            h1=len(re.findall(r'<h1\\b[^>]*>',html,re.I)),
                            words=len(clean(content(html)).split()),
                            pickup_form='formspree.io/' in html))
    return urls,pages,missing,omitted

def write_report():
    urls,pages,missing,omitted=inspect()
    for p in pages:p['noindex']='noindex' in p['robots']
    active=[p for p in pages if not p['noindex']]
    noindex=[p for p in pages if p['noindex']]
    crosscanon=[p for p in pages if p['canonical'] and slug(p['canonical'])!=p['path']]
    missingcanon=[p for p in pages if not p['canonical']]
    thin=[p for p in active if p['words']<350]
    titles=defaultdict(list);descs=defaultdict(list)
    for p in active:
        if p['title']:titles[p['title'].lower()].append(p['path'])
        if p['description']:descs[p['description'].lower()].append(p['path'])
    dt=[(k,v) for k,v in titles.items() if len(v)>1]
    dd=[(k,v) for k,v in descs.items() if len(v)>1]
    freq=Counter(t for p in active for t in p['paragraphs'])
    copied=[]
    for p in active:
        n=len(p['paragraphs'])
        repeated=sum(freq[t]>=12 for t in p['paragraphs'])
        if n>=5 and repeated>=3 and repeated/n>=.35:
            copied.append((repeated/n,repeated,n,p['path']))
    copied.sort(reverse=True)
    counts=Counter(p['category'] for p in pages)
    lines=['# VGM sitemap-wide source quality inventory','',
       'SOURCE ONLY: this report does not establish live Google indexing, organic keyword positions, a spam penalty or lead delivery.','',
       '- Sitemap URLs: **%d**'%len(urls),
       '- Extra on-disk index.html pages absent from sitemap: **%d**'%len(omitted),
       '- Extra pages with source noindex: **%d**, without source noindex: **%d**'%(
            sum(p['noindex'] for p in omitted),sum(not p['noindex'] for p in omitted)),
       '- HTML files resolved: **%d**, missing: **%d**'%(len(pages),len(missing)),
       '- Source indexable: **%d**, sitemap noindex: **%d**'%(len(active),len(noindex)),
       '- Canonical target different URL: **%d**, canonical missing: **%d**'%(len(crosscanon),len(missingcanon)),
       '- Title missing: **%d**, description missing: **%d**'%(
           sum(not p['title'] for p in pages),sum(not p['description'] for p in pages)),
       '- H1 not exactly one: **%d**, indexable pages under 350 approximate words: **%d**'%(
           sum(p['h1']!=1 for p in pages),len(thin)),
       '- Duplicate title clusters: **%d**, description clusters: **%d**'%(len(dt),len(dd)),
       '- Indexable pages with 35%%+ shared long paragraph share: **%d**'%len(copied),
       '',
       '## URL classes','| Class | Count |','|---|---:|']
    lines.extend('| %s | %s |'%(name,n) for name,n in counts.most_common())
    lines.extend(['','## Priority city owner pages',
       '| URL | Robots | Canonical | H1 | Approx. words | Shared long paragraphs |',
       '|---|---|---|---:|---:|---:|'])
    paths={p['path']:p for p in pages}
    omitted_paths={p['path']:p for p in omitted}
    for city in IMPORTANT:
        path='/'+city+'-appliance-pickup/'
        p=paths.get(path)
        if not p:
            extra=omitted_paths.get(path)
            if extra:
                canon=('self' if extra['canonical'] and slug(extra['canonical'])==path
                       else extra['canonical'] or 'missing')
                lines.append('| %s | %s (off sitemap) | %s | %d | %d | not scored |'%(
                    path,'noindex' if extra['noindex'] else 'no noindex',
                    canon,extra['h1'],extra['words']))
            else:
                lines.append('| %s | no index.html found | - | - | - | - |'%path)
            continue
        n=len(p['paragraphs']);k=sum(freq[t]>=12 for t in p['paragraphs'])
        canon='self' if p['canonical'] and slug(p['canonical'])==p['path'] else (p['canonical'] or 'missing')
        lines.append('| %s | %s | %s | %d | %d | %d/%d |'%(
            path,'noindex' if p['noindex'] else 'indexable',canon,p['h1'],p['words'],k,n))
    def section(label,items,limit=30):
        lines.extend(['','## '+label])
        lines.extend('- '+str(x) for x in items[:limit])
        if len(items)>limit:lines.append('- And %d more'% (len(items)-limit))
        if not items:lines.append('None found.')
    section('On-disk pages excluded from sitemap',[
        '%s | %s | canonical %s | form %s'%(p['path'],
            'noindex' if p['noindex'] else 'no source noindex',
            p['canonical'] or 'missing',
            'yes' if p['pickup_form'] else 'no')
        for p in omitted],100)
    section('Unresolved sitemap URLs',['%s: %s'%(p,why) for p,why in missing])
    section('Sitemap noindex pages',[p['path'] for p in noindex],50)
    section('Non-self canonical',[p['path']+' -> '+p['canonical'] for p in crosscanon])
    section('Thin indexable source pages',[p['path']+' (%d words)'%p['words'] for p in thin])
    section('Potential repeated-paragraph page clusters',[
        '%s (%d/%d long paragraphs repeated on 12+ indexable pages, %.0f%%)'%(path,k,n,ratio*100)
        for ratio,k,n,path in copied],50)
    section('Duplicate title examples',['%d URLs | %s | %s'%(len(v),k[:80],', '.join(v[:3])) for k,v in dt],15)
    section('Duplicate description examples',['%d URLs | %s | %s'%(len(v),k[:80],', '.join(v[:3])) for k,v in dd],15)
    lines.extend(['','## Decision gate',
       'Review local operational coverage, authentic utility to the customer, 28-to-90-day Google query-page data, index reports and actual leads before rewrites. Do not bulk delete or index pages based on this source scan.',''])
    return '\n'.join(lines)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    text=write_report()
    print(text)
    if args.output:args.output.write_text(text,encoding='utf-8')
if __name__=='__main__':main()
