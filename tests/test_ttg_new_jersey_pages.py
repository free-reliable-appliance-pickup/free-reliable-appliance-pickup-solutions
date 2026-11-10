"""New Jersey 251-page California Gold request-only tests."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
K={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class NewJerseyGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mp=ROOT/"data/ttg-state-batches/NJ.json"
  cls.batch=json.loads(cls.mp.read_text())
  cls.pages=cls.batch["pages"]
 def test_manifest_matrix(self):
  self.assertEqual(check_manifest(self.mp),[])
  self.assertEqual(len(self.pages),251)
  cities={}
  for p in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-nj-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",p)
   if m:cities.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(cities),50)
  for types in cities.values():self.assertEqual(types,K)
 def test_customer_intake_photos_stove_safety(self):
  photos=set()
  for p in self.pages:
   h=(ROOT/p).read_text()
   pg=Page();pg.feed(h)
   self.assertEqual(pg.h1,1,p)
   self.assertEqual(len(pg.forms),1,p)
   self.assertEqual(len(pg.images),2,p)
   self.assertEqual(pg.state_options,["","NJ"],p)
   self.assertIn("noindex, follow",h,p)
   self.assertIn("Free Reliable Appliance Pickup",h,p)
   self.assertIn('name="paid_option"',h,p)
   self.assertIn('name="privacy_acknowledgment"',h,p)
   self.assertNotIn("Iowa",h,p)
   self.assertNotIn("Des Moines",h,p)
   if p.endswith("-washer-dryer-pickup/index.html"):
    photos.add(re.search(r'<figure><img src="([^"]+)"',h).group(1))
   if p.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type" required',h,p)
    self.assertIn('name="connection_status" required',h,p)
  self.assertEqual(len(photos),50)
 def test_hub_and_release_gate(self):
  h=(ROOT/"new-jersey-appliance-pickup/index.html").read_text()
  for p in self.pages:
   if p.endswith("-nj-appliance-pickup/index.html"):
    self.assertIn('href="/'+p.removesuffix("index.html")+'"',h)
  self.assertIn("Free pickup is not guaranteed",h)
  self.assertIn("confirmed local pickup option",h)
  self.assertNotIn("https://freereliableappliancepickup.com/new-jersey-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
  ledger=json.loads((ROOT/"data/ttg-release-readiness/NJ.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"])
  self.assertEqual(ledger["verified_cities"],[])
  self.assertFalse(ledger["form_receipt"]["verified"])
  self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
