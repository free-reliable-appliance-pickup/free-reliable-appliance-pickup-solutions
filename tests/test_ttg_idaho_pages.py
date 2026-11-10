"""TTG Idaho Gold: 63 municipalities across 24 counties, five categories, active state hub preserved."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class IdahoGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.path=ROOT/"data/ttg-state-batches/ID.json"
  cls.m=json.loads(cls.path.read_text());cls.pages=cls.m["pages"]
 def test_complete_matrix(self):
  self.assertEqual(check_manifest(self.path),[])
  self.assertEqual(len(self.pages),315)
  found={}
  for path in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-id-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
   self.assertIsNotNone(m,path)
   found.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(found),63)
  for v in found.values():self.assertEqual(v,CATS)
 def test_branding_forms_and_original_photos(self):
  laundry=set()
  for path in self.pages:
   html=(ROOT/path).read_text();p=Page();p.feed(html)
   self.assertEqual(p.h1,1,path);self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path);self.assertEqual(p.state_options,["","ID"],path)
   for text in ('Free Reliable Appliance Pickup','noindex, follow','name="source_page"','name="paid_option"','name="privacy_acknowledgment"','name="photos_available"','https://formspree.io/f/mvzeapzd'):
    self.assertIn(text,html,path)
   self.assertNotIn("New Hampshire",html,path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    match=re.search(r'<figure><img src="([^"]+)"',html);self.assertIsNotNone(match,path)
    laundry.add(match.group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',html,path);self.assertIn('name="connection_status"',html,path)
  self.assertEqual(len(laundry),63)
 def test_protect_live_hub_and_index_gates(self):
  self.assertEqual(self.m["existing_indexed_state_hub_preserved"],"idaho-appliance-pickup/index.html")
  self.assertNotIn("idaho-appliance-pickup/index.html",self.pages)
  hub=(ROOT/"idaho-appliance-pickup/index.html").read_text()
  self.assertIn("Idaho Free Appliance",hub)
  sitemap=(ROOT/"sitemap.xml").read_text()
  for path in self.pages:self.assertNotIn("https://freereliableappliancepickup.com/"+path.replace("index.html",""),sitemap)
  ledger=json.loads((ROOT/"data/ttg-release-readiness/ID.json").read_text())
  self.assertFalse(self.m["operator_coverage_verified"]);self.assertEqual(ledger["verified_cities"],[])
  self.assertFalse(ledger["form_receipt"]["verified"]);self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
