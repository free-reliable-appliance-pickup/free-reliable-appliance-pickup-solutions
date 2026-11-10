"""South Dakota TTG Gold: 50 cities, five category pages each, state hub."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class SouthDakotaGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/SD.json"
  cls.batch=json.loads(cls.manifest.read_text());cls.pages=cls.batch["pages"]
 def test_matrix_and_images(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.pages),251)
  found={}
  for path in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-sd-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
   if m:found.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(found),50)
  for types in found.values():self.assertEqual(types,CATS)
 def test_forms_photos_brand_and_safety(self):
  laundry=set()
  for path in self.pages:
   html=(ROOT/path).read_text();p=Page();p.feed(html)
   self.assertEqual(p.h1,1,path)
   self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path)
   self.assertEqual(p.state_options,["","SD"],path)
   for x in ('Free Reliable Appliance Pickup','noindex, follow','name="source_page"','name="paid_option"','name="privacy_acknowledgment"','name="photos_available"'):
    self.assertIn(x,html,path)
   self.assertNotIn("New Hampshire",html,path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    laundry.add(re.search(r'<figure><img src="([^"]+)"',html).group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',html,path)
    self.assertIn('name="connection_status"',html,path)
  self.assertEqual(len(laundry),50)
 def test_internal_links_and_release_gates(self):
  hub=(ROOT/"south-dakota-appliance-pickup/index.html").read_text()
  self.assertIn("Free Appliance Pickup in South Dakota",hub)
  for path in self.pages:
   if path.endswith("-sd-appliance-pickup/index.html"):
    self.assertIn('href="/'+path.removesuffix("index.html")+'"',hub)
  self.assertNotIn("https://freereliableappliancepickup.com/south-dakota-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
  ledger=json.loads((ROOT/"data/ttg-release-readiness/SD.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"])
  self.assertEqual(ledger["verified_cities"],[])
  self.assertFalse(ledger["form_receipt"]["verified"])
  self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
