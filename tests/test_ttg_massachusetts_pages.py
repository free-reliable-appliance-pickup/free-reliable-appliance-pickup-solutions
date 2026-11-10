"""Massachusetts customer-facing 50x5 free pickup matrix guards."""
import json, re, unittest
from scripts.ttg_state_batch_qa import ROOT, Page, check_manifest
CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class MassachusettsGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mp=ROOT/"data/ttg-state-batches/MA.json"
  cls.batch=json.loads(cls.mp.read_text())
  cls.pages=cls.batch["pages"]
 def test_city_matrix(self):
  self.assertEqual(check_manifest(self.mp),[])
  self.assertEqual(len(self.pages),251)
  cities={}
  for p in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-ma-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",p)
   if m:cities.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(cities),50)
  for c in cities.values():self.assertEqual(c,CATS)
 def test_forms_images_brand_and_stoves(self):
  washers=set()
  for p in self.pages:
   h=(ROOT/p).read_text(); pg=Page(); pg.feed(h)
   self.assertEqual(pg.h1,1,p)
   self.assertEqual(len(pg.forms),1,p)
   self.assertEqual(len(pg.images),2,p)
   self.assertEqual(pg.state_options,["","MA"],p)
   for s in ('Free Reliable Appliance Pickup','noindex, follow','name="source_page"','name="paid_option"','name="privacy_acknowledgment"','name="photos_available"'):
    self.assertIn(s,h,p)
   self.assertNotIn("Maryland",h,p)
   if p.endswith("-washer-dryer-pickup/index.html"):
    washers.add(re.search(r'<figure><img src="([^"]+)"',h).group(1))
   if p.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',h,p)
    self.assertIn('name="connection_status"',h,p)
  self.assertEqual(len(washers),50)
 def test_hub_sitemap_and_release_gate(self):
  h=(ROOT/"massachusetts-appliance-pickup/index.html").read_text()
  self.assertIn("Free Appliance Pickup in Massachusetts",h)
  for p in self.pages:
   if p.endswith("-ma-appliance-pickup/index.html"):
    self.assertIn('href="/'+p.removesuffix("index.html")+'"',h)
  self.assertNotIn("https://freereliableappliancepickup.com/massachusetts-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
  ledger=json.loads((ROOT/"data/ttg-release-readiness/MA.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"])
  self.assertEqual(ledger["verified_cities"],[])
  self.assertFalse(ledger["form_receipt"]["verified"])
  self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
