#!/usr/bin/env python3
import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import time
from html import unescape

BASE = "https://freereliableappliancepickup.com"
UA = "FreeReliableSEOHealthMonitor/1.1 (+https://freereliableappliancepickup.com/)"
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
MAX_FETCH_ATTEMPTS = 3

PRIORITY_PATHS = [
    "/",
    "/rancho-cucamonga-appliance-pickup/",
    "/rancho-cucamonga-washer-dryer-pickup/",
    "/upland-appliance-pickup/",
    "/upland-washer-dryer-pickup/",
    "/claremont-appliance-pickup/",
    "/claremont-washer-dryer-pickup/",
    "/la-verne-appliance-pickup/",
    "/la-verne-washer-dryer-pickup/",
    "/san-dimas-appliance-pickup/",
    "/san-dimas-washer-dryer-pickup/",
    "/pomona-appliance-pickup/",
    "/pomona-washer-dryer-pickup/",
    "/inland-empire-appliance-pickup/",
    "/san-gabriel-valley-appliance-pickup/",
    "/orange-county-appliance-pickup/",
    "/phoenix-appliance-pickup/",
    "/fresno-appliance-pickup/",
    "/portland-appliance-pickup/",
    "/salem-appliance-pickup/",
    "/denver-appliance-pickup/",
    "/service-areas/",
]

CTX = ssl.create_default_context()

