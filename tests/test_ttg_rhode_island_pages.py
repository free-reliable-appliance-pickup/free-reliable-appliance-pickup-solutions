"""Rhode Island 39-municipality California-Gold request-only rollout."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest

CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class RhodeIslandGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mp=ROOT/"data/ttg-state-batches/RI.json"
  cls.batch=json.loads(cls.mp.read_text());cls.pages=cls.batch["pages"]

 def test_all_39_towns_and_five_categories(self):
  self.assertEqual(check_manifest(self.mp),[])
  self.assertEqual(len(self.pages),196)
  city={}
  for path in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-ri-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
   if m: city.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(city),39)
  for kinds in city.values(): self.assertEqual(kinds,CATS)
  self.assertIn("new-shoreham",city)

 def test_branding_images_forms_and_safety(self):
  laundry=set()
  for path in self.pages:
   html=(ROOT/path).read_text()
   page=Page(); page.feed(html)
   self.assertEqual(page.h1,1,path)
   self.assertEqual(len(page.forms),1,path)
   self.assertEqual(len(page.images),2,path)
   self.assertEqual(page.state_options,["","RI"],path)
   for fragment in ('Free Reliable Appliance Pickup','noindex, follow','name="source_page"',
       'name="paid_option"','name="privacy_acknowledgment"','name="photos_available"'):
    self.assertIn(fragment,html,path)
   self.assertNotIn("Connecticut",html,path)
   self.assertNotIn("MassDEP",html,path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    laundry.add(re.search(r'<figure><img src="([^"]+)"',html).group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',html,path)
    self.assertIn('name="connection_status"',html,path)
  self.assertEqual(len(laundry),39)

 def test_hub_and_release_gate(self):
  hub=(ROOT/"rhode-island-appliance-pickup/index.html").read_text()
  self.assertIn("Free Appliance Pickup in Rhode Island",hub)
  for path in self.pages:
   if path.endswith("-ri-appliance-pickup/index.html"):
    self.assertIn('href="/'+path.removesuffix("index.html")+'"',hub)
  sitemap=(ROOT/"sitemap.xml").read_text()
  self.assertNotIn("https://freereliableappliancepickup.com/rhode-island-appliance-pickup/",sitemap)
  self.assertNotIn("-ri-appliance-pickup/",sitemap)
  ledger=json.loads((ROOT/"data/ttg-release-readiness/RI.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"])
  self.assertEqual(ledger["verified_cities"],[])
  self.assertFalse(ledger["form_receipt"]["verified"])
  self.assertFalse(ledger["owner_release_approval"]["approved"])

if __name__=="__main__": unittest.main()
