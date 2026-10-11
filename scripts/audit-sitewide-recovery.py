#!/usr/bin/env python3
"""Read-only, whole-repository SEO / conversion inventory. No changes to pages.

This is a source audit, NOT confirmation of indexing, live Google rankings,
actual pickup coverage, successful Formspree delivery, or physical image content.
"""
from collections import Counter, defaultdict
from datetime import date
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
HOST = "freereliableappliancepickup.com"
BASE = "https://" + HOST
REPORT = ROOT / "reports/sitewide-recovery-audit.json"
PAGES = sorted(ROOT.glob("*/index.html"))
ALL_FILES = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts}
PUBLISHED = set()
try:
    root = ET.parse(ROOT / "sitemap.xml").getroot()
    for e in root.iter():
        if e.tag.rsplit("}", 1)[-1] == "loc" and e.text:
            p = urlsplit(e.text.strip())
            if p.hostname in (HOST, "www." + HOST):
                PUBLISHED.add(p.path.rstrip("/") + "/")
except Exception as exc:
    print("SITEMAP_PARSE_ERROR", str(exc))

def attrs(tag):
    return {m.group(1).lower(): unescape(m.group(3))
            for m in re.finditer(r'([\w:-]+)\s*=\s*(["\x27])(.*?)\2', tag, re.I | re.S)}

def strip(text):
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", text))).strip()

def local_file(ref, base_url):
    if not ref or ref.startswith(("#", "tel:", "sms:", "mailto:", "data:", "javascript:")):
        return None
    u = urlsplit(urljoin(base_url, unescape(ref)))
    if u.scheme not in ("http", "https") or u.hostname not in (HOST, "www." + HOST):
        return None
    path = unquote(u.path).lstrip("/")
    if not path or path.endswith("/"):
        path += "index.html"
    return path

def page_names(form):
    return {attrs(m.group(0)).get("name", "") for m in
            re.finditer(r"<(?:input|select|textarea)\b[^>]*>", form, re.I)}

def slug_city(stem):
    for s in ("-washer-dryer-pickup", "-refrigerator-pickup", "-stove-oven-pickup",
              "-freezer-pickup", "-appliance-pickup"):
        if stem.endswith(s):
            return stem[:-len(s)].replace("-", " ")
    return stem.replace("-", " ")

results = []
exact_titles = defaultdict(list)
exact_descriptions = defaultdict(list)
repeat_blocks = defaultdict(set)
js_routes_without_city = []
for p in PAGES:
    rel = p.parent.name
    path = "/" + rel + "/"
    url = BASE + path
    html = p.read_text(encoding="utf-8", errors="replace")
    head = html.split("</head>", 1)[0]
    tags = re.findall(r"<(?:meta|link)\b[^>]*>", head, re.I | re.S)
    metas = [attrs(tag) for tag in tags if re.match(r"<meta\b", tag, re.I)]
    linktags = [attrs(tag) for tag in tags if re.match(r"<link\b", tag, re.I)]
    robots = " ".join(x.get("content", "") for x in metas if x.get("name", "").lower() == "robots").lower()
    indexable = "noindex" not in robots
    canon = [x.get("href", "") for x in linktags if x.get("rel", "").lower() == "canonical"]
    title = strip((re.search(r"<title[^>]*>(.*?)</title>", head, re.I | re.S) or ["", ""])[1])
    description = next((x.get("content") for x in metas if x.get("name", "").lower() == "description"), "")
    h1 = re.findall(r"<h1\b", html, re.I)
    forms = [m.group(0) for m in re.finditer(r"<form\b[^>]*>.*?</form>", html, re.I | re.S)]
    requests = [f for f in forms if "formspree.io/" in f.lower()]
    request_fields = set().union(*(page_names(f) for f in requests)) if requests else set()
    routes_js = bool(re.search(r'<script\b[^>]*\bsrc=["\x27][^"\x27]*customer-routing\.js', html, re.I))
    links = re.findall(r'<a\b[^>]*\bhref=["\x27]([^"\x27]+)', html, re.I)
    imgs = re.findall(r'<img\b[^>]*>', html, re.I)
    broken_links, broken_images = set(), set()
    for href in links:
        file_path = local_file(href, url)
        if file_path is not None and file_path not in ALL_FILES:
            broken_links.add(file_path)
    for tag in imgs:
        src = attrs(tag).get("src", "")
        file_path = local_file(src, url)
        if file_path is not None and file_path not in ALL_FILES:
            broken_images.add(file_path)
    structured = re.findall(r'<script\b[^>]*type=["\x27]application/ld\+json["\x27][^>]*>(.*?)</script>', html, re.I | re.S)
    bad_schema = 0
    for block in structured:
        try:
            json.loads(unescape(block))
        except (ValueError, TypeError):
            bad_schema += 1
    clean = strip(html)
    visible_words = len(clean.split())
    name = slug_city(rel)
    chunks = []
    for m in re.finditer(r"<(?:p|li|h2|h3)\b[^>]*>(.*?)</(?:p|li|h2|h3)>", html, re.I | re.S):
        t = strip(m.group(1)).lower()
        if len(t) >= 65:
            t = re.sub(r"\b" + re.escape(name) + r"\b", "[city]", t, flags=re.I)
            t = re.sub(r"\b\d{5}(?:-\d{4})?\b", "[zip]", t)
            t = re.sub(r"\s+", " ", t)
            chunks.append(t)
    for chunk in set(chunks):
        repeat_blocks[chunk].add(rel)
    if indexable:
        if title:
            exact_titles[title.lower()].append(rel)
        if description:
            exact_descriptions[description.lower()].append(rel)
    problems = []
    if indexable and canon != [url]:
        problems.append("canonical_missing_or_not_self")
    if indexable and len(h1) != 1:
        problems.append("missing_or_multiple_h1")
    if indexable and (not title or not description):
        problems.append("missing_title_or_description")
    if requests and not {"city", "state", "appliance"}.issubset(request_fields):
        problems.append("intake_missing_city_state_or_appliance")
    if requests and "source_page" not in request_fields:
        problems.append("intake_missing_source_page")
    if requests and "condition" not in request_fields:
        problems.append("intake_missing_condition")
    if routes_js and requests and not {"city", "state", "appliance"}.issubset(request_fields):
        js_routes_without_city.append(rel)
    if broken_links:
        problems.append("broken_local_links")
    if broken_images:
        problems.append("broken_local_images")
    if bad_schema:
        problems.append("invalid_jsonld")
    if indexable and visible_words < 400 and rel.endswith(("-appliance-pickup", "-washer-dryer-pickup")):
        problems.append("short_location_service_copy_review")
    results.append({
        "page": path, "sitemap": path in PUBLISHED, "indexableInSource": indexable,
        "canonical": canon, "title": title, "description": description,
        "h1Count": len(h1), "visibleWordsApprox": visible_words,
        "hasRequestForm": bool(requests), "hasRoutingScript": routes_js,
        "requestFields": sorted(request_fields), "images": len(imgs),
        "jsonLdBlocks": len(structured), "brokenLinks": sorted(broken_links)[:25],
        "brokenImages": sorted(broken_images)[:25], "invalidJsonLdBlocks": bad_schema,
        "problems": problems
    })

