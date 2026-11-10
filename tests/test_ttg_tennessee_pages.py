"""Tennessee request-only 61-page rollout QA."""
import json
import unittest
from scripts.ttg_state_batch_qa import ROOT, check_manifest
class TennesseeBatchTests(unittest.TestCase):
    def test_manifest(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/TN.json"),[])
    def test_all_city_and_appliance_links(self):
        pages=json.loads((ROOT/"data/ttg-state-batches/TN.json").read_text())["pages"]
        self.assertEqual(len(pages),61)
        hub=(ROOT/"tennessee-appliance-pickup/index.html").read_text()
        for path in pages:
            html=(ROOT/path).read_text()
            self.assertIn('content="noindex, follow"',html)
            self.assertIn('name="privacy_acknowledgment"',html)
            self.assertIn('name="paid_option"',html)
            if path!="tennessee-appliance-pickup/index.html":
                self.assertIn('href="/'+path.removesuffix("/index.html")+'/"',hub)
    def test_local_recycling_claims(self):
        n=(ROOT/"nashville-tn-appliance-pickup/index.html").read_text()
        k=(ROOT/"knoxville-tn-refrigerator-pickup/index.html").read_text()
        self.assertIn("convenience-center bulky-items guidance",n)
        self.assertIn("professionally recovered",k)
    def test_gas_fuel_safety(self):
        for path in json.loads((ROOT/"data/ttg-state-batches/TN.json").read_text())["pages"]:
            if "-stove-oven-" not in path:continue
            h=(ROOT/path).read_text()
            self.assertIn('name="fuel_type" required',h)
            self.assertIn('name="connection_status" required',h)
    def test_release_unverified(self):
        r=json.loads((ROOT/"data/ttg-release-readiness/TN.json").read_text())
        self.assertEqual(r["verified_cities"],[])
        self.assertFalse(r["form_receipt"]["verified"])
if __name__=="__main__":unittest.main()
