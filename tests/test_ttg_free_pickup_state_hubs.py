"""Free appliance pickup messaging must be prominent but conditional on state hubs."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
STATES_UPDATED = ["alabama","arizona","florida","georgia","idaho","illinois","kansas","nevada","new-mexico","new-york","north-carolina","oklahoma","utah","washington"]
ALREADY_GOLD = ["california", "colorado", "minnesota", "oregon", "texas"]


class StateFreePickupHeadings(unittest.TestCase):
    """Regression checks for high-intent statewide wording and qualification."""

    def test_all_existing_state_hubs_have_free_pickup_titles(self):
        """Protect the 19 statewide titles and user-visible H1 headings."""
        for state in STATES_UPDATED + ALREADY_GOLD:
            with self.subTest(state=state):
                html = (ROOT / f"{state}-appliance-pickup/index.html").read_text(encoding="utf-8")
                title = re.search(r"<title>([^<]+)</title>", html, re.I)
                h1 = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", html, re.I)
                self.assertIsNotNone(title)
                self.assertIsNotNone(h1)
                self.assertIn("Free Appliance Pickup", title.group(1))
                clean_h1 = re.sub(r"<[^>]+>", "", h1.group(1))
                clean_h1 = re.sub(r"\s+", " ", clean_h1).strip()
                self.assertIn("Free Appliance Pickup", clean_h1)

    def test_new_phrasing_does_not_guarantee_coverage(self):
        """Each updated page explains free collection is conditional."""
        for state in STATES_UPDATED:
            with self.subTest(state=state):
                html = (ROOT / f"{state}-appliance-pickup/index.html").read_text(encoding="utf-8")
                self.assertNotIn("eligibility", re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I).group(1).lower())
                self.assertIn("Free pickup is not guaranteed", html)
                self.assertIn("confirmed local pickup option", html)
                self.assertEqual(len(re.findall(r"<h1\b", html, re.I)), 1)
                self.assertIn(f"https://freereliableappliancepickup.com/{state}-appliance-pickup/", html)

    def test_illinois_and_minnesota_remain_unverified(self):
        """No copy-only statewide change should silently index staging markets."""
        for state in ("illinois", "minnesota"):
            with self.subTest(state=state):
                html = (ROOT / f"{state}-appliance-pickup/index.html").read_text(encoding="utf-8")
                self.assertIn('content="noindex, follow"', html)


    def test_california_request_form_is_first_and_photo_ready(self):
        """Keep California's active statewide pickup form visible before long city guides."""
        html = (ROOT / "california-appliance-pickup/index.html").read_text(encoding="utf-8")
        main = html.split("<main>", 1)[1]
        first_section = re.search(r"<section\b[^>]*>", main)
        self.assertIsNotNone(first_section)
        self.assertIn('id="request"', first_section.group(0))
        self.assertEqual(html.count('<form '), 1)
        self.assertIn("<h2>Request Free Appliance Pickup in California</h2>", html)
        form = html.split("<form ", 1)[1].split("</form>", 1)[0]
        self.assertIn('action="https://formspree.io/f/mvzeapzd"', form)
        for name in ("name", "phone", "address", "city", "zip",
                     "appliance", "condition", "floor", "stairs",
                     "photos_available"):
            field = re.search(r'<(?:input|select)\b[^>]*\bname="' + name + r'"[^>]*>', form)
            self.assertIsNotNone(field, name)
            self.assertIn("required", field.group(0), name)
        self.assertIn('name="photo_link"', form)
        self.assertIn('name="source_page" value="california-appliance-pickup"', form)
        self.assertIn('name="state" value="California"', form)
        self.assertIn('<div class="site-request-next-steps">', html)
        self.assertLess(html.index("</form>"), html.index('class="site-request-next-steps"'))
        self.assertIn('name="robots" content="index, follow', html)
        self.assertIn("Free Reliable Appliance Pickup", html)
        self.assertIn("Free pickup is not guaranteed", html)




    def test_oregon_request_form_is_first_and_photo_ready(self):
        """Preserve Oregon's statewide one-form, real-city intake above local guides."""
        html = (ROOT / "oregon-appliance-pickup/index.html").read_text(encoding="utf-8")
        main = html.split("<main>", 1)[1]
        first_section = re.search(r"<section\b[^>]*>", main)
        self.assertIsNotNone(first_section)
        self.assertIn('id="request"', first_section.group(0))
        self.assertEqual(html.count('<form '), 1)
        self.assertIn("<h2>Request Free Appliance Pickup in Oregon</h2>", html)
        form = html.split("<form ", 1)[1].split("</form>", 1)[0]
        self.assertIn('action="https://formspree.io/f/mvzeapzd"', form)
        self.assertIn('data-photo-first-enhanced="1"', form)
        for name in ("name", "phone", "address", "city", "zip",
                     "appliance", "condition", "floor", "stairs", "photos_available"):
            field = re.search(r'<(?:input|select)\b[^>]*\bname="' + name + r'"[^>]*>', form)
            self.assertIsNotNone(field, name)
            self.assertIn("required", field.group(0), name)
        self.assertIn('pattern="[0-9]{5}"', form)
        self.assertIn('name="photo_link"', form)
        self.assertIn('name="state" value="Oregon"', form)
        self.assertIn('name="source_page" value="oregon-appliance-pickup"', form)
        self.assertIn('<div class="site-request-next-steps">', html)
        self.assertLess(html.index("</form>"), html.index('class="site-request-next-steps"'))
        self.assertIn('name="robots" content="index, follow', html)
        self.assertIn("Free Reliable Appliance Pickup", html)
        self.assertIn("Free pickup is not guaranteed", html)


    def test_eight_legacy_state_hubs_have_form_first_and_photo_questions(self):
        """The eight older state hubs must show their existing request form above guides."""
        state_names = ("florida", "georgia", "colorado", "idaho",
                       "nevada", "new-mexico", "new-york", "utah")
        for slug in state_names:
            with self.subTest(state=slug):
                html = (ROOT / f"{slug}-appliance-pickup/index.html").read_text(encoding="utf-8")
                state_label = slug.replace("-", " ").title()
                main = re.split(r"<main\b[^>]*>", html, maxsplit=1)[1]
                first_section = re.search(r"<section\b[^>]*>", main)
                self.assertIsNotNone(first_section)
                self.assertIn('id="request"', first_section.group(0))
                self.assertIn(f"<h2>Request Free Appliance Pickup in {state_label}</h2>", html)
                self.assertEqual(len(re.findall(r"<form\b", html)), 1)
                form = re.split(r"<form\b", html, maxsplit=1)[1].split("</form>", 1)[0]
                self.assertIn('action="https://formspree.io/f/mvzeapzd"', form)
                self.assertIn('data-photo-first-enhanced="1"', form)
                for name in ("name", "phone", "address", "city", "zip",
                             "appliance", "condition", "floor", "stairs",
                             "photos_available"):
                    field = re.search(r'<(?:input|select)\b[^>]*\bname="' + name + r'"[^>]*>', form)
                    self.assertIsNotNone(field, name)
                    self.assertIn("required", field.group(0), name)
                self.assertIn('pattern="[0-9]{5}"', form)
                self.assertIn('name="photo_link"', form)
                self.assertIn(f'name="source_page" value="{slug}-appliance-pickup"', form)
                self.assertIn('<div class="site-request-next-steps">', html)
                self.assertLess(html.index("</form>"), html.index('class="site-request-next-steps"'))
                self.assertIn('name="robots" content="index, follow', html)
                self.assertIn("Free Reliable Appliance Pickup", html)
                self.assertEqual(len(re.findall(r"<h1\b", html, re.I)), 1)

if __name__ == "__main__":
    unittest.main()
