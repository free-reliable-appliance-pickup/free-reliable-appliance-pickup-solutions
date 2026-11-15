"""Regression checks for Florida priority-city request forms.

These request-only pages must not claim active local coverage or be indexed
until the operating route has been independently verified.
"""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CITIES = ("miami", "tampa", "orlando", "jacksonville", "tallahassee")
TYPES = ("appliance", "washer-dryer", "refrigerator", "freezer", "stove-oven")
ZIP_PATTERN = r"[0-9]{5}(-[0-9]{4})?"


class FloridaPriorityZipTests(unittest.TestCase):
    def test_priority_guides_accept_zip4_and_keep_request_only_safeguards(self):
        for city in CITIES:
            for appliance_type in TYPES:
                slug = f"{city}-fl-{appliance_type}-pickup"
                with self.subTest(page=slug):
                    html = (ROOT / slug / "index.html").read_text(encoding="utf-8")
                    self.assertIn('<meta name="robots" content="noindex, follow">', html)
                    self.assertIn('https://formspree.io/f/mvzeapzd', html)
                    self.assertIn('name="photos_available" required', html)
                    zip_inputs = re.findall(r'<input\b[^>]*\bname="zip"[^>]*>', html)
                    self.assertEqual(len(zip_inputs), 1, "One required ZIP input per page")
                    zip_input = zip_inputs[0]
                    self.assertIn("required", zip_input)
                    self.assertIn('maxlength="10"', zip_input)
                    self.assertIn('autocomplete="postal-code"', zip_input)
                    self.assertIn(f'pattern="{ZIP_PATTERN}"', zip_input)
                    self.assertIn("ZIP+4", html)
                    for valid in ("33101", "32801", "02108", "33101-1234"):
                        self.assertIsNotNone(re.fullmatch(ZIP_PATTERN, valid))
                    for invalid in ("3310", "331011234", "33101-123", "33101-12345", "abcde"):
                        self.assertIsNone(re.fullmatch(ZIP_PATTERN, invalid))


if __name__ == "__main__":
    unittest.main()
