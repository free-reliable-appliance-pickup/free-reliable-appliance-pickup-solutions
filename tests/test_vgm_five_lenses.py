"""No-cost safety checks for the static five-lens VGM report."""
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

MODULE = Path(__file__).resolve().parents[1] / "scripts/vgm-free-five-lenses.py"
spec = importlib.util.spec_from_file_location("vgm_free_five_lenses", MODULE)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class FiveLensesTests(unittest.TestCase):
    def test_empty_root_reports_without_network(self):
        with TemporaryDirectory() as temp:
            result = audit.generate(Path(temp))
            for name in ("Auditor", "Researcher", "Planner", "Scorer", "Gatekeeper"):
                self.assertIn(name, result)
            self.assertIn("No live rankings", result)

    def test_city_with_markup_and_robots(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "rancho-cucamonga-appliance-pickup"
            page.mkdir()
            (page / "index.html").write_text(
                '<html><head><title>Free Appliance Pickup Rancho Cucamonga</title>'
                '<meta name="description" content="Condition and access review.">'
                '<meta name="robots" content="index, follow">'
                '<link rel="canonical" href="https://freereliableappliancepickup.com/'
                'rancho-cucamonga-appliance-pickup/"></head>'
                '<body><h1>Free Appliance Pickup</h1><form action="/"></form>'
                '<a href="tel:+19093756685">Call</a><p>Garage access</p></body></html>',
                encoding="utf-8"
            )
            (root / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
            result = audit.generate(root)
            self.assertIn("User-agent * present", result)
            self.assertIn("Root Allow /: True", result)
            self.assertIn("Source-only review of 1 existing priority city hubs", result)
            self.assertNotIn("non-self-canonical", result)
            self.assertTrue((page / "index.html").exists())

    def test_indexed_noindex_and_missing_h1_are_flagged_not_fixed(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "fontana-appliance-pickup"
            target.mkdir()
            (target / "index.html").write_text(
                '<head><title>Fontana</title><meta name="robots" content="noindex">'
                '<link rel="canonical" href="https://freereliableappliancepickup.com/'
                'fontana-appliance-pickup/"></head><body>No h1</body>',
                encoding="utf-8"
            )
            (root / "sitemap.xml").write_text(
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                '<url><loc>https://freereliableappliancepickup.com/'
                'fontana-appliance-pickup/</loc></url></urlset>', encoding="utf-8"
            )
            before = (target / "index.html").read_bytes()
            result = audit.generate(root)
            self.assertIn("noindex and present in XML sitemap", result)
            self.assertIn("H1 count 0", result)
            self.assertEqual(before, (target / "index.html").read_bytes())


if __name__ == "__main__":
    unittest.main()
