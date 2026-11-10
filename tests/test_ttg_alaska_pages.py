"""Alaska Gold: 50 communities x 5 pickup requests plus state hub."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
KINDS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class AlaskaGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/AK.json"
  cls.batch=json.loads(cls.manifest.read_text());cls.pages=cls.batch["pages"]
 def test_matrix_assets_and_release(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.pages),251)
  towns={}
  for path in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-ak-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
   if m:towns.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(towns),50)
  for kinds in towns.values():self.assertEqual(kinds,KINDS)
 def test_brand_forms_photos_and_safety(self):
  laundry=set()
  for path in self.pages:
   html=(ROOT/path).read_text();p=Page();p.feed(html)
   self.assertEqual(p.h1,1,path);self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path);self.assertEqual(p.state_options,["","AK"],path)
   for s in ('Free Reliable Appliance Pickup','noindex, follow','name="source_page"','name="paid_option"','name="privacy_acknowledgment"','name="photos_available"'):
    self.assertIn(s,html,path)
   self.assertNotIn("New Hampshire",html,path)
   self.assertIn("Alaska access:",html,path)
   if path.endswith("-washer-dryer-pickup/index.html"):laundry.add(re.search(r'<figure><img src="([^"]+)"',html).group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',html,path);self.assertIn('name="connection_status"',html,path)
  self.assertEqual(len(laundry),50)
 def test_hub_links_and_readiness(self):
  hub=(ROOT/"alaska-appliance-pickup/index.html").read_text()
  self.assertIn("Free Appliance Pickup in Alaska",hub)
  for path in self.pages:
   if path.endswith("-ak-appliance-pickup/index.html"):
    self.assertIn('href="/'+path.removesuffix("index.html")+'"',hub)
  self.assertNotIn("https://freereliableappliancepickup.com/alaska-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
  ledger=json.loads((ROOT/"data/ttg-release-readiness/AK.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"]);self.assertEqual(ledger["verified_cities"],[])
  self.assertFalse(ledger["form_receipt"]["verified"]);self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
