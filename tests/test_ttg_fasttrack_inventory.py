"""Safety checks for TTG nationwide state/city source inventory."""
import tempfile
import unittest
from pathlib import Path

from scripts.ttg_fasttrack_inventory import (
    ROOT, collect, load_sources, page_presence, slugify, status_for,
)


class FastTrackInventoryTests(unittest.TestCase):
    def test_slug_keeps_readable_url(self):
        self.assertEqual(slugify("La Cañada Flintridge"), "la-canada-flintridge")
        self.assertEqual(slugify("St. Petersburg"), "st-petersburg")

    def test_legacy_city_path_is_not_auto_attributed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "springfield-appliance-pickup").mkdir()
            (root / "springfield-appliance-pickup/index.html").write_text(
                "<html></html>", encoding="utf-8"
            )
            codes = {"springfield": {"IL", "MO"}}
            record = page_presence(root, "springfield", "IL", "appliance", codes)
            self.assertEqual(record["source"], "ambiguous-needs-manual-attribution")
            self.assertIsNotNone(record["file"])
            (root / "springfield-il-appliance-pickup").mkdir()
            (root / "springfield-il-appliance-pickup/index.html").write_text(
                "<html></html>", encoding="utf-8"
            )
            specific = page_presence(root, "springfield", "IL", "appliance", codes)
            self.assertEqual(specific["source"], "state-scoped")

    def test_route_does_not_turn_request_only_into_coverage(self):
        state = {"state": "Illinois", "state_code": "IL", "status": "request-only"}
        city = {"city": "Chicago", "state_code": "IL", "region": "Chicago Metro"}
        self.assertEqual(status_for(city, state, [])[0], "request-only")
        markets = [{"state_code": "IL", "region": "Chicago Metro", "status": "direct"}]
        self.assertEqual(status_for(city, state, markets), ("direct", "region"))
        markets.append({"state_code": "IL", "city": "Chicago", "status": "request-only"})
        self.assertEqual(status_for(city, state, markets), ("request-only", "exact"))

    def test_real_checkout_has_fifty_state_summaries(self):
        routing, cities = load_sources(ROOT)
        self.assertEqual(len(routing["state_defaults"]), 50)
        self.assertGreater(len(cities["cities"]), 0)
        summaries, details = collect(ROOT)
        self.assertEqual(len(summaries), 50)
        self.assertTrue(any(x["state_code"] == "IL" for x in details))
        self.assertTrue(all(x["index_permission"].startswith("manual_") for x in details))
        self.assertTrue(all(x["release_status"] == "not_determined_by_source_inventory"
                            for x in summaries))


if __name__ == "__main__":
    unittest.main()