def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8"})
    last_error = None
    for attempt in range(1, MAX_FETCH_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                body = r.read().decode("utf-8", "replace")
                return r.getcode(), r.geturl(), dict(r.headers), body
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code not in RETRYABLE_STATUS or attempt == MAX_FETCH_ATTEMPTS:
                raise
        except (urllib.error.URLError, TimeoutError) as e:
            last_error = e
            if attempt == MAX_FETCH_ATTEMPTS:
                raise
        time.sleep(attempt)
    raise last_error

def text_content(html):
    txt = re.sub(r"<script\b[\s\S]*?</script>", " ", html, flags=re.I)
    txt = re.sub(r"<style\b[\s\S]*?</style>", " ", txt, flags=re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    return re.sub(r"\s+", " ", unescape(txt)).strip()

def first(pattern, html):
    m = re.search(pattern, html, re.I | re.S)
    return unescape(m.group(1)).strip() if m else ""

def canonical(html):
    m = re.search(r'<link[^>]+rel=["\'][^"\']*canonical[^"\']*["\'][^>]+href=["\']([^"\']+)', html, re.I)
    if not m:
        m = re.search(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\'][^"\']*canonical[^"\']*["\']', html, re.I)
    return unescape(m.group(1)).strip() if m else ""

def meta_content(html, name):
    patterns = [
        rf'<meta[^>]+name=["\']{re.escape(name)}["\'][^>]+content=["\']([^"\']*)',
        rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']{re.escape(name)}["\']'
    ]
    for p in patterns:
        v = first(p, html)
        if v:
            return v
    return ""

def jsonld_errors(html):
    errors = []
    blocks = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>', html, re.I)
    for i, block in enumerate(blocks, 1):
        try:
            json.loads(unescape(block).strip())
        except Exception as e:
            errors.append(f"JSON-LD block {i}: {e}")
    return len(blocks), errors

def jsonld_duplicate_webpage_ids(html):
    ids = []
    blocks = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>', html, re.I)

    def collect(node):
        if not isinstance(node, dict):
            return
        node_type = node.get("@type")
        is_webpage = node_type == "WebPage" or (isinstance(node_type, list) and "WebPage" in node_type)
        if is_webpage and node.get("@id"):
            ids.append(str(node["@id"]).strip())
        graph = node.get("@graph")
        if isinstance(graph, list):
            for item in graph:
                collect(item)

    for block in blocks:
        try:
            collect(json.loads(unescape(block).strip()))
        except Exception:
            continue

    seen = set()
    duplicates = []
    for item in ids:
        if item in seen and item not in duplicates:
            duplicates.append(item)
        seen.add(item)
    return duplicates

def audit_page(url):
    findings = []
    try:
        status, final_url, headers, html = fetch(url)
    except Exception as e:
        return [f"FAIL fetch: {e}"], None

    if status != 200:
        findings.append(f"HTTP status {status}")
    if final_url.rstrip("/") != url.rstrip("/"):
        findings.append(f"Redirected to {final_url}")

    title = first(r"<title[^>]*>([\s\S]*?)</title>", html)
    desc = meta_content(html, "description")
    robots = meta_content(html, "robots").lower()
    canon = canonical(html)
    h1s = re.findall(r"<h1\b[^>]*>([\s\S]*?)</h1>", html, re.I)
    visible = text_content(html)
    ld_count, ld_errors = jsonld_errors(html)
    duplicate_webpages = jsonld_duplicate_webpage_ids(html)

    if not title:
        findings.append("Missing <title>")
    elif not (25 <= len(title) <= 70):
        findings.append(f"Title length {len(title)} chars")

    if not desc:
        findings.append("Missing meta description")
    elif not (70 <= len(desc) <= 180):
        findings.append(f"Meta description length {len(desc)} chars")

    if "noindex" in robots:
        findings.append("CRITICAL: meta robots contains noindex")

    if not canon:
        findings.append("Missing canonical")
    else:
        expected = url
        if canon.rstrip("/") != expected.rstrip("/"):
            findings.append(f"Canonical mismatch: {canon}")
        if "github.io" in canon:
            findings.append(f"CRITICAL: canonical points to github.io: {canon}")

    if len(h1s) != 1:
        findings.append(f"Expected exactly 1 H1, found {len(h1s)}")

    if len(visible) < 500:
        findings.append(f"Very thin rendered text: {len(visible)} chars")

    if ld_count == 0:
        findings.append("No JSON-LD structured data found")
    findings.extend(ld_errors)
    for duplicate_id in duplicate_webpages:
        findings.append(f"Duplicate WebPage JSON-LD @id: {duplicate_id}")

    return findings, {
        "title": title,
        "description": desc,
        "canonical": canon,
        "robots": robots,
        "jsonld_blocks": ld_count,
        "text_chars": len(visible),
    }

def sitemap_urls():
    url = BASE + "/sitemap.xml"
    status, _, _, xml = fetch(url)
    if status != 200:
        raise RuntimeError(f"sitemap.xml returned {status}")
    root = ET.fromstring(xml)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text.strip() for loc in root.findall(".//s:loc", ns) if loc.text]

def check_robots():
    findings = []
    try:
        status, _, _, body = fetch(BASE + "/robots.txt")
        if status != 200:
            findings.append(f"robots.txt returned HTTP {status}")
        if "sitemap:" not in body.lower():
            findings.append("robots.txt does not advertise a sitemap")
        if re.search(r"(?mi)^\s*disallow:\s*/\s*$", body):
            findings.append("CRITICAL: robots.txt appears to disallow the entire site")
    except Exception as e:
        findings.append(f"robots.txt fetch failed: {e}")
    return findings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="Also verify every sitemap URL returns 200 and is not noindex")
    ap.add_argument("--report", default="seo-health-report.md")
    args = ap.parse_args()

    problems = []
    checked = 0

    robots_findings = check_robots()
    for f in robots_findings:
        problems.append(("robots.txt", f))

    try:
        sm_urls = sitemap_urls()
        sm_set = {u.rstrip("/") for u in sm_urls}
        for path in PRIORITY_PATHS:
            u = BASE + path
            if u.rstrip("/") not in sm_set:
                problems.append((u, "Priority URL missing from sitemap.xml"))
    except Exception as e:
        sm_urls = []
        problems.append(("sitemap.xml", f"FAIL: {e}"))

    for path in PRIORITY_PATHS:
        url = BASE + path
        findings, _ = audit_page(url)
        checked += 1
        for f in findings:
            problems.append((url, f))

    if args.full and sm_urls:
        for url in sm_urls:
            if url.rstrip("/") in { (BASE+p).rstrip("/") for p in PRIORITY_PATHS }:
                continue
            try:
                status, final_url, _, html = fetch(url, timeout=15)
                checked += 1
                if status != 200:
                    problems.append((url, f"HTTP {status}"))
                robots = meta_content(html, "robots").lower()
                if "noindex" in robots:
                    problems.append((url, "meta robots contains noindex"))
                canon = canonical(html)
                if not canon:
                    problems.append((url, "Missing canonical"))
                elif canon.rstrip("/") != url.rstrip("/"):
                    problems.append((url, f"Canonical mismatch: {canon}"))
                for duplicate_id in jsonld_duplicate_webpage_ids(html):
                    problems.append((url, f"Duplicate WebPage JSON-LD @id: {duplicate_id}"))
            except Exception as e:
                problems.append((url, f"Fetch failed: {e}"))

    lines = [
        "# SEO Health Monitor",
        "",
        f"- Site: {BASE}",
        f"- Pages checked: {checked}",
        f"- Findings: {len(problems)}",
        "",
    ]
    if problems:
        lines += ["## Findings", ""]
        for where, issue in problems:
            lines.append(f"- **{where}** — {issue}")
    else:
        lines += ["## Result", "", "No SEO health problems detected in this run."]

    report = "\n".join(lines) + "\n"
    with open(args.report, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(report)

    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
