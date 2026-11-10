"""Michigan FastTrack request-only batch: enforce safety, city navigation and intent."""
import unittest
import json
from scripts.ttg_state_batch_qa import ROOT,check_manifest
class MichiganFastTrack(unittest.TestCase):
    def test_state_manifest(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/MI.json"),[])
    def test_61_pages_reachable_and_unverified(self):
        manifest=json.loads((ROOT/"data/ttg-state-batches/MI.json").read_text())
        self.assertEqual(len(manifest["pages"]),61)
        hub=(ROOT/"michigan-appliance-pickup/index.html").read_text()
        for path in manifest["pages"]:
            html=(ROOT/path).read_text()
            self.assertIn('content="noindex, follow"',html)
            self.assertIn('name="privacy_acknowledgment"',html)
            self.assertIn('name="paid_option"',html)
            if path=="michigan-appliance-pickup/index.html": continue
            self.assertIn('href="/'+path.removesuffix("/index.html")+'/"',hub)
    def test_stove_gas_fields(self):
        for path in json.loads((ROOT/"data/ttg-state-batches/MI.json").read_text())["pages"]:
            if "-stove-oven-" not in path:continue
            html=(ROOT/path).read_text()
            self.assertIn('name="fuel_type" required',html)
            self.assertIn('name="connection_status" required',html)
            self.assertIn("qualified professional",html)
    def test_local_public_alternatives_and_readiness(self):
        a=(ROOT/"grand-rapids-mi-appliance-pickup/index.html").read_text()
        self.assertIn("City of Grand Rapids guidelines",a)
        self.assertIn("$40 bulky-item",a)
        ledger=json.loads((ROOT/"data/ttg-release-readiness/MI.json").read_text())
        self.assertEqual(ledger["verified_cities"],[])
        self.assertFalse(ledger["form_receipt"]["verified"])
if __name__=="__main__":unittest.main()
