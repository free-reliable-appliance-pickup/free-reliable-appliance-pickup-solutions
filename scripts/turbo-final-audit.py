#!/usr/bin/env python3
"""Fast final audit for the configured Turbo priority SEO network."""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE="https://freereliableappliancepickup.com/"
CFG=json.loads((ROOT/"data/turbo-seo-network.json").read_text(encoding="utf-8"))

def p(slug): return ROOT/slug/"index.html"
def url(slug): return BASE+slug+"/"
def laundry(slug):
    return slug[:-len("-appliance-pickup")]+"-washer-dryer-pickup" if slug.endswith("-appliance-pickup") else slug

def robots(raw):
    m=re.search(r'<meta\b[^>]*name=["\']robots["\'][^>]*>',raw,re.I)
    return m.group(0).lower() if m else ""

def indexable(slug):
    if not p(slug).is_file(): return False
    return "noindex" not in robots(p(slug).read_text(encoding="utf-8",errors="replace"))

def sitemap_urls():
    out=set()
    for name in ("sitemap.xml","sitemap-regular-washer-dryer.xml"):
        path=ROOT/name
        if not path.exists(): continue
        tree=ET.parse(path)
        for el in tree.getroot().iter():
            if el.tag.endswith("loc") and el.text:
                out.add(el.text.strip())
    return out

def hrefs(raw):
    return re.findall(r'href\s*=\s*["\']([^"\']+)["\']',raw,re.I)

targets=set()
for region in CFG["regions"].values():
    targets.add(region["hub"])
    targets.add(laundry(region["hub"]))
    for slug in region["members"]:
        targets.add(slug)
        targets.add(laundry(slug))
for slug in CFG.get("specialty_pages",{}):
    targets.add(slug)

published=sitemap_urls()
fail=[]
warn=[]
checked=0

for slug in sorted(targets):
    path=p(slug)
    if not path.exists():
        warn.append(f"{slug}: configured target does not exist; skipped")
        continue
    raw=path.read_text(encoding="utf-8",errors="replace")
    if "noindex" in robots(raw):
        warn.append(f"{slug}: noindex target intentionally skipped")
        continue
    checked+=1

    canon=re.findall(r'<link\b[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)',raw,re.I)
    if canon != [url(slug)]:
        fail.append(f"{slug}: canonical {canon} != {url(slug)}")
    if not re.search(r'<title>[^<]{8,}</title>',raw,re.I|re.S):
        fail.append(f"{slug}: missing/short title")
    h1=re.findall(r'<h1\b[^>]*>[\s\S]*?</h1>',raw,re.I)
    if len(h1)!=1:
        fail.append(f"{slug}: expected 1 H1, found {len(h1)}")
    if not re.search(r'<meta\b[^>]*name=["\']description["\'][^>]*content=["\'][^"\']{40,}',raw,re.I):
        fail.append(f"{slug}: missing/short meta description")
    if '<!-- turbo-seo-network-v1 -->' not in raw:
        fail.append(f"{slug}: missing turbo managed network block")
    if url(slug) not in published:
        fail.append(f"{slug}: missing from published sitemaps")
    if "<img" not in raw.lower():
        fail.append(f"{slug}: no image")
    internal=0
    for href in hrefs(raw):
        if href.startswith("/"):
            internal+=1
            clean=href.split("#",1)[0].split("?",1)[0].strip("/")
            if clean and (ROOT/clean/"index.html").exists() and not indexable(clean):
                # Ignore navigation to intentionally consolidated aliases only when outside the managed block.
                marker=raw.find("<!-- turbo-seo-network-v1 -->")
                end=raw.find("</section>",marker) if marker>=0 else -1
                if marker>=0 and end>=0 and href in raw[marker:end]:
                    fail.append(f"{slug}: turbo block links to noindex target {clean}")
    if internal < 3:
        fail.append(f"{slug}: fewer than 3 internal links")

print("TURBO_CONFIGURED_TARGETS",len(targets))
print("TURBO_INDEXABLE_TARGETS_CHECKED",checked)
print("TURBO_WARNINGS",len(warn))
for x in warn: print("WARN",x)
if fail:
    print("TURBO_FINAL_AUDIT_FAILURES",len(fail))
    for x in fail: print("FAIL",x)
    sys.exit(1)
print("PASS: Turbo priority network has valid canonicals, metadata, H1s, managed links, sitemap coverage and images.")
