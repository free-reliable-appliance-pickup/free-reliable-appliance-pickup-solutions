"""Guards for non-activated TTG premium-market research corridors."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PremiumMarketResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "data/ttg-markets/national-premium-territory-candidates.json").read_text())
        cls.routing = json.loads((ROOT / "data/market-routing.json").read_text())
        cls.states = {v["state_code"]: v for v in cls.routing["state_defaults"]}

    def test_unique_corridors_and_documented_income_proxy(self):
        seen = set()
        for row in self.data["candidates"]:
            key = (row["state_code"], row["corridor"])
            self.assertNotIn(key, seen, key)
            seen.add(key)
            self.assertGreater(row["income_usd"], 0)
            self.assertTrue(row["source"].startswith("https://www.census.gov/quickfacts/"), key)
            self.assertGreaterEqual(len(row["focus_cities"]), 2, key)
            self.assertEqual(len(set(row["focus_cities"])), len(row["focus_cities"]))
            self.assertIn("proxy", row["confidence"], key)
            self.assertIn(row["state_code"], self.states, key)
            self.assertEqual(row["status"], "research_priority")

    def test_no_markets_auto_released_or_priced(self):
        for row in self.data["candidates"]:
            for field in ("lead_volume_verified", "working_quality_verified",
                          "partner_profit_verified", "partner_retention_verified",
                          "territory_for_sale"):
                self.assertIs(row[field], False, (row["state_code"], field))
            self.assertIsNone(row["territory_price_cents"])
            self.assertEqual(self.states[row["state_code"]]["lead_priority"], 2)

    def test_newly_promoted_states_stay_request_only(self):
        for code in ("OH", "PA", "TN", "WI"):
            row = self.states[code]
            self.assertEqual(row["lead_priority"], 2)
            self.assertEqual(row["status"], "request-only")
        self.assertGreaterEqual(len(self.data["candidates"]), 17)

    def test_default_routing_does_not_auto_index(self):
        rules = self.routing["rules"]
        self.assertFalse(rules["automaticCityPageCreation"])
        self.assertTrue(rules["coverageConfirmationRequired"])
        self.assertNotIn("request-only", rules["indexableCityStatuses"])


if __name__ == "__main__":
    unittest.main()
