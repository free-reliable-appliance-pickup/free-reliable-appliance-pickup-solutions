"""Conversion guardrails for apartments and rental-property requests."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "landlord-property-manager-appliance-pickup",
    "multifamily-appliance-pickup",
]

class ApartmentLeadIntakeTests(unittest.TestCase):
    def test_first_main_panel_is_customer_form_and_no_duplicate_forms(self):
        for slug in PAGES:
            with self.subTest(slug=slug):
                html = (ROOT / slug / "index.html").read_text(encoding="utf-8")
                self.assertRegex(html, r'(?is)<main>\s*<section id="request"')
                self.assertEqual(len(re.findall(r"<form\\b", html, re.I)), 1)
                self.assertIn('action="https://formspree.io/f/mvzeapzd"', html)
                self.assertIn('name="photos_available" required', html)
                self.assertIn('name="photo_link"', html)
                self.assertIn('name="phone"', html)
                self.assertIn("Free Appliance", html)
                self.assertIn("not guarantee free pickup", html.lower())

    def test_property_manager_routes_are_form_qualified(self):
        html = (ROOT / PAGES[0] / "index.html").read_text(encoding="utf-8")
        for field in ("zip", "volume", "frequency", "city", "state", "message"):
            with self.subTest(field=field):
                self.assertIn(f'name="{field}"', html)

    def test_multifamily_keeps_volume_and_cadence(self):
        html = (ROOT / PAGES[1] / "index.html").read_text(encoding="utf-8")
        self.assertIn('name="frequency"', html)
        self.assertIn('name="volume"', html)
        self.assertIn('name="locations"', html)

if __name__ == "__main__":
    unittest.main()
