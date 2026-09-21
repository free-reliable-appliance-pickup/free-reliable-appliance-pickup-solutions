#!/usr/bin/env python3
from pathlib import Path
from html import unescape
from urllib.parse import urlsplit, urlunsplit
import re
import xml.etree.ElementTree as ET

BASE = "https://freereliableappliancepickup.com"
ROOT = Path(__file__).resolve().parents[1]

lists = [
    ROOT / "data" / "california-seo-model-pages.txt",
    ROOT / "data" / "california-washer-dryer-seo-model-pages.txt",
]
extra = [
    "refrigerator-pickup",
    "freezer-pickup",
    "stove-oven-pickup",
    "washer-dryer-pickup",
    "appliance-pickup-checklist",
    "free-pickup-qualification",
    "how-appliance-pickup-works",
    "about",
    "denver-appliance-pickup",
    "aurora-appliance-pickup",
    "portland-appliance-pickup",
    "salem-appliance-pickup",
    "oregon-appliance-pickup",
    "colorado-appliance-pickup",
    "old-appliance-disposal-options",
    "landlord-property-manager-appliance-pickup",
    "high-desert-rv-appliance-pickup",
    "antelope-valley-rv-appliance-pickup",
]

slugs = []
seen_slugs = set()
for list_path in lists:
    if not list_path.exists():
        continue
    for raw in list_path.read_text(encoding="utf-8").splitlines():
        slug = raw.strip().strip("/")
        if slug and slug not in seen_slugs:
            seen_slugs.add(slug)
            slugs.append(slug)
for slug in extra:
    if slug not in seen_slugs:
        seen_slugs.add(slug)
        slugs.append(slug)

def normalize_image(src: str):
    src = unescape(src.strip())
    if not src:
        return None
    low = src.lower()
    if low.startswith("data:"):
        return None
    if src.startswith("//"):
        src = "https:" + src
    elif src.startswith("/"):
        src = BASE + src
    elif src.startswith("http://") or src.startswith("https://"):
        pass
    else:
        src = BASE + "/" + src.lstrip("./")

    parts = urlsplit(src)
    host = (parts.hostname or "").lower()
    if host not in {"freereliableappliancepickup.com", "www.freereliableappliancepickup.com"}:
        return None
    path_low = parts.path.lower()
    if any(x in path_low for x in [
        "file_00000000b7c082308dccc73e5bd3acd2",
        "favicon",
        "logo",
    ]):
        return None
    if not re.search(r"\.(?:jpe?g|png|webp|gif)$", parts.path, re.I):
        return None
    return urlunsplit(("https", "freereliableappliancepickup.com", parts.path, "", ""))

entries = []
for slug in slugs:
    page_path = ROOT / slug / "index.html"
    if not page_path.exists():
        continue
    html = page_path.read_text(encoding="utf-8", errors="replace")

    candidates = []
    candidates.extend(re.findall(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']', html, re.I))
    candidates.extend(re.findall(r'<meta\b[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', html, re.I))

    images = []
    seen = set()
    for src in candidates:
        img = normalize_image(src)
        if img and img not in seen:
            seen.add(img)
            images.append(img)

    if images:
        entries.append((f"{BASE}/{slug}/", images[:12]))

ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
ET.register_namespace("image", "http://www.google.com/schemas/sitemap-image/1.1")
ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
ins = "http://www.google.com/schemas/sitemap-image/1.1"
urlset = ET.Element(f"{{{ns}}}urlset")

for page_url, images in entries:
    u = ET.SubElement(urlset, f"{{{ns}}}url")
    ET.SubElement(u, f"{{{ns}}}loc").text = page_url
    for image_url in images:
        im = ET.SubElement(u, f"{{{ins}}}image")
        ET.SubElement(im, f"{{{ins}}}loc").text = image_url

tree = ET.ElementTree(urlset)
ET.indent(tree, space="  ")
out = ROOT / "sitemap-images.xml"
tree.write(out, encoding="utf-8", xml_declaration=True)

image_count = sum(len(images) for _, images in entries)
print(f"IMAGE_SITEMAP_PAGES={len(entries)}")
print(f"IMAGE_SITEMAP_IMAGES={image_count}")
