"""NY TTG Gold: 60 places × five Free Appliance Pickup categories."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class NewYorkGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/NY.json";cls.m=json.loads(cls.manifest.read_text());cls.pages=cls.m["pages"]
 def test_complete_city_category_matrix(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.pages),300)
  allcities={}
  for path in self.pages:
   match=re.fullmatch(r"([a-z0-9-]+)-ny-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
   self.assertIsNotNone(match,path);allcities.setdefault(match.group(1),set()).add(match.group(2))
  self.assertEqual(len(allcities),60)
  for kinds in allcities.values():self.assertEqual(kinds,CATS)
 def test_genuine_images_and_safe_form(self):
  photos=set()
  for path in self.pages:
   html=(ROOT/path).read_text();p=Page();p.feed(html)
   self.assertEqual(p.h1,1,path);self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path);self.assertEqual(p.state_options,["","NY"],path)
   for x in ('Free Reliable Appliance Pickup','noindex, follow','name="source_page"','name="phone"','name="address"','name="zip"','name="photos_available"','name="paid_option"','name="privacy_acknowledgment"','name="_subject" value="NY ','https://formspree.io/f/mvzeapzd'):
    self.assertIn(x,html,path)
   self.assertNotIn("pickup eligibility",html.lower(),path)
   self.assertNotIn("Albuquerque",html,path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    image=re.search(r'<figure><img src="([^"]+)"',html);self.assertIsNotNone(image,path);photos.add(image.group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',html,path);self.assertIn('name="connection_status"',html,path)
  self.assertEqual(len(photos),60)
 def test_live_hub_and_noindex_hold(self):
  self.assertEqual(self.m["existing_indexed_state_hub_preserved"],"new-york-appliance-pickup/index.html")
  self.assertNotIn("new-york-appliance-pickup/index.html",self.pages)
  self.assertIn("New York Free Appliance Pickup",(ROOT/"new-york-appliance-pickup/index.html").read_text())
  sitemap=(ROOT/"sitemap.xml").read_text()
  for path in self.pages:self.assertNotIn("https://freereliableappliancepickup.com/"+path.replace("index.html",""),sitemap)
  ledger=json.loads((ROOT/"data/ttg-release-readiness/NY.json").read_text());self.assertEqual(ledger["verified_cities"],[])
  self.assertFalse(ledger["form_receipt"]["verified"]);self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
