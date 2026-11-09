"""No-network tests for TTG state batch preflight."""
import json
from pathlib import Path
import tempfile
import unittest
from scripts.ttg_state_batch_qa import check_manifest


class StateBatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "data/ttg-state-batches").mkdir(parents=True)
        (self.root / "data/market-routing.json").write_text(json.dumps({
            "state_defaults": [{"state": "Illinois", "state_code": "IL", "status": "request-only"}]
        }))
        self.slug = "chicago-il-appliance-pickup"
        folder = self.root / self.slug
        folder.mkdir()
        (self.root / "used-appliances.webp").write_bytes(b"fixture")
        self.page = folder / "index.html"
        fields = ("name", "phone", "address", "city", "zip", "appliance",
                  "condition", "floor", "stairs", "photos_available", "access", "message")
        self.html = (
            '<html><head><meta name="robots" content="noindex, follow">'
            f'<link rel="canonical" href="https://freereliableappliancepickup.com/{self.slug}/">'
            '</head><body><h1>Chicago used appliance request</h1>'
            '<img src="/used-appliances.webp" alt="A photo of several used household appliances">'
            '<script src="/assets/customer-routing.js"></script>'
            '<a href="/privacy/">Privacy</a>'
            '<form action="https://formspree.io/f/mvzeapzd" method="POST">'
            f'<input type="hidden" name="source_page" value="{self.slug}">'
            + "".join(f'<input name="{name}" required>' for name in fields)
            + '<select name="state" required><option value=""></option>'
              '<option value="IL">Illinois</option></select>'
              '<input name="paid_option" type="checkbox">'
              '</form></body></html>'
        )
        self.page.write_text(self.html)
        self.manifest = self.root / "data/ttg-state-batches/IL.json"
        self.batch = {"state_code": "IL", "mode": "request-only",
                      "pages": [self.slug + "/index.html"]}
        self.save()

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        self.manifest.write_text(json.dumps(self.batch))

    def errors(self):
        return check_manifest(self.manifest, self.root)

    def test_valid_manifest(self):
        self.assertEqual(self.errors(), [])

    def test_statewide_hub_and_city_in_same_batch(self):
        hub_slug = "illinois-appliance-pickup"
        hub_folder = self.root / hub_slug
        hub_folder.mkdir()
        (hub_folder / "index.html").write_text(self.html.replace(self.slug, hub_slug))
        self.batch["pages"].append(hub_slug + "/index.html")
        self.save()
        self.assertEqual(self.errors(), [])

    def test_reject_other_state_in_form(self):
        self.page.write_text(self.html.replace('value="IL"', 'value="GA"'))
        self.assertTrue(any("state options" in e for e in self.errors()))

    def test_reject_indexable_unverified_market(self):
        self.page.write_text(self.html.replace("noindex, follow", "index, follow"))
        self.assertTrue(any("noindex" in e for e in self.errors()))

    def test_negative_guarantee_disclosures_are_accepted(self):
        self.page.write_text(self.html.replace("</body>",
            "<p>No Illinois region is guaranteed free pickup.</p></body>").replace(
            "<h1>Chicago used appliance request</h1>",
            '<meta name="description" content="no guaranteed free pickup">'
            "<h1>Chicago used appliance request</h1>"))
        self.assertEqual(self.errors(), [])

    def test_affirmative_guarantee_is_rejected(self):
        self.page.write_text(self.html.replace(
            "</body>", "<p>We offer guaranteed free pickup in Chicago.</p></body>"))
        self.assertTrue(any("affirmative guaranteed pickup" in e for e in self.errors()))

    def test_disclaimer_cannot_mask_later_guarantee(self):
        self.page.write_text(self.html.replace("</body>",
            "<p>No pickup is guaranteed. We offer guaranteed free pickup.</p></body>"))
        self.assertTrue(any("affirmative guaranteed pickup" in e for e in self.errors()))

    def test_reverse_wording_guarantee_is_rejected(self):
        self.page.write_text(self.html.replace("</body>",
            "<p>Free pickup is guaranteed for all units.</p></body>"))
        self.assertTrue(any("affirmative guaranteed pickup" in e for e in self.errors()))

    def test_reject_missing_image(self):
        self.page.write_text(self.html.replace("/used-appliances.webp", "/gone.webp"))
        self.assertTrue(any("image asset" in e for e in self.errors()))

    def test_reject_unapproved_activation(self):
        self.batch["mode"] = "index-candidate"
        self.save()
        self.assertTrue(any("approval" in e for e in self.errors()))

    def test_reject_missing_page(self):
        self.batch["pages"] = ["aurora-il-appliance-pickup/index.html"]
        self.save()
        self.assertTrue(any("page missing" in e for e in self.errors()))

    def test_reject_other_state_embedded_in_city_slug(self):
        wrong_slug = "chicago-il-ga-appliance-pickup"
        folder = self.root / wrong_slug
        folder.mkdir()
        (folder / "index.html").write_text(self.html.replace(self.slug, wrong_slug))
        self.batch["pages"] = [wrong_slug + "/index.html"]
        self.save()
        self.assertTrue(any("wrong state-coded" in e for e in self.errors()))

    def test_reject_unknown_appliance_category_slug(self):
        wrong_slug = "chicago-il-garbage-pickup"
        folder = self.root / wrong_slug
        folder.mkdir()
        (folder / "index.html").write_text(self.html.replace(self.slug, wrong_slug))
        self.batch["pages"] = [wrong_slug + "/index.html"]
        self.save()
        self.assertTrue(any("wrong state-coded" in e for e in self.errors()))

    def test_reject_path_traversal(self):
        self.batch["pages"] = ["../chicago-il-appliance-pickup/index.html"]
        self.save()
        self.assertTrue(any("unsafe" in e for e in self.errors()))

    def test_reject_duplicate_page(self):
        self.batch["pages"] *= 2
        self.save()
        self.assertTrue(any("unique" in e for e in self.errors()))

    def test_reject_missing_phone(self):
        self.page.write_text(self.html.replace('<input name="phone" required>', ""))
        self.assertTrue(any("phone" in e for e in self.errors()))


if __name__ == "__main__":
    unittest.main()
