#!/usr/bin/env python3
"""Check the images on the canonical pages in sitemap.xml before a market rollout."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

from PIL import Image

BASE = 'https://freereliableappliancepickup.com/'
MIN_HERO_WIDTH = 500  # Catch thumbnail-sized hero derivatives, not portrait originals.
MAX_HERO_BYTES = 1_500_000  # Protect LCP/mobile delivery while preserving sharp originals elsewhere.

APPLIANCE_HERO_TERMS = {
    'refrigerator-pickup': ('refrigerator', 'fridge'),
    'freezer-pickup': ('freezer',),
    'washer-dryer-pickup': ('washer', 'dryer', 'laundry'),
    'stove-oven-pickup': ('stove', 'range', 'oven'),
}

GENERIC_APPLIANCE_ASSET = {
    'refrigerator-pickup': 'major-appliance-pickup-photo-1.jpg',
    'stove-oven-pickup': 'major-appliance-pickup-photo-2.jpg',
    'freezer-pickup': 'major-appliance-pickup-photo-3.jpg',
}

KNOWN_SHARED_APPLIANCE_ASSETS = {
    'refrigerator': 'major-appliance-pickup-photo-1.jpg',
    'freezer': 'major-appliance-pickup-photo-3.jpg',
    'stove-oven': 'major-appliance-pickup-photo-2.jpg',
}


IMAGE_LAYOUT_PRIORITY_SLUGS = {
    'fontana-appliance-pickup',
    'upland-appliance-pickup',
    'montclair-appliance-pickup',
    'claremont-appliance-pickup',
    'la-verne-appliance-pickup',
    'san-dimas-appliance-pickup',
    'fresno-appliance-pickup',
    'west-covina-appliance-pickup',
    'san-gabriel-appliance-pickup',
    'el-monte-appliance-pickup',
    'azusa-appliance-pickup',
    'duarte-appliance-pickup',
    'monterey-park-appliance-pickup',
    'rosemead-appliance-pickup',
    'diamond-bar-appliance-pickup',
    'rowland-heights-appliance-pickup',
    'hacienda-heights-appliance-pickup',
    'chino-hills-appliance-pickup',
    'corona-appliance-pickup',
    'eastvale-appliance-pickup',
    'rialto-appliance-pickup',
    'san-bernardino-appliance-pickup',
    'redlands-appliance-pickup',
    'highland-appliance-pickup',
    'yucaipa-appliance-pickup',
    'anaheim-appliance-pickup',
    'irvine-appliance-pickup',
    'tustin-appliance-pickup',
    'sacramento-appliance-pickup',
    'stockton-appliance-pickup',
    'grand-terrace-appliance-pickup',
    'bloomington-appliance-pickup'
}

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
    layout_findings = []
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

        # Keep the four national appliance hubs semantically aligned with
        # their primary content image. This prevents a future image swap from
        # shipping refrigerator, freezer, laundry or stove pages with an
        # obviously mismatched hero/content alt signal.
        expected_terms = APPLIANCE_HERO_TERMS.get(slug)
        content_image = next((
            attrs for attrs in parser.images
            if attrs.get('src')
            and 'logo' not in attrs.get('alt', '').lower()
        ), None)

        if expected_terms:
            if content_image is None:
                problems.append(f'{url}: no non-logo appliance image found')
            else:
                alt = content_image.get('alt', '').strip().lower()
                if not any(term in alt for term in expected_terms):
                    problems.append(
                        f'{url}: primary appliance image alt {alt!r} does not match expected terms {expected_terms}'
                    )

        # When a city/appliance page uses the shared major-appliance asset set,
        # enforce the established appliance mapping. Bespoke local photos are
        # allowed and are not forced onto the shared assets.
        if content_image is not None:
            src_name = Path(urlparse(urljoin(url, content_image.get('src', ''))).path).name
            shared_names = set(KNOWN_SHARED_APPLIANCE_ASSETS.values())
            if src_name in shared_names:
                expected_asset = None
                if slug == 'refrigerator-pickup' or slug.endswith('-refrigerator-pickup'):
                    expected_asset = KNOWN_SHARED_APPLIANCE_ASSETS['refrigerator']
                elif slug == 'freezer-pickup' or slug.endswith('-freezer-pickup'):
                    expected_asset = KNOWN_SHARED_APPLIANCE_ASSETS['freezer']
                elif slug == 'stove-oven-pickup' or slug.endswith('-stove-oven-pickup'):
                    expected_asset = KNOWN_SHARED_APPLIANCE_ASSETS['stove-oven']
                if expected_asset and src_name != expected_asset:
                    problems.append(
                        f'{url}: shared appliance image {src_name} should be {expected_asset}'
                    )

        for attrs in parser.images:
            src = attrs.get('src', '')

            # Several city appliance pages reuse the numbered generic
            # refrigerator/stove/freezer photo set. Enforce the established
            # mapping whenever one of those generic assets is used so a
            # template copy cannot silently swap freezer and stove imagery.
            generic_type = next(
                (kind for kind in GENERIC_APPLIANCE_ASSET if slug == kind or slug.endswith('-' + kind)),
                None
            )
            if generic_type and 'major-appliance-pickup-photo-' in src:
                expected_asset = GENERIC_APPLIANCE_ASSET[generic_type]
                if expected_asset not in src:
                    problems.append(
                        f'{url}: generic appliance image {src} does not match expected {expected_asset}'
                    )
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
                if size is not None and slug in IMAGE_LAYOUT_PRIORITY_SLUGS:
                    declared_width = attrs.get('width')
                    declared_height = attrs.get('height')
                    if declared_width != str(size[0]) or declared_height != str(size[1]):
                        layout_findings.append(
                            f'{slug} | {src} | declared={declared_width}x{declared_height} '
                            f'actual={size[0]}x{size[1]}'
                        )
                if size is None:
                    problems.append(f'{url}: unreadable image {src}')
                elif attrs.get('fetchpriority') == 'high' and size[0] < MIN_HERO_WIDTH:
                    problems.append(f'{url}: hero {src} only {size[0]}px wide')
                elif attrs.get('fetchpriority') == 'high' and asset.stat().st_size > MAX_HERO_BYTES:
                    problems.append(f'{url}: hero {src} is {asset.stat().st_size / 1_000_000:.2f} MB; use an optimized derivative under {MAX_HERO_BYTES / 1_000_000:.1f} MB')

    # Check group-hero layout on key Northwest pages, including intentionally
    # noindex request pages that are excluded from the public XML sitemap.
    # The group photo must retain its actual intrinsic aspect ratio to avoid
    # layout shift on mobile. Never assume a generated photo's dimensions.
    northwest_group_pages = {
        'seattle-appliance-pickup',
        'tacoma-appliance-pickup',
        'spokane-appliance-pickup',
        'vancouver-appliance-pickup',
        'salem-appliance-pickup',
        'portland-appliance-pickup',
        'washington-appliance-pickup',
    }
    for slug in sorted(northwest_group_pages):
        page = Path(slug) / 'index.html'
        if not page.is_file():
            problems.append(f'{slug}: missing Northwest city page')
            continue
        parser = ImageRefs()
        parser.feed(page.read_text(encoding='utf-8', errors='replace'))
        hero_images = [
            attrs for attrs in parser.images
            if 'group-appliances.webp' in urlparse(attrs.get('src', '')).path
        ]
        if not hero_images:
            problems.append(f'{slug}: no major-appliance group photo')
            continue
        for attrs in hero_images:
            src = attrs['src']
            asset = Path(urlparse(urljoin(BASE, src)).path.lstrip('/'))
            if not asset.is_file():
                problems.append(f'{slug}: missing group hero {src}')
                continue
            try:
                with Image.open(asset) as photo:
                    actual_width, actual_height = photo.size
            except (OSError, ValueError):
                problems.append(f'{slug}: unreadable group hero {src}')
                continue
            if (attrs.get('width'), attrs.get('height')) != (str(actual_width), str(actual_height)):
                problems.append(
                    f'{slug}: group hero {src} dimensions '
                    f'{attrs.get("width")}x{attrs.get("height")} '
                    f'do not match file {actual_width}x{actual_height}'
                )

    # Image filenames and alt text alone are not proof of the appliance shown:
    # 2026-10-16 visual review found three Rancho specialty heroes whose
    # filenames/alt tags said "stove", "refrigerator", or "freezer" but all
    # displayed washing machines. Pin only visually verified original photo
    # references until each replacement has had a real category review.
    rancho_verified_hero_paths = {
        'rancho-cucamonga-stove-oven-pickup': '/assets/rancho-cucamonga/rancho-cucamonga-stove-oven-real-stainless-range-20261016.jpg',
        'rancho-cucamonga-refrigerator-pickup': '/assets/rancho-cucamonga/rancho-cucamonga-refrigerator-real-french-door-20261016.jpg',
        'rancho-cucamonga-freezer-pickup': '/assets/rancho-cucamonga/rancho-cucamonga-freezer-real-upright-20261016.jpg',
    }
    for slug, expected_src in sorted(rancho_verified_hero_paths.items()):
        page = Path(slug) / 'index.html'
        if not page.is_file():
            problems.append(f'{slug}: missing verified specialty page')
            continue
        html = page.read_text(encoding='utf-8', errors='replace')
        parser = ImageRefs()
        parser.feed(html)
        real_images = [
            attrs for attrs in parser.images
            if attrs.get('src') and 'logo' not in attrs.get('alt', '').lower()
        ]
        if not real_images or urlparse(real_images[0]['src']).path != expected_src:
            problems.append(f'{slug}: hero not approved visual category photo {expected_src}')
        full_url = BASE.rstrip('/') + expected_src
        if f'<meta property="og:image" content="{full_url}">' not in html:
            problems.append(f'{slug}: social image not aligned with verified category hero')
        if f'<meta name="twitter:image" content="{full_url}">' not in html:
            problems.append(f'{slug}: Twitter image not aligned with verified category hero')
        if f'"url":"{full_url}"' not in html:
            problems.append(f'{slug}: JSON-LD primary image not aligned with verified hero')
    rancho_general_page = Path('rancho-cucamonga-appliance-pickup/index.html')
    if rancho_general_page.is_file():
        html = rancho_general_page.read_text(encoding='utf-8', errors='replace')
        for verified_gallery_src in ('/IMG-20241201-WA0066.jpg', '/IMG-20240222-WA0006.jpg'):
            if f'src="{verified_gallery_src}"' not in html:
                problems.append(f'Rancho city gallery missing verified photo {verified_gallery_src}')
        for invalid_src in ('/assets/california/real-appliances/real-refrigerator.jpg',
                            '/assets/california/real-appliances/real-freezer.jpg'):
            if f'src="{invalid_src}"' in html:
                problems.append(f'Rancho city gallery uses mislabeled washer {invalid_src}')

    # The legacy "real-refrigerator.jpg" and "real-freezer.jpg" files
    # visually show washing machines. Keep these 17 California pages and the
    # image sitemap free of those misleading asset references.
    reviewed_california_photo_slugs = (
        'los-angeles-appliance-pickup',
        'orange-county-appliance-pickup',
        'inland-empire-appliance-pickup',
        'irvine-appliance-pickup',
        'fontana-appliance-pickup',
        'mission-viejo-appliance-pickup',
        'west-covina-appliance-pickup',
        'monrovia-appliance-pickup',
        'claremont-appliance-pickup',
        'san-dimas-appliance-pickup',
        'whittier-appliance-pickup',
        'diamond-bar-appliance-pickup',
        'el-monte-appliance-pickup',
        'temple-city-appliance-pickup',
        'san-gabriel-appliance-pickup',
        'san-marino-appliance-pickup',
        'yorba-linda-appliance-pickup',
    )
    misleading_photo_urls = (
        '/assets/california/real-appliances/real-refrigerator.jpg',
        '/assets/california/real-appliances/real-freezer.jpg',
    )
    for slug in reviewed_california_photo_slugs:
        path = Path(slug) / 'index.html'
        if not path.is_file():
            problems.append(f'{slug}: missing reviewed California photo page')
            continue
        raw = path.read_text(encoding='utf-8', errors='replace')
        for misleading_url in misleading_photo_urls:
            if misleading_url in raw:
                problems.append(f'{slug}: mislabeled washing-machine photo {misleading_url}')
    image_sitemap = Path('sitemap-images.xml')
    if image_sitemap.is_file():
        index = image_sitemap.read_text(encoding='utf-8', errors='replace')
        for misleading_url in misleading_photo_urls:
            if misleading_url in index:
                problems.append(f'image sitemap contains misleading refrigerator/freezer photo {misleading_url}')
    print(f'IMAGE_LAYOUT_PRIORITY_MISMATCHES {len(layout_findings)}')
    for finding in layout_findings:
        print('IMAGE_LAYOUT_REVIEW', finding)
    print(f'ACTIVE_PAGES={checked_pages} LOCAL_IMAGE_REFERENCES={checked_images} PROBLEMS={len(problems)}')
    for problem in problems:
        print(problem)
    raise SystemExit(bool(problems))


if __name__ == '__main__':
    main()
