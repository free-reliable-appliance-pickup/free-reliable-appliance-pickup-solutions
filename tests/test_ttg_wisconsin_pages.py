"""Wisconsin request-only batch coverage and safety tests."""
import json
import unittest
from scripts.ttg_state_batch_qa import ROOT,check_manifest

class WisconsinBatchTests(unittest.TestCase):
    """Guard Wisconsin city guides, municipal rules and local activation."""
    def test_manifest(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/WI.json"),[])
    def test_all_pages_and_hub_links(self):
        pages=json.loads((ROOT/"data/ttg-state-batches/WI.json").read_text())["pages"]
        self.assertEqual(len(pages),61)
        hub=(ROOT/"wisconsin-appliance-pickup/index.html").read_text()
        for p in pages:
            html=(ROOT/p).read_text()
            self.assertIn('content="noindex, follow"',html)
            self.assertIn('value="quote_ok"',html)
            self.assertIn('name="privacy_acknowledgment"',html)
            if p!="wisconsin-appliance-pickup/index.html":
                self.assertIn('href="/'+p.removesuffix("/index.html")+'/"',hub)
    def test_local_public_alternatives(self):
        m=(ROOT/"milwaukee-wi-appliance-pickup/index.html").read_text()
        d=(ROOT/"madison-wi-appliance-pickup/index.html").read_text()
        self.assertIn("not accepted curbside",m)
        self.assertIn("more than eight units",d)
    def test_gas_stove_safety(self):
        for p in json.loads((ROOT/"data/ttg-state-batches/WI.json").read_text())["pages"]:
            if "-stove-oven-" not in p: continue
            h=(ROOT/p).read_text()
            self.assertIn('name="fuel_type" required',h)
            self.assertIn('name="connection_status" required',h)
    def test_release_unapproved(self):
        r=json.loads((ROOT/"data/ttg-release-readiness/WI.json").read_text())
        self.assertEqual(r["verified_cities"],[])
        self.assertFalse(r["form_receipt"]["verified"])
        self.assertFalse(r["owner_release_approval"]["approved"])

if __name__=="__main__":unittest.main()
