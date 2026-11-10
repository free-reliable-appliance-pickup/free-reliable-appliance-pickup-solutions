"""Florida TTG gapfill: 64 existing communities preserved plus 30 new x5."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
class FloridaGold(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/FL.json";cls.m=json.loads(cls.manifest.read_text());cls.pages=cls.m["pages"]
 def test_preserve_64_existing_and_complete_30_new(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.pages),150)
  self.assertEqual(len(self.m["preserved_existing_category_paths"]),320)
  self.assertEqual(len(self.m["communities"]),94)
  self.assertEqual(len(self.pages)+len(self.m["preserved_existing_category_paths"]),470)
  self.assertFalse(set(self.pages)&set(self.m["preserved_existing_category_paths"]))
  self.assertIn("miami-fl-appliance-pickup/index.html",self.m["preserved_existing_category_paths"])
  self.assertIn("tampa-fl-appliance-pickup/index.html",self.m["preserved_existing_category_paths"])
  for path in self.m["preserved_existing_category_paths"]:self.assertTrue((ROOT/path).is_file(),path)
 def test_form_photos_and_copy(self):
  photo=set()
  for path in self.pages:
   h=(ROOT/path).read_text();p=Page();p.feed(h)
   self.assertEqual(p.h1,1,path);self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path);self.assertEqual(p.state_options,["","FL"],path)
   for q in ("Free Reliable Appliance Pickup","noindex, follow",'name="source_page"','name="phone"','name="photos_available"','name="paid_option"','name="privacy_acknowledgment"','name="_subject" value="FL ','https://formspree.io/f/mvzeapzd'):self.assertIn(q,h,path)
   self.assertNotIn("pickup eligibility",h.lower(),path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    m=re.search(r'<figure><img src="([^"]+)"',h);self.assertIsNotNone(m,path);photo.add(m.group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',h,path);self.assertIn('name="connection_status"',h,path)
  self.assertEqual(len(photo),30)
 def test_release_safety(self):
  self.assertIn("Free Appliance Pickup",(ROOT/"florida-appliance-pickup/index.html").read_text())
  sitemap=(ROOT/"sitemap.xml").read_text()
  for p in self.pages:self.assertNotIn("https://freereliableappliancepickup.com/"+p.replace("index.html",""),sitemap)
  l=json.loads((ROOT/"data/ttg-release-readiness/FL.json").read_text())
  self.assertEqual(l["verified_cities"],[])
  self.assertFalse(l["form_receipt"]["verified"]);self.assertFalse(l["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
