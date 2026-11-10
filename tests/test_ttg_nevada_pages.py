"""Nevada TTG Gold: 50 communities x five pickup request types."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class NevadaGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/NV.json";cls.m=json.loads(cls.manifest.read_text());cls.pages=cls.m["pages"]
 def test_full_matrix(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.pages),250)
  cities={}
  for path in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-nv-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
   self.assertIsNotNone(m,path);cities.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(cities),50)
  for kinds in cities.values():self.assertEqual(kinds,CATS)
 def test_photo_form_and_brand(self):
  laundry=set()
  for path in self.pages:
   html=(ROOT/path).read_text();p=Page();p.feed(html)
   self.assertEqual(p.h1,1,path);self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path);self.assertEqual(p.state_options,["","NV"],path)
   for v in ("Free Reliable Appliance Pickup","noindex, follow",'name="source_page"','name="phone"','name="photos_available"','name="paid_option"','name="privacy_acknowledgment"',"https://formspree.io/f/mvzeapzd"):
    self.assertIn(v,html,path)
   self.assertNotIn("pickup eligibility",html.lower(),path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    img=re.search(r'<figure><img src="([^"]+)"',html);self.assertIsNotNone(img,path);laundry.add(img.group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',html,path);self.assertIn('name="connection_status"',html,path)
  self.assertEqual(len(laundry),50)
 def test_no_activation(self):
  self.assertEqual(self.m["existing_indexed_state_hub_preserved"],"nevada-appliance-pickup/index.html")
  self.assertNotIn("nevada-appliance-pickup/index.html",self.pages)
  self.assertIn("Nevada Free Appliance",(ROOT/"nevada-appliance-pickup/index.html").read_text())
  sitemap=(ROOT/"sitemap.xml").read_text()
  for path in self.pages:self.assertNotIn("https://freereliableappliancepickup.com/"+path.replace("index.html",""),sitemap)
  ready=json.loads((ROOT/"data/ttg-release-readiness/NV.json").read_text());self.assertEqual(ready["verified_cities"],[])
  self.assertFalse(ready["form_receipt"]["verified"]);self.assertFalse(ready["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
