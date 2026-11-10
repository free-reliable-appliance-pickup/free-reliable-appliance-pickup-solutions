"""Iowa 251-page Gold-model request-only content tests."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
K={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class IowaGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mp=ROOT/"data/ttg-state-batches/IA.json"
  cls.batch=json.loads(cls.mp.read_text())
  cls.paths=cls.batch["pages"]
 def test_matrix_and_manifest(self):
  self.assertEqual(check_manifest(self.mp),[])
  self.assertEqual(len(self.paths),251)
  cities={}
  for p in self.paths:
   m=re.fullmatch(r"([a-z0-9-]+)-ia-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",p)
   if m:cities.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(cities),50)
  for types in cities.values():self.assertEqual(types,K)
 def test_forms_images_stoves(self):
  sets=set()
  for p in self.paths:
   h=(ROOT/p).read_text();pg=Page();pg.feed(h)
   self.assertEqual(pg.h1,1,p)
   self.assertEqual(len(pg.forms),1,p)
   self.assertEqual(len(pg.images),2,p)
   self.assertEqual(pg.state_options,["","IA"],p)
   self.assertIn("noindex, follow",h,p)
   self.assertIn("Free Reliable Appliance Pickup",h,p)
   self.assertIn('name="paid_option"',h,p)
   self.assertIn('name="privacy_acknowledgment"',h,p)
   self.assertNotIn("Nebraska",h,p)
   self.assertNotIn("Omaha",h,p)
   if p.endswith("-washer-dryer-pickup/index.html"):
    sets.add(re.search(r'<figure><img src="([^"]+)"',h).group(1))
   if p.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type" required',h,p)
    self.assertIn('name="connection_status" required',h,p)
  self.assertEqual(len(sets),50)
 def test_hub_and_release(self):
  h=(ROOT/"iowa-appliance-pickup/index.html").read_text()
  for p in self.paths:
   if p.endswith("-ia-appliance-pickup/index.html"):
    self.assertIn('href="/'+p.removesuffix("index.html")+'"',h)
  self.assertIn("Free pickup is not guaranteed",h)
  self.assertIn("confirmed local pickup option",h)
  self.assertNotIn("https://freereliableappliancepickup.com/iowa-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
  ledger=json.loads((ROOT/"data/ttg-release-readiness/IA.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"])
  self.assertEqual(ledger["verified_cities"],[])
  self.assertFalse(ledger["form_receipt"]["verified"])
  self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
