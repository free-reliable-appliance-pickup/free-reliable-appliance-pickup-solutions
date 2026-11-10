"""Kentucky 50-city, 251-page Free Appliance Pickup customer-journey checks."""
from pathlib import Path
from html import unescape
import hashlib
import json
import re
import unittest
from scripts.ttg_state_batch_qa import ROOT,Page,check_manifest

CITY_KINDS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}

class KentuckyGoldRollout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads((ROOT/"data/ttg-state-batches/KY.json").read_text(encoding="utf-8"))
        cls.pages=cls.manifest["pages"]

    def test_complete_state_matrix_and_no_duplicate_city_routes(self):
        self.assertEqual(len(self.pages),251)
        self.assertEqual(len(self.pages),len(set(self.pages)))
        towns={}
        for p in self.pages:
            match=re.fullmatch(r"([a-z0-9-]+)-ky-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",p)
            if match:towns.setdefault(match.group(1),set()).add(match.group(2))
        self.assertEqual(len(towns),50)
        for city,kinds in towns.items():
            self.assertEqual(kinds,CITY_KINDS,city)
        self.assertIn("kentucky-appliance-pickup/index.html",self.pages)

    def test_all_forms_images_and_canonicals_follow_california_contract(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/KY.json"),[])
        for rel in self.pages:
            with self.subTest(rel=rel):
                html=(ROOT/rel).read_text(encoding="utf-8")
                page=Page()
                page.feed(html)
                title=unescape(re.search(r"<title>(.*?)</title>",html).group(1))
                h1=unescape(re.search(r"<h1\b[^>]*>(.*?)</h1>",html).group(1))
                self.assertIn("Free Reliable Appliance Pickup",title)
                self.assertRegex(h1,r"^Free (?:Appliance|Washer & Dryer|Refrigerator|Stove & Oven|Freezer) Pickup in ")
                self.assertNotIn("eligibilit",title.lower())
                self.assertNotIn("eligibilit",h1.lower())
                self.assertEqual(len(page.forms),1)
                self.assertIn('name="privacy_acknowledgment"',html)
                self.assertIn('name="paid_option"',html)
                self.assertIn('name="source_page"',html)
                self.assertEqual(page.state_options,["","KY"])
                self.assertEqual(page.canonicals,["https://freereliableappliancepickup.com/"+rel.removesuffix("index.html")])
                self.assertEqual(len([img for img in page.images if "site-brand-logo" not in (img.get("class") or "").split()]),1)
                self.assertIn("not a completed",html.lower())
                self.assertIn("noindex, follow",html)
                self.assertIn("Request Free ",html)

    def test_all_stove_pages_require_fuel_and_safe_disconnection(self):
        stoves=[p for p in self.pages if p.endswith("-stove-oven-pickup/index.html")]
        self.assertEqual(len(stoves),50)
        for rel in stoves:
            html=(ROOT/rel).read_text(encoding="utf-8")
            self.assertIn('name="fuel_type" required',html,rel)
            self.assertIn('name="connection_status" required',html,rel)
            self.assertIn("qualified professional",html.lower(),rel)
            self.assertIn("Do not loosen a gas connection",html,rel)

    def test_laundry_photos_are_not_repeated(self):
        images=[]
        for rel in self.pages:
            if not rel.endswith("-washer-dryer-pickup/index.html"):continue
            html=(ROOT/rel).read_text(encoding="utf-8")
            src=re.search(r'<figure><img src="([^"]+)"',html).group(1)
            images.append(hashlib.sha256((ROOT/src.lstrip("/")).read_bytes()).hexdigest())
        self.assertEqual(len(images),50)
        self.assertEqual(len(set(images)),50)

    def test_city_navigation_and_official_guidance(self):
        hub=(ROOT/"kentucky-appliance-pickup/index.html").read_text(encoding="utf-8")
        for rel in self.pages:
            if rel.endswith("-ky-appliance-pickup/index.html"):
                self.assertIn('href="/'+rel.removesuffix("index.html")+'"',hub)
            elif rel!="kentucky-appliance-pickup/index.html":
                slug=rel.split("-ky-",1)[0]
                general=(ROOT/(slug+"-ky-appliance-pickup/index.html")).read_text(encoding="utf-8")
                self.assertIn('href="/'+rel.removesuffix("index.html")+'"',general)
        self.assertIn("https://www.lexingtonky.gov/living/waste-collection/appliances",hub)
        self.assertIn("https://louisvilleky.gov/government/public-works/large-items",hub)

    def test_release_is_not_falsely_activated(self):
        ledger=json.loads((ROOT/"data/ttg-release-readiness/KY.json").read_text(encoding="utf-8"))
        self.assertEqual(ledger["verified_cities"],[])
        self.assertFalse(ledger["form_receipt"]["verified"])
        self.assertFalse(ledger["owner_release_approval"]["approved"])
        self.assertFalse(self.manifest["operator_coverage_verified"])
        self.assertEqual(self.manifest["mode"],"request-only")

if __name__=="__main__":
    unittest.main()
