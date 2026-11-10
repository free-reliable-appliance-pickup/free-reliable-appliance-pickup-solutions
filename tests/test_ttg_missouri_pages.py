"""Missouri TTG static batch safety regression."""
import json
import unittest
from scripts.ttg_state_batch_qa import ROOT,check_manifest
class TestMissouri(unittest.TestCase):
 def test_manifest(self):
  self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/MO.json"),[])
 def test_noindex_intake_and_links(self):
  pages=json.loads((ROOT/"data/ttg-state-batches/MO.json").read_text())["pages"]
  self.assertEqual(len(pages),53)
  hub=(ROOT/"missouri-appliance-pickup/index.html").read_text()
  for p in pages:
   h=(ROOT/p).read_text()
   self.assertIn('content="noindex, follow"',h)
   self.assertIn('name="privacy_acknowledgment"',h)
   self.assertIn('value="quote_ok"',h)
   if p!="missouri-appliance-pickup/index.html":self.assertIn('href="/'+p.removesuffix("/index.html")+'/"',hub)
 def test_unverified(self):
  d=json.loads((ROOT/"data/ttg-release-readiness/MO.json").read_text())
  self.assertEqual(d["verified_cities"],[])
  self.assertFalse(d["form_receipt"]["verified"])
  self.assertFalse(d["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
