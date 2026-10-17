#!/usr/bin/env python3
"""Free, read-only SEO Autopilot V4 workers. No credentials or paid AI required."""
import argparse
import collections
import html.parser
import json
import pathlib
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = "https://freereliableappliancepickup.com"
EXCLUDED = {".git", "node_modules", ".venv"}

class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.tels = []
        self.forms = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a":
            href = d.get("href", "").strip()
            if href.startswith("tel:"): self.tels.append(href)
            elif href: self.links.append(href)
        if tag == "form": self.forms.append(d.get("action", ""))

def pages():
    for path in ROOT.rglob("*.html"):
        if not any(part in EXCLUDED for part in path.parts):
            yield path

def target(href, source):
    if href.startswith(("#", "mailto:", "javascript:", "data:", "sms:")): return None
    u = urllib.parse.urlsplit(urllib.parse.urljoin(BASE + "/" + source.relative_to(ROOT).as_posix(), href))
    if u.netloc not in ("freereliableappliancepickup.com", "www.freereliableappliancepickup.com"): return None
    path = urllib.parse.unquote(u.path).lstrip("/")
    if not path: return ROOT / "index.html"
    candidate = ROOT / path
    if candidate.is_dir() or not candidate.suffix: candidate = candidate / "index.html"
    return candidate

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", default="seo-autopilot-v4-report.md")
    args = p.parse_args()
    all_pages = list(pages())
    issues = []
    stats = collections.Counter()
    internal = collections.Counter()
    phone_pages = 0
    form_pages = 0
    for page in all_pages:
        relative = page.relative_to(ROOT).as_posix()
        parser = Links()
        try: parser.feed(page.read_text(encoding="utf-8"))
        except (UnicodeError, OSError) as e:
            issues.append((relative, "read error: " + str(e))); continue
        if parser.tels: phone_pages += 1
        if parser.forms: form_pages += 1
        for href in parser.links:
            dest = target(href, page)
            if dest is None: stats["external_links_seen"] += 1; continue
            stats["internal_links_seen"] += 1
            try: rel = dest.relative_to(ROOT).as_posix()
            except ValueError: issues.append((relative, "unsafe link path: " + href)); continue
            internal[rel] += 1
            if not dest.is_file(): issues.append((relative, "missing internal target: " + href))
        if re.search(r'<form\\b', page.read_text(encoding="utf-8"), re.I) and not parser.forms:
            issues.append((relative, "form markup could not be parsed"))
    lines = ["# SEO Autopilot V4 — Read-only link and lead audit", "",
        "This is a source-code audit, not proof of live delivery, working calls, or form submissions.", "",
        f"- HTML pages scanned: {len(all_pages)}",
        f"- Internal links checked: {stats['internal_links_seen']}",
        f"- External links identified (not network-tested): {stats['external_links_seen']}",
        f"- Pages with telephone links: {phone_pages}",
        f"- Pages with form tags: {form_pages}",
        f"- Missing internal targets: {len(issues)}", "",
        "## Findings", ""]
    lines += [f"- \`{page}\`: {problem}" for page, problem in issues[:200]] or ["No missing internal targets detected."]
    lines += ["", "## Least-linked HTML destinations", ""]
    ranked = sorted(((internal[p.relative_to(ROOT).as_posix()], p.relative_to(ROOT).as_posix()) for p in all_pages))
    lines += [f"- {n} incoming links: \`{name}\`" for n, name in ranked[:30]]
    pathlib.Path(args.report).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Scanned {len(all_pages)} HTML files; found {len(issues)} link findings; report: {args.report}")
    return 1 if issues else 0

if __name__ == "__main__": sys.exit(main())
