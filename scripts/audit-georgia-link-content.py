#!/usr/bin/env python3
"""Read-only staged Georgia link and near-duplicate content diagnostic.

Does not establish local service coverage, indexing, live form delivery or rankings.
Local links with missing targets are release errors. Similarity is diagnostic until
city pages have verified operations and may legitimately be indexed.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import itertools
import os
import re
import sys

BASE = "https://freereliableappliancepickup.com/"
SKIP_TEXT_TAGS = {"form", "style", "script", "nav", "header", "footer", "template", "noscript"}


class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.text = []
        self.skipped = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a":
            if a.get("name"):
                self.ids.add(a["name"])
            if a.get("href"):
                self.links.append(a["href"])
        if tag in SKIP_TEXT_TAGS:
            self.skipped.append(tag)
    def handle_endtag(self, tag):
        if tag in SKIP_TEXT_TAGS and tag in self.skipped:
            # Keep diagnostics stable for nested elements without relying on CSS.
            pos = len(self.skipped) - 1 - self.skipped[::-1].index(tag)
            del self.skipped[pos:]
    def handle_data(self, data):
        if not self.skipped:
            self.text.append(data)


def visible_words(reader, cities):
    s = " ".join(reader.text).lower()
    s = re.sub(r"\b\d{5}(?:-\d{4})?\b", " ZIP ", s)
    for city in sorted(cities, key=len, reverse=True):
        s = re.sub(r"\b" + re.escape(city).replace(r"\ ", r"[\s-]+") + r"\b", "city", s)
    return re.findall(r"[a-z0-9']+", s)


def shingles(tokens, n=5):
    return {" ".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)}


def inspect(root):
    pages = sorted(set(root.glob("*-ga-*-pickup/index.html")) |
                   set(root.glob("*-ga-appliance-pickup/index.html")))
    # The full integration release candidate must remain differentiated.
    # Smaller noindex staging branches keep similarity as a diagnostic.
    integrated_release = os.environ.get("GITHUB_REF_NAME") == "vgm/georgia-integration-test-all43-20261107"
    if integrated_release and len(pages) != 43:
        print(f"FAIL: integrated Georgia branch expected 43 guides, found {len(pages)}")
        return 1
    if not pages:
        print("FAIL: no Georgia pages to inspect")
        return 1
    hub = root / "georgia-appliance-pickup/index.html"
    targets = pages + ([hub] if hub.is_file() else [])
    cities = {p.parent.name.split("-ga-", 1)[0].replace("-", " ") for p in pages}
    parsed = {}
    broken = []
    fragment_errors = []
    for path in targets:
        reader = Reader()
        reader.feed(path.read_text(encoding="utf-8"))
        parsed[path] = reader

    for path, reader in parsed.items():
        for href in reader.links:
            absolute = urljoin(BASE + str(path.parent).replace("\\", "/") + "/", href)
            parsed_href = urlparse(absolute)
            if parsed_href.scheme not in ("http", "https"):
                continue
            if parsed_href.netloc not in ("freereliableappliancepickup.com",):
                continue
            local_path = unquote(parsed_href.path).lstrip("/")
            target = root / local_path
            if parsed_href.path.endswith("/") or not target.suffix:
                target = target / "index.html"
            if not target.is_file():
                broken.append(f"{path}: {href} -> missing {target}")
            elif target == path and parsed_href.fragment:
                if unquote(parsed_href.fragment) not in reader.ids:
                    fragment_errors.append(f"{path}: broken in-page fragment {href}")

    normalized = []
    for p in pages:
        words = visible_words(parsed[p], cities)
        normalized.append((p, len(words), shingles(words)))
    pairs = []
    for (pa, na, sa), (pb, nb, sb) in itertools.combinations(normalized, 2):
        if not sa or not sb:
            continue
        intersection = len(sa & sb)
        union = len(sa | sb)
        score = intersection / union if union else 0
        pairs.append((score, str(pa.parent), str(pb.parent), na, nb))
    pairs.sort(reverse=True)
    # An all-template city guide should not be described as differentiated SEO
    # content until a locally-verified substantive section is added.
    excessive = [p for p in pairs if p[0] >= .65]
    print("GEORGIA_LINK_PAGES_AUDITED", len(targets))
    print("GEORGIA_LOCAL_BROKEN_LINKS", len(broken))
    print("GEORGIA_INPAGE_FRAGMENT_ERRORS", len(fragment_errors))
    print("GEORGIA_CORE_WORDS_MIN", min(n for _, n, _ in normalized))
    print("GEORGIA_CORE_WORDS_MEDIAN", sorted(n for _, n, _ in normalized)[len(normalized)//2])
    print("GEORGIA_NEAR_DUPLICATE_PAIRS_065", len(excessive))
    for score, a, b, na, nb in pairs[:12]:
        print(f"GEORGIA_SIMILARITY {score:.3f} {a} vs {b} (core={na},{nb})")
    for problem in broken[:70]:
        print("FAIL", problem)
    for problem in fragment_errors[:70]:
        print("FAIL", problem)
    if excessive:
        if integrated_release:
            for score, a, b, _, _ in excessive[:12]:
                print(f"FAIL: Georgia near-duplicate {score:.3f} {a} vs {b}")
        else:
            print("NOTE: similarity warnings are diagnostic for noindex drafts, not authority to publish them.")
    return 1 if broken or fragment_errors or (integrated_release and excessive) else 0


if __name__ == "__main__":
    sys.exit(inspect(Path(".")))
