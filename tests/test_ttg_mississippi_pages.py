"""TTG Mississippi Gold rollout safeguards for 50 cities and 251 request pages."""
import json
import re
import unittest
from html import unescape
from scripts.ttg_state_batch_qa import ROOT, Page, check_manifest
KINDS={"appliance","washer-dryer","refrigerator","stove-oven","freezer"}
class MississippiGoldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batch=json.loads((ROOT/"data/ttg-state-batches/MS.json").read_text())
        cls.paths=cls.batch["pages"]
    def test_50_cities_and_five_categories(self):
        self.assertEqual(len(self.paths),251)
        self.assertEqual(len(self.paths),len(set(self.paths)))
        cities={}
        for p in self.paths:
            m=re.fullmatch(r"([a-z0-9-]+)-ms-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",p)
            if m:cities.setdefault(m.group(1),set()).add(m.group(2))
        self.assertEqual(len(cities),50)
        for city,kinds in cities.items():self.assertEqual(kinds,KINDS,city)
        self.assertIn("mississippi-appliance-pickup/index.html",self.paths)
    def test_all_pages_have_protected_request_forms_and_photos(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/MS.json"),[])
        for path in self.paths:
            with self.subTest(path=path):
                html=(ROOT/path).read_text()
                pg=Page();pg.feed(html)
                h1=unescape(re.search(r"<h1[^>]*>(.*?)</h1>",html).group(1))
                title=unescape(re.search(r"<title>(.*?)</title>",html).group(1))
                self.assertTrue(h1.startswith("Free ") and " Pickup in " in h1)
                self.assertNotIn("eligibility",h1.lower())
                self.assertIn("Free Reliable Appliance Pickup",title)
                self.assertEqual(pg.state_options,["","MS"])
                self.assertEqual(len(pg.forms),1)
                self.assertEqual(len(pg.images),2)
                self.assertEqual(pg.fields["source_page"][0]["value"],path.split("/")[0])
                self.assertIn("noindex, follow",html)
                self.assertIn('name="privacy_acknowledgment"',html)
                self.assertIn('name="paid_option"',html)
    def test_stove_forms_require_disconnection_details(self):
        for path in self.paths:
            if not path.endswith("-stove-oven-pickup/index.html"):continue
            html=(ROOT/path).read_text()
            self.assertIn('name="fuel_type" required',html,path)
            self.assertIn('name="connection_status" required',html,path)
    def test_hub_links_and_release_guards(self):
        hub=(ROOT/"mississippi-appliance-pickup/index.html").read_text()
        for path in self.paths:
            if path.endswith("-ms-appliance-pickup/index.html"):self.assertIn('href="/'+path.removesuffix("index.html")+'"',hub)
        self.assertIn("Free pickup is not guaranteed",hub)
        self.assertIn("confirmed local pickup option",hub)
        self.assertNotIn("https://freereliableappliancepickup.com/mississippi-appliance-pickup/",(ROOT/"sitemap.xml").read_text())
        ledger=json.loads((ROOT/"data/ttg-release-readiness/MS.json").read_text())
        self.assertFalse(self.batch["operator_coverage_verified"])
        self.assertEqual(ledger["verified_cities"],[])
        self.assertFalse(ledger["form_receipt"]["verified"])
        self.assertFalse(ledger["owner_release_approval"]["approved"])
if __name__=="__main__":unittest.main()
