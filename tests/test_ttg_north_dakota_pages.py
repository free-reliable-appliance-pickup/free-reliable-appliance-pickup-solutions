"""North Dakota 50-market California-model intake and release safeguards."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class NorthDakotaGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mp=ROOT/"data/ttg-state-batches/ND.json"
  cls.batch=json.loads(cls.mp.read_text());cls.pages=cls.batch["pages"]
 def test_city_matrix(self):
  self.assertEqual(check_manifest(self.mp),[])
  self.assertEqual(len(self.pages),251)
  cities={}
  for path in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-nd-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
   if m:cities.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(cities),50)
  for kinds in cities.values():self.assertEqual(kinds,CATS)
 def test_page_forms_images_and_no_local_claims(self):
  photos=set()
  for path in self.pages:
   html=(ROOT/path).read_text()
   p=Page();p.feed(html)
   self.assertEqual(p.h1,1,path)
   self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path)
   self.assertEqual(p.state_options,["","ND"],path)
   for frag in ('Free Reliable Appliance Pickup','noindex, follow','name="source_page"','name="paid_option"','name="privacy_acknowledgment"','name="photos_available"'):
    self.assertIn(frag,html,path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    photos.add(re.search(r'<figure><img src="([^"]+)"',html).group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',html,path)
    self.assertIn('name="connection_status"',html,path)
  self.assertEqual(len(photos),50)
 def test_state_hub_and_release(self):
  hub=(ROOT/"north-dakota-appliance-pickup/index.html").read_text()
  self.assertIn("Free Appliance Pickup in North Dakota",hub)
  for p in self.pages:
   if p.endswith("-nd-appliance-pickup/index.html"):
    self.assertIn('href="/'+p.removesuffix("index.html")+'"',hub)
  sitemap=(ROOT/"sitemap.xml").read_text()
  self.assertNotIn("https://freereliableappliancepickup.com/north-dakota-appliance-pickup/",sitemap)
  ledger=json.loads((ROOT/"data/ttg-release-readiness/ND.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"])
  self.assertFalse(ledger["form_receipt"]["verified"])
  self.assertFalse(ledger["owner_release_approval"]["approved"])
  self.assertEqual(ledger["verified_cities"],[])
if __name__=="__main__":unittest.main()
