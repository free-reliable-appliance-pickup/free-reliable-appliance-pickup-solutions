"""Maryland 50-city California-model noindex request-only rollout checks."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class MarylandGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mp=ROOT/"data/ttg-state-batches/MD.json"
  cls.batch=json.loads(cls.mp.read_text())
  cls.pages=cls.batch["pages"]
 def test_city_matrix_and_manifest(self):
  self.assertEqual(check_manifest(self.mp),[])
  self.assertEqual(len(self.pages),251)
  city_types={}
  for p in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-md-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",p)
   if m:city_types.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(city_types),50)
  for v in city_types.values():self.assertEqual(v,CATS)
 def test_forms_images_branding_and_safety(self):
  washer_paths=set()
  for p in self.pages:
   h=(ROOT/p).read_text();pg=Page();pg.feed(h)
   self.assertEqual(pg.h1,1,p)
   self.assertEqual(len(pg.forms),1,p)
   self.assertEqual(len(pg.images),2,p)
   self.assertEqual(pg.state_options,["","MD"],p)
   self.assertIn("Free Reliable Appliance Pickup",h,p)
   self.assertIn("noindex, follow",h,p)
   self.assertIn('name="source_page"',h,p)
   self.assertIn('name="privacy_acknowledgment"',h,p)
   self.assertIn('name="paid_option"',h,p)
   self.assertIn('name="photos_available"',h,p)
   self.assertNotIn("Nebraska",h,p)
   if p.endswith("-washer-dryer-pickup/index.html"):
    washer_paths.add(re.search(r'<figure><img src="([^"]+)"',h).group(1))
   if p.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',h,p)
    self.assertIn('name="connection_status"',h,p)
  self.assertEqual(len(washer_paths),50)
 def test_state_hub_and_release_gate(self):
  h=(ROOT/"maryland-appliance-pickup/index.html").read_text()
  self.assertIn("Free Appliance Pickup in Maryland",h)
  for p in self.pages:
   if p.endswith("-md-appliance-pickup/index.html"):
    self.assertIn('href="/'+p.removesuffix("index.html")+'"',h)
  self.assertNotIn("https://freereliableappliancepickup.com/maryland-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
  ledger=json.loads((ROOT/"data/ttg-release-readiness/MD.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"])
  self.assertEqual(ledger["verified_cities"],[])
  self.assertFalse(ledger["form_receipt"]["verified"])
  self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
