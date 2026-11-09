"""Offline QA for the 61 manifest-listed, request-only Illinois pages."""
import json
import unittest
from scripts.ttg_illinois_live_smoke import ROOT, check_page, Extract


CITIES = ("aurora", "champaign", "cicero", "elgin", "joliet", "naperville",
          "peoria", "rockford", "schaumburg", "springfield", "waukegan")
CATEGORIES = ("washer-dryer", "refrigerator", "stove-oven", "freezer")


class IllinoisCategoryPages(unittest.TestCase):
    """Protect intake form and navigation quality without making network requests."""

    @classmethod
    def setUpClass(cls):
        """Load the exact manifest of Illinois request pages."""
        cls.pages = json.loads(
            (ROOT / "data/ttg-state-batches/IL.json").read_text(encoding="utf-8")
        )["pages"]

    def test_expected_61_pages(self):
        """Keep all 17 original guides and 44 new categories."""
        self.assertEqual(len(self.pages), 61)
        for city in CITIES:
            for category in CATEGORIES:
                with self.subTest(city=city, category=category):
                    self.assertIn(f"{city}-il-{category}-pickup/index.html", self.pages)

    def test_all_pages_request_only(self):
        """Check noindex, one hero, self-canonical, and required Formspree fields."""
        for path in self.pages:
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                slug = path.removesuffix("/index.html")
                self.assertEqual(check_page(slug, text, self.pages), [])

    def test_parent_city_links(self):
        """Make each original city page link to all four of its category guides."""
        for city in CITIES:
            html = (ROOT / f"{city}-il-appliance-pickup/index.html").read_text(encoding="utf-8")
            for category in CATEGORIES:
                with self.subTest(city=city, category=category):
                    self.assertIn(f"/{city}-il-{category}-pickup/", html)

    def test_stove_fuel_and_connection_intake(self):
        """Require fuel and connection status for all Illinois stove requests."""
        for city in (*CITIES[:2], "chicago", *CITIES[2:]):
            slug = f"{city}-il-stove-oven-pickup"
            html = (ROOT / slug / "index.html").read_text(encoding="utf-8")
            parser = Extract()
            parser.feed(html)
            for field in ("fuel_type", "connection_status"):
                with self.subTest(city=city, field=field):
                    elements = parser.fields.get(field, [])
                    self.assertEqual(len(elements), 1)
                    self.assertIn("required", elements[0])
            self.assertIn("noindex, follow", html)
            self.assertIn("Do not loosen or disconnect a gas line", html)

    def test_category_hero_assets(self):
        """Prevent broken image paths in all 44 new category pages."""
        for city in CITIES:
            for category in CATEGORIES:
                slug = f"{city}-il-{category}-pickup"
                with self.subTest(slug=slug):
                    html = (ROOT / slug / "index.html").read_text(encoding="utf-8")
                    parser = Extract()
                    parser.feed(html)
                    self.assertEqual(len(parser.images), 1)
                    photo = parser.images[0].get("src", "")
                    self.assertTrue(photo.startswith("/"))
                    self.assertTrue((ROOT / photo.lstrip("/")).is_file())


if __name__ == "__main__":
    unittest.main()
