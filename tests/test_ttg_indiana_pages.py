"""TTG Indiana request-only batch QA."""
import json
import unittest
from scripts.ttg_state_batch_qa import ROOT,check_manifest
class IndianaBatchTests(unittest.TestCase):
    def test_manifest(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/IN.json"),[])
    def test_city_hub_links(self):
        pages=json.loads((ROOT/"data/ttg-state-batches/IN.json").read_text())["pages"]
        self.assertEqual(len(pages),49)
        hub=(ROOT/"indiana-appliance-pickup/index.html").read_text()
        for p in pages:
            h=(ROOT/p).read_text()
            self.assertIn('content="noindex, follow"',h)
            self.assertIn('name="privacy_acknowledgment"',h)
            self.assertIn('name="paid_option"',h)
            if p!="indiana-appliance-pickup/index.html":
                self.assertIn('href="/'+p.removesuffix("/index.html")+'/"',hub)
    def test_stove_safety(self):
        for p in json.loads((ROOT/"data/ttg-state-batches/IN.json").read_text())["pages"]:
            if "-stove-oven-" not in p:continue
            h=(ROOT/p).read_text()
            self.assertIn('name="fuel_type" required',h)
            self.assertIn('name="connection_status" required',h)
    def test_recycling_source_and_inactive_release(self):
        h=(ROOT/"lafayette-in-refrigerator-pickup/index.html").read_text()
        self.assertIn("official refrigerator disposal resource",h)
        r=json.loads((ROOT/"data/ttg-release-readiness/IN.json").read_text())
        self.assertFalse(r["form_receipt"]["verified"])
        self.assertEqual(r["verified_cities"],[])
if __name__=="__main__":unittest.main()
