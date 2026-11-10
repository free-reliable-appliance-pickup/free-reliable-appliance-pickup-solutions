"""WV TTG Gold: 50 towns, five categories, 251 pages."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class WestVirginiaGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/WV.json"
  cls.batch=json.loads(cls.manifest.read_text());cls.pages=cls.batch["pages"]
 def test_matrix_and_assets(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.pages),251)
  cities={}
  for path in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-wv-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
   if m:cities.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(cities),50)
  for kinds in cities.values():self.assertEqual(kinds,CATS)
 def test_forms_photos_and_stove_safety(self):
  laundry=set()
  for path in self.pages:
   html=(ROOT/path).read_text();p=Page();p.feed(html)
   self.assertEqual(p.h1,1,path);self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path);self.assertEqual(p.state_options,["","WV"],path)
   for s in ('Free Reliable Appliance Pickup','noindex, follow','name="source_page"','name="paid_option"','name="privacy_acknowledgment"','name="photos_available"'):
    self.assertIn(s,html,path)
   self.assertNotIn("New Hampshire",html,path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    laundry.add(re.search(r'<figure><img src="([^"]+)"',html).group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',html,path);self.assertIn('name="connection_status"',html,path)
  self.assertEqual(len(laundry),50)
 def test_state_hub_and_readiness(self):
  hub=(ROOT/"west-virginia-appliance-pickup/index.html").read_text()
  self.assertIn("Free Appliance Pickup in West Virginia",hub)
  for path in self.pages:
   if path.endswith("-wv-appliance-pickup/index.html"):
    self.assertIn('href="/'+path.removesuffix("index.html")+'"',hub)
  self.assertNotIn("https://freereliableappliancepickup.com/west-virginia-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
  ready=json.loads((ROOT/"data/ttg-release-readiness/WV.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"])
  self.assertEqual(ready["verified_cities"],[])
  self.assertFalse(ready["form_receipt"]["verified"])
  self.assertFalse(ready["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
