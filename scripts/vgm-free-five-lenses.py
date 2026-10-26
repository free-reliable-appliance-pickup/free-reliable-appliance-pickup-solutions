#!/usr/bin/env python3
"""VGM five free SEO checks. Read-only repository audit; no network calls."""
import argparse
from collections import Counter
from html import unescape
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

BASE = "https://freereliableappliancepickup.com/"
CITIES = ("rancho-cucamonga", "fontana", "upland", "claremont",
          "la-verne", "san-dimas", "pomona", "pasadena",
          "los-angeles", "riverside", "anaheim", "irvine")


def find_meta(html, kind, key, match, result):
    head = html.split("</head>", 1)[0]
    for tag in re.findall("<" + kind + r"\b[^>]*>", head, re.I):
        attrs = dict((k.lower(), unescape(a or b)) for k, a, b in
                     re.findall(r'([\w:-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', tag))
        if attrs.get(key, "").lower() == match.lower():
            return attrs.get(result, "")
    return ""


def page(root, city):
    slug = city + "-appliance-pickup"
    path = root / slug / "index.html"
    if not path.is_file():
        return None
    raw = path.read_text(encoding="utf-8", errors="replace")
    title = re.search(r"<title\b[^>]*>(.*?)</title>", raw, re.I | re.S)
    hrefs = [unescape(v) for v in re.findall(r'<a\b[^>]*\bhref="([^"]+)"', raw, re.I)]
    schema = []
    invalid = 0
    for item in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
                           raw, re.I | re.S):
        try:
            schema.append(json.loads(item))
        except ValueError:
            invalid += 1
    return dict(slug=slug, raw=raw, hrefs=hrefs, schemas=schema,
                invalid=invalid, title=unescape(title.group(1)).strip() if title else "",
                description=find_meta(raw, "meta", "name", "description", "content"),
                robots=find_meta(raw, "meta", "name", "robots", "content").lower(),
                canonical=find_meta(raw, "link", "rel", "canonical", "href"),
                h1=len(re.findall(r"<h1\b", raw, re.I)),
                form=bool(re.search(r"<form\b", raw, re.I)))


def types_of(value):
    kinds = set()
    def inspect(x):
        if isinstance(x, list):
            for v in x:
                inspect(v)
        elif isinstance(x, dict):
            kind = x.get("@type")
            if isinstance(kind, str):
                kinds.add(kind)
            elif isinstance(kind, list):
                kinds.update(v for v in kind if isinstance(v, str))
            for v in x.values():
                inspect(v)
    inspect(value)
    return kinds


def sitemap(root):
    file = root / "sitemap.xml"
    return {x.text.strip() for x in ET.parse(file).findall(".//{*}loc") if x.text} if file.is_file() else set()


def generate(root):
    pages = [p for city in CITIES if (p := page(root, city)) is not None]
    indexed = sitemap(root)
    titles = Counter(p["title"] for p in pages if p["title"])
    out = ["# VGM Five Free SEO Lenses — California", "",
           "Source-only review of " + str(len(pages)) + " existing priority city hubs.",
           "No live rankings, search volume, backlink counts, AI citations, or crawler HTTP access measured.",
           "", "## 1. Auditor — source technical health"]
    for p in pages:
        issues = []
        if not p["title"]: issues.append("missing title")
        if not p["description"]: issues.append("missing meta description")
        if p["h1"] != 1: issues.append("H1 count " + str(p["h1"]))
        if p["canonical"] != BASE + p["slug"] + "/": issues.append("non-self-canonical")
        if "noindex" in p["robots"] and BASE + p["slug"] + "/" in indexed:
            issues.append("noindex and present in XML sitemap")
        if titles[p["title"]] > 1: issues.append("duplicate title in this sample")
        if p["invalid"]: issues.append("invalid JSON-LD")
        if issues:
            out.append("- " + p["slug"] + ": " + ", ".join(issues))
    out.extend(["- For internal 404s and image references, use the existing repo's full link and image audits.",
                "", "## 2. Researcher — query and content ownership"])
    for p in pages:
        city = p["slug"].removesuffix("-appliance-pickup")
        out.append("- " + city + ": general page owns appliance pickup/removal; compare real Search Console queries "
                   "against the existing washer/dryer page before changing titles or creating pages.")
    out.extend(["- No keyword volumes or SERP positions have been estimated.",
                "", "## 3. Planner — useful service information and contact route"])
    for p in pages:
        gap = []
        city = p["slug"].removesuffix("-appliance-pickup")
        child = city + "-washer-dryer-pickup"
        if (root / child / "index.html").is_file() and not any(child in h for h in p["hrefs"]):
            gap.append("existing laundry owner not linked")
        if not p["form"] and not any("request" in h.lower() for h in p["hrefs"]):
            gap.append("no request form or link detected")
        if not any(h.startswith("tel:") for h in p["hrefs"]):
            gap.append("no direct tel link")
        if not re.search("garage|driveway|stairs|elevator|access", p["raw"], re.I):
            gap.append("no explicit pickup-access wording")
        if gap:
            out.append("- " + p["slug"] + ": " + ", ".join(gap))
    out.extend(["", "## 4. Scorer — readable answer structure proxy, NOT a citation score"])
    for p in pages:
        types = types_of(p["schemas"])
        gaps = []
        if "Service" not in types and "LocalBusiness" not in types:
            gaps.append("Service/LocalBusiness structured data")
        if not re.search(r"faq|frequently asked", p["raw"], re.I):
            gaps.append("FAQ or customer questions")
        if gaps:
            out.append("- " + p["slug"] + ": review " + ", ".join(gaps))
    out.extend(["- A real AI citation assessment requires separate observed AI search results.",
                "", "## 5. Gatekeeper — repository robots.txt directives"])
    path = root / "robots.txt"
    if not path.is_file():
        out.append("- robots.txt not present in repository")
    else:
        raw = path.read_text(encoding="utf-8", errors="replace")
        out.append("- General crawler rules: " +
                   ("User-agent * present" if re.search(r"^\s*User-agent:\s*\*\s*$", raw, re.I | re.M)
                    else "no wildcard group"))
        out.append("- Root Allow /: " + str(bool(re.search(r"^\s*Allow:\s*/\s*$", raw, re.I | re.M))))
        out.append("- Root Disallow / directive present: " +
                   str(bool(re.search(r"^\s*Disallow:\s*/\s*$", raw, re.I | re.M))))
    out.extend(["- This does not test live Googlebot, GPTBot, ClaudeBot or PerplexityBot access.",
                "", "## Safety and actions",
                "- Validate findings with actual pages and Search Console before editing.",
                "- Preserve deliberate canonical/noindex choices and existing SEO experiment guard.",
                "- Pursue legitimate local California editorial citations and backlinks only.",
                "- Keep separate real-image, technical, routing and form audits in force.", ""])
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path("vgm-five-lenses.md"))
    args = parser.parse_args()
    report = generate(args.root.resolve())
    args.output.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
