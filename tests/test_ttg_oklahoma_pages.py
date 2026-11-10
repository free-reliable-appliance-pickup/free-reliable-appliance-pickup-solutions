"""Oklahoma 50 city / 251 page California-style request-only rollout guards."""
from pathlib import Path
import hashlib
import json
import re
import unittest
from html import unescape
from scripts.ttg_state_batch_qa import ROOT, Page, check_manifest

KINDS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class OklahomaGoldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads((ROOT/"data/ttg-state-batches/OK.json").read_text(encoding="utf-8"))
        cls.pages=cls.manifest["pages"]

    def test_50_unique_cities_five_types_and_hub(self):
        self.assertEqual(len(self.pages),251)
        self.assertEqual(len(self.pages),len(set(self.pages)))
        bycity={}
        for page in self.pages:
            m=re.fullmatch(r"([a-z0-9-]+)-ok-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",page)
            if m:bycity.setdefault(m.group(1),set()).add(m.group(2))
        self.assertEqual(len(bycity),50)
        for name,kinds in bycity.items():self.assertEqual(kinds,KINDS,name)
        self.assertIn("oklahoma-appliance-pickup/index.html",self.pages)

    def test_every_form_image_canonical_and_noindex(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/OK.json"),[])
        for page in self.pages:
            with self.subTest(page=page):
                h=(ROOT/page).read_text(encoding="utf-8")
                parsed=Page();parsed.feed(h)
                title=unescape(re.search(r"<title>(.*?)</title>",h).group(1))
                heading=unescape(re.search(r"<h1[^>]*>(.*?)</h1>",h).group(1))
                self.assertIn("Free Reliable Appliance Pickup",title)
                self.assertTrue(heading.startswith("Free ") and " Pickup in " in heading)
                self.assertNotIn("eligibilit",heading.lower())
                self.assertEqual(len(parsed.forms),1)
                self.assertEqual(parsed.state_options,["","OK"])
                self.assertIn('name="privacy_acknowledgment"',h)
                self.assertIn('name="paid_option"',h)
                self.assertEqual(len(parsed.images),2)
                self.assertIn('noindex, follow',h)
                self.assertIn("not a completed",h.lower())
                self.assertIn("Request Free ",h)

    def test_50_laundry_images_are_different_files(self):
        sigs=[]
        for page in self.pages:
            if not page.endswith("-washer-dryer-pickup/index.html"):continue
            h=(ROOT/page).read_text(encoding="utf-8")
            src=re.search(r'<figure><img src="([^"]+)"',h).group(1)
            sigs.append(hashlib.sha256((ROOT/src.lstrip("/")).read_bytes()).hexdigest())
        self.assertEqual(len(sigs),50)
        self.assertEqual(len(set(sigs)),50)

    def test_stoves_require_fuel_and_professional_disconnection(self):
        count=0
        for page in self.pages:
            if not page.endswith("-stove-oven-pickup/index.html"):continue
            count+=1
            h=(ROOT/page).read_text(encoding="utf-8")
            self.assertIn('name="fuel_type" required',h,page)
            self.assertIn('name="connection_status" required',h,page)
            self.assertIn("qualified professional",h.lower(),page)
            self.assertIn("Do not loosen a gas connection",h,page)
        self.assertEqual(count,50)

    def test_links_approval_and_public_options(self):
        hub=(ROOT/"oklahoma-appliance-pickup/index.html").read_text(encoding="utf-8")
        for page in self.pages:
            if page.endswith("-ok-appliance-pickup/index.html"):
                self.assertIn('href="/'+page.removesuffix("index.html")+'"',hub)
        self.assertIn("Free pickup is not guaranteed.",hub)
        self.assertIn("confirmed local pickup option",hub)
        self.assertIn("https://www.okc.gov/Services/Water-Trash-Recycling/Bulky-Waste",hub)
        self.assertIn("https://www.cityoftulsa.org/bulkywaste",hub)
        self.assertNotIn("https://freereliableappliancepickup.com/oklahoma-appliance-pickup/",(ROOT/"sitemap.xml").read_text(encoding="utf-8"))
        ledger=json.loads((ROOT/"data/ttg-release-readiness/OK.json").read_text(encoding="utf-8"))
        self.assertFalse(self.manifest["operator_coverage_verified"])
        self.assertEqual(ledger["verified_cities"],[])
        self.assertFalse(ledger["form_receipt"]["verified"])
        self.assertFalse(ledger["owner_release_approval"]["approved"])

if __name__=="__main__":unittest.main()
