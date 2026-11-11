"""Guard California's highest-priority washer and dryer pickup conversion flows."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SLUGS = (
    "california",
    "rancho-cucamonga",
    "fontana",
    "upland",
    "ontario",
    "fresno",
    "los-angeles",
    "orange-county",
    "sacramento",
    "san-diego",
    "riverside",
)


class CaliforniaLaundryIntakeTests(unittest.TestCase):
    def test_each_laundry_page_starts_with_real_request_form(self):
        for slug in SLUGS:
            with self.subTest(market=slug):
                html = (ROOT / f"{slug}-washer-dryer-pickup/index.html").read_text(encoding="utf-8")
                main = re.search(r"(?is)<main\b[^>]*>\s*<section\b[^>]*>", html)
                self.assertIsNotNone(main, slug)
                self.assertIn('id="request"', main.group())
                self.assertEqual(len(re.findall(r"<form\b", html, re.I)), 1, slug)
                self.assertIn('action="https://formspree.io/f/mvzeapzd"', html)
                self.assertIn('name="phone"', html)
                self.assertIn('name="zip"', html)
                self.assertIn('name="appliance"', html)
                self.assertIn('name="condition"', html)
                self.assertIn('name="photos_available" required', html)
                self.assertIn('name="photo_link"', html)
                self.assertIn('name="washer_test"', html)
                self.assertIn('name="dryer_test"', html)
                self.assertIn('name="dryer_type"', html)
                self.assertIn("Free Reliable Appliance Pickup", html)
                self.assertIn("Free Washer", html)
                self.assertIn("Free pickup is not guaranteed", html)
                self.assertRegex(html, r'(?i)name="robots" content="index,\s*follow')

    def test_rancho_hero_cta_leads_to_its_own_form(self):
        html = (ROOT / "rancho-cucamonga-washer-dryer-pickup/index.html").read_text(encoding="utf-8")
        self.assertIn('href="#request">Check Pickup Availability', html)
        self.assertIn('href="#request">Request Pickup', html)
        self.assertIn('name="source_page" value="rancho-cucamonga-washer-dryer-pickup"', html)

    def test_form_has_exactly_one_submit_button(self):
        for slug in SLUGS:
            with self.subTest(market=slug):
                html = (ROOT / f"{slug}-washer-dryer-pickup/index.html").read_text(encoding="utf-8")
                form = re.search(r"(?is)<form\b[^>]*>(.*?)</form>", html)
                self.assertIsNotNone(form)
                self.assertEqual(len(re.findall(r'<button\b[^>]*type="submit"', form.group(1), re.I)), 1)


if __name__ == "__main__":
    unittest.main()
