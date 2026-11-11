"""Arizona TTG Gold: only missing local pages; preserve known organic routes."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
class ArizonaGold(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/AZ.json";cls.m=json.loads(cls.manifest.read_text());cls.pages=cls.m["pages"]
 def test_matrix_and_preservation(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.m["communities"]),70)
  self.assertEqual(len(self.pages)+len(self.m["preserved_existing_category_paths"]),350)
  self.assertFalse(set(self.pages)&set(self.m["preserved_existing_category_paths"]))
  for path in self.m["preserved_existing_category_paths"]:self.assertTrue((ROOT/path).is_file(),path)
  self.assertIn("phoenix-appliance-pickup/index.html",self.m["preserved_existing_category_paths"])
  self.assertIn("phoenix-washer-dryer-pickup/index.html",self.m["preserved_existing_category_paths"])
  self.assertIn("glendale-az-appliance-pickup/index.html",self.m["preserved_existing_category_paths"])
  self.assertIn("el-mirage-az-appliance-pickup/index.html",self.m["preserved_existing_category_paths"])
 def test_safe_forms_and_photos(self):
  seen=set()
  for path in self.pages:
   html=(ROOT/path).read_text();p=Page();p.feed(html)
   self.assertEqual(p.h1,1,path);self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path);self.assertEqual(p.state_options,["","AZ"],path)
   for q in ("Free Reliable Appliance Pickup","noindex, follow",'name="source_page"','name="phone"','name="photos_available"','name="paid_option"','name="privacy_acknowledgment"','name="_subject" value="AZ ','https://formspree.io/f/mvzeapzd'):
    self.assertIn(q,html,path)
   self.assertNotIn("pickup eligibility",html.lower(),path)
   self.assertNotIn("New Mexico",html,path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    photo=re.search(r'<figure><img src="([^"]+)"',html);self.assertIsNotNone(photo,path);seen.add(photo.group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',html,path);self.assertIn('name="connection_status"',html,path)
  self.assertEqual(len(seen),len([p for p in self.pages if p.endswith("-washer-dryer-pickup/index.html")]))
 def test_indexing_release_guard(self):
  self.assertIn("Arizona Free Appliance Pickup",(ROOT/"arizona-appliance-pickup/index.html").read_text())
  sitemap=(ROOT/"sitemap.xml").read_text()
  for path in self.pages:self.assertNotIn("https://freereliableappliancepickup.com/"+path.replace("index.html",""),sitemap)
  l=json.loads((ROOT/"data/ttg-release-readiness/AZ.json").read_text());self.assertEqual(l["verified_cities"],[])
  self.assertFalse(l["form_receipt"]["verified"]);self.assertFalse(l["owner_release_approval"]["approved"])
 def test_state_hub_customer_intake_first(self):
  h=(ROOT/"arizona-appliance-pickup/index.html").read_text()
  self.assertIn("Arizona Free Appliance Pickup",h)
  self.assertIn('Free Reliable Appliance Pickup',h)
  self.assertEqual(h.index('<section id="request"'),h.index('<main>')+len('<main>\n'))
  for text in ('name="photos_available" required','name="access" required','name="message" required','name="privacy_acknowledgment" value="acknowledged" required','name="paid_option"'):
   self.assertIn(text,h)
  self.assertIn('action="https://formspree.io/f/mvzeapzd"',h)
  self.assertIn('content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"',h)
if __name__=="__main__":unittest.main()
