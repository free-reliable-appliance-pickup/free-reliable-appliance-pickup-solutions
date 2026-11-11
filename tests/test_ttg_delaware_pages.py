"""Delaware all-57 incorporated-municipality Gold staging: offline integrity check."""
import json,re,unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest
CATS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class DelawareGoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=ROOT/"data/ttg-state-batches/DE.json"
  cls.batch=json.loads(cls.manifest.read_text())
  cls.pages=cls.batch["pages"]
 def test_57_by_five(self):
  self.assertEqual(check_manifest(self.manifest),[])
  self.assertEqual(len(self.pages),286)
  grouped={}
  for path in self.pages:
   m=re.fullmatch(r"([a-z0-9-]+)-de-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
   if m:grouped.setdefault(m.group(1),set()).add(m.group(2))
  self.assertEqual(len(grouped),57)
  for cats in grouped.values():self.assertEqual(cats,CATS)
 def test_forms_images_and_guidance(self):
  seen=set()
  for path in self.pages:
   raw=(ROOT/path).read_text(encoding="utf-8")
   p=Page();p.feed(raw)
   self.assertEqual(p.h1,1,path)
   self.assertEqual(len(p.forms),1,path)
   self.assertEqual(len(p.images),2,path)
   self.assertEqual(p.state_options,["","DE"],path)
   self.assertIn("Free Reliable Appliance Pickup",raw,path)
   self.assertIn("noindex, follow",raw,path)
   self.assertIn('name="privacy_acknowledgment"',raw,path)
   self.assertIn("dnrec.delaware.gov/waste-hazardous/management/hazardous/household/",raw,path)
   self.assertNotIn("Rhode Island",raw,path)
   if path.endswith("-washer-dryer-pickup/index.html"):
    img=re.search(r'<figure><img src="([^"]+)"',raw)
    self.assertIsNotNone(img,path)
    seen.add(img.group(1))
   if path.endswith("-stove-oven-pickup/index.html"):
    self.assertIn('name="fuel_type"',raw,path)
    self.assertIn('name="connection_status"',raw,path)
  self.assertEqual(len(seen),57)
 def test_hub_and_release(self):
  hub=(ROOT/"delaware-appliance-pickup/index.html").read_text()
  self.assertIn("Free Appliance Pickup in Delaware",hub)
  for path in self.pages:
   if path.endswith("-de-appliance-pickup/index.html"):
    self.assertIn('href="/'+path.removesuffix("index.html")+'"',hub)
  self.assertNotIn("https://freereliableappliancepickup.com/delaware-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
  ledger=json.loads((ROOT/"data/ttg-release-readiness/DE.json").read_text())
  self.assertFalse(self.batch["operator_coverage_verified"])
  self.assertFalse(ledger["form_receipt"]["verified"])
  self.assertFalse(ledger["owner_release_approval"]["approved"])

 def test_statewide_city_not_prefilled_and_zip_required(self):
  """Prevent the statewide form from silently supplying Delaware as a customer city."""
  html=(ROOT/"delaware-appliance-pickup/index.html").read_text(encoding="utf-8")
  form=html.split("<form",1)[1].split("</form>",1)[0]
  field=re.search(r'<input\b[^>]*\bname="city"[^>]*>',form)
  self.assertIsNotNone(field)
  self.assertIn('required',field.group())
  self.assertIn('placeholder="Enter actual pickup city or town"',field.group())
  self.assertNotIn('value="Delaware"',field.group())
  self.assertIn('name="state"',form)
  self.assertIn('value="DE"',form)
  self.assertIn('name="zip"',form)
  self.assertIn('name="address"',form)
 def test_statewide_free_pickup_copy_and_noindex(self):
  """Preserve the California-model headline and request-only Delaware status."""
  html=(ROOT/"delaware-appliance-pickup/index.html").read_text(encoding="utf-8")
  self.assertIn("<h2>Request Free Appliance Pickup in Delaware</h2>",html)
  self.assertNotIn("in Delaware in Delaware",html)
  self.assertIn("DE Free Appliance Pickup request",html)
  self.assertIn("Request Free Appliance Pickup</button>",html)
  self.assertIn('<meta name="robots" content="noindex, follow">',html)
  self.assertEqual(html.count("<form"),1)

 def test_statewide_intake_collects_required_customer_details(self):
  """Keep the customer-facing Delaware form usable before territories are activated."""
  html=(ROOT/"delaware-appliance-pickup/index.html").read_text(encoding="utf-8")
  form=html.split("<form",1)[1].split("</form>",1)[0]
  for name in ("name","phone","address","city","state","zip",
               "appliance","condition","floor","stairs","photos_available",
               "access","message","privacy_acknowledgment"):
   control=re.search(r'<(?:input|select|textarea)\b[^>]*\bname="'+name+r'"[^>]*>',form)
   self.assertIsNotNone(control,name)
   self.assertIn("required",control.group(),name)
  self.assertIn('name="photo_link"',form)
  self.assertIn('name="source_page" value="delaware-appliance-pickup"',form)
  self.assertIn('action="https://formspree.io/f/mvzeapzd"',html)
if __name__=="__main__":unittest.main()
