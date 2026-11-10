"""TTG Maine Gold: 50 municipalities x 5 pickup types plus state hub."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class MaineGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/ME.json"
  cls.batch=json.loads(cls.manifest.read_text());cls.pages=cls.batch["pages"]
 def test_matrix_and_asset_validation(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.pages),251)
  groups={}
  for path in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-me-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
   if m:groups.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(groups),50)
  for kinds in groups.values():self.assertEqual(kinds,CATS)
 def test_forms_photos_company_and_safety(self):
  laundry=set()
  for path in self.pages:
   html=(ROOT/path).read_text();p=Page();p.feed(html)
   self.assertEqual(p.h1,1,path)
   self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path)
   self.assertEqual(p.state_options,["","ME"],path)
   for s in ('Free Reliable Appliance Pickup','noindex, follow','name="source_page"','name="paid_option"','name="privacy_acknowledgment"','name="photos_available"'):
    self.assertIn(s,html,path)
   self.assertNotIn("New Hampshire",html,path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    laundry.add(re.search(r'<figure><img src="([^"]+)"',html).group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',html,path)
    self.assertIn('name="connection_status"',html,path)
  self.assertEqual(len(laundry),50)
 def test_navigation_and_release_guard(self):
  hub=(ROOT/"maine-appliance-pickup/index.html").read_text()
  self.assertIn("Free Appliance Pickup in Maine",hub)
  for path in self.pages:
   if path.endswith("-me-appliance-pickup/index.html"):
    self.assertIn('href="/'+path.removesuffix("index.html")+'"',hub)
  self.assertNotIn("https://freereliableappliancepickup.com/maine-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
  ledger=json.loads((ROOT/"data/ttg-release-readiness/ME.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"])
  self.assertEqual(ledger["verified_cities"],[])
  self.assertFalse(ledger["form_receipt"]["verified"])
  self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
