"""SC Turbo batch request-only checks."""
import json
import unittest
from scripts.ttg_state_batch_qa import ROOT,check_manifest
class SouthCarolinaFastTrack(unittest.TestCase):
    def test_manifest(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/SC.json"),[])
    def test_all_links_and_nonindex(self):
        m=json.loads((ROOT/"data/ttg-state-batches/SC.json").read_text())
        self.assertEqual(len(m["pages"]),251)
        hub=(ROOT/"south-carolina-appliance-pickup/index.html").read_text()
        for path in m["pages"]:
            h=(ROOT/path).read_text()
            self.assertIn('content="noindex, follow"',h)
            self.assertIn('name="privacy_acknowledgment"',h)
            self.assertIn('name="paid_option"',h)
            if path!="south-carolina-appliance-pickup/index.html":
                slug=path.removesuffix("/index.html")
                if "-sc-appliance-pickup" in path:
                    self.assertIn('href="/'+slug+'/"',hub)
                else:
                    city=slug.split("-sc-",1)[0]
                    city_hub=(ROOT/(city+"-sc-appliance-pickup/index.html")).read_text()
                    self.assertIn('href="/'+slug+'/"',city_hub)
    def test_public_alternatives(self):
        m=(ROOT/"myrtle-beach-sc-appliance-pickup/index.html").read_text()
        g=(ROOT/"greenville-sc-refrigerator-pickup/index.html").read_text()
        self.assertIn("Horry County location directory",m)
        self.assertIn("Residential Waste and Recycling Centers",g)
    def test_stove_safety(self):
        for path in json.loads((ROOT/"data/ttg-state-batches/SC.json").read_text())["pages"]:
            if "-stove-oven-" not in path:continue
            h=(ROOT/path).read_text()
            self.assertIn('name="fuel_type" required',h)
            self.assertIn('name="connection_status" required',h)
    def test_release_unverified(self):
        r=json.loads((ROOT/"data/ttg-release-readiness/SC.json").read_text())
        self.assertFalse(r["form_receipt"]["verified"])
        self.assertEqual(r["verified_cities"],[])
if __name__=="__main__":unittest.main()
