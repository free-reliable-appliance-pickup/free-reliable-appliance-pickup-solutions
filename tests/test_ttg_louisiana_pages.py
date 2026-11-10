"""Louisiana 251-page TTG Free Appliance Pickup rollout tests."""
import hashlib
import json
import re
import unittest
from html import unescape
from scripts.ttg_state_batch_qa import ROOT, Page, check_manifest
KINDS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class LouisianaGoldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batch=json.loads((ROOT/"data/ttg-state-batches/LA.json").read_text())
        cls.paths=cls.batch["pages"]
    def test_full_fifty_city_five_category_matrix(self):
        self.assertEqual(len(self.paths),251)
        self.assertEqual(len(self.paths),len(set(self.paths)))
        cities={}
        for p in self.paths:
            m=re.fullmatch(r"([a-z0-9-]+)-la-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",p)
            if m:cities.setdefault(m.group(1),set()).add(m.group(2))
        self.assertEqual(len(cities),50)
        for city,types in cities.items():self.assertEqual(types,KINDS,city)
        self.assertIn("louisiana-appliance-pickup/index.html",self.paths)
    def test_request_forms_photos_headings_and_staging(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/LA.json"),[])
        for p in self.paths:
            with self.subTest(page=p):
                h=(ROOT/p).read_text()
                pg=Page();pg.feed(h)
                title=unescape(re.search(r"<title>(.*?)</title>",h).group(1))
                heading=unescape(re.search(r"<h1[^>]*>(.*?)</h1>",h).group(1))
                self.assertTrue(heading.startswith("Free ") and " Pickup in " in heading)
                self.assertNotIn("eligibility",heading.lower())
                self.assertIn("Free Reliable Appliance Pickup",title)
                self.assertEqual(pg.state_options,["","LA"])
                self.assertEqual(len(pg.forms),1)
                self.assertEqual(len(pg.images),2)
                self.assertEqual(pg.fields["source_page"][0]["value"],p.split("/")[0])
                self.assertIn("noindex, follow",h)
                self.assertIn('name="privacy_acknowledgment"',h)
                self.assertIn('name="paid_option"',h)
    def test_stove_intake_disconnection_safety(self):
        pages=[x for x in self.paths if x.endswith("-stove-oven-pickup/index.html")]
        self.assertEqual(len(pages),50)
        for p in pages:
            h=(ROOT/p).read_text()
            self.assertIn('name="fuel_type" required',h,p)
            self.assertIn('name="connection_status" required',h,p)
    def test_washer_photos_are_distinct(self):
        files=[]
        for p in self.paths:
            if not p.endswith("-washer-dryer-pickup/index.html"):continue
            h=(ROOT/p).read_text()
            path=re.search(r'<figure><img src="([^"]+)"',h).group(1)
            files.append(hashlib.sha256((ROOT/path.lstrip("/")).read_bytes()).digest())
        self.assertEqual(len(files),50)
        self.assertEqual(len(set(files)),50)
    def test_statewide_links_and_release_guard(self):
        h=(ROOT/"louisiana-appliance-pickup/index.html").read_text()
        for p in self.paths:
            if p.endswith("-la-appliance-pickup/index.html"):
                self.assertIn('href="/'+p.removesuffix("index.html")+'"',h)
        self.assertIn("Free pickup is not guaranteed",h)
        self.assertIn("confirmed local pickup option",h)
        self.assertNotIn("https://freereliableappliancepickup.com/louisiana-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
        ledger=json.loads((ROOT/"data/ttg-release-readiness/LA.json").read_text())
        self.assertFalse(self.batch["operator_coverage_verified"])
        self.assertEqual(ledger["verified_cities"],[])
        self.assertFalse(ledger["form_receipt"]["verified"])
        self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