for row in results:
    name = row["page"].strip("/")
    repeated = [chunk for chunk, sites in repeat_blocks.items()
                if name in sites and len(sites) >= 5]
    row["repeatedTextBlocksOn5PlusPages"] = len(repeated)
    if row["indexableInSource"] and row["visibleWordsApprox"] < 1100 and len(repeated) >= 6:
        row["problems"].append("thin_repeated_location_content_review")
    if row["indexableInSource"] and not row["sitemap"]:
        row["problems"].append("indexable_url_not_in_primary_sitemap")

counts = Counter(issue for row in results for issue in row["problems"])
duplicated_titles = {s: v for s, v in exact_titles.items() if len(v) >= 2}
duplicated_descriptions = {s: v for s, v in exact_descriptions.items() if len(v) >= 2}
report = {
    "date": date.today().isoformat(),
    "scope": "all root-level */index.html files in GitHub checkout; static source audit",
    "limitation": "Does not prove live Google indexing, rankings, physical partner coverage, or form delivery",
    "totals": {
        "pagesScanned": len(results), "listedInPrimarySitemap": sum(x["sitemap"] for x in results),
        "sourceIndexable": sum(x["indexableInSource"] for x in results),
        "sourceNoindex": sum(not x["indexableInSource"] for x in results),
        "missingFormRouteFields": len(js_routes_without_city),
        "exactDuplicateTitles": len(duplicated_titles),
        "exactDuplicateDescriptions": len(duplicated_descriptions)
    },
    "problemCounts": counts,
    "duplicateTitles": duplicated_titles,
    "duplicateDescriptions": duplicated_descriptions,
    "routingBrokenPageSlugs": js_routes_without_city,
    "repeatedTextClusters": [
        {"pages": sorted(sites), "sample": chunk[:180]}
        for chunk, sites in sorted(repeat_blocks.items(), key=lambda x: -len(x[1]))
        if len(sites) >= 8
    ][:75],
    "pages": results
}
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("SOURCE_PAGES_SCANNED", len(results))
print("SITEMAP_URLS", len(PUBLISHED))
for key, n in sorted(report["totals"].items()):
    print("TOTAL", key, n)
for key, n in counts.most_common():
    print("PROBLEM", key, n)
for key in ("intake_missing_city_state_or_appliance", "intake_missing_source_page",
            "intake_missing_condition", "broken_local_images", "broken_local_links",
            "canonical_missing_or_not_self", "invalid_jsonld",
            "thin_repeated_location_content_review"):
    affected = [row["page"] for row in results if key in row["problems"]]
    print("SAMPLE", key, ", ".join(affected[:20]) or "none")
print("REPORT_ARTIFACT", str(REPORT.relative_to(ROOT)))
