"""PA batch QA: market and release safety."""
import unittest
import json
from scripts.ttg_state_batch_qa import ROOT,check_manifest
class PennsylvaniaBatchTests(unittest.TestCase):
    def test_manifest(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/PA.json"),[])
    def test_city_links(self):
        paths=json.loads((ROOT/"data/ttg-state-batches/PA.json").read_text())["pages"]
        self.assertEqual(len(paths),251)
        hub=(ROOT/"pennsylvania-appliance-pickup/index.html").read_text()
        self.assertIn("Official recycling and disposal alternatives",hub)
        for path in paths:
            text=(ROOT/path).read_text()
            self.assertIn('content="noindex, follow"',text)
            self.assertIn('name="paid_option"',text)
            self.assertIn('name="privacy_acknowledgment"',text)
            if path!="pennsylvania-appliance-pickup/index.html":
                self.assertIn('href="/'+path.removesuffix("/index.html")+'/"',hub)
    def test_appliance_safety(self):
        paths=json.loads((ROOT/"data/ttg-state-batches/PA.json").read_text())["pages"]
        for path in paths:
            if "-stove-oven-" not in path:continue
            text=(ROOT/path).read_text()
            self.assertIn('name="fuel_type" required',text)
            self.assertIn('name="connection_status" required',text)
            self.assertIn("qualified",text)
    def test_unverified_operator_ledger(self):
        ledger=json.loads((ROOT/"data/ttg-release-readiness/PA.json").read_text())
        self.assertFalse(ledger["form_receipt"]["verified"])
        self.assertEqual(ledger["verified_cities"],[])

    def test_pennsylvania_50_city_gold(self):
        """Every target city has five separate request guides with safe release gates."""
        import re
        cities=["allentown","bethlehem","easton","erie","harrisburg","lancaster","mechanicsburg","norristown","philadelphia","pittsburgh","reading","scranton","state-college","west-chester","wilkes-barre","york","king-of-prussia","conshohocken","plymouth-meeting","willow-grove","bensalem","levittown","doylestown","newtown","lansdale","pottstown","phoenixville","exton","downingtown","media","upper-darby","ardmore","bryn-mawr","wayne","drexel-hill","monroeville","bethel-park","cranberry-township","wexford","greensburg","altoona","johnstown","hazleton","lebanon","carlisle","chambersburg","east-stroudsburg","hershey","camp-hill","kennett-square"]
        categories=["appliance","washer-dryer","refrigerator","stove-oven","freezer"]
        rows=json.loads((ROOT/"data/ttg-state-batches/PA.json").read_text())
        before=set(["allentown-pa-appliance-pickup/index.html","allentown-pa-freezer-pickup/index.html","allentown-pa-refrigerator-pickup/index.html","allentown-pa-stove-oven-pickup/index.html","allentown-pa-washer-dryer-pickup/index.html","bethlehem-pa-appliance-pickup/index.html","easton-pa-appliance-pickup/index.html","erie-pa-appliance-pickup/index.html","erie-pa-freezer-pickup/index.html","erie-pa-refrigerator-pickup/index.html","erie-pa-stove-oven-pickup/index.html","erie-pa-washer-dryer-pickup/index.html","harrisburg-pa-appliance-pickup/index.html","harrisburg-pa-freezer-pickup/index.html","harrisburg-pa-refrigerator-pickup/index.html","harrisburg-pa-stove-oven-pickup/index.html","harrisburg-pa-washer-dryer-pickup/index.html","lancaster-pa-appliance-pickup/index.html","lancaster-pa-freezer-pickup/index.html","lancaster-pa-refrigerator-pickup/index.html","lancaster-pa-stove-oven-pickup/index.html","lancaster-pa-washer-dryer-pickup/index.html","mechanicsburg-pa-appliance-pickup/index.html","norristown-pa-appliance-pickup/index.html","pennsylvania-appliance-pickup/index.html","philadelphia-pa-appliance-pickup/index.html","philadelphia-pa-freezer-pickup/index.html","philadelphia-pa-refrigerator-pickup/index.html","philadelphia-pa-stove-oven-pickup/index.html","philadelphia-pa-washer-dryer-pickup/index.html","pittsburgh-pa-appliance-pickup/index.html","pittsburgh-pa-freezer-pickup/index.html","pittsburgh-pa-refrigerator-pickup/index.html","pittsburgh-pa-stove-oven-pickup/index.html","pittsburgh-pa-washer-dryer-pickup/index.html","reading-pa-appliance-pickup/index.html","reading-pa-freezer-pickup/index.html","reading-pa-refrigerator-pickup/index.html","reading-pa-stove-oven-pickup/index.html","reading-pa-washer-dryer-pickup/index.html","scranton-pa-appliance-pickup/index.html","scranton-pa-freezer-pickup/index.html","scranton-pa-refrigerator-pickup/index.html","scranton-pa-stove-oven-pickup/index.html","scranton-pa-washer-dryer-pickup/index.html","state-college-pa-appliance-pickup/index.html","west-chester-pa-appliance-pickup/index.html","wilkes-barre-pa-appliance-pickup/index.html","york-pa-appliance-pickup/index.html"])
        self.assertEqual(len(rows["pages"]),251)
        self.assertEqual(len(cities),50)
        photos=[]
        for city in cities:
            for cat in categories:
                path=f"{city}-pa-{cat}-pickup/index.html"
                self.assertIn(path,rows["pages"])
                html=(ROOT/path).read_text()
                self.assertIn('content="noindex, follow"',html)
                self.assertIn('Free Reliable Appliance Pickup',html)
                self.assertIn('name="source_page" value="'+path.split("/",1)[0]+'"',html)
                self.assertIn('action="https://formspree.io/f/mvzeapzd"',html)
                if path not in before:
                    self.assertEqual(html.index('<section id="request"'),html.index("<main>")+len("<main>"))
                    self.assertIn('Independent Pennsylvania appliance disposal',html)
                if cat=="washer-dryer" and path not in before:
                    photo=re.search(r'<figure><img src="([^"]+)"',html)
                    self.assertIsNotNone(photo,path)
                    photos.append(photo.group(1))
        self.assertEqual(len(photos),42)
        self.assertEqual(len(set(photos)),42)

if __name__=="__main__":unittest.main()
