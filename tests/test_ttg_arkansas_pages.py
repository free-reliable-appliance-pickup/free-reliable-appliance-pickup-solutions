"""Arkansas California Free Pickup Gold request-only regression checks."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
K={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class ArkansasGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mp=ROOT/"data/ttg-state-batches/AR.json"
  cls.batch=json.loads(cls.mp.read_text())
  cls.pages=cls.batch["pages"]
 def test_manifest_city_matrix(self):
  self.assertEqual(check_manifest(self.mp),[])
  self.assertEqual(len(self.pages),251)
  cities={}
  for p in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-ar-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",p)
   if m:cities.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(cities),50)
  for kinds in cities.values():self.assertEqual(kinds,K)
 def test_customer_request_fields_and_photos(self):
  washer=set()
  for p in self.pages:
   h=(ROOT/p).read_text()
   pg=Page();pg.feed(h)
   self.assertEqual(pg.h1,1,p)
   self.assertEqual(len(pg.forms),1,p)
   self.assertEqual(len(pg.images),2,p)
   self.assertEqual(pg.state_options,["","AR"],p)
   self.assertIn("noindex, follow",h,p)
   self.assertIn("Free Reliable Appliance Pickup",h,p)
   self.assertIn('name="paid_option"',h,p)
   self.assertIn('name="privacy_acknowledgment"',h,p)
   self.assertNotIn("Louisiana",h,p)
   self.assertNotIn("Baton Rouge",h,p)
   if p.endswith("-washer-dryer-pickup/index.html"):
    washer.add(re.search(r'<figure><img src="([^"]+)"',h).group(1))
   if p.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type" required',h,p)
    self.assertIn('name="connection_status" required',h,p)
  self.assertEqual(len(washer),50)
 def test_hub_release_gate(self):
  h=(ROOT/"arkansas-appliance-pickup/index.html").read_text()
  for p in self.pages:
   if p.endswith("-ar-appliance-pickup/index.html"):
    self.assertIn('href="/'+p.removesuffix("index.html")+'"',h)
  self.assertIn("Free pickup is not guaranteed",h)
  self.assertIn("confirmed local pickup option",h)
  self.assertNotIn("https://freereliableappliancepickup.com/arkansas-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
  ledger=json.loads((ROOT/"data/ttg-release-readiness/AR.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"])
  self.assertEqual(ledger["verified_cities"],[])
  self.assertFalse(ledger["form_receipt"]["verified"])
  self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
