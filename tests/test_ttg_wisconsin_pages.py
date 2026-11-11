"""Wisconsin request-only batch coverage and safety tests."""
import json
import unittest
from scripts.ttg_state_batch_qa import ROOT,check_manifest

class WisconsinBatchTests(unittest.TestCase):
    """Guard Wisconsin city guides, municipal rules and local activation."""
    def test_manifest(self):
        self.assertEqual(check_manifest(ROOT/"data/ttg-state-batches/WI.json"),[])
    def test_all_pages_and_hub_links(self):
        pages=json.loads((ROOT/"data/ttg-state-batches/WI.json").read_text())["pages"]
        self.assertEqual(len(pages),151)
        hub=(ROOT/"wisconsin-appliance-pickup/index.html").read_text()
        for p in pages:
            html=(ROOT/p).read_text()
            self.assertIn('content="noindex, follow"',html)
            self.assertIn('value="quote_ok"',html)
            self.assertIn('name="privacy_acknowledgment"',html)
            if p!="wisconsin-appliance-pickup/index.html":
                self.assertIn('href="/'+p.removesuffix("/index.html")+'/"',hub)
    def test_local_public_alternatives(self):
        m=(ROOT/"milwaukee-wi-appliance-pickup/index.html").read_text()
        d=(ROOT/"madison-wi-appliance-pickup/index.html").read_text()
        self.assertIn("not accepted curbside",m)
        self.assertIn("more than eight units",d)
    def test_gas_stove_safety(self):
        for p in json.loads((ROOT/"data/ttg-state-batches/WI.json").read_text())["pages"]:
            if "-stove-oven-" not in p: continue
            h=(ROOT/p).read_text()
            self.assertIn('name="fuel_type" required',h)
            self.assertIn('name="connection_status" required',h)
    def test_nonworking_condition_details_and_dispatch_gate(self):
        """Nonworking must require a defect explanation and be routed for partner review."""
        router=(ROOT/"assets/customer-routing.js").read_text()
        self.assertIn(r"non[\s-]*working|not[\s-]*working",router)
        self.assertIn("details.required=hasProblem",router)
        self.assertIn("REVIEW REPORTED CONDITION WITH PARTNER BEFORE DISPATCH",router)
        page=(ROOT/"wisconsin-appliance-pickup/index.html").read_text()
        self.assertIn("<option>Nonworking</option>",page)
    def test_release_unapproved(self):
        r=json.loads((ROOT/"data/ttg-release-readiness/WI.json").read_text())
        self.assertEqual(r["verified_cities"],[])
        self.assertFalse(r["form_receipt"]["verified"])
        self.assertFalse(r["owner_release_approval"]["approved"])

    def test_new_wisconsin_gold_grid(self):
        """Validate 18 cities with complete category-specific request pages."""
        manifest=json.loads((ROOT/"data/ttg-state-batches/WI.json").read_text())
        areas=["wauwatosa","oak-creek","franklin","menomonee-falls","germantown",
               "mequon","new-berlin","greenfield","west-bend","middleton","verona",
               "neenah","de-pere","fond-du-lac","manitowoc","hudson","stevens-point","beloit"]
        cat=["appliance","washer-dryer","refrigerator","stove-oven","freezer"]
        photos=set()
        for city in areas:
            for suffix in cat:
                slug=f"{city}-wi-{suffix}-pickup"
                path=f"{slug}/index.html"
                self.assertIn(path,manifest["pages"])
                page=(ROOT/path).read_text()
                self.assertTrue(page.index('<section id="request"')>page.index("<main>"))
                self.assertIn('content="noindex, follow"',page)
                self.assertIn('name="photos_available" required',page)
                self.assertIn('name="privacy_acknowledgment" value="acknowledged" required',page)
                self.assertIn('name="source_page" value="'+slug+'"',page)
                if suffix=="washer-dryer":
                    import re
                    image=re.search(r'<figure><img src="([^"]+)"',page)
                    self.assertIsNotNone(image)
                    photos.add(image.group(1))
        self.assertEqual(len(photos),18)

if __name__=="__main__":unittest.main()
