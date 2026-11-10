"""TTG Ohio staged pickup guides: protect request-only claims and distinct existing Columbus URLs."""
from pathlib import Path
import json
import unittest
from scripts.ttg_state_batch_qa import ROOT, check_manifest
class OhioStateBatchTests(unittest.TestCase):
    def test_request_only_preflight(self):
        self.assertEqual(check_manifest(ROOT / "data/ttg-state-batches/OH.json"), [])
    def test_ohio_rollout_count_and_columbus_protection(self):
        rows=json.loads((ROOT / "data/ttg-state-batches/OH.json").read_text())["pages"]
        self.assertEqual(len(rows),26)
        self.assertNotIn("columbus-appliance-pickup/index.html",rows)
        hub=(ROOT / "ohio-appliance-pickup/index.html").read_text()
        for r in rows:
            if r == "ohio-appliance-pickup/index.html": continue
            self.assertIn('/'+r.replace('/index.html','')+'/', hub)
        for slug in ("columbus-appliance-pickup","columbus-washer-dryer-pickup",
                     "columbus-refrigerator-pickup","columbus-stove-pickup","columbus-freezer-pickup"):
            self.assertIn('/'+slug+'/',hub)
        self.assertIn("City of Columbus bulk collection guide",hub)
    def test_new_ohio_routes_not_advertised_as_active(self):
        ledger=json.loads((ROOT/"data/ttg-release-readiness/OH.json").read_text())
        self.assertEqual(ledger["verified_cities"],[])
        self.assertFalse(ledger["form_receipt"]["verified"])
        for path in json.loads((ROOT/"data/ttg-state-batches/OH.json").read_text())["pages"]:
            h=(ROOT/path).read_text()
            self.assertIn('content="noindex, follow"',h)
            self.assertIn("not a completed Ohio pickup",h)
            self.assertIn('name="privacy_acknowledgment"',h)
            self.assertIn('name="paid_option"',h)
    def test_distinct_category_guidance(self):
        for city in ("cleveland","cincinnati","dayton","toledo","akron"):
            for kind in ("washer-dryer","refrigerator","stove-oven","freezer"):
                path=ROOT/f"{city}-oh-{kind}-pickup/index.html"
                h=path.read_text()
                self.assertIn('action="https://formspree.io/f/mvzeapzd"',h)
                self.assertIn(f'name="source_page" value="{city}-oh-{kind}-pickup"',h)
                if kind=="stove-oven":
                    self.assertIn('name="fuel_type" required',h)
                    self.assertIn('name="connection_status" required',h)
if __name__=="__main__": unittest.main()
