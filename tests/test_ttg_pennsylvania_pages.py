"""PA batch QA: market and release safety."""
import unittest
import json
from scripts.ttg_state_batch_qa import ROOT,check_manifest
class PennsylvaniaBatchTests(unittest.TestCase):
    def test_manifest(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/PA.json"),[])
    def test_city_links(self):
        paths=json.loads((ROOT/"data/ttg-state-batches/PA.json").read_text())["pages"]
        self.assertEqual(len(paths),49)
        hub=(ROOT/"pennsylvania-appliance-pickup/index.html").read_text()
        self.assertIn("Official recycling and disposal alternatives",hub)
        for path in paths:
            text=(ROOT/path).read_text()
            self.assertIn('content="noindex, follow"',text)
            self.assertIn('name="paid_option"',text)
            self.assertIn('name="privacy_acknowledgment"',text)
            if path!="pennsylvania-appliance-pickup/index.html":
                self.assertIn('href="/'+path.removesuffix("/index.html")+'/"',hub)
    def test_appliance_safety(self):
        paths=json.loads((ROOT/"data/ttg-state-batches/PA.json").read_text())["pages"]
        for path in paths:
            if "-stove-oven-" not in path:continue
            text=(ROOT/path).read_text()
            self.assertIn('name="fuel_type" required',text)
            self.assertIn('name="connection_status" required',text)
            self.assertIn("qualified",text)
    def test_unverified_operator_ledger(self):
        ledger=json.loads((ROOT/"data/ttg-release-readiness/PA.json").read_text())
        self.assertFalse(ledger["form_receipt"]["verified"])
        self.assertEqual(ledger["verified_cities"],[])
if __name__=="__main__":unittest.main()
