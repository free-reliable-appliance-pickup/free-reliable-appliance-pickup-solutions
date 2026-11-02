#!/usr/bin/env python3
"""Verify Antelope Valley support-page Request Pickup links resolve to a real hub form."""
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITIES = ("quartz-hill", "littlerock", "lake-los-angeles", "pearblossom", "leona-valley")
SUFFIXES = ("appliance-pickup", "washer-dryer-pickup")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.forms = 0
        self.canonicals = []
        self.robots = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "form":
            self.forms += 1
        if tag == "link" and attrs.get("rel", "").lower() == "canonical":
            self.canonicals.append(attrs.get("href"))
        if tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.robots.append(attrs.get("content", ""))


def parse(path):
    page = Page()
    page.feed(path.read_text(encoding="utf-8"))
    return page


def main():
    failures = []
    for suffix in SUFFIXES:
        hub_slug = "antelope-valley-" + suffix
        hub = parse(ROOT / hub_slug / "index.html")
        if "request" not in hub.ids or not hub.forms:
            failures.append(f"{hub_slug}: target request ID/form missing")
        expected = f"/{hub_slug}/#request"
        canonical = f"https://freereliableappliancepickup.com/{hub_slug}/"
        for city in CITIES:
            path = ROOT / f"{city}-{suffix}" / "index.html"
            page = parse(path)
            if "#request" in page.links:
                failures.append(f"{path}: broken local #request remains")
            if expected not in page.links:
                failures.append(f"{path}: missing correct hub request link {expected}")
            if page.canonicals != [canonical]:
                failures.append(f"{path}: canonical changed unexpectedly")
            if not any("noindex" in robots.lower() for robots in page.robots):
                failures.append(f"{path}: support alias must remain noindex")
            if page.forms:
                failures.append(f"{path}: support alias unexpectedly gained a form")
    if failures:
        for failure in failures:
            print("FAIL", failure)
        raise SystemExit(f"{len(failures)} Antelope Valley request-link error(s)")
    print("PASS: 10 Antelope Valley support aliases route to two valid hub request forms")


if __name__ == "__main__":
    main()
