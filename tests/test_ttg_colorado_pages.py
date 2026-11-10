"""Colorado TTG Gold: 70 communities × 5 pickup categories, only missing pages."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
class ColoradoGold(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/CO.json";cls.m=json.loads(cls.manifest.read_text());cls.pages=cls.m["pages"]
 def test_gapfill_and_preserve_existing(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.m["communities"]),70)
  self.assertEqual(len(self.pages)+len(self.m["preserved_existing_category_paths"]),350)
  self.assertFalse(set(self.pages)&set(self.m["preserved_existing_category_paths"]))
  self.assertIn("denver-appliance-pickup/index.html",self.m["preserved_existing_category_paths"])
  self.assertIn("aurora-appliance-pickup/index.html",self.m["preserved_existing_category_paths"])
  self.assertIn("montrose-co-appliance-pickup/index.html",self.pages)
  for path in self.m["preserved_existing_category_paths"]:self.assertTrue((ROOT/path).is_file(),path)
 def test_branded_intake_and_unique_original_laundry(self):
  photos=set()
  for path in self.pages:
   h=(ROOT/path).read_text();p=Page();p.feed(h)
   self.assertEqual(p.h1,1,path);self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path);self.assertEqual(p.state_options,["","CO"],path)
   for s in ("Free Reliable Appliance Pickup","noindex, follow",'name="source_page"','name="phone"','name="photos_available"','name="paid_option"','name="privacy_acknowledgment"','name="_subject" value="CO ','https://formspree.io/f/mvzeapzd'):self.assertIn(s,h,path)
   self.assertNotIn("pickup eligibility",h.lower(),path)
   self.assertNotIn("New Mexico",h,path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    photo=re.search(r'<figure><img src="([^"]+)"',h);self.assertIsNotNone(photo,path);photos.add(photo.group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',h,path);self.assertIn('name="connection_status"',h,path)
  self.assertEqual(len(photos),len([x for x in self.pages if x.endswith("-washer-dryer-pickup/index.html")]))
 def test_staging_guards(self):
  self.assertIn("Free Appliance Pickup",(ROOT/"colorado-appliance-pickup/index.html").read_text())
  sitemap=(ROOT/"sitemap.xml").read_text()
  for path in self.pages:self.assertNotIn("https://freereliableappliancepickup.com/"+path.replace("index.html",""),sitemap)
  l=json.loads((ROOT/"data/ttg-release-readiness/CO.json").read_text())
  self.assertEqual(l["verified_cities"],[]);self.assertFalse(l["form_receipt"]["verified"]);self.assertFalse(l["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
