"""South Carolina TTG: 50-city 251-page eligibility matrix validation."""
import json
import unittest
from scripts.ttg_state_batch_qa import ROOT, Page, check_manifest
CITIES=["charleston","north-charleston","mount-pleasant","summerville","goose-creek","hanahan","moncks-corner","johns-island","myrtle-beach","north-myrtle-beach","conway","surfside-beach","murrells-inlet","little-river","loris","carolina-forest","hilton-head-island","bluffton","beaufort","hardeeville","port-royal","ridgeland","walterboro","columbia","west-columbia","cayce","lexington","irmo","blythewood","sumter","camden","orangeburg","greenville","greer","simpsonville","mauldin","easley","spartanburg","anderson","greenwood","seneca","taylors","boiling-springs","rock-hill","fort-mill","tega-cay","clover","indian-land","aiken","florence"]
KINDS=("appliance","washer-dryer","refrigerator","stove-oven","freezer")
class SCMatrixTests(unittest.TestCase):
 def test_full_matrix_and_noindex(self):
  manifest=ROOT/"data/ttg-state-batches/SC.json"
  paths=json.loads(manifest.read_text())["pages"]
  self.assertEqual(len(CITIES),50)
  self.assertEqual(len(paths),251)
  self.assertEqual(len(paths),len(set(paths)))
  for city in CITIES:
   for kind in KINDS:
    rel=f"{city}-sc-{kind}-pickup/index.html"
    self.assertIn(rel,paths)
    raw=(ROOT/rel).read_text(encoding="utf-8")
    parsed=Page(); parsed.feed(raw)
    self.assertIn("noindex",",".join(parsed.robots))
    self.assertEqual(len([img for img in parsed.images if "site-brand-logo" not in (img.get("class") or "").split()]),1)
    self.assertEqual(parsed.state_options,["","SC"])
    self.assertEqual(parsed.fields["source_page"][0]["value"],rel.split("/")[0])
    self.assertTrue(all((ROOT/img["src"].lstrip("/")).is_file() for img in parsed.images))
  self.assertEqual(check_manifest(manifest),[])
 def test_hub_and_legacy_categories(self):
  hub=(ROOT/"south-carolina-appliance-pickup/index.html").read_text()
  for city in CITIES:self.assertIn(f"/{city}-sc-appliance-pickup/",hub)
  self.assertIn('id="ttg-sc-complete-grid"',hub)
  for city in ["aiken","anderson","beaufort","conway","florence","fort-mill","goose-creek","lexington","mount-pleasant","north-myrtle-beach"]:
   raw=(ROOT/f"{city}-sc-appliance-pickup/index.html").read_text()
   for kind in KINDS[1:]:self.assertIn(f"/{city}-sc-{kind}-pickup/",raw)
