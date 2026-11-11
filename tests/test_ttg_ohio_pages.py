"""TTG Ohio staged pickup guides: protect request-only claims and distinct existing Columbus URLs."""
from pathlib import Path
import json
import unittest
from scripts.ttg_state_batch_qa import ROOT, check_manifest
class OhioStateBatchTests(unittest.TestCase):
    def test_request_only_preflight(self):
        self.assertEqual(check_manifest(ROOT / "data/ttg-state-batches/OH.json"), [])
    def test_ohio_rollout_count_and_columbus_protection(self):
        rows=json.loads((ROOT / "data/ttg-state-batches/OH.json").read_text())["pages"]
        self.assertEqual(len(rows),246)
        self.assertNotIn("columbus-appliance-pickup/index.html",rows)
        hub=(ROOT / "ohio-appliance-pickup/index.html").read_text()
        for r in rows:
            if r == "ohio-appliance-pickup/index.html": continue
            self.assertIn('/'+r.replace('/index.html','')+'/', hub)
        for slug in ("columbus-appliance-pickup","columbus-washer-dryer-pickup",
                     "columbus-refrigerator-pickup","columbus-stove-pickup","columbus-freezer-pickup"):
            self.assertIn('/'+slug+'/',hub)
        self.assertIn("City of Columbus bulk collection guide",hub)
    def test_new_ohio_routes_not_advertised_as_active(self):
        ledger=json.loads((ROOT/"data/ttg-release-readiness/OH.json").read_text())
        self.assertEqual(ledger["verified_cities"],[])
        self.assertFalse(ledger["form_receipt"]["verified"])
        for path in json.loads((ROOT/"data/ttg-state-batches/OH.json").read_text())["pages"]:
            h=(ROOT/path).read_text()
            self.assertIn('content="noindex, follow"',h)
            self.assertIn("not a completed Ohio pickup",h)
            self.assertIn('name="privacy_acknowledgment"',h)
            self.assertIn('name="paid_option"',h)
    def test_distinct_category_guidance(self):
        for city in ("cleveland","cincinnati","dayton","toledo","akron"):
            for kind in ("washer-dryer","refrigerator","stove-oven","freezer"):
                path=ROOT/f"{city}-oh-{kind}-pickup/index.html"
                h=path.read_text()
                self.assertIn('action="https://formspree.io/f/mvzeapzd"',h)
                self.assertIn(f'name="source_page" value="{city}-oh-{kind}-pickup"',h)
                if kind=="stove-oven":
                    self.assertIn('name="fuel_type" required',h)
                    self.assertIn('name="connection_status" required',h)

    def test_50_city_golds_and_distinct_photo_sources(self):
        import re
        rows=json.loads((ROOT/"data/ttg-state-batches/OH.json").read_text())["pages"]
        bycity={}
        laundry=[]
        for path in rows:
            m=re.fullmatch(r"(.+)-oh-(appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup/index.html",path)
            if not m:continue
            city,category=m.groups()
            bycity.setdefault(city,set()).add(category)
            if city in {"dublin","hilliard","upper-arlington","worthington","westerville","gahanna","new-albany","reynoldsburg","pickerington","grove-city","powell","delaware","lewis-center","sunbury","canal-winchester","lancaster","newark","pataskala","marysville","lakewood","parma","strongsville","westlake","rocky-river","north-olmsted","north-royalton","solon","beachwood","mentor","mason","west-chester","fairfield","hamilton","blue-ash","loveland","cuyahoga-falls","stow","kent","kettering","centerville","beavercreek","perrysburg","sylvania","canton"} and category=="washer-dryer":
                h=(ROOT/path).read_text()
                mimg=re.search(r'<figure><img src="([^"]+)"',h)
                self.assertIsNotNone(mimg,path)
                laundry.append(mimg.group(1))
        self.assertEqual(len(bycity),49)
        self.assertTrue(all(len(v)==5 for v in bycity.values()))
        self.assertEqual(len(laundry),44)
        self.assertEqual(len(set(laundry)),44)
        # Columbus already has five owned legacy landing pages; avoid new duplicate city-intent URLs.
        for kind in ("appliance","washer-dryer","refrigerator","stove","freezer"):
            self.assertTrue((ROOT/f"columbus-{kind}-pickup/index.html").is_file())
        self.assertEqual(len(bycity)+1,50)

if __name__=="__main__": unittest.main()
