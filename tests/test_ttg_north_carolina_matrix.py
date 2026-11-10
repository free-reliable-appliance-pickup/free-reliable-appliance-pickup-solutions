"""North Carolina TTG FastTrack 50-market matrix check."""
import json
import unittest
from scripts.ttg_state_batch_qa import ROOT, Page, check_manifest
CITIES=["charlotte","concord","gastonia","huntersville","cornelius","davidson","matthews","mint-hill","waxhaw","indian-trail","monroe","mooresville","kannapolis","belmont","statesville","raleigh","durham","cary","apex","morrisville","holly-springs","fuquay-varina","garner","wake-forest","knightdale","chapel-hill","carrboro","clayton","greensboro","winston-salem","high-point","kernersville","burlington","clemmons","lexington","thomasville","asheville","hendersonville","hickory","pinehurst","southern-pines","sanford","fayetteville","wilmington","leland","southport","calabash","shallotte","jacksonville","new-bern"]
KINDS=("appliance","washer-dryer","refrigerator","stove-oven","freezer")
class NCMatrixTests(unittest.TestCase):
 def test_50_by_5_matrix_and_staged_intake(self):
  manifest=ROOT/"data/ttg-state-batches/NC.json"
  rows=json.loads(manifest.read_text())["pages"]
  self.assertEqual(len(rows),250)
  self.assertEqual(len(set(rows)),250)
  for city in CITIES:
   for kind in KINDS:
    rel=f"{city}-nc-{kind}-pickup/index.html"
    self.assertIn(rel,rows)
    h=(ROOT/rel).read_text()
    p=Page();p.feed(h)
    self.assertEqual(p.robots,["noindex, follow"])
    self.assertEqual(len(p.images),1)
    self.assertTrue((ROOT/p.images[0]["src"].lstrip("/")).is_file())
    self.assertEqual(p.state_options,["","NC"])
    self.assertEqual(p.fields["source_page"][0]["value"],rel.split("/")[0])
  self.assertEqual(check_manifest(manifest),[])
 def test_hub_links_all_markets(self):
  hub=(ROOT/"north-carolina-appliance-pickup/index.html").read_text()
  for city in CITIES:self.assertIn(f'/{city}-nc-appliance-pickup/',hub)
  self.assertIn('id="ttg-nc-complete-grid"',hub)
