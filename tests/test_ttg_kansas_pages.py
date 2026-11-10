"""Kansas 251-page TTG California Gold customer request safety."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
K={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class KansasGold(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/KS.json"
  cls.batch=json.loads(cls.manifest.read_text())
  cls.pages=cls.batch["pages"]
 def test_50_city_category_matrix_and_valid_manifest(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.pages),251)
  cities={}
  for p in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-ks-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",p)
   if m:cities.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(cities),50)
  for types in cities.values():self.assertEqual(types,K)
 def test_customer_copy_forms_photos_and_safe_disconnection(self):
  photos=set()
  for p in self.pages:
   h=(ROOT/p).read_text()
   page=Page();page.feed(h)
   self.assertEqual(page.h1,1,p)
   self.assertEqual(len(page.forms),1,p)
   self.assertEqual(len(page.images),2,p)
   self.assertEqual(page.state_options,["","KS"],p)
   self.assertIn("noindex, follow",h,p)
   self.assertIn("Free Reliable Appliance Pickup",h,p)
   self.assertIn('name="paid_option"',h,p)
   self.assertIn('name="privacy_acknowledgment"',h,p)
   self.assertNotIn("Arkansas",h,p)
   self.assertNotIn("Little Rock",h,p)
   if p.endswith("-washer-dryer-pickup/index.html"):
    photos.add(re.search(r'<figure><img src="([^"]+)"',h).group(1))
   if p.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type" required',h,p)
    self.assertIn('name="connection_status" required',h,p)
  self.assertEqual(len(photos),50)
 def test_stage_not_activated(self):
  hub=(ROOT/"kansas-appliance-pickup/index.html").read_text()
  for p in self.pages:
   if p.endswith("-ks-appliance-pickup/index.html"):
    self.assertIn('href="/'+p.removesuffix("index.html")+'"',hub)
  self.assertIn("Free pickup is not guaranteed",hub)
  self.assertIn("confirmed local pickup option",hub)
  self.assertNotIn("https://freereliableappliancepickup.com/kansas-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
  ready=json.loads((ROOT/"data/ttg-release-readiness/KS.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"])
  self.assertEqual(ready["verified_cities"],[])
  self.assertFalse(ready["form_receipt"]["verified"])
  self.assertFalse(ready["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
