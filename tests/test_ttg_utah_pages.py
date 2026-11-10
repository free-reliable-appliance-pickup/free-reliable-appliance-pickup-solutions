"""Utah TTG Gold: 83 municipalities in 16 county groups, five pickup types each."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class UtahGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/UT.json"
  cls.m=json.loads(cls.manifest.read_text());cls.pages=cls.m["pages"]
 def test_complete_matrix(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.pages),415)
  cities={}
  for path in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-ut-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
   self.assertIsNotNone(m,path);cities.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(cities),83)
  for kinds in cities.values():self.assertEqual(kinds,CATS)
 def test_forms_photos_brand_and_safe_state(self):
  laundry=set()
  for path in self.pages:
   html=(ROOT/path).read_text();p=Page();p.feed(html)
   self.assertEqual(p.h1,1,path);self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path);self.assertEqual(p.state_options,["","UT"],path)
   for x in ('Free Reliable Appliance Pickup','noindex, follow','name="source_page"','name="paid_option"','name="privacy_acknowledgment"','name="photos_available"','https://formspree.io/f/mvzeapzd'):
    self.assertIn(x,html,path)
   self.assertNotIn("New Hampshire",html,path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    m=re.search(r'<figure><img src="([^"]+)"',html);self.assertIsNotNone(m,path)
    laundry.add(m.group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',html,path);self.assertIn('name="connection_status"',html,path)
  self.assertEqual(len(laundry),83)
 def test_existing_hub_and_activation_guards(self):
  self.assertEqual(self.m["existing_indexed_state_hub_preserved"],"utah-appliance-pickup/index.html")
  self.assertNotIn("utah-appliance-pickup/index.html",self.pages)
  hub=(ROOT/"utah-appliance-pickup/index.html").read_text()
  self.assertIn("Utah Free Appliance",hub)
  sitemap=(ROOT/"sitemap.xml").read_text()
  for path in self.pages:self.assertNotIn("https://freereliableappliancepickup.com/"+path.replace("index.html",""),sitemap)
  ledger=json.loads((ROOT/"data/ttg-release-readiness/UT.json").read_text())
  self.assertFalse(self.m["operator_coverage_verified"]);self.assertEqual(ledger["verified_cities"],[])
  self.assertFalse(ledger["form_receipt"]["verified"]);self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
