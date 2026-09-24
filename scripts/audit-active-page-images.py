#!/usr/bin/env python3
"""Check the images on the canonical pages in sitemap.xml before a market rollout."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

from PIL import Image

BASE = 'https://freereliableappliancepickup.com/'
MIN_HERO_WIDTH = 500  # Catch thumbnail-sized hero derivatives, not portrait originals.


class ImageRefs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.images.append(dict(attrs))


def main():
    root = ET.parse('sitemap.xml').getroot()
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [el.text.strip() for el in root.findall('.//s:loc', ns) if el.text]
    problems = []
    checked_pages = 0
    checked_images = 0
    inspected_assets = {}
    for url in urls:
        if not url.startswith(BASE):
            continue
        slug = url[len(BASE):].strip('/')
        page = Path(slug) / 'index.html' if slug else Path('index.html')
        if not page.is_file():
            problems.append(f'{url}: missing page')
            continue
        checked_pages += 1
        parser = ImageRefs()
        parser.feed(page.read_text(encoding='utf-8', errors='replace'))
        for attrs in parser.images:
            src = attrs.get('src', '')
            if not src or src.startswith('data:'):
                continue
            image_url = urljoin(url, src)
            parsed = urlparse(image_url)
            if parsed.netloc != urlparse(BASE).netloc:
                continue  # Remote images are outside this repository's control.
            asset = Path(parsed.path.lstrip('/'))
            if not asset.is_file():
                problems.append(f'{url}: missing image {src}')
                continue
            checked_images += 1
            if asset.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'}:
                if asset not in inspected_assets:
                    try:
                        with Image.open(asset) as image:
                            inspected_assets[asset] = (image.width, image.height)
                    except (OSError, ValueError):
                        inspected_assets[asset] = None
                size = inspected_assets[asset]
                if size is None:
                    problems.append(f'{url}: unreadable image {src}')
                elif attrs.get('fetchpriority') == 'high' and size[0] < MIN_HERO_WIDTH:
                    problems.append(f'{url}: hero {src} only {size[0]}px wide')
    print(f'ACTIVE_PAGES={checked_pages} LOCAL_IMAGE_REFERENCES={checked_images} PROBLEMS={len(problems)}')
    for problem in problems:
        print(problem)
    raise SystemExit(bool(problems))


if __name__ == '__main__':
    main()
