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
                h1 = re.search(r"<h1[^>]*>([\\s\\S]*?)</h1>", html, re.I)
                self.assertIsNotNone(title)
                self.assertIsNotNone(h1)
                self.assertIn("Free Appliance Pickup", title.group(1))
                clean_h1 = re.sub(r"<[^>]+>", "", h1.group(1))
                clean_h1 = re.sub(r"\\s+", " ", clean_h1).strip()
                self.assertIn("Free Appliance Pickup", clean_h1)

    def test_new_phrasing_does_not_guarantee_coverage(self):
        """Each updated page explains free collection is conditional."""
        for state in STATES_UPDATED:
            with self.subTest(state=state):
                html = (ROOT / f"{state}-appliance-pickup/index.html").read_text(encoding="utf-8")
                self.assertIn("Free appliance pickup eligibility:", html)
                self.assertIn("Free pickup is not guaranteed", html)
                self.assertIn("confirmed local pickup option", html)
                self.assertEqual(len(re.findall(r"<h1\\b", html, re.I)), 1)
                self.assertIn(f"https://freereliableappliancepickup.com/{state}-appliance-pickup/", html)

    def test_illinois_and_minnesota_remain_unverified(self):
        """No copy-only statewide change should silently index staging markets."""
        for state in ("illinois", "minnesota"):
            with self.subTest(state=state):
                html = (ROOT / f"{state}-appliance-pickup/index.html").read_text(encoding="utf-8")
                self.assertIn('content="noindex, follow"', html)


if __name__ == "__main__":
    unittest.main()
