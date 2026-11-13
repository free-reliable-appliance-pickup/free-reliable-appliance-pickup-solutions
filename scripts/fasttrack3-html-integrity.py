#!/usr/bin/env python3
"""Read-only FastTrack 3 HTML consistency inventory for indexed sitemap pages.

Checks duplicate element attributes, duplicate IDs, and broken same-page
fragment links. Reports evidence only; never modifies HTML or auto-indexes pages.
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

SITEMAP = Path("sitemap.xml")
LIMIT = 75

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.fragments = []
        self.duplicates = []

    def handle_starttag(self, tag, attrs):
        self._inspect(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self._inspect(tag, attrs)

    def _inspect(self, tag, attrs):
        line, _ = self.getpos()
        names = Counter(name.lower() for name, _ in attrs)
        for name, num in names.items():
            if num > 1:
                self.duplicates.append((line, tag, name, num))
        for name, value in attrs:
            if name.lower() == "id" and value:
                self.ids.append((line, value))
            if tag.lower() == "a" and name.lower() == "href" and value and value.startswith("#") and len(value) > 1:
                self.fragments.append((line, unquote(value[1:])))

def active_files():
    root = ET.parse(SITEMAP).getroot()
    for loc in root.iter():
        if not loc.tag.endswith("loc") or not loc.text:
            continue
        parsed = urlsplit(loc.text.strip())
        path = unquote(parsed.path).lstrip("/")
        file = (Path(path) / "index.html") if not path or path.endswith("/") else Path(path)
        yield loc.text.strip(), file

def main():
    seen, missing, duplicate_attrs, duplicate_ids, missing_fragments, parsed = set(), [], [], [], [], 0
    for url, path in active_files():
        if str(path) in seen:
            continue
        seen.add(str(path))
        if not path.is_file():
            missing.append((str(path), url))
            continue
        parser = Inspector()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        parser.close()
        parsed += 1
        duplicate_attrs.extend((str(path), *item) for item in parser.duplicates)
        id_count = Counter(name for _, name in parser.ids)
        duplicate_ids.extend((str(path), name, count) for name, count in id_count.items() if count > 1)
        ids = set(id_count)
        missing_fragments.extend((str(path), line, fragment) for line, fragment in parser.fragments if fragment not in ids)

    def show(label, items):
        print(f"{label}={len(items)}")
        for item in items[:LIMIT]:
            print("  ", *item, sep=" | ")
        if len(items) > LIMIT:
            print(f"  ... {len(items)-LIMIT} more (diagnostic output capped)")

    print(f"FASTTRACK_HTML_ACTIVE_URLS={len(seen)} PARSED_PAGES={parsed}")
    show("MISSING_LOCAL_SITEMAP_FILES", missing)
    show("DUPLICATE_HTML_ATTRIBUTES", duplicate_attrs)
    show("DUPLICATE_HTML_IDS", duplicate_ids)
    show("BROKEN_SAME_PAGE_FRAGMENTS", missing_fragments)
    print("FASTTRACK_HTML_INTEGRITY_INVENTORY_COMPLETE")
    if missing or duplicate_attrs or duplicate_ids or missing_fragments:
        raise SystemExit("FASTTRACK_HTML_INTEGRITY_FAILED: fix HTML defects before merge")

if __name__ == "__main__":
    main()
