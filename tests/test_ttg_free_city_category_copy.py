"""TTG staged city page search intent: free-pickup phrasing without false coverage."""
from html import unescape
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
KINDS = ("appliance", "washer-dryer", "refrigerator", "stove-oven", "freezer")
IL = ("aurora", "champaign", "chicago", "cicero", "elgin", "joliet",
      "naperville", "peoria", "rockford", "schaumburg", "springfield", "waukegan")
GA = ("alpharetta", "athens", "atlanta", "augusta", "columbus", "conyers",
      "decatur", "douglasville", "duluth", "lawrenceville", "macon",
      "marietta", "mcdonough", "norcross", "roswell", "savannah", "smyrna")
GA_CAT = ("atlanta", "lawrenceville", "marietta")
FL = ("miami", "orlando", "tampa", "jacksonville", "fort-lauderdale",
      "hialeah", "st-petersburg", "west-palm-beach", "sarasota",
      "clearwater", "fort-myers")
TX = ("arlington", "frisco", "plano", "irving", "garland", "mckinney",
      "waco", "lubbock", "corpus-christi", "brownsville", "killeen",
      "laredo", "mcallen", "georgetown", "new-braunfels", "denton",
      "grand-prairie", "carrollton", "cedar-park", "beaumont", "temple")

def target_paths():
    paths = []
    for city in IL:
        paths.extend(f"{city}-il-{kind}-pickup/index.html" for kind in KINDS)
    for city in GA:
        paths.append(f"{city}-ga-appliance-pickup/index.html")
    for city in GA_CAT:
        paths.extend(f"{city}-ga-{kind}-pickup/index.html" for kind in KINDS[1:])
    for city in FL:
        paths.extend(f"{city}-fl-{kind}-pickup/index.html" for kind in KINDS[1:])
    for city in TX:
        paths.append(f"{city}-tx-appliance-pickup/index.html")
    paths.extend(f"pasadena-tx-{kind}-pickup/index.html" for kind in KINDS)
    return paths

def webpages(node):
    if isinstance(node, list):
        for part in node:
            yield from webpages(part)
    if isinstance(node, dict):
        types = node.get("@type", [])
        if isinstance(types, str):
            types = [types]
        if "WebPage" in types:
            yield node
        for part in node.values():
            yield from webpages(part)

class HighIntentFreeCityCopy(unittest.TestCase):
    """Test the exact reviewed pages; do not expand unverified service coverage."""

    def test_selected_batch_has_159_unique_pages(self):
        """Changes cover Illinois, Georgia and priority FL/TX markets exactly."""
        self.assertEqual(len(target_paths()), 159)
        self.assertEqual(len(set(target_paths())), 159)

    def test_page_headings_forms_and_schema_remain_consistent(self):
        """Preserve visible Free headline, Formspree, canonical and JSON-LD."""
        for path in target_paths():
            with self.subTest(path=path):
                raw = (ROOT / path).read_text(encoding="utf-8")
                title = re.search(r"<title>(.*?)</title>", raw, re.I | re.S)
                h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.I | re.S)
                description = re.search(r'<meta name="description" content="([^"]*)"', raw, re.I)
                self.assertIsNotNone(title)
                self.assertIsNotNone(h1)
                self.assertIsNotNone(description)
                plain_title = unescape(title.group(1))
                plain_h1 = unescape(re.sub(r"<[^>]+>", "", h1.group(1)))
                free_pattern = r"\bFree\s+(?:Appliance|Washer|Refrigerator|Stove|Range|Oven|Freezer)"
                self.assertRegex(plain_title, free_pattern)
                self.assertRegex(plain_h1, free_pattern)
                self.assertIn("formspree.io/f/mvzeapzd", raw)
                self.assertRegex(
                    raw.lower(),
                    r"(eligibility|qualifying|qualification|not guaranteed|not confirmed|local operator|route availability)"
                )
                slug = path.removesuffix("/index.html")
                self.assertIn("https://freereliableappliancepickup.com/" + slug + "/", raw)
                self.assertEqual(len(re.findall(r"<h1\b", raw, re.I)), 1)
                if "-il-" in path:
                    self.assertIn('content="noindex, follow"', raw)
                scripts = re.findall(
                    r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
                    raw, re.I | re.S)
                for content in scripts:
                    for page in webpages(json.loads(content)):
                        self.assertEqual(unescape(page.get("name", "")), plain_title)
                        if "description" in page:
                            self.assertEqual(unescape(page["description"]), unescape(description.group(1)))

if __name__ == "__main__":
    unittest.main()
