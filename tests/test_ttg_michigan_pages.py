"""Michigan FastTrack request-only batch: enforce safety, city navigation and intent."""
import unittest
import json
from scripts.ttg_state_batch_qa import ROOT,check_manifest
class MichiganFastTrack(unittest.TestCase):
    def test_state_manifest(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/MI.json"),[])
    def test_61_pages_reachable_and_unverified(self):
        manifest=json.loads((ROOT/"data/ttg-state-batches/MI.json").read_text())
        self.assertEqual(len(manifest["pages"]),251)
        hub=(ROOT/"michigan-appliance-pickup/index.html").read_text()
        for path in manifest["pages"]:
            html=(ROOT/path).read_text()
            self.assertIn('content="noindex, follow"',html)
            self.assertIn('name="privacy_acknowledgment"',html)
            self.assertIn('name="paid_option"',html)
            if path=="michigan-appliance-pickup/index.html": continue
            self.assertIn('href="/'+path.removesuffix("/index.html")+'/"',hub)
    def test_stove_gas_fields(self):
        for path in json.loads((ROOT/"data/ttg-state-batches/MI.json").read_text())["pages"]:
            if "-stove-oven-" not in path:continue
            html=(ROOT/path).read_text()
            self.assertIn('name="fuel_type" required',html)
            self.assertIn('name="connection_status" required',html)
            self.assertIn("qualified professional",html)
    def test_local_public_alternatives_and_readiness(self):
        a=(ROOT/"grand-rapids-mi-appliance-pickup/index.html").read_text()
        self.assertIn("City of Grand Rapids guidelines",a)
        self.assertIn("$40 bulky-item",a)
        ledger=json.loads((ROOT/"data/ttg-release-readiness/MI.json").read_text())
        self.assertEqual(ledger["verified_cities"],[])
        self.assertFalse(ledger["form_receipt"]["verified"])

    def test_50_city_five_category_michigan_gold(self):
        """Michigan Gold: 50 real markets, five categories and no unverified indexing."""
        import re
        cities=["ann-arbor","battle-creek","dearborn","detroit","farmington-hills","flint","grand-rapids","holland","kalamazoo","lansing","livonia","muskegon","novi","rochester-hills","saginaw","southfield","sterling-heights","traverse-city","troy","warren","westland","canton","taylor","royal-oak","west-bloomfield","pontiac","st-clair-shores","roseville","madison-heights","birmingham","allen-park","redford","auburn-hills","shelby-township","macomb-township","clinton-township","waterford-township","kentwood","wyoming","walker","grandville","portage","ypsilanti","jackson","midland","bay-city","marquette","petoskey","grand-haven","brighton"]
        categories=["appliance","washer-dryer","refrigerator","stove-oven","freezer"]
        m=json.loads((ROOT/"data/ttg-state-batches/MI.json").read_text())
        self.assertEqual(len(cities),50)
        self.assertEqual(len(m["pages"]),251)
        photos=[]
        prior=set(["ann-arbor-mi-appliance-pickup/index.html","ann-arbor-mi-freezer-pickup/index.html","ann-arbor-mi-refrigerator-pickup/index.html","ann-arbor-mi-stove-oven-pickup/index.html","ann-arbor-mi-washer-dryer-pickup/index.html","battle-creek-mi-appliance-pickup/index.html","dearborn-mi-appliance-pickup/index.html","detroit-mi-appliance-pickup/index.html","detroit-mi-freezer-pickup/index.html","detroit-mi-refrigerator-pickup/index.html","detroit-mi-stove-oven-pickup/index.html","detroit-mi-washer-dryer-pickup/index.html","farmington-hills-mi-appliance-pickup/index.html","flint-mi-appliance-pickup/index.html","flint-mi-freezer-pickup/index.html","flint-mi-refrigerator-pickup/index.html","flint-mi-stove-oven-pickup/index.html","flint-mi-washer-dryer-pickup/index.html","grand-rapids-mi-appliance-pickup/index.html","grand-rapids-mi-freezer-pickup/index.html","grand-rapids-mi-refrigerator-pickup/index.html","grand-rapids-mi-stove-oven-pickup/index.html","grand-rapids-mi-washer-dryer-pickup/index.html","holland-mi-appliance-pickup/index.html","kalamazoo-mi-appliance-pickup/index.html","kalamazoo-mi-freezer-pickup/index.html","kalamazoo-mi-refrigerator-pickup/index.html","kalamazoo-mi-stove-oven-pickup/index.html","kalamazoo-mi-washer-dryer-pickup/index.html","lansing-mi-appliance-pickup/index.html","lansing-mi-freezer-pickup/index.html","lansing-mi-refrigerator-pickup/index.html","lansing-mi-stove-oven-pickup/index.html","lansing-mi-washer-dryer-pickup/index.html","livonia-mi-appliance-pickup/index.html","michigan-appliance-pickup/index.html","muskegon-mi-appliance-pickup/index.html","novi-mi-appliance-pickup/index.html","rochester-hills-mi-appliance-pickup/index.html","saginaw-mi-appliance-pickup/index.html","southfield-mi-appliance-pickup/index.html","southfield-mi-freezer-pickup/index.html","southfield-mi-refrigerator-pickup/index.html","southfield-mi-stove-oven-pickup/index.html","southfield-mi-washer-dryer-pickup/index.html","sterling-heights-mi-appliance-pickup/index.html","sterling-heights-mi-freezer-pickup/index.html","sterling-heights-mi-refrigerator-pickup/index.html","sterling-heights-mi-stove-oven-pickup/index.html","sterling-heights-mi-washer-dryer-pickup/index.html","traverse-city-mi-appliance-pickup/index.html","traverse-city-mi-freezer-pickup/index.html","traverse-city-mi-refrigerator-pickup/index.html","traverse-city-mi-stove-oven-pickup/index.html","traverse-city-mi-washer-dryer-pickup/index.html","troy-mi-appliance-pickup/index.html","warren-mi-appliance-pickup/index.html","warren-mi-freezer-pickup/index.html","warren-mi-refrigerator-pickup/index.html","warren-mi-stove-oven-pickup/index.html","warren-mi-washer-dryer-pickup/index.html"])
        for city in cities:
            for cat in categories:
                path=f"{city}-mi-{cat}-pickup/index.html"
                self.assertIn(path,m["pages"])
                html=(ROOT/path).read_text()
                self.assertIn('content="noindex, follow"',html)
                self.assertIn('Free Reliable Appliance Pickup',html)
                self.assertIn('href="https://freereliableappliancepickup.com/'+path.removesuffix("index.html")+'"',html)
                self.assertIn('action="https://formspree.io/f/mvzeapzd"',html)
                self.assertIn('name="source_page" value="'+path.split("/",1)[0]+'"',html)
                if path not in prior:
                    self.assertEqual(html.index('<section id="request"'),html.index("<main>")+len("<main>"))
                    self.assertIn('Michigan EGLE',html)
                if cat=="washer-dryer" and path not in prior:
                    photo=re.search(r'<figure><img src="([^"]+)"',html)
                    self.assertIsNotNone(photo,path)
                    photos.append(photo.group(1))
        self.assertEqual(len(photos),40)
        self.assertEqual(len(set(photos)),40)

if __name__=="__main__":unittest.main()
