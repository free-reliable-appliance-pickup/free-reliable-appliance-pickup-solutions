"""Alabama 50 cities / 251 Free Appliance Pickup request pages release guards."""
from pathlib import Path
import hashlib
import json
import re
import unittest
from html import unescape
from scripts.ttg_state_batch_qa import ROOT, Page, check_manifest

KINDS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class AlabamaGoldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batch=json.loads((ROOT/"data/ttg-state-batches/AL.json").read_text(encoding="utf-8"))
        cls.pages=cls.batch["pages"]
    def test_50_cities_and_all_five_intents(self):
        self.assertEqual(len(self.pages),251)
        self.assertEqual(len(self.pages),len(set(self.pages)))
        cities={}
        for p in self.pages:
            m=re.fullmatch(r"([a-z0-9-]+)-al-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",p)
            if m:cities.setdefault(m.group(1),set()).add(m.group(2))
        self.assertEqual(len(cities),50)
        for c,kinds in cities.items():self.assertEqual(kinds,KINDS,c)
        self.assertIn("alabama-appliance-pickup/index.html",self.pages)
    def test_every_form_title_image_and_noindex(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/AL.json"),[])
        for p in self.pages:
            with self.subTest(page=p):
                h=(ROOT/p).read_text(encoding="utf-8")
                pg=Page();pg.feed(h)
                title=unescape(re.search(r"<title>(.*?)</title>",h).group(1))
                heading=unescape(re.search(r"<h1>(.*?)</h1>",h).group(1))
                self.assertIn("Free Reliable Appliance Pickup",title)
                self.assertTrue(heading.startswith("Free ") and " Pickup in " in heading)
                self.assertNotIn("eligibilit",heading.lower())
                self.assertEqual(pg.state_options,["","AL"])
                self.assertEqual(len(pg.forms),1)
                self.assertEqual(pg.fields["source_page"][0].get("value"),p.split("/")[0])
                self.assertEqual(len(pg.images),2)
                self.assertIn("noindex, follow",h)
                self.assertIn('name="privacy_acknowledgment"',h)
                self.assertIn('name="paid_option"',h)
    def test_laundry_photos_unique(self):
        files=[]
        for p in self.pages:
            if not p.endswith("-washer-dryer-pickup/index.html"):continue
            h=(ROOT/p).read_text(encoding="utf-8")
            src=re.search(r'<figure><img src="([^"]+)"',h).group(1)
            files.append(hashlib.sha256((ROOT/src.lstrip("/")).read_bytes()).digest())
        self.assertEqual(len(files),50)
        self.assertEqual(len(set(files)),50)
    def test_stove_safety_fields(self):
        stoves=[p for p in self.pages if p.endswith("-stove-oven-pickup/index.html")]
        self.assertEqual(len(stoves),50)
        for p in stoves:
            h=(ROOT/p).read_text(encoding="utf-8")
            self.assertIn('name="fuel_type" required',h,p)
            self.assertIn('name="connection_status" required',h,p)
            self.assertIn("qualified professional",h.lower(),p)
    def test_state_hub_and_release_guard(self):
        h=(ROOT/"alabama-appliance-pickup/index.html").read_text(encoding="utf-8")
        for p in self.pages:
            if p.endswith("-al-appliance-pickup/index.html"):
                self.assertIn('href="/'+p.removesuffix("index.html")+'"',h)
        self.assertIn("Free pickup is not guaranteed",h)
        self.assertIn("confirmed local pickup option",h)
        self.assertNotIn("https://freereliableappliancepickup.com/alabama-appliance-pickup/",(ROOT/"sitemap.xml").read_text(encoding="utf-8"))
        ledger=json.loads((ROOT/"data/ttg-release-readiness/AL.json").read_text(encoding="utf-8"))
        self.assertFalse(self.batch["operator_coverage_verified"])
        self.assertEqual(ledger["verified_cities"],[])
        self.assertFalse(ledger["form_receipt"]["verified"])
        self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
