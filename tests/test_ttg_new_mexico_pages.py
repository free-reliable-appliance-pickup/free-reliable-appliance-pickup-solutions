"""New Mexico TTG Gold: 50 authentic communities × 5 free pickup requests."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class NewMexicoGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/NM.json";cls.m=json.loads(cls.manifest.read_text());cls.pages=cls.m["pages"]
 def test_complete_matrix(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.pages),250)
  communities={}
  for path in self.pages:
   match=re.fullmatch(r"([a-z0-9-]+)-nm-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
   self.assertIsNotNone(match,path);communities.setdefault(match.group(1),set()).add(match.group(2))
  self.assertEqual(len(communities),50)
  for kinds in communities.values():self.assertEqual(kinds,CATS)
 def test_intake_and_state_routing(self):
  laundry=set()
  for path in self.pages:
   html=(ROOT/path).read_text();p=Page();p.feed(html)
   self.assertEqual(p.h1,1,path);self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path);self.assertEqual(p.state_options,["","NM"],path)
   for v in ('Free Reliable Appliance Pickup','noindex, follow','name="source_page"','name="phone"','name="address"','name="zip"','name="photos_available"','name="paid_option"','name="privacy_acknowledgment"','name="_subject" value="NM ','https://formspree.io/f/mvzeapzd'):
    self.assertIn(v,html,path)
   self.assertNotIn("pickup eligibility",html.lower(),path)
   self.assertNotIn("Las Vegas",html,path);self.assertNotIn("Nevada",html,path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    photo=re.search(r'<figure><img src="([^"]+)"',html);self.assertIsNotNone(photo,path);laundry.add(photo.group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',html,path);self.assertIn('name="connection_status"',html,path)
  self.assertEqual(len(laundry),50)
 def test_release_guard(self):
  self.assertEqual(self.m["existing_indexed_state_hub_preserved"],"new-mexico-appliance-pickup/index.html")
  self.assertNotIn("new-mexico-appliance-pickup/index.html",self.pages)
  self.assertIn("New Mexico Free Appliance",(ROOT/"new-mexico-appliance-pickup/index.html").read_text())
  sitemap=(ROOT/"sitemap.xml").read_text()
  for path in self.pages:self.assertNotIn("https://freereliableappliancepickup.com/"+path.replace("index.html",""),sitemap)
  ledger=json.loads((ROOT/"data/ttg-release-readiness/NM.json").read_text())
  self.assertEqual(ledger["verified_cities"],[]);self.assertFalse(ledger["form_receipt"]["verified"]);self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
