"""NC Turbo FastTrack request-only batch: prevent premature pickup claims."""
import json
import unittest
from scripts.ttg_state_batch_qa import ROOT, check_manifest
class NorthCarolinaBatchTests(unittest.TestCase):
    def test_manifest_preflight(self):
        self.assertEqual(check_manifest(ROOT / "data/ttg-state-batches/NC.json"), [])
    def test_all_city_pages_in_state_directory(self):
        pages=json.loads((ROOT/"data/ttg-state-batches/NC.json").read_text())["pages"]
        self.assertEqual(len(pages),68)
        hub=(ROOT/"north-carolina-appliance-pickup/index.html").read_text()
        for path in pages:
            slug=path.removesuffix("/index.html")
            self.assertIn('href="/'+slug+'/"',hub)
            html=(ROOT/path).read_text()
            self.assertIn('content="noindex, follow"',html)
            self.assertIn('name="privacy_acknowledgment"',html)
            self.assertIn('name="paid_option"',html)
            self.assertIn('not a completed North Carolina pickup',html)
        self.assertIn('<h2>North Carolina City Appliance Pickup Eligibility Guides</h2>',hub)
    def test_stoves_disconnection_fields(self):
        pages=json.loads((ROOT/"data/ttg-state-batches/NC.json").read_text())["pages"]
        for path in pages:
            if "-stove-oven-" not in path: continue
            html=(ROOT/path).read_text()
            self.assertIn('name="fuel_type" required',html)
            self.assertIn('name="connection_status" required',html)
            self.assertIn('qualified professional',html)
    def test_no_activation(self):
        ledger=json.loads((ROOT/"data/ttg-release-readiness/NC.json").read_text())
        self.assertEqual(ledger["verified_cities"],[])
        self.assertFalse(ledger["form_receipt"]["verified"])
if __name__=="__main__": unittest.main()
