"""Guard the Washington statewide customer pickup form-first layout."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class WashingtonStateFormFirst(unittest.TestCase):
    def test_washington_form_is_first_and_photo_ready(self):
        html = (ROOT / "washington-appliance-pickup/index.html").read_text(encoding="utf-8")
        self.assertEqual(html.count('<form '), 1)
        self.assertEqual(html.count('id="request"'), 1)
        main = html.split("<main>", 1)[1]
        first_section = re.search(r"<section\b[^>]*>", main)
        self.assertIsNotNone(first_section)
        self.assertIn('id="request"', first_section.group(0))
        self.assertIn("<h2>Request Free Appliance Pickup in Washington</h2>", html)
        form = html.split("<form ", 1)[1].split("</form>", 1)[0]
        self.assertIn('action="https://formspree.io/f/mvzeapzd"', form)
        self.assertIn('method="POST"', form)
        self.assertIn('data-photo-first-enhanced="1"', form)
        for name in ("name", "phone", "address", "city", "zip",
                     "appliance", "condition", "floor", "stairs",
                     "photos_available"):
            field = re.search(r'<(?:input|select)\b[^>]*\bname="' + name + r'"[^>]*>', form)
            self.assertIsNotNone(field, name)
            self.assertIn("required", field.group(0), name)
        self.assertIn('pattern="[0-9]{5}"', form)
        self.assertIn('name="photo_link"', form)
        self.assertIn('name="state" value="Washington"', form)
        self.assertIn('name="source_page" value="washington-appliance-pickup"', form)
        self.assertIn('name="service" value="General major appliance pickup"', form)
        self.assertIn('<div class="site-request-next-steps">', html)
        self.assertLess(html.index("</form>"), html.index('class="site-request-next-steps"'))
        self.assertIn("Free Reliable Appliance Pickup", html)
        self.assertIn("Free pickup is not guaranteed", html)
        self.assertIn('name="robots" content="index, follow', html)


if __name__ == "__main__":
    unittest.main()
