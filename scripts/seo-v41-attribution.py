#!/usr/bin/env python3
"""Read-only audit of source attribution for active sitemap pickup pages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import argparse, json, re, sys, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
class Forms(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms = []
        self.current = None
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "form":
            self.current = {"action": d.get("action", ""), "method": d.get("method", "get").lower(), "fields": {}}
            self.forms.append(self.current)
        elif tag in ("input", "select", "textarea") and self.current is not None:
            if d.get("name"):
                self.current["fields"][d["name"]] = d.get("value", "")
    def handle_endtag(self, tag):
        if tag == "form":
            self.current = None

def audit():
    sitemap = ET.parse(ROOT / "sitemap.xml")
    pages = []
    for node in sitemap.iter():
        if node.tag.endswith("loc") and node.text:
            slug = urlparse(node.text.strip()).path.strip("/")
            if slug.endswith(("appliance-pickup", "washer-dryer-pickup")):
                pages.append(slug)
    issues = []
    checked = 0
    for slug in sorted(set(pages)):
        path = ROOT / slug / "index.html"
        if not path.is_file():
            issues.append({"page": slug, "issue": "missing source HTML"})
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', html, re.I):
            continue
        parser = Forms()
        parser.feed(html)
        forms = [f for f in parser.forms if "formspree.io" in f["action"]]
        if not forms:
            issues.append({"page": slug, "issue": "missing Formspree form"})
            continue
        checked += 1
        for form in forms:
            fields = form["fields"]
            if fields.get("source_page") != slug:
                issues.append({"page": slug, "issue": "missing or mismatched source_page"})
            if not fields.get("city"):
                issues.append({"page": slug, "issue": "missing city"})
            if form["method"] != "post":
                issues.append({"page": slug, "issue": "form method is not POST"})
    return {"active_forms_checked": checked, "issues": issues, "issue_count": len(issues)}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--fail", action="store_true")
    p.add_argument("--output", default="seo-v41-attribution.json")
    args = p.parse_args()
    report = audit()
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"active_forms_checked": report["active_forms_checked"], "issue_count": report["issue_count"], "first_issues": report["issues"][:20]}, indent=2))
    if args.fail and report["issues"]:
        sys.exit(1)
