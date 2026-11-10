"""Montana Gold: 50 city/community markets x five categories and statewide hub."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class MontanaGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/MT.json"
  cls.batch=json.loads(cls.manifest.read_text());cls.pages=cls.batch["pages"]
 def test_50_market_category_matrix_and_existing_images(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.pages),251)
  names={}
  for path in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-mt-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
   if m:names.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(names),50)
  for kinds in names.values():self.assertEqual(kinds,CATS)
 def test_safe_forms_photos_brand_and_stoves(self):
  laundry=set()
  for path in self.pages:
   html=(ROOT/path).read_text();page=Page();page.feed(html)
   self.assertEqual(page.h1,1,path)
   self.assertEqual(len(page.forms),1,path)
   self.assertEqual(len(page.images),2,path)
   self.assertEqual(page.state_options,["","MT"],path)
   for value in ('Free Reliable Appliance Pickup','noindex, follow','name="source_page"','name="paid_option"','name="privacy_acknowledgment"','name="photos_available"'):
    self.assertIn(value,html,path)
   self.assertNotIn("Connecticut",html,path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    laundry.add(re.search(r'<figure><img src="([^"]+)"',html).group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',html,path)
    self.assertIn('name="connection_status"',html,path)
  self.assertEqual(len(laundry),50)
 def test_hub_and_release_gates(self):
  hub=(ROOT/"montana-appliance-pickup/index.html").read_text()
  self.assertIn("Free Appliance Pickup in Montana",hub)
  for path in self.pages:
   if path.endswith("-mt-appliance-pickup/index.html"):
    self.assertIn('href="/'+path.removesuffix("index.html")+'"',hub)
  self.assertNotIn("https://freereliableappliancepickup.com/montana-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
  ledger=json.loads((ROOT/"data/ttg-release-readiness/MT.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"])
  self.assertEqual(ledger["verified_cities"],[])
  self.assertFalse(ledger["form_receipt"]["verified"])
  self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
