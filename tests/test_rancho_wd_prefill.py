"""Keep Rancho Cucamonga washer/dryer request links focused and functional."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
GENERAL = ROOT / "rancho-cucamonga-appliance-pickup" / "index.html"
LAUNDRY = ROOT / "rancho-cucamonga-washer-dryer-pickup" / "index.html"
PREFILLED = "/rancho-cucamonga-appliance-pickup/?appliance=washer-dryer#request"


class RanchoWasherDryerPrefillTests(unittest.TestCase):
    def test_laundry_ctas_use_prefilled_request(self):
        html = LAUNDRY.read_text(encoding="utf-8")
        self.assertGreaterEqual(html.count(f'href="{PREFILLED}"'), 3)
        self.assertNotIn('href="/rancho-cucamonga-appliance-pickup/#request"', html)
        self.assertIn("Free Washer", html)

    def test_general_request_preserves_form_and_tracks_origin(self):
        html = GENERAL.read_text(encoding="utf-8")
        self.assertIn('id="request"', html)
        self.assertIn('action="https://formspree.io/f/mvzeapzd"', html)
        self.assertIn('<option>Washer and Dryer</option>', html)
        self.assertIn("new URLSearchParams(location.search).get('appliance')!=='washer-dryer'", html)
        self.assertIn("origin.name='request_origin'", html)
        self.assertIn("rancho-cucamonga-washer-dryer-pickup", html)
        self.assertIn("select.selectedIndex=i", html)


if __name__ == "__main__":
    unittest.main()
