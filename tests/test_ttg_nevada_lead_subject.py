"""Regression: Nevada source_page should override stale UT Formspree subjects without impacting other states."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class NevadaSubjectSafety(unittest.TestCase):
 def test_targeted_routing_guard_present(self):
  js=(ROOT/"assets/customer-routing.js").read_text()
  self.assertIn("function correctNevadaRequestSubject(form)",js)
  self.assertIn("subject.value='NV '+subject.value.slice(3)",js)
  self.assertIn("-nv-(?:appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup",js)
  self.assertIn(".forEach(correctNevadaRequestSubject)",js)
 def test_existing_nv_leads_have_nm_other_states_untouched(self):
  html=(ROOT/"las-vegas-nv-appliance-pickup/index.html").read_text()
  self.assertIn('name="_subject" value="UT Las Vegas Appliance',html)
  self.assertIn('name="source_page" value="las-vegas-nv-appliance-pickup"',html)
  self.assertIn('name="state" required',html)
  self.assertIn('value="NV" selected',html)
if __name__=="__main__":unittest.main()
