"""Deterministic TTG Illinois safety preflight tests (no network or AI credits)."""
import tempfile
from pathlib import Path
import unittest

from scripts.ttg_validate_illinois import validate


class IllinoisPreflightTests(unittest.TestCase):
    def setUp(self):
        """Build a complete, minimal Illinois request page fixture."""
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.dir = self.root / "chicago-il-appliance-pickup"
        self.dir.mkdir()
        (self.root / "photo.webp").write_bytes(b"test illustrative image")
        self.html = self.dir / "index.html"
        self.sample = (
            '<html><head><meta name="robots" content="noindex, follow">'
            '<link rel="canonical" href="https://freereliableappliancepickup.com/chicago-il-appliance-pickup/">'
            '</head><body><h1>Chicago appliance requests</h1>'
            '<img src="/photo.webp" alt="Photo of used household appliances">'
            '<script src="/assets/customer-routing.js"></script>'
            '<form method="POST" action="https://formspree.io/f/mvzeapzd">'
            '<input name="source_page" value="chicago-il-appliance-pickup">'
            + "".join(
                f'<input name="{name}" required>' for name in (
                    "name","phone","address","city","zip","appliance","condition",
                    "floor","stairs","photos_available","access","message"
                )
            )
            + '<select name="state" required><option value=""></option>'
            '<option value="IL">Illinois</option></select>'
            '<select name="paid_option"><option value="free_only">Free only</option></select>'
            '<a href="/privacy/">Privacy Policy</a>'
            '</form></body></html>'
        )
        self.html.write_text(self.sample)

    def tearDown(self):
        """Release per-test temporary files."""
        self.temp.cleanup()

    def check(self, value):
        """Run preflight on the candidate HTML."""
        self.html.write_text(value)
        return validate(self.html, self.root, request_only=True)

    def test_valid_request_only_fixture(self):
        """A complete, accurately scoped request page passes."""
        self.assertEqual(self.check(self.sample), [])

    def test_reject_indexable_unverified_market(self):
        """Noindex must not be removed by a template change."""
        failures = self.check(self.sample.replace("noindex, follow", "index, follow"))
        self.assertTrue(any("noindex" in e for e in failures))

    def test_reject_mismatched_canonical(self):
        """Canonical should identify only this city's owner URL."""
        failures = self.check(self.sample.replace("/chicago-il-appliance-pickup/", "/aurora-il-appliance-pickup/"))
        self.assertTrue(any("canonical" in e for e in failures))

    def test_reject_broken_photo(self):
        """An HTML photo path without the actual asset is not accepted."""
        failures = self.check(self.sample.replace("/photo.webp", "/not-found.webp"))
        self.assertTrue(any("photo missing" in e for e in failures))

    def test_reject_missing_phone(self):
        """Every request needs a required, reachable callback field."""
        failures = self.check(self.sample.replace('<input name="phone" required>', ""))
        self.assertTrue(any("phone" in e for e in failures))


if __name__ == "__main__":
    unittest.main()
