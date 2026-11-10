"""Targeted Nevada email subject correction and Rancho JS budget regression."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class NevadaSubjectSafety(unittest.TestCase):
 def test_loader_and_budget(self):
  js=(ROOT/"assets/customer-routing.js").read_text()
  self.assertIn("import('/assets/nv-subject.js')",js)
  self.assertIn("pathname.includes('-nv-')",js)
  self.assertLessEqual((ROOT/"assets/customer-routing.js").stat().st_size,40000)
 def test_fix_only_for_nv_and_old_ut(self):
  fix=(ROOT/"assets/nv-subject.js").read_text()
  self.assertIn("function correctNevadaFormSubjects()",fix)
  self.assertIn("-nv-(?:appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup",fix)
  self.assertIn("subject.value='NV '+subject.value.slice(3)",fix)
  self.assertIn("if(subject&&/^UT /.test(subject.value))",fix)
 def test_current_nv_form_source_and_state(self):
  html=(ROOT/"las-vegas-nv-appliance-pickup/index.html").read_text()
  self.assertIn('name="_subject" value="UT Las Vegas Appliance',html)
  self.assertIn('name="source_page" value="las-vegas-nv-appliance-pickup"',html)
  self.assertIn('value="NV" selected',html)
if __name__=="__main__":unittest.main()
