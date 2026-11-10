"""Virginia FastTrack batch: verify request-only image and lead safety."""
import json
import unittest
from scripts.ttg_state_batch_qa import ROOT,check_manifest
class VirginiaBatchTests(unittest.TestCase):
    def test_batch_manifest(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/VA.json"),[])
    def test_hub_covers_all_pages(self):
        m=json.loads((ROOT/"data/ttg-state-batches/VA.json").read_text())
        self.assertEqual(len(m["pages"]),49)
        hub=(ROOT/"virginia-appliance-pickup/index.html").read_text()
        for path in m["pages"]:
            h=(ROOT/path).read_text()
            self.assertIn('content="noindex, follow"',h)
            self.assertIn('name="privacy_acknowledgment"',h)
            self.assertIn('name="paid_option"',h)
            if path=="virginia-appliance-pickup/index.html": continue
            self.assertIn('href="/'+path.removesuffix("/index.html")+'/"',hub)
    def test_safety_for_stoves(self):
        paths=json.loads((ROOT/"data/ttg-state-batches/VA.json").read_text())["pages"]
        for path in paths:
            if "-stove-oven-" not in path: continue
            html=(ROOT/path).read_text()
            self.assertIn('name="fuel_type" required',html)
            self.assertIn('name="connection_status" required',html)
            self.assertIn("qualified",html)
    def test_official_sources_and_unverified_release(self):
        for p in ("richmond-va-appliance-pickup/index.html","virginia-beach-va-appliance-pickup/index.html"):
            self.assertIn("Official recycling and municipal alternatives",(ROOT/p).read_text())
        ledger=json.loads((ROOT/"data/ttg-release-readiness/VA.json").read_text())
        self.assertFalse(ledger["form_receipt"]["verified"])
        self.assertEqual(ledger["verified_cities"],[])
if __name__=="__main__":unittest.main()
